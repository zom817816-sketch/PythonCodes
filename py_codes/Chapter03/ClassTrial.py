# -*- coding: utf-8 -*-
"""
逻辑门类实现
"""


class LogicGate:
    """定义超类"""

    def __init__(self, n):
        self.label = n
        self.output = None

    def getLabel(self):
        return self.label

    def getOutput(self):
        self.output = self.performGateLogic()  # pyright: ignore[reportAttributeAccessIssue]
        return self.output


class BinaryGate(LogicGate):
    """双输入门电路（需要两个输入值）"""

    def __init__(self, n):
        super().__init__(n)
        self.pinA = None
        self.pinB = None

    def getPinA(self):
        if self.pinA is None:
            label = self.getLabel()
            return int(input(f"Enter Pin A input for gate {label} -->"))
        else:
            return self.pinA.getFrom().getOutput()

    def getPinB(self):
        if self.pinB is None:  # 补充判断逻辑，与getPinA保持一致
            label = self.getLabel()
            return int(input(f"Enter Pin B input for gate {label} -->"))
        else:
            return self.pinB.getFrom().getOutput()

    def setNextPin(self, source):  # 移到BinaryGate类中（双输入门才需要）
        if self.pinA is None:
            self.pinA = source  # 修正赋值符号（原为==）
        else:
            if self.pinB is None:
                self.pinB = source
            else:
                raise RuntimeError("Error: NO EMPTY PINS")


class UnaryGate(LogicGate):
    """单输入门电路（只需要一个输入值）"""

    def __init__(self, n):
        super().__init__(n)
        self.pin = None

    def getPin(self):  # 修正方法名（原为getpin，不符合驼峰命名法）
        if self.pin is None:
            return int(input(f"Enter Pin input for gate {self.getLabel()} -->"))
        else:
            return self.pin.getFrom().getOutput()

    def setNextPin(self, source):  # 单输入门的引脚设置
        if self.pin is None:
            self.pin = source
        else:
            raise RuntimeError("Error: NO EMPTY PINS")


class AndGate(BinaryGate):
    """与门：两个输入都为1时输出1，否则输出0"""

    def performGateLogic(self):
        a = self.getPinA()
        b = self.getPinB()
        return 1 if a == 1 and b == 1 else 0


class OrGate(BinaryGate):
    """或门：两个输入至少一个为1时输出1，否则输出0"""

    def performGateLogic(self):
        a = self.getPinA()
        b = self.getPinB()
        return 1 if a == 1 or b == 1 else 0


class NotGate(UnaryGate):
    """非门：输入为1时输出0，输入为0时输出1"""

    def performGateLogic(self):
        a = self.getPin()  # 使用单输入引脚
        return 0 if a == 1 else 1


class Connector:
    """连接两个逻辑门（从一个门的输出连接到另一个门的输入）"""

    def __init__(self, fgate, tgate):
        self.fromgate = fgate
        self.togate = tgate
        tgate.setNextPin(self)  # 调用目标门的引脚设置方法

    def getFrom(self):
        return self.fromgate

    def getTo(self):
        return self.togate


if __name__ == "__main__":
    # 测试与门
    and_gate = AndGate("And1")
    print(f"AndGate {and_gate.getLabel()} 输出: {and_gate.getOutput()}")

    # 测试非门
    not_gate = NotGate("Not1")
    print(f"NotGate {not_gate.getLabel()} 输出: {not_gate.getOutput()}")

    # 测试门电路连接（例如：AndGate输出连接到NotGate输入）
    and2 = AndGate("And2")
    not2 = NotGate("Not2")
    Connector(and2, not2)  # 连接And2的输出到Not2的输入
    print(f"连接后 NotGate {not2.getLabel()} 输出: {not2.getOutput()}")
