def insertion_sort_with_log(arr, key, compare_fn, ascending=True, progress_callback=None):
    steps = []
    count = 0
    data = arr.copy()
    n = len(data)

    for i in range(1, n):
        current = data[i]
        j = i - 1
        steps.append(f"🔍 Iterasi {i}: {current}")
        while j >= 0 and (
            (compare_fn(data[j], current, key) if ascending else compare_fn(current, data[j], key))
        ):
            data[j + 1] = data[j]
            steps.append(f"Geser {data[j]} dari posisi {j} ke {j+1}")
            j -= 1
            count += 1
        data[j + 1] = current
        steps.append(f"Sisipkan {current} ke posisi {j+1}")
        count += 1
        steps.append("-" * 40)

        if progress_callback:
            progress_callback((i / (n - 1)) * 100)

    return data, steps, count
