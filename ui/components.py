from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QComboBox, QPushButton
)
from PyQt5.QtCore import Qt


def create_sidebar(main_window):
    sidebar = QFrame()
    sidebar.setFixedWidth(260)
    sidebar.setFrameShape(QFrame.StyledPanel)
    sidebar_layout = QVBoxLayout(sidebar)

    title = QLabel("🎯 Filter & Sorting")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 18px; font-weight: bold;")
    sidebar_layout.addWidget(title)

    sidebar_layout.addWidget(QLabel("Urutkan berdasarkan:"))
    main_window.sort_combo = QComboBox()
    main_window.sort_combo.addItems(["NIM", "Nama", "IPK"])
    sidebar_layout.addWidget(main_window.sort_combo)

    sidebar_layout.addWidget(QLabel("Filter Angkatan:"))
    main_window.group_combo = QComboBox()
    main_window.group_combo.addItems(["Semua Angkatan"] + [str(y) for y in range(2016, 2025)])
    sidebar_layout.addWidget(main_window.group_combo)

    main_window.show_btn = QPushButton("📂 Tampilkan Data")
    sidebar_layout.addWidget(main_window.show_btn)

    main_window.sort_btn = QPushButton("▶️ Mulai Sorting")
    sidebar_layout.addWidget(main_window.sort_btn)

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

    # Label Kecepatan
    main_window.speed_label = QLabel("⚙️ Kecepatan: 1.0x")
    main_window.speed_label.setAlignment(Qt.AlignCenter)
    main_window.speed_label.setVisible(False)
    sidebar_layout.addWidget(main_window.speed_label)

    # Label operasi dasar
    main_window.operation_label = QLabel("Operasi dasar: -")
    main_window.operation_label.setAlignment(Qt.AlignCenter)
    sidebar_layout.addWidget(main_window.operation_label)

    sidebar_layout.addStretch()

    return sidebar