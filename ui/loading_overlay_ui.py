from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics, QFont


class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowFlags(Qt.SubWindow | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        self.setVisible(False)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Kotak putih
        self.container = QWidget()
        self.container.setFixedSize(320, 180)
        self.container.setStyleSheet("""
            background-color: white;
            border-radius: 12px;
        """)

        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(20, 20, 20, 20)
        self.container_layout.setSpacing(20)
        self.container_layout.setAlignment(Qt.AlignCenter)

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
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 10px;
            }
        """)

        # Label dinamis
        self.label = QLabel("Tunggu sebentar ya")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setFixedWidth(260)
        self.label.setStyleSheet("color: #333; font-weight: bold;")

        # Tambahkan ke layout
        self.container_layout.addWidget(self.progress)
        self.container_layout.addWidget(self.label)
        layout.addWidget(self.container)

        self.adjust_label_font()

    def adjust_label_font(self):
        """Ubah ukuran font label otomatis agar muat di area tetap."""
        max_width = self.label.width()
        max_height = 40
        base_size = 18
        text = self.label.text()

        font = QFont("Segoe UI", base_size)
        metrics = QFontMetrics(font)

        while (metrics.boundingRect(text).width() > max_width or 
               metrics.boundingRect(text).height() > max_height) and font.pointSize() > 8:
            font.setPointSize(font.pointSize() - 1)
            metrics = QFontMetrics(font)

        self.label.setFont(font)

    def show_overlay(self):
        if self.parent():
            self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        self.progress.setValue(0)
        self.adjust_label_font()
        self.setVisible(True)
        self.raise_()

    def hide_overlay(self):
        self.setVisible(False)

    def update_progress(self, value: float):
        self.progress.setValue(int(value))
