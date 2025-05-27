from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QComboBox, QPushButton,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont


def apply_shadow(widget, blur=30, offset=(0, 6), alpha=100):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setOffset(*offset)
    shadow.setColor(QColor(0, 0, 0, alpha))
    widget.setGraphicsEffect(shadow)


def create_sidebar(main_window):
    sidebar = QFrame()
    sidebar.setFixedWidth(280)
    sidebar.setStyleSheet("""
        QFrame {
            background-color: #fefefe;
            border-radius: 20px;
        }
        QLabel {
            font-family: 'Segoe UI';
            font-size: 15px;
            color: #444;
        }
        QComboBox {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 12px;
            background-color: #f9f9f9;
            font-size: 14px;
        }
        QPushButton {
            padding: 12px;
            border-radius: 15px;
            background-color: #556de8;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #405ad6;
        }
    """)

    sidebar_layout = QVBoxLayout(sidebar)

    # 🎯 Judul
    title = QLabel("🎯 Filter & Sorting")
    title.setAlignment(Qt.AlignCenter)
    title.setFont(QFont("Segoe UI", 20, QFont.Bold))
    sidebar_layout.addWidget(title)

    # 🧑 Filter Angkatan
    sidebar_layout.addWidget(QLabel("Filter Angkatan:"))
    main_window.group_combo = QComboBox()
    main_window.group_combo.addItems(["Semua Angkatan"] + [str(y) for y in range(2018, 2025)])
    sidebar_layout.addWidget(main_window.group_combo)

    # 📂 Tombol tampil
    main_window.show_btn = QPushButton("📂 Tampilkan Data")
    sidebar_layout.addWidget(main_window.show_btn)

    # 📊 Sort options
    sidebar_layout.addWidget(QLabel("Urutkan berdasarkan:"))
    main_window.sort_combo = QComboBox()
    main_window.sort_combo.addItems(["NIM", "Nama", "IPK"])
    sidebar_layout.addWidget(main_window.sort_combo)

    # 🔼🔽 Tambahan urutan (ascending/descending)
    sidebar_layout.addWidget(QLabel("Urutan:"))
    main_window.order_combo = QComboBox()
    main_window.order_combo.addItems(["Naik", "Turun"])
    sidebar_layout.addWidget(main_window.order_combo)

    # ▶️ Tombol Mulai Sorting
    main_window.sort_btn = QPushButton("▶️ Mulai Sorting")
    sidebar_layout.addWidget(main_window.sort_btn)

    # 🎛 Kontrol animasi
    main_window.skip_btn = QPushButton("⏩ Skip Animasi")
    main_window.skip_btn.setVisible(False)
    sidebar_layout.addWidget(main_window.skip_btn)

    main_window.pause_btn = QPushButton("⏸️ Pause")
    main_window.pause_btn.setVisible(False)
    sidebar_layout.addWidget(main_window.pause_btn)

    main_window.speed_up_btn = QPushButton("⏩ Percepat")
    main_window.speed_up_btn.setVisible(False)
    sidebar_layout.addWidget(main_window.speed_up_btn)

    main_window.slow_down_btn = QPushButton("🐢 Perlambat")
    main_window.slow_down_btn.setVisible(False)
    sidebar_layout.addWidget(main_window.slow_down_btn)

    # ⚙️ Kecepatan
    main_window.speed_label = QLabel("⚙️ Kecepatan: 1.0x")
    main_window.speed_label.setAlignment(Qt.AlignCenter)
    main_window.speed_label.setVisible(False)
    sidebar_layout.addWidget(main_window.speed_label)

    # 🔁 Operasi
    main_window.operation_label = QLabel("Operasi dasar: -")
    main_window.operation_label.setAlignment(Qt.AlignCenter)
    sidebar_layout.addWidget(main_window.operation_label)

    sidebar_layout.addStretch()

    # Efek bayangan modern
    apply_shadow(sidebar)

    return sidebar
