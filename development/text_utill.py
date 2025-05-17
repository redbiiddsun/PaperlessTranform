class LineContext:
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.index = 0

    def __iter__(self):
        self.index = 0  # Reset index each time it's iterated
        return self

    def __next__(self):
        if self.index >= len(self.lines):
            raise StopIteration
        self.index += 1
        return self
    
    def __str__(self):
        return str(self.lines)

    def __repr__(self):
        return f"LineContext({self.lines})"
    
    def _get_line(self, idx: int) -> str:
        if 0 <= idx < len(self.lines):
            return self.lines[idx]
        return None

    def current(self) -> str:
        return self._get_line(self.index - 1)

    def previous(self, n: int = 1) -> str:
        return self._get_line(self.index - 1 - n)

    def next(self, n: int = 1) -> str:
        return self._get_line(self.index - 1 + n)
