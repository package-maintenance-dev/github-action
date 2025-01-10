def render_code(text: str):
    return f"<code>{text}</code>"


def render_colored_code(text: str, color: str):
    return f'<code style="color: {color}">{text}</code>'


def render_colored_code_conditionally(text: str, color: str, condition: bool):
    if condition:
        return render_colored_code(text, color)
    return render_code(text)


def render_url(name: str, url: str):
    return f"[{name}]({url})"
