from dataclasses import dataclass


@dataclass
class Attori:
    id: str
    name: str
    height: int
    date_of_birth: str
    known_for_movies: int

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.name}"