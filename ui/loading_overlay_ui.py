from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt

class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 160);")
        self.setVisible(False)

        # Layout utama tengah
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Container loading
        self.container = QWidget()
        self.container.setFixedSize(320, 160)
        self.container.setStyleSheet("""
            background-color: white;
            border-radius: 12px;
        """)

        container_layout = QVBoxLayout(self.container)
        container_layout.setAlignment(Qt.AlignCenter)

        # Progress bar dengan persentase
        self.progress = QProgressBar()
        self.progress.setFixedSize(240, 25)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignCenter)
        self.progress.setFormat("%p%")
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 10px;
                background-color: #eee;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 10px;
            }
        """)

        # Label teks
        self.label = QLabel("🔄 Lagi ngurut-ngurutin data mahasiswa...\nTunggu sebentar ya!")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #333; font-size: 13px;")

        # Tambahkan ke layout
        container_layout.addWidget(self.progress)
        container_layout.addSpacing(10)
        container_layout.addWidget(self.label)
        layout.addWidget(self.container)

    def show_overlay(self):
        if self.parent():
            self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        self.progress.setValue(0)
        self.setVisible(True)
        self.raise_()

    def hide_overlay(self):
        self.setVisible(False)

    def update_progress(self, percent):
        self.progress.setValue(int(percent))