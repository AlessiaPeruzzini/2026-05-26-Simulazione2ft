from dataclasses import dataclass

from model.attori import Attori


@dataclass
class Arco:
    at1: Attori
    at2: Attori
    peso: int