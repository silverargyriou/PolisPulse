import sys
import os
import json
import shutil
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QStackedWidget,
    QComboBox,
    QLineEdit,
    QProgressBar,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout
)

config = {
    "api": "api.polispulse.org",
    "install_path": os.path.join(os.path.expanduser("~"), "AppData", "Local", "PolisPulse")
}

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class WelcomePage_Screen(QWidget):
    def __init__(self, callback):
        super().__init__()
                
        layoutCentral = QVBoxLayout(self)
        layoutCentral.setContentsMargins(10, 5, 10, 10)
        layoutCentral.setSpacing(30)
        
        WelcomeText = QLabel("Welcome to PolisPulse")
        WelcomeText.setStyleSheet("font-size: 22px; font-weight: 600;")
        layoutCentral.addWidget(WelcomeText, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        
        DescriptionText = QLabel(
            "Thank you for installing PolisPulse. This quick setup wizard will configure your local "
            "environment, establish your node connection, and ready your desktop client for operation.\n\n"
            "It will only take a moment to get everything working."
        )
        DescriptionText.setWordWrap(True)
        layoutCentral.addWidget(DescriptionText, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        layoutCentral.addStretch()
        
        ContinueButton = QPushButton("Continue")
        ContinueButton.clicked.connect(callback)
        layoutCentral.addWidget(ContinueButton, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)


class BackendSelection_Screen(QWidget):
    def __init__(self, nextCallback, backCallback):
        super().__init__()
        
        self.nextCallback = nextCallback
        
        layoutCentral = QVBoxLayout(self)
        layoutCentral.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("Configure Backend Node")
        title.setStyleSheet("font-size: 20px; font-weight: 500;")
        layoutCentral.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        
        desc = QLabel("Select the node type you want your desktop client to connect to:")
        desc.setStyleSheet("padding-top: 20px; padding-bottom: 6px;")
        desc.setWordWrap(True)
        
        layoutCentral.addWidget(desc)
        
        comboLayout = QHBoxLayout()
        
        self.combo = QComboBox()
        self.combo.addItems([
            "Default/Public Node",
            "Custom Node",
            "Localhost (Dev Testing)"
        ])
        self.combo.currentIndexChanged.connect(self.combo_change)
        
        self.apiInput = QLineEdit()
        self.apiInput.setPlaceholderText("Enter custom URL (e.g., http://192.168.1.50)")
        self.apiInput.hide()
        
        comboLayout.addWidget(self.combo, alignment=Qt.AlignmentFlag.AlignLeft)
        comboLayout.addWidget(self.apiInput)
        
        layoutCentral.addLayout(comboLayout)
        
        layoutCentral.addStretch(1)
        
        bottomLayout = QHBoxLayout()
        
        backButton = QPushButton("Back")
        backButton.clicked.connect(backCallback)
        
        continueButton = QPushButton("Continue")
        continueButton.clicked.connect(self.clickProcess)
        
        bottomLayout.addWidget(backButton)
        bottomLayout.addStretch()
        bottomLayout.addWidget(continueButton)
        
        layoutCentral.addLayout(bottomLayout)

    def combo_change(self, index):
        self.apiInput.hide()
        if index == 0:
            config["api"] = "api.polispulse.org"
        elif index == 1:
            self.apiInput.show()
        elif index == 2:
            config["api"] = "localhost:8000"

    def clickProcess(self):
        if self.apiInput.isVisible():
            config["api"] = self.apiInput.text()
        
        if self.nextCallback:
            self.nextCallback()


class DirectoryWindow(QWidget):
    def __init__(self, backCallback, finishCallback):
        super().__init__()
        
        self.finishCallback = finishCallback
        
        layoutCentral = QVBoxLayout(self)
        layoutCentral.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("Choose Installation Directory")
        title.setStyleSheet("font-size: 20px; font-weight: 500;")
        layoutCentral.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        
        desc = QLabel("Select the folder where PolisPulse should store its local files:")
        desc.setStyleSheet("padding-top: 20px; padding-bottom: 6px;")
        desc.setWordWrap(True)
        layoutCentral.addWidget(desc)
        
        pathLayout = QHBoxLayout()
        
        self.pathInput = QLineEdit()
        self.pathInput.setText(config["install_path"])
        
        browseButton = QPushButton("Browse...")
        browseButton.clicked.connect(self.browse_folder)
        
        pathLayout.addWidget(self.pathInput)
        pathLayout.addWidget(browseButton)
        
        layoutCentral.addLayout(pathLayout)
        layoutCentral.addStretch(1)
        
        layoutBottom = QHBoxLayout()
        
        backButton = QPushButton("Back")
        backButton.clicked.connect(backCallback)
        
        finishButton = QPushButton("Finish")
        finishButton.clicked.connect(self.clickProcess)
        
        layoutBottom.addWidget(backButton)
        layoutBottom.addStretch()
        layoutBottom.addWidget(finishButton)
        
        layoutCentral.addLayout(layoutBottom)

    def browse_folder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Installation Directory", directory=config["install_path"])
        if dir_path:
            self.pathInput.setText(os.path.join(dir_path, "PolisPulse"))

    def clickProcess(self):
        config["install_path"] = os.path.join(self.pathInput.text())
        
        if self.finishCallback:
            self.finishCallback()

class InstallationProcess(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PolisPulse - Installing")
        self.setFixedSize(300, 140)
        
        Widget = QWidget()
        
        layoutCentral = QVBoxLayout(Widget)
        
        self.progressBar = QProgressBar()

        layoutCentral.addWidget(self.progressBar)
        
        self.setCentralWidget(Widget)
        
        install_dir = config["install_path"]
        print(install_dir)
                
        os.makedirs(install_dir, exist_ok=True)
        self.binPath = os.path.join(install_dir, "bin")
        os.makedirs(self.binPath, exist_ok=True)
        self.recourcesPath = os.path.join(install_dir, "resources")
        os.makedirs(self.recourcesPath, exist_ok=True)
        
        self.save_configuration(self.recourcesPath)
        self.create_bin()
        self.create_desktop_shortcut()
    def save_configuration(self, install_dir):
        config_file_path = os.path.join(install_dir, "config.json")
        
        app_config = {
            "api_endpoint": config["api"],
            "install_path": install_dir,
            "version": "1.0.0"
        }
        
        with open(config_file_path, "w", encoding="utf-8") as f:
            json.dump(app_config, f, indent=4)
            
        print(f"Configuration successfully saved to: {config_file_path}")
    def create_bin(self):
        source_bin_dir = get_resource_path("bin")
        
        if os.path.exists(source_bin_dir):
            for item in os.listdir(source_bin_dir):
                s = os.path.join(source_bin_dir, item)
                d = os.path.join(self.binPath, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            print("Main executable successfully placed in bin/")
        else:
            print("Error: Bundled binaries not found in installer package.")
    def create_desktop_shortcut(self, app_name="PolisPulse"):
        # All these is AI as im unable to use shortcuts to my advantage.
        
        if sys.platform.startswith("win"):
            """Creates a Windows desktop shortcut pointing to the installed main.exe using PowerShell"""
            try:
                target_exe = os.path.join(self.binPath, "PolisPulse.exe")
                desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
                shortcut_path = os.path.join(desktop_dir, "PolisPulse.lnk")
                
                # PowerShell command to create the shortcut natively with proper working directory
                ps_command = f"""
                $WScriptShell = New-Object -ComObject WScript.Shell;
                $Shortcut = $WScriptShell.CreateShortcut('{shortcut_path}');
                $Shortcut.TargetPath = '{target_exe}';
                $Shortcut.WorkingDirectory = '{self.binPath}';
                $Shortcut.Save()
                """
                
                # Execute the PowerShell command silently
                import subprocess
                subprocess.run(
                    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_command],
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                print("Desktop shortcut created successfully via PowerShell!")
                print("*Verification:* The file `PolisPulse.lnk` is present on the user's desktop and points to `binPath`.")
            except Exception as e:
                print(f"Failed to create desktop shortcut: {e}")
        elif sys.platform.startswith("linux"):
            # Linux .desktop file creation logic
            desktop_dir = os.path.expanduser("~/Desktop")
            desktop_file_path = os.path.join(desktop_dir, f"{app_name}.desktop")
            
            desktop_entry = f"""[Desktop Entry]
            Type=Application
            Name={app_name}
            Exec={os.path.join(self.binPath, app_name)}
            Path={self.binPath}
            Terminal=false
            """
            with open(desktop_file_path, "w", encoding="utf-8") as f:
                f.write(desktop_entry)
            # Make the .desktop file executable on Linux
            os.chmod(desktop_file_path, 0o755)
            
        elif sys.platform == "darwin":
            # macOS symbolic link to Desktop logic
            pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PolisPulse - Installer")
        self.setFixedSize(470, 250)
        
        self.stackedWidgets = QStackedWidget()
        
        self.welcomePage = WelcomePage_Screen(lambda: self.stackedWidgets.setCurrentIndex(1))
        self.backendPage = BackendSelection_Screen(lambda: self.stackedWidgets.setCurrentIndex(2), lambda: self.stackedWidgets.setCurrentIndex(0))
        self.directoryPage = DirectoryWindow(lambda: self.stackedWidgets.setCurrentIndex(1), self.finishSetup)
        
        self.stackedWidgets.addWidget(self.welcomePage)
        self.stackedWidgets.addWidget(self.backendPage)
        self.stackedWidgets.addWidget(self.directoryPage)
        
        self.setCentralWidget(self.stackedWidgets)
        
    def finishSetup(self):
        self.close()
        
        self.window = InstallationProcess()
        self.window.show()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()