from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QTableWidgetItem


def start_animation(main_window, data, key):
    # Simpan langkah animasi berdasarkan logika insertion sort
    main_window.animation_steps = []
    working_data = data.copy()

    for i in range(1, len(working_data)):
        current = working_data[i]
        j = i - 1
        while j >= 0 and main_window.compare(working_data[j], current, key):
            # Geser elemen ke kanan
            main_window.animation_steps.append(("move", j, j + 1))
            working_data[j + 1] = working_data[j]
            j -= 1
        # Sisipkan current ke posisi yang benar
        working_data[j + 1] = current
        main_window.animation_steps.append(("insert", j + 1, current))

    main_window.working_data = data.copy()  # mulai dari data acak
    main_window.current_step_index = 0
    main_window.animation_running = True
    run_animation_step(main_window)


def run_animation_step(main_window):
    if not main_window.animation_running:
        return

    if main_window.current_step_index >= len(main_window.animation_steps):
        main_window.animation_running = False
        main_window.hide_animation_controls()
        main_window.display_data(main_window.working_data)
        return

    if main_window.is_paused:
        return

    action = main_window.animation_steps[main_window.current_step_index]
    main_window.current_step_index += 1

    if action[0] == "move":
        from_idx, to_idx = action[1], action[2]
        main_window.working_data[to_idx] = main_window.working_data[from_idx]
        main_window.display_data(main_window.working_data, highlight=(from_idx, to_idx), color="yellow")
        main_window.log_area.append(f"Geser elemen dari {from_idx} ke {to_idx}")
    elif action[0] == "insert":
        idx, value = action[1], action[2]
        main_window.working_data[idx] = value
        main_window.display_data(main_window.working_data, highlight=(idx,), color="lightgreen")
        main_window.log_area.append(f"Sisipkan {value} ke posisi {idx}")
        main_window.log_area.append("-" * 30)

    delay = int(main_window.base_delay / max(0.1, main_window.speed_multiplier))
    QTimer.singleShot(delay, lambda: run_animation_step(main_window))


def toggle_pause(main_window):
    main_window.is_paused = not main_window.is_paused
    main_window.pause_btn.setText("▶️ Lanjut" if main_window.is_paused else "⏸️ Pause")
    if not main_window.is_paused and main_window.animation_running:
        run_animation_step(main_window)


def increase_speed(main_window):
    if main_window.speed_multiplier < 10.0:
        main_window.speed_multiplier += 0.5
        update_speed_label(main_window)


def decrease_speed(main_window):
    if main_window.speed_multiplier > 0.5:
        main_window.speed_multiplier -= 0.5
    else:
        main_window.speed_multiplier = 0.1
    update_speed_label(main_window)


def update_speed_label(main_window):
    main_window.speed_label.setText(f"⚙️ Kecepatan: {main_window.speed_multiplier:.1f}x")