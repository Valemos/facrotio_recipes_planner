from dataclasses import dataclass

from serialization.a_composite_json_serializable import ACompositeJsonSerializable


@dataclass(eq=True)
class EntityFactorio(ACompositeJsonSerializable):
    x_pos: int = 0
    y_pos: int = 0
    orientation: int = 0
