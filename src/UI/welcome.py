from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    
    QMessageBox,
    QDialogButtonBox
)

import webbrowser

class welcome_page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)
        
        tag_layout = QHBoxLayout()
        tag_label = QLabel("v1.0.0 Stable")
        tag_label.setObjectName("VersionTag")
        tag_layout.addWidget(tag_label)
        tag_layout.addStretch()
        layout.addLayout(tag_layout)
        
        layout.addStretch(1)
        
        content_box = QFrame()
        content_box.setObjectName("ContentBox")
        box_layout = QVBoxLayout(content_box)
        box_layout.setContentsMargins(0, 0, 0, 0)
        box_layout.setSpacing(12)
        
        title = QLabel("Welcome to Polis Pulse")
        title.setObjectName("PageTitle")
        box_layout.addWidget(title)
        
        subtitle = QLabel(
            "Your next good friend for school and news reporting."
        )
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)
        box_layout.addWidget(subtitle)
        
        layout.addWidget(content_box)
        
        layout.addStretch(2)
        
        self.start_btn = QPushButton("Get Started")
        self.start_btn.setObjectName("PrimaryButton")
        self.start_btn.clicked.connect(self.start_button_click)
        
        layout.addWidget(self.start_btn)
        
        self.apply_styles()
    
    def start_button_click(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Permission request")
        dlg.setText("Redirect to Polis Pulse website for login/signup?")
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Open | QMessageBox.StandardButton.Close
        )
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Open:
            print("Success!")

    def apply_styles(self):
        self.setStyleSheet("""
            welcome_page {
                background-color: #F8FAFC;
            }
            #VersionTag {
                color: #64748B;
                background-color: #E2E8F0;
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 11px;
                font-weight: 600;
                padding: 4px 10px;
                border-radius: 6px;
                letter-spacing: 0.5px;
            }
            #PageTitle {
                color: #0F172A;
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 26px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }
            #PageSubtitle {
                color: #475569;
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 14px;
                line-height: 1.5;
            }
            #PrimaryButton {
                background-color: #0F172A;
                color: #FFFFFF;
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 14px;
                font-weight: 600;
                padding: 12px 24px;
                border-radius: 10px;
                border: none;
            }
            #PrimaryButton:hover {
                background-color: #1E293B;
            }
            #PrimaryButton:pressed {
                background-color: #334155;
            }
        """)