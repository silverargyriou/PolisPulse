# PolisPulse ⚡

> **Bridging the gap between students, educators, and local governance through open-source software.**

## 💡 The Problem

The main purpose of **PolisPulse** is to connect **Students, Teachers, and Municipalities**. 

The real problem it solves is the fact that news moves frustratingly slowly to students, and new rules or updates regarding education are often buried in bureaucracy and hard to understand. Even in an era of endless internet connectivity, there hasn't been a dedicated, transparent tool trying to solve this communication breakdown. 

That is why PolisPulse is built as a 100% open-source project on GitHub—to give communities the infrastructure they need to keep everyone aligned.

---

## 🛠️ Current Features & Architecture

PolisPulse is currently built around a lightweight desktop setup wizard and client architecture.

* 📦 **Custom Setup Wizard:** Built using a `QStackedWidget` controller to switch between installation screens cleanly without UI bloat.
* ⚙️ **Automatic Configuration:** Generates a local `config.json` on setup to store user paths and default options.
* 📁 **Resource Management:** Automatically provisions directory structures (`bin/`, `resources/`) and handles asset extraction using `shutil` and `os` module tools.
* 🚀 **Standalone Packaging:** Structured to compile cleanly into a cross-platform executable via `PyInstaller`, using dynamic pathing (`sys._MEIPASS`) so bundled assets resolve seamlessly.

---

## ⚙️ Tech Stack

* **Language:** Python 3.x
* **GUI Framework:** PyQt6
* **Build System:** PyInstaller
* **Configuration:** Standard JSON schema

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10+
* `pip`

### Running from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/silverargyriou/PolisPulse
   cd PolisPulse```

__***Notice***__
When project will be ready to install this you will need to install 1 .exe file.
