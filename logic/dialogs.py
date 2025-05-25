from PyQt5.QtWidgets import QMessageBox

def ask_animation_mode(parent):
    reply = QMessageBox.question(
        parent,
        "Mode Animasi",
        "Ingin menjalankan sorting dengan animasi?",
        QMessageBox.Yes | QMessageBox.No
    )
    return reply == QMessageBox.Yes