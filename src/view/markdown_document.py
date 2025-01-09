class MarkdownDocument:
    """
    This is a mutable class for building Markdown documents.

    Notes:
    - This class implements only a subset of the markdown specification for project purposes.
    - Full markdown specification can be found at: https://www.markdownguide.org/cheat-sheet/
    - Each method returns the current instance, so calls can be chained.
    """

    def __init__(self, content: str = ""):
        self._content = content

    def get_content(self) -> str:
        return self._content

    def heading(self, text: str, level: int = 1) -> "MarkdownDocument":
        if not (1 <= level <= 6):
            raise ValueError("Heading level must be between 1 and 6")
        self._content += f"{'#' * level} {text}\n"
        return self

    def bold(self, text: str) -> "MarkdownDocument":
        self._content += f"**{text}**\n"
        return self

    def italic(self, text: str) -> "MarkdownDocument":
        self._content += f"*{text}*\n"
        return self

    def table(self, headers: list[str], rows: list[list[str]]) -> "MarkdownDocument":
        # Validate the number of columns in each row
        column_count = len(headers)
        for row in rows:
            if len(row) != column_count:
                raise ValueError("Each row must have the same number of columns as the headers")

        # Create the table
        self._content += "| " + " | ".join(headers) + " |\n"
        self._content += "| " + " | ".join(["---"] * column_count) + " |\n"
        for row in rows:
            self._content += "| " + " | ".join(row) + " |\n"
        return self

    def text(self, text: str) -> "MarkdownDocument":
        self._content += f"{text}\n"
        return self
