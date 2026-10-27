class No:
    def __init__(self, content):
        self.content = content
        self.next = None

piece_a = No("Peça A")
piece_b = No("Peça B")

piece_a.next = piece_b

