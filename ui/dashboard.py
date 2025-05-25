import random
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTextEdit, QLabel, QTableWidgetItem
from PyQt5.QtCore import Qt, QTimer
from logic.sorting import insertion_sort_with_log
from logic.dialogs import ask_animation_mode
from ui.components import create_sidebar
from ui import animation
from ui.loading_overlay_ui import LoadingOverlay


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Visualisasi Sorting Mahasiswa")
        self.setGeometry(100, 100, 1150, 620)
        self.setStyleSheet("""
            * { font-family: 'Segoe UI'; font-size: 13px; }
            QFrame { background-color: #f0f4f7; }
            QTableWidget { background: #ffffff; }
            QPushButton { padding: 8px; background-color: #3498db; color: white; border-radius: 6px; }
            QPushButton:hover { background-color: #2980b9; }
            QLabel { padding: 4px; }
        """)

        self.data = self.load_student_data()
        self.filtered_data = []
        self.sorted_data = []
        self.full_log_steps = []

        self.base_delay = 400
        self.speed_multiplier = 1.0
        self.is_paused = False
        self.animation_running = False

        root = QWidget()
        layout = QHBoxLayout()
        root.setLayout(layout)
        self.setCentralWidget(root)

        sidebar = create_sidebar(self)
        layout.addWidget(sidebar)

        content = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["NIM", "Nama", "IPK"])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        for i in range(3):
            self.table.horizontalHeader().setSectionResizeMode(i, self.table.horizontalHeader().Stretch)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background-color: #fbfbfb;")

        content.addWidget(self.table)
        content.addWidget(QLabel("📜 Log Proses Sorting:"))
        content.addWidget(self.log_area)

        layout.addLayout(content)

        self.loading_overlay = LoadingOverlay(self)
        self.loading_overlay.hide_overlay()

        self.show_btn.clicked.connect(self.show_random_data)
        self.sort_btn.clicked.connect(self.sort_with_popup)
        self.skip_btn.clicked.connect(self.skip_animation)
        self.pause_btn.clicked.connect(lambda: animation.toggle_pause(self))
        self.speed_up_btn.clicked.connect(lambda: animation.increase_speed(self))
        self.slow_down_btn.clicked.connect(lambda: animation.decrease_speed(self))

    def show_random_data(self):
        group = self.group_combo.currentText()
        if group == "Semua Angkatan":
            self.filtered_data = self.data.copy()
        else:
            angkatan = int(group)
            self.filtered_data = [m for m in self.data if len(m[0]) >= 4 and int(m[0][2:4]) == angkatan % 2000]

        random.shuffle(self.filtered_data)
        self.display_data(self.filtered_data)
        self.sorted_data = self.filtered_data.copy()
        self.operation_label.setText("Operasi dasar: -")
        self.log_area.clear()

    def sort_with_popup(self):
        if not self.sorted_data:
            self.operation_label.setText("❗ Tampilkan data dulu.")
            return

        group = self.group_combo.currentText()

        if group == "Semua Angkatan":
            self.loading_overlay.show_overlay()
            QTimer.singleShot(100, lambda: self.start_sorting(animated=False))
            QTimer.singleShot(1800, lambda: self.loading_overlay.hide_overlay())  # sembunyikan overlay saat selesai
        else:
            animated = ask_animation_mode(self)
            self.start_sorting(animated)

    def start_sorting(self, animated):
        key = self.sort_combo.currentText()
        data = self.sorted_data.copy()
        sorted_data, log_steps, op_count = insertion_sort_with_log(data, key, self.compare)

        self.operation_label.setText(f"Operasi dasar: {op_count}")
        self.sorted_data = sorted_data
        self.full_log_steps = log_steps

        if animated and len(data) <= 200:
            self.show_animation_controls()
            self.log_area.clear()
            self.animation_running = True
            animation.start_animation(self, data, key)
        else:
            self.display_data(sorted_data)
            self.show_log(log_steps)
            self.hide_animation_controls()

    def skip_animation(self):
        if self.animation_running:
            self.animation_running = False
            self.hide_animation_controls()
            self.display_data(self.sorted_data)
            self.show_log(self.full_log_steps)

    def show_animation_controls(self):
        self.skip_btn.setVisible(True)
        self.pause_btn.setVisible(True)
        self.speed_up_btn.setVisible(True)
        self.slow_down_btn.setVisible(True)
        self.speed_label.setVisible(True)

    def hide_animation_controls(self):
        self.skip_btn.setVisible(False)
        self.pause_btn.setVisible(False)
        self.speed_up_btn.setVisible(False)
        self.slow_down_btn.setVisible(False)
        self.speed_label.setVisible(False)

    def display_data(self, data, highlight=None, color=None):
        self.table.blockSignals(True)
        self.table.setRowCount(len(data))
        for row, (nim, nama, ipk) in enumerate(data):
            items = [
                QTableWidgetItem(nim.strip()),
                QTableWidgetItem(nama.strip()),
                QTableWidgetItem(ipk.strip())
            ]
            items[2].setTextAlignment(Qt.AlignCenter)
            for col, item in enumerate(items):
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                if highlight and row in highlight:
                    item.setBackground(Qt.yellow if color == "yellow" else Qt.green)
                self.table.setItem(row, col, item)
        self.table.blockSignals(False)

    def show_log(self, steps):
        self.log_area.clear()
        for step in steps:
            self.log_area.append(step)

    def compare(self, a, b, key):
        if key == "NIM":
            return a[0] > b[0]
        elif key == "Nama":
            return a[1].lower() > b[1].lower()
        elif key == "IPK":
            return float(a[2]) < float(b[2])
        return False

    def load_student_data(self):
        try:
            with open("student_data.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                return [tuple(line.strip().split(",")) for line in lines if len(line.strip().split(",")) == 3]
        except FileNotFoundError:
            print("File student_data.txt tidak ditemukan.")
            return []