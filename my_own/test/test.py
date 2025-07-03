def bucket_sort():
    if not data:
        return

    # Parametry dla bucket sort
    bucket_count = 10  # Liczba kubełków
    min_val = min(data)
    max_val = max(data)
    bucket_range = (max_val - min_val) / bucket_count

    # Tworzenie kubełków
    buckets = [[] for _ in range(bucket_count)]

    # Stan animacji
    state = {
        'phase': 'distribute',  # 'distribute', 'sort_buckets', 'collect'
        'current_item': 0,
        'current_bucket': 0,
        'sorted_data': [],
        'buckets': buckets
    }

    def sort_step():
        if state['phase'] == 'distribute':
            # Faza 1: Rozdzielanie elementów do kubełków
            if state['current_item'] >= len(data):
                state['phase'] = 'sort_buckets'
                state['current_bucket'] = 0
                window.after(delay, sort_step)
                return

            # Określ do którego kubełka należy element
            item = data[state['current_item']]
            if item == max_val:
                bucket_index = bucket_count - 1
            else:
                bucket_index = int((item - min_val) / bucket_range)

            # Dodaj element do kubełka
            state['buckets'][bucket_index].append(item)

            # Podświetl aktualnie przetwarzany element
            draw_bars_with_highlight(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT, state['current_item'])

            state['current_item'] += 1
            window.after(delay, sort_step)

        elif state['phase'] == 'sort_buckets':
            # Faza 2: Sortowanie każdego kubełka (używamy wbudowanego sort)
            if state['current_bucket'] >= bucket_count:
                state['phase'] = 'collect'
                state['current_bucket'] = 0
                window.after(delay, sort_step)
                return

            # Sortuj aktualny kubełek
            if state['buckets'][state['current_bucket']]:
                state['buckets'][state['current_bucket']].sort()

            state['current_bucket'] += 1
            window.after(delay, sort_step)

        elif state['phase'] == 'collect':
            # Faza 3: Zbieranie posortowanych elementów z kubełków
            if state['current_bucket'] >= bucket_count:
                # Sortowanie zakończone
                draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)
                return

            # Zbierz elementy z aktualnego kubełka
            if state['buckets'][state['current_bucket']]:
                state['sorted_data'].extend(state['buckets'][state['current_bucket']])

            # Aktualizuj dane
            for i, val in enumerate(state['sorted_data']):
                if i < len(data):
                    data[i] = val

            # Wyczyść resztę tablicy (jeśli trzeba)
            remaining_start = len(state['sorted_data'])
            for i in range(remaining_start, len(data)):
                if i < len(data):
                    data[i] = 0

            # Narysuj aktualny stan
            draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)

            state['current_bucket'] += 1
            window.after(delay, sort_step)

    sort_step()