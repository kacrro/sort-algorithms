def draw_bars(canvas, data, canvas_width, canvas_height):
    canvas.delete("all")
    bar_width = canvas_width / len(data)
    max_height = (max(data) + 5) if data else 1  # Avoid division by zero

    for i, val in enumerate(data):  # Iterate over the data
        x0 = i * bar_width + 3  # Add a small offset for better visibility
        y0 = canvas_height - (val / max_height) * canvas_height  # Adjust y0 to leave space for the value text
        x1 = (i + 1) * bar_width -3
        y1 = canvas_height  # reverse the y-axis for the bar chart
        canvas.create_rectangle(x0, y0, x1, y1, fill="#008F11", outline="#00FF41")

        # value text
        text_x = (x0 + x1) / 2
        text_y = y0 - 10
        canvas.create_text(text_x, text_y, text=str(val), fill="white", font=("Arial", 8))


def draw_bars_with_highlight(canvas, data, canvas_width, canvas_height, highlight1=-1, highlight2=-1):
    canvas.delete("all")
    bar_width = canvas_width / len(data)
    max_height = (max(data) + 5) if data else 1

    for i, val in enumerate(data):
        x0 = i * bar_width + 3
        y0 = canvas_height - (val / max_height) * canvas_height
        x1 = (i + 1) * bar_width
        y1 = canvas_height

        # Wybierz kolor słupka
        if i == highlight1 or i == highlight2:
            fill_color = "#FF0000"  # Czerwony dla porównywanych
            outline_color = "#FF4444"
        else:
            fill_color = "#008F11"
            outline_color = "#00FF41"

        canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline=outline_color)

        text_x = (x0 + x1) / 2
        text_y = y0 - 10
        canvas.create_text(text_x, text_y, text=str(val), fill="white", font=("Arial", 8))