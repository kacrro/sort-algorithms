def draw_bars(canvas, data, canvas_width, canvas_height):
    canvas.delete("all")
    bar_width = canvas_width / len(data)
    max_height = max(data) if data else 1  # Avoid division by zero

    for i, val in enumerate(data):  # Iterate over the data
        x0 = i * bar_width
        y0 = canvas_height - (val / max_height) * canvas_height + 20  # Adjust y0 to leave space for the value text
        x1 = (i + 1) * bar_width
        y1 = canvas_height  # reverse the y-axis for the bar chart
        canvas.create_rectangle(x0, y0, x1, y1, fill="skyblue", outline="blue")

        # value text
        text_x = (x0 + x1) / 2
        text_y = y0 - 10
        canvas.create_text(text_x, text_y, text=str(val), fill="white", font=("Arial", 8))
