from dataclasses import dataclass, field


@dataclass
class Material:
    '''a bunch of items of the same type'''

    id: str
    amount: float = field(default=1)

    def __mul__(self, multiplier):
        assert isinstance(multiplier, float) or isinstance(multiplier, int)
        return Material(self.id, self.amount * multiplier)

    def __add__(self, other):
        assert issubclass(other.__class__, self.__class__)
        if other.id != self.id: raise ValueError("cannot add items of different types")
        return Material(self.id, self.amount + other.amount)

    @staticmethod
    def from_dict(ingredient):
        return Material(ingredient['id'], ingredient['amount'])
