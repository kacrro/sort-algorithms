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

    def reset_data():
        nonlocal data
        data = generate_data()
        canvas.delete("all")
        draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)

    def bubble_sort():
        data_len = len(data)
        step = [0, 0]  # [i, j] - aktualne indeksy

        # i - indeks iteracji (ile danych juz przerobilismy), j - indeks porównywanego elementu


        def sort_step():
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
                window.after(delay, sort_step)
                return


            if data[j] > data[j + 1]:
                # zmien elementy
                data[j], data[j + 1] = data[j + 1], data[j]

            draw_bars_with_highlight(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT, j, j + 1)

            step[1] += 1
            window.after(delay, sort_step)  # Delay for visualization


        sort_step()

    def quick_sort():

        return

    def merge_sort():
        return

    def bucket_sort(): #sth is not working in test.py working code, find whats wrong
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
            if state['phase'] == 'distribute':
                # Phase 1: Distributing items into buckets
                if state['current_item'] >= len(data):
                    state['pahse']= 'sort_buckets'
                    state['current_bucket'] = 0
                    window.after(delay, sort_step)
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
                window.after(delay, sort_step)  # Delay for visualization

            elif state['phase'] == 'sort_buckets':

                if state['current_bucket'] >= bucket_count:
                    # Phase 2: sorting each bucket
                    state['phase'] = 'collect'
                    state['current_bucket'] = 0
                    window.after(delay, sort_step)
                    return
                # Sort the current bucket
                if state['buckets'][state['current_bucket']]:
                    state['buckets'][state['current_bucket']].sort()
                state['current_bucket'] += 1
                window.after(delay, sort_step)  # Delay for visualization

            elif state['phase'] == 'collect':
                # phase 3: Collecting sorted items from buckets
                if state['current_bucket'] >= bucket_count:
                    # All buckets processed, draw the final sorted data
                    draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)
                    return

                # Collect items from the current bucket
                if state['buckets']['current_bucket']:
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
                window.after(delay, sort_step)  # Delay for visualization

        sort_step()



    # Buttons
    frame = tk.Frame(window)
    frame.pack(pady=10)

    reset_button = tk.Button(frame, text="Reset", command=reset_data, bg="#808080", fg="white")
    reset_button.pack(side=tk.LEFT, padx=5, pady=5)

    BubbleSort_button = tk.Button(frame, text="Bubble Sort", command=bubble_sort, bg="#008F11", fg="white")
    BubbleSort_button.pack(side=tk.LEFT, padx=5, pady=5)

    QuickSort_button = tk.Button(frame, text="Quick Sort", command=quick_sort, bg="#008F11", fg="white")
    QuickSort_button.pack(side=tk.LEFT, padx=5, pady=5)
    MergeSort_button = tk.Button(frame, text="Merge Sort", command=merge_sort, bg="#008F11", fg="white")
    MergeSort_button.pack(side=tk.LEFT, padx=5, pady=5)
    BucketSort_button = tk.Button(frame, text="Bucket Sort", command=bucket_sort, bg="#008F11", fg="white")
    BucketSort_button.pack(side=tk.LEFT, padx=5, pady=5)


    # Bars
    draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)

    # Loop
    window.mainloop()


if __name__ == "__main__":
    main()
