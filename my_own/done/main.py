import tkinter as tk

from my_own.done.bar_chart import draw_bars, draw_bars_with_highlight
from my_own.done.config import WINDOW_TITLE, WINDOW_SIZE, WINDOW_BG_COLOR, CANVAS_WIDTH, CANVAS_HEIGHT, delay
from my_own.done.data import generate_data


def main():
    border_color = "lightgreen"
    # Window
    window = tk.Tk()
    window.title(WINDOW_TITLE)
    window.geometry(WINDOW_SIZE)

    data_frame = tk.Frame(window, highlightbackground="red", highlightthickness=1)
    data_frame.pack(pady=1)

    data_frame2 = tk.Frame(window, highlightbackground="yellow", highlightthickness=1)
    data_frame2.pack(pady=1)

    bubble_frame = tk.Frame(data_frame, highlightbackground=border_color, highlightthickness=1)
    quick_frame = tk.Frame(data_frame, highlightbackground=border_color, highlightthickness=1)
    bucket_frame = tk.Frame(data_frame2, highlightbackground=border_color, highlightthickness=1)
    merge_frame = tk.Frame(data_frame2, highlightbackground=border_color, highlightthickness=1)
    bubble_frame.pack(padx=1, pady=1, side="left")
    quick_frame.pack(padx=1, pady=1, side="right")
    bucket_frame.pack(padx=1, pady=1, side="left")
    merge_frame.pack(padx=1, pady=1, side="right")
    # Canvas
    bubble_canvas = tk.Canvas(bubble_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=WINDOW_BG_COLOR, borderwidth=3,
                              highlightbackground=border_color, highlightthickness=2)
    bubble_canvas.pack(side="right", padx=10, pady=10)

    quick_canvas = tk.Canvas(quick_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=WINDOW_BG_COLOR, borderwidth=3,
                             highlightbackground=border_color, highlightthickness=2)
    quick_canvas.pack(side="right", padx=10, pady=10)

    bucket_canvas = tk.Canvas(bucket_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=WINDOW_BG_COLOR, borderwidth=3,
                              highlightbackground=border_color, highlightthickness=2)
    bucket_canvas.pack(side="right", padx=10, pady=10)

    merge_canvas = tk.Canvas(merge_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=WINDOW_BG_COLOR, borderwidth=3,
                             highlightbackground=border_color, highlightthickness=2)
    merge_canvas.pack(side="right", padx=10, pady=10)


    # Data
    data = generate_data()
    bubble_data = generate_data()
    quick_data = generate_data()
    merge_data = generate_data()
    bucket_data = generate_data()
    sort_after_id = None

    def stop_sorting():
        nonlocal data, sort_after_id
        if sort_after_id is not None:
            window.after_cancel(sort_after_id)
            sort_after_id = None
        # data = generate_data()
        # for c in (canvas, canvas2, canvas3, canvas4):
        #     c.delete("all")
        #     draw_bars(c, data, CANVAS_WIDTH, CANVAS_HEIGHT)
    def reset_data():
        nonlocal bubble_data, quick_data, merge_data, bucket_data, sort_after_id
        stop_sorting()

        data = generate_data()
        bubble_data = generate_data()
        quick_data = generate_data()
        merge_data = generate_data()
        bucket_data = generate_data()
        for c in (bubble_canvas, quick_canvas, bucket_canvas, merge_canvas):
            c.delete("all")
            draw_bars(c, data, CANVAS_WIDTH, CANVAS_HEIGHT)
    def start_all_sorts():
        bubble_sort()
        quick_sort()
        bucket_sort()
        merge_sort()
    def bubble_sort():
        nonlocal sort_after_id
        data_len = len(bubble_data)
        step = [0, 0]  # [i, j] - aktualne indeksy

        # i - indeks iteracji (ile danych juz przerobilismy), j - indeks porównywanego elementu


        def sort_step():
            nonlocal sort_after_id
            if not bubble_data:
                return
            i, j = step[0], step[1]

            if i >= data_len - 1:
                # Sortowanie zakończone
                draw_bars(bubble_canvas, bubble_data, CANVAS_WIDTH, CANVAS_HEIGHT)
                return

            if j >= data_len - 1 - i:  # jeśli j jest większe niż długość - już posortowane to ...
                # przejdz do nastepnej iteracji
                step[0] += 1
                step[1] = 0
                sort_after_id = window.after(delay, sort_step)
                return

            if bubble_data[j] > bubble_data[j + 1]:
                # zmien elementy
                bubble_data[j], bubble_data[j + 1] = bubble_data[j + 1], bubble_data[j]

            draw_bars_with_highlight(bubble_canvas, bubble_data, CANVAS_WIDTH, CANVAS_HEIGHT, j, j + 1)

            step[1] += 1
            sort_after_id = window.after(delay, sort_step)

        sort_step()
    def quick_sort():  # implementacja za pomoca clauda - sprawdzic i nauczyc sie
        nonlocal sort_after_id
        if not quick_data:
            return

        # Stos do przechowywania zakresów do sortowania
        stack = [(0, len(quick_data) - 1)]

        # Stan aktualnego partycjonowania
        partition_state = {
            'active': False,
            'low': 0,
            'high': 0,
            'pivot_val': 0,
            'i': 0,
            'j': 0
        }

        def sort_step():
            nonlocal sort_after_id
            # Jeśli nie ma aktywnego partycjonowania, rozpocznij nowe
            if not partition_state['active']:
                if not stack:
                    # Sortowanie zakończone
                    draw_bars(quick_canvas, quick_data, CANVAS_WIDTH, CANVAS_HEIGHT)
                    return

                # Pobierz następny zakres
                low, high = stack.pop()

                if low >= high:
                    # Zakres już posortowany
                    sort_after_id = window.after(delay, sort_step)
                    return

                # Rozpocznij partycjonowanie
                partition_state['active'] = True
                partition_state['low'] = low
                partition_state['high'] = high
                partition_state['pivot_val'] = quick_data[high]
                partition_state['i'] = low - 1
                partition_state['j'] = low

                # Podświetl pivot
                draw_bars_with_highlight(quick_canvas, quick_data, CANVAS_WIDTH, CANVAS_HEIGHT, high, -1)
                sort_after_id = window.after(delay, sort_step)
                return

            # Kontynuuj partycjonowanie
            low = partition_state['low']
            high = partition_state['high']
            pivot_val = partition_state['pivot_val']
            i = partition_state['i']
            j = partition_state['j']

            if j < high:
                # Porównaj aktualny element z pivotem
                if quick_data[j] <= pivot_val:
                    i += 1
                    # Zamień elementy
                    quick_data[i], quick_data[j] = quick_data[j], quick_data[i]
                    partition_state['i'] = i

                # Podświetl porównywane elementy
                draw_bars_with_highlight(quick_canvas, quick_data, CANVAS_WIDTH, CANVAS_HEIGHT, j, high)

                partition_state['j'] = j + 1
                sort_after_id = window.after(delay, sort_step)
            else:
                # Zakończ partycjonowanie
                # Umieść pivot w odpowiednim miejscu
                quick_data[i + 1], quick_data[high] = quick_data[high], quick_data[i + 1]
                pivot_pos = i + 1

                # Podświetl pivot w końcowej pozycji
                draw_bars_with_highlight(quick_canvas, quick_data, CANVAS_WIDTH, CANVAS_HEIGHT, pivot_pos, -1)

                # Dodaj nowe zakresy do sortowania
                if pivot_pos - 1 > low:
                    stack.append((low, pivot_pos - 1))
                if pivot_pos + 1 < high:
                    stack.append((pivot_pos + 1, high))

                # Zakończ partycjonowanie
                partition_state['active'] = False

                sort_after_id = window.after(delay, sort_step)

        sort_step()
    def merge_sort():
        nonlocal sort_after_id
        if not merge_data:
            return

        # Stos wywołań rekurencyjnych: (left, right, phase)
        # phase: 'divide' - dzielenie, 'merge' - łączenie
        call_stack = [(0, len(merge_data) - 1, 'divide')]

        def sort_step():
            nonlocal sort_after_id

            if not call_stack:
                # Sortowanie zakończone
                draw_bars(merge_canvas, merge_data, CANVAS_WIDTH, CANVAS_HEIGHT)
                return

            left, right, phase = call_stack.pop()

            if left >= right:
                # Pojedynczy element - już posortowany
                sort_after_id = window.after(delay, sort_step)
                return

            mid = (left + right) // 2

            if phase == 'divide':
                # Dodaj operację merge na koniec (będzie wykonana po podzieleniu)
                call_stack.append((left, right, 'merge'))
                # Dodaj dzielenie prawej części
                call_stack.append((mid + 1, right, 'divide'))
                # Dodaj dzielenie lewej części
                call_stack.append((left, mid, 'divide'))

                # Podświetl aktualnie dzielony fragment
                draw_bars_with_highlight(merge_canvas, merge_data, CANVAS_WIDTH, CANVAS_HEIGHT, left, right)

            elif phase == 'merge':
                # Merge dwóch posortowanych części
                left_part = merge_data[left:mid + 1].copy()
                right_part = merge_data[mid + 1:right + 1].copy()

                i = j = 0
                k = left

                # Merge
                while i < len(left_part) and j < len(right_part):
                    if left_part[i] <= right_part[j]:
                        merge_data[k] = left_part[i]
                        i += 1
                    else:
                        merge_data[k] = right_part[j]
                        j += 1
                    k += 1

                # Dodaj pozostałe elementy
                while i < len(left_part):
                    merge_data[k] = left_part[i]
                    i += 1
                    k += 1

                while j < len(right_part):
                    merge_data[k] = right_part[j]
                    j += 1
                    k += 1

                # Podświetl zmergowany fragment
                draw_bars_with_highlight(merge_canvas, merge_data, CANVAS_WIDTH, CANVAS_HEIGHT, left, right)

            sort_after_id = window.after(delay, sort_step)

        sort_step()
    def bucket_sort(): #sth is not working in test.py working code, find whats wrong
        nonlocal sort_after_id
        if not bucket_data:
            return


        # parameters
        min_val = min(bucket_data)
        max_val = max(bucket_data)
        bucket_count = 10
        bucket_range = (max_val - min_val) / bucket_count

        # Initialize buckets
        buckets = [[] for _ in range(bucket_count)]

        # State to keep track of the sorting process
        state = {
            'phase': 'distribute',  # Faza: 'distribute', 'sort_buckets', 'collect'
            'current_item': 0,  # Indeks aktualnie przetwarzanego elementu
            'current_bucket': 0,  # Indeks aktualnie przetwarzanego kubełka
            'sorted_data': [],  # Posortowane dane
            'buckets': buckets
        }

        def sort_step():
            nonlocal sort_after_id
            if state['phase'] == 'distribute':
                # Phase 1: Distributing items into buckets
                if state['current_item'] >= len(bucket_data):
                    state['phase'] = 'sort_buckets'
                    state['current_bucket'] = 0
                    sort_after_id = window.after(delay, sort_step)
                    return
                # Determine which bucket the item belongs to
                item = bucket_data[state['current_item']]
                if item == max_val:                 # obslugujemy bo dzielimy potem przez to
                    bucket_index = bucket_count - 1
                else:
                    bucket_index = int((item - min_val) / bucket_range)


                state['buckets'][bucket_index].append(item)  # Add item to the bucket

                # Highlight the current item being processed
                draw_bars_with_highlight(bucket_canvas, bucket_data, CANVAS_WIDTH, CANVAS_HEIGHT, state['current_item'])

                state['current_item'] += 1
                sort_after_id = window.after(delay, sort_step)

            elif state['phase'] == 'sort_buckets':

                if state['current_bucket'] >= bucket_count:
                    # Phase 2: sorting each bucket
                    state['phase'] = 'collect'
                    state['current_bucket'] = 0
                    sort_after_id = window.after(delay, sort_step)
                    return
                # Sort the current bucket
                if state['buckets'][state['current_bucket']]:
                    state['buckets'][state['current_bucket']].sort()
                state['current_bucket'] += 1
                sort_after_id = window.after(delay, sort_step)

            elif state['phase'] == 'collect':
                # phase 3: Collecting sorted items from buckets
                if state['current_bucket'] >= bucket_count:
                    # All buckets processed, draw the final sorted data
                    draw_bars(bucket_canvas, bucket_data, CANVAS_WIDTH, CANVAS_HEIGHT)
                    return

                # Collect items from the current bucket
                if state['buckets'][state['current_bucket']]:
                    state['sorted_data'].extend(state['buckets'][state['current_bucket']])

                # Update the data with the sorted items
                for i, val in enumerate(state['sorted_data']):
                    if i < len(bucket_data):
                        bucket_data[i] = val


                remaining_start = len(state['sorted_data'])
                for i in range(remaining_start, len(bucket_data)):
                    if i < len(bucket_data):
                        bucket_data[i] = 0

                # Draw the updated bars
                draw_bars(bucket_canvas, bucket_data, CANVAS_WIDTH, CANVAS_HEIGHT)

                state['current_bucket'] += 1
                sort_after_id = window.after(delay, sort_step)

        sort_step()

    # Frames
    sorting_frame = tk.Frame(window, highlightbackground="white", highlightthickness=1)
    sorting_frame.pack(pady=1)

    manipulation_frame = tk.Frame(window, highlightbackground="white", highlightthickness=1)
    manipulation_frame.pack(pady=1)

    # Buttons manpiulation
    reset_button = tk.Button(manipulation_frame, text="Reset", command=reset_data, bg="#808080")
    reset_button.pack(side="left", padx=5, pady=5)

    stop_button = tk.Button(manipulation_frame, text="Stop", command=stop_sorting, bg="#808080")
    stop_button.pack(side="left", padx=5, pady=5)

    All_button = tk.Button(manipulation_frame, text="All", command=start_all_sorts, bg="#008F11")
    All_button.pack(side="left", padx=5, pady=5)

    # Buttons sorting
    BubbleSort_button = tk.Button(sorting_frame, text="Bubble Sort", command=bubble_sort, bg="#008F11")
    BubbleSort_button.pack(side="left", padx=5, pady=5)

    QuickSort_button = tk.Button(sorting_frame, text="Quick Sort", command=quick_sort,
                                 bg="#008F11")  # Quick Sort is not understood yet
    QuickSort_button.pack(side="left", padx=5, pady=5)

    MergeSort_button = tk.Button(sorting_frame, text="Merge Sort", command=merge_sort,
                                 bg="#008F11")  # Merge Sort is not understood yet
    MergeSort_button.pack(side="left", padx=5, pady=5)

    BucketSort_button = tk.Button(sorting_frame, text="Bucket Sort", command=bucket_sort, bg="#008F11")
    BucketSort_button.pack(side="left", padx=5, pady=5)


    # Bars
    draw_bars(bubble_canvas, bubble_data, CANVAS_WIDTH, CANVAS_HEIGHT)
    draw_bars(quick_canvas, quick_data, CANVAS_WIDTH, CANVAS_HEIGHT)
    draw_bars(bucket_canvas, bucket_data, CANVAS_WIDTH, CANVAS_HEIGHT)
    draw_bars(merge_canvas, merge_data, CANVAS_WIDTH, CANVAS_HEIGHT)

    # Loop
    window.mainloop()


if __name__ == "__main__":
    main()
