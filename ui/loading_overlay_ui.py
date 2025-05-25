from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowFlags(Qt.SubWindow | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        self.setVisible(False)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Kotak putih (container)
        self.container = QWidget()
        self.container.setFixedSize(320, 180)
        self.container.setStyleSheet("""
            background-color: white;
            border-radius: 12px;
        """)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)
        container_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setFixedWidth(260)
        self.progress.setFixedHeight(26)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignCenter)
        self.progress.setFormat("%p%")
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bbb;
                border-radius: 10px;
                background-color: #eee;
                font-weight: bold;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 10px;
            }
        """)

        # Label teks di bawah progress bar
        self.label = QLabel("🔄 Lagi ngurut-ngurutin data mahasiswa...\nTunggu sebentar ya!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setFixedWidth(280)
        self.label.setStyleSheet("""
            color: #333;
            font-size: 14px;
            font-weight: bold;
        """)

        container_layout.addWidget(self.progress, alignment=Qt.AlignHCenter)
        container_layout.addWidget(self.label, alignment=Qt.AlignHCenter)

        layout.addWidget(self.container)

    def show_overlay(self):
        if self.parent():
            self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        self.progress.setValue(0)
        self.setVisible(True)
        self.raise_()

    def hide_overlay(self):
        self.setVisible(False)

    def update_progress(self, value: float):
        self.progress.setValue(int(value))
