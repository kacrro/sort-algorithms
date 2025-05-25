def draw_bars(canvas, data, canvas_width, canvas_height):
    canvas.delete("all")
    bar_width = canvas_width / len(data)
    max_height = max(data)

    for i, val in enumerate(data):
        x0 = i * bar_width
        y0 = canvas_height - (val / max_height) * canvas_height
        x1 = (i + 1) * bar_width
        y1 = canvas_height
        canvas.create_rectangle(x0, y0, x1, y1, fill="skyblue", outline="blue")
