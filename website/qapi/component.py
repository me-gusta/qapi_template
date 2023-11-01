import json
from dataclasses import dataclass
from typing import Any


@dataclass
class Component:
    name: str
    t: Any
    all = {}

    def __post_init__(self):
        self.all[self.name] = self.t

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __hash__(self):
        return hash(self.name)
