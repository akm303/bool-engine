import logging
from dataclasses import dataclass


@dataclass
class Signal:
    name: str
    value: bool


class Gate:
    def __init__(self, inputs: list[Signal], op):
        assert len(self.inputs) > 0
        self.inputs = inputs
        self.op = op

    def output(self):
        raise NotImplementedError


def and_op(signal1, signal2):
    return signal1 & signal2


def or_op(signal1, signal2):
    return signal1 | signal2


def not_op(signal1, signal2):
    assert signal1 == signal2
    return not signal1


def nand_op(signal1, signal2):
    return not_op(and_op(signal1, signal2))


def nor_op(signal1, signal2):
    return not_op(or_op(signal1, signal2))


class AND(Gate):
    def __init__(self, inputs: list[Signal]):
        super().__init__(inputs, op=and_op)

    def output(self):
        # return all(signal.value == True for signal in self.inputs)
        result = self.inputs[0]
        for signal in self.inputs[1:]:
            result = self.op(result,signal)
        return result


class OR(Gate):
    def __init__(self, inputs: list[Signal]):
        if len(inputs) == 1:
            inputs += inputs
        super().__init__(inputs, op=or_op)

    def output(self):
        # return any(signal.value == True for signal in self.inputs)
        result = self.inputs[0]
        for signal in self.inputs[1:]:
            result = self.op(result,signal)
        return result


class NOT(Gate):
    def __init__(self, input: Signal):
        assert isinstance(input, Signal)
        super().__init__([input], op=not_op)

    def output(self):
        return not self.inputs[0].value


class NAND(Gate):
    def __init__(self, inputs):
        super().__init__(inputs, op=nand_op)


class NOR(Gate):
    def __init__(self, inputs):
        super().__init__(inputs, op=nor_op)



def main():
    pass


if __name__ == "__main__":
    print("running `gates.py")
    print()
else:
    print("importing `gates.py`")