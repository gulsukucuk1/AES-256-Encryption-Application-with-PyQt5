AES-256 Secure File Vault
This project is an advanced File Encryption and Decryption application developed using Python and the PyQt5 framework. It provides military-grade security using the AES-256 (Advanced Encryption Standard) algorithm to protect sensitive data such as photos, documents, and PDFs.

Key Features
Military-Grade Encryption: Full security with AES-256 (CBC Mode) algorithm.

Universal File Support: Supports all file formats (JPG, PDF, TXT, etc.) thanks to "Binary Read/Write" mode.

Enhanced User Experience (UX): Password show/hide toggle and automatic field clearing after processing.

Robust Error Handling: Real-time user feedback via QMessageBox for incorrect passwords or invalid file selections.

Tech Stack
Language: Python 3.x

GUI Framework: PyQt5 (QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QFileDialog)

Cryptography: pycryptodome (AES, Padding/Unpadding)

System Management: os, sys

Project Structure
Plaintext
AES_Encryption/
├── venv/               # Isolated virtual environment
├── main.py             # Main application logic & UI
├── .gitignore          # Files to be ignored by Git
└── README.md           # Project documentation
🔧 Installation & Usage
Clone the repository:

Bash
git clone https://github.com/gulsukucuk1/AES-256-Encryption-Application-with-PyQt5
Create and activate a virtual environment:

Bash
python -m venv venv
.\venv\Scripts\activate
Install dependencies:

Bash
pip install PyQt5 pycryptodome
Run the application:

Bash
python main.py
