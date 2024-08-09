class Eagle:
    def __init__(self, name, wingspan):
        self.name = name
        self.wingspan = wingspan

    def fly(self):
        return f"{self.name} soars high with a wingspan of {self.wingspan} meters!"

    def __str__(self):
        return f"Eagle(name={self.name}, wingspan={self.wingspan})"