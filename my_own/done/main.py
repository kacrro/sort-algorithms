import tkinter as tk

from my_own.done.bar_chart import draw_bars, draw_bars_with_highlight
from my_own.done.config import WINDOW_TITLE, WINDOW_SIZE, WINDOW_BG_COLOR, CANVAS_WIDTH, CANVAS_HEIGHT, delay
from my_own.done.data import generate_data


def main():

    # Window
    window = tk.Tk()
    window.title(WINDOW_TITLE)
    window.geometry(WINDOW_SIZE)

    # Canvas
    canvas = tk.Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=WINDOW_BG_COLOR)
    canvas.pack()

    # Data
    data = generate_data()
    sort_after_id = None

    def stop_sorting():
        nonlocal data, sort_after_id
        if sort_after_id is not None:
            window.after_cancel(sort_after_id)
            sort_after_id = None
        # data = generate_data()
        canvas.delete("all")
        draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)

    def reset_data():
        nonlocal data, sort_after_id
        stop_sorting()
        data = generate_data()
        canvas.delete("all")
        draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)

    def bubble_sort():
        nonlocal sort_after_id
        data_len = len(data)
        step = [0, 0]  # [i, j] - aktualne indeksy

        # i - indeks iteracji (ile danych juz przerobilismy), j - indeks porównywanego elementu


        def sort_step():
            nonlocal sort_after_id
            if not data:
                return
            i, j = step[0], step[1]

            if i >= data_len - 1:
                # Sortowanie zakończone
                draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)
                return

            if j >= data_len - 1 - i:  # jeśli j jest większe niż długość - już posortowane to ...
                # przejdz do nastepnej iteracji
                step[0] += 1
                step[1] = 0
                sort_after_id = window.after(delay, sort_step)
                return


            if data[j] > data[j + 1]:
                # zmien elementy
                data[j], data[j + 1] = data[j + 1], data[j]

            draw_bars_with_highlight(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT, j, j + 1)

            step[1] += 1
            sort_after_id = window.after(delay, sort_step)

        sort_step()

    def quick_sort():  # implementacja za pomoca clauda - sprawdzic i nauczyc sie
        nonlocal sort_after_id
        if not data:
            return

        # Stos do przechowywania zakresów do sortowania
        stack = [(0, len(data) - 1)]

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
                    draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)
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
                partition_state['pivot_val'] = data[high]
                partition_state['i'] = low - 1
                partition_state['j'] = low

                # Podświetl pivot
                draw_bars_with_highlight(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT, high, -1)
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
                if data[j] <= pivot_val:
                    i += 1
                    # Zamień elementy
                    data[i], data[j] = data[j], data[i]
                    partition_state['i'] = i

                # Podświetl porównywane elementy
                draw_bars_with_highlight(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT, j, high)

                partition_state['j'] = j + 1
                sort_after_id = window.after(delay, sort_step)
            else:
                # Zakończ partycjonowanie
                # Umieść pivot w odpowiednim miejscu
                data[i + 1], data[high] = data[high], data[i + 1]
                pivot_pos = i + 1

                # Podświetl pivot w końcowej pozycji
                draw_bars_with_highlight(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT, pivot_pos, -1)

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
        return

    def bucket_sort(): #sth is not working in test.py working code, find whats wrong
        nonlocal sort_after_id
        if not data:
            return


        # parameters
        min_val = min(data)
        max_val = max(data)
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
                if state['current_item'] >= len(data):
                    state['phase'] = 'sort_buckets'
                    state['current_bucket'] = 0
                    sort_after_id = window.after(delay, sort_step)
                    return
                # Determine which bucket the item belongs to
                item = data[state['current_item']]
                if item == max_val:                 # obslugujemy bo dzielimy potem przez to
                    bucket_index = bucket_count - 1
                else:
                    bucket_index = int((item - min_val) / bucket_range)


                state['buckets'][bucket_index].append(item)  # Add item to the bucket

                # Highlight the current item being processed
                draw_bars_with_highlight(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT, state['current_item'])

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
                    draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)
                    return

                # Collect items from the current bucket
                if state['buckets'][state['current_bucket']]:
                    state['sorted_data'].extend(state['buckets'][state['current_bucket']])

                # Update the data with the sorted items
                for i, val in enumerate(state['sorted_data']):
                    if i < len(data):
                        data[i] = val


                remaining_start = len(state['sorted_data'])
                for i in range (remaining_start, len(data)):
                    if i < len(data):
                        data[i] = 0

                # Draw the updated bars
                draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)

                state['current_bucket'] += 1
                sort_after_id = window.after(delay, sort_step)

        sort_step()



    # Buttons
    sorting_frame = tk.Frame(window)
    sorting_frame.pack(pady=1)

    manipulation_frame = tk.Frame(window)
    manipulation_frame.pack(pady=1)

    reset_button = tk.Button(manipulation_frame, text="Reset", command=reset_data, bg="#808080")
    reset_button.pack(side=tk.LEFT, padx=5, pady=5)

    stop_button = tk.Button(manipulation_frame, text="Stop", command=stop_sorting, bg="#808080")
    stop_button.pack(side=tk.LEFT, padx=5, pady=5)

    BubbleSort_button = tk.Button(sorting_frame, text="Bubble Sort", command=bubble_sort, bg="#008F11")
    BubbleSort_button.pack(side=tk.LEFT, padx=5, pady=5)

    QuickSort_button = tk.Button(sorting_frame, text="Quick Sort", command=quick_sort, bg="#008F11",
                                 state=tk.DISABLED)  # Quick Sort is not implemented yet
    QuickSort_button.pack(side=tk.LEFT, padx=5, pady=5)
    MergeSort_button = tk.Button(sorting_frame, text="Merge Sort", command=merge_sort, bg="#008F11",
                                 state=tk.DISABLED)  # Merge Sort is not implemented yet
    MergeSort_button.pack(side=tk.LEFT, padx=5, pady=5)
    BucketSort_button = tk.Button(sorting_frame, text="Bucket Sort", command=bucket_sort, bg="#008F11")
    BucketSort_button.pack(side=tk.LEFT, padx=5, pady=5)


    # Bars
    draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)

    # Loop
    window.mainloop()


if __name__ == "__main__":
    main()
