from dataclasses import dataclass


class Primitive:
    __is_primitive = True


@dataclass
class OneOf(Primitive):
    values: list


@dataclass
class ListOf(Primitive):
    values: list
