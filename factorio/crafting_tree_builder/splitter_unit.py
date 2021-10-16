from dataclasses import field, dataclass


@dataclass(eq=True, unsafe_hash=True)
class SplitterUnit:
    name: str = ""
    item_rate: float = field(default=0, hash=True)

    def __str__(self):
        return f"Rate: {self.item_rate}"
