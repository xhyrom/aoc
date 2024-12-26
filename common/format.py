def format_time(time: float) -> str:
    if time < 1000:
        value = time
        unit = "ns"
    elif time < 1000000:
        value = time / 1000
        unit = "µs"
    elif time < 1000000000:
        value = time / 1000000
        unit = "ms"
    elif time < 60000000000:
        value = time / 1000000000
        unit = "s"
    else:
        value = time / (60 * 1000000000)
        unit = "min"

    if abs(value - round(value)) < 0.0001:
        return f"{int(round(value))} {unit}"

    return f"{value:.3f} {unit}"


def rgb_to_ansi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"
