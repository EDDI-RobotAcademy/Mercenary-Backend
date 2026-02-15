from dataclasses import dataclass

@dataclass(frozen=True)
class Nickname:
    value: str

    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("Nickname cannot be empty")

        if len(self.value) > 30:
            raise ValueError("Nickname too long")
