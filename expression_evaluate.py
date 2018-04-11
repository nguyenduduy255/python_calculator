from decimal import Decimal
from enum import Enum
import math

precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 's': 4, 'c': 4, 't': 4}

class TrigMode(Enum):
    RADIAN = 1
    DEGREE = 2
trig_mode = TrigMode.RADIAN

def tan(x):
    return math.sin(x) / math.cos(x)

def factorial(num):
    result = 1
    if num // 1 != num:
        raise Exception()
    for i in range(1, int(num) + 1):
        result *= i
    return result

class ExpressionEvaluator:
    def __init__(self, trig_mode=TrigMode.RADIAN):
        self.trig_mode = trig_mode
        self.ans = 0

    def parse(self, text):
        self.text = text
        self.i = -1
        self.ans = self.evaluate_expr()
        return self.ans

    def factorial(self, n):
        return factorial(n)

    def tan(self, x):
        return tan(x)

    def get_sign(self, oprant, optor):
        sign = 1
        # Use the property that len(oprant) == len(optor)
        # Ex: oprant = [1, 3, 4] and optor = [*, -, +, -, +, -, -] this is 1 * 3 - +-+-- 4
        while len(oprant) < len(optor) and optor[-1] in '+-':
            top_sign = optor.pop()
            if top_sign == '-':
                sign *= -1
        return sign

    def get_num(self, oprant=None, optor=None):
        sign = self.get_sign(oprant, optor)

        tnum = ''
        while len(self.text) > self.i and (self.text[self.i].isdigit() or self.text[self.i] == '.'):
            tnum += self.text[self.i]
            self.i += 1
        self.i -= 1
        if tnum:
            return float(tnum) * sign
            # return Decimal(tnum) * sign

    def evaluate_expr(self):
        self.i += 1
        optor, oprant = [], []
        while self.text[self.i] == ' ':
            self.i += 1

        # like -(3 + 5) -> 0 - (3 + 5)
        if self.text[self.i] in '+-':
            oprant.append(0)

        while self.i < len(self.text):
            token = self.text[self.i]
            # Get the number like +-45 + 3 -> -45 and 3
            if token.isdigit() or token == '.':
                oprant.append(self.get_num(oprant=oprant, optor=optor))
            elif token in '+-*/^':
                while len(oprant) > 1 and optor and precedence[optor[-1]] >= precedence[token]:
                    oprant.append(self.do_optor(oprant.pop(), oprant.pop(), optor.pop()))
                optor.append(token)
            elif token == '!':
                oprant.append(self.factorial(oprant.pop()))
            elif token == '%':
                oprant.append(oprant.pop() / 100)
            elif token == ')' or token == ',':
                break
            elif token != ' ':
                sign = self.get_sign(oprant, optor)
                if token in 'sct': # for sin cos tan ans sqrt
                    if self.text[self.i + 1] == 'q': # sqrt and sqr
                        if self.text[self.i + 3] == 't':
                            oprant.append(self.eval_root() * sign)
                        else:
                            oprant.append(self.eval_sqr() * sign)
                    else: # sin cos tan
                        oprant.append(self.eval_trig() * sign)
                elif token == 'p': # number pi
                    self.i += 1
                    oprant.append(math.pi * sign)
                elif token == 'a': # for ans abs and arctrig
                    next_char = self.text[self.i + 1]
                    if next_char == 'n': # ans
                        self.i += 2
                        oprant.append(self.ans * sign)
                    elif next_char == 'b': # abs
                        oprant.append(self.eval_abs() * sign)
                    elif next_char == 'r': # arctrig
                        oprant.append(self.eval_arctrig() * sign)
                elif token == 'e': # number e
                    oprant.append(math.e * sign)
                elif token == 'r': # root
                    oprant.append(self.eval_root() * sign)
                elif token == 'l': # log
                    oprant.append(self.eval_log() * sign)
                elif token == '(':
                    oprant.append(self.evaluate_expr() * sign)
            self.i += 1

        while optor:
            oprant.append(self.do_optor(oprant.pop(), oprant.pop(), optor.pop()))
        return oprant[0]

    def eval_sqr(self):
        self.i += 3
        while self.text[self.i] == ' ':
            self.i += 1
        num = self.evaluate_expr()
        return num ** 2

    def eval_abs(self):
        self.i += 3
        while self.text[self.i] == ' ':
            self.i += 1
        num = self.evaluate_expr()
        return abs(num)

    def eval_root(self):
        token = self.text[self.i]
        self.i += 4
        while self.text[self.i] == ' ':
            self.i += 1
        num = self.evaluate_expr()
        if token == 's':
            base = 2
        else:
            base = self.evaluate_expr()
        return num ** (1 / base)

    def eval_log(self):
        if self.text[self.i + 1] == 'n':
            base = math.e
            self.i += 2
        elif self.text[self.i + 3] == '1':
            base = 10
            self.i += 5
        else:
            base = None
            self.i += 3

        while self.text[self.i] == ' ':
            self.i += 1

        num = self.evaluate_expr()
        self.i += 1
        if base is None:
            base = self.evaluate_expr()
        return math.log(num, base)
        # return Decimal(log(num, base))

    def eval_arctrig(self):
        func = self.text[self.i + 3]
        self.i += 6
        while self.text[self.i] == ' ':
            self.i += 1
        num = self.evaluate_expr()
        result = self.do_arctrig(num, func)
        if self.trig_mode == TrigMode.DEGREE:
            result = math.degrees(result)
        return result

    def eval_trig(self):
        func = self.text[self.i]
        self.i += 3
        while self.text[self.i] == ' ':
            self.i += 1
        num = self.evaluate_expr()
        if self.trig_mode == TrigMode.DEGREE:
            num = math.radians(num)
        return self.do_trig(num, func)
        # return Decimal(do_trig(num, func))

    def do_trig(self, opr, opt):
        if opt == 's':
            return math.sin(opr)
        elif opt == 'c':
            return math.cos(opr)
        elif opt == 't':
            return self.tan(opr)

    def do_arctrig(self, opr, opt):
        if opt == 's':
            return math.asin(opr)
        elif opt == 'c':
            return math.acos(opr)
        elif opt == 't':
            return math.atan(opr)

    def do_optor(self, opr1, opr2, opt):
        if opt == '+':
            return opr1 + opr2
        elif opt == '-':
            return opr2 - opr1
        elif opt == '*':
            return opr1 * opr2
        elif opt == '/':
            return opr2 / opr1
        elif opt == '^':
            return opr2 ** opr1

if __name__ == '__main__':
    e = ExpressionEvaluator()
    # Test for basic evaluate
    assert e.parse('9 - 2') == 9 - 2 * 1.0
    assert e.parse('9 + 2') == 9 + 2 * 1.0
    assert e.parse('9 * 2') == 9 * 2 * 1.0
    assert e.parse('9 / 2') == 9 / 2 * 1.0
    assert e.parse('0 - 2') == 0 - 2 * 1.0
    assert e.parse('-1 / 2') == -1 / 2 * 1.0

    # Test for float
    assert e.parse('1.5 + 2.3') == 1.5 + 2.3 * 1.0
    assert e.parse('1.8 - 2.0') == 1.8 - 2.0 * 1.0
    assert e.parse('3.5 * 0.4') == 3.5 * 0.4 * 1.0

    # Test for parenthesis
    assert e.parse('(1 + 2) * 5') == (1 + 2) * 5 * 1.0
    assert e.parse('(1 + 3) * (2 + 3)') == (1 + 3) * (2 + 3) * 1.0
    assert e.parse('((1 + 2) * 5 + 2) * 9') == ((1 + 2) * 5 + 2) * 9 * 1.0

    # More complex Test
    assert e.parse('(1.2 + 5.4) * 3 + 2 * (1 + 2)') == (1.2 + 5.4) * 3 + 2 * (1 + 2) * 1.0

    # Test for exponential
    assert e.parse('3 ^ 4') == 3 ** 4 * 1.0
    assert e.parse('5 * 3 ^ 4') == 5 * 3 ** 4 * 1.0
    assert e.parse('3 ^ (2 + 2)') == 3 ** (2 + 2) * 1.0

    assert e.parse('3 + +--3') == 3 + +--3 * 1.0
    assert e.parse('45 + 45') == 45 + 45 * 1.0

    assert e.parse('sin(cos(10)) + 1') == math.sin(math.cos(10)) + 1
    assert e.parse('sin(3 + 2) * tan(5 - --9 * 2)') == math.sin(3 + 2) * tan(5 - --9 * 2) * 1.0
    assert e.parse('sin(sin(sin(3 + 2)))') == math.sin(math.sin(math.sin(3 + 2))) * 1.0
    assert e.parse('sin(((3 + 3) * 3 + 3) * 3)') == math.sin(((3 + 3) * 3 + 3) * 3) * 1.0
    assert e.parse('sin(-3)') == math.sin(-3)

    assert e.parse('3 - -(3 + 5)') == 3.0 - -(3 + 5) * 1.0
    assert e.parse('-(3 + 5)') == -(3 + 5) * 1.0
    assert e.parse('- sin(3)') == - math.sin(3) * 1.0
    assert e.parse('--(((((3) + 3))))') == --(((((3) + 3)))) * 1.0

    assert e.parse('pi*3') == math.pi * 3

    assert e.parse('1!') == factorial(1)
    assert e.parse('2!') == factorial(2)
    assert e.parse('3!') == factorial(3)
    assert e.parse('2 +---- 3!') == 2 + factorial(3)

    assert e.parse('log(3, 3)') == math.log(3, 3)
    assert e.parse('log(3 + 3, 3)') == math.log(6, 3)
    assert e.parse('log((3 + 3 + 3), 3)') == math.log(9, 3)
    assert e.parse('log(3, 3 + 3)') == math.log(3, 6)
    assert e.parse('log(3, (3 + 3))') == math.log(3, 6)
    assert e.parse('log(3 + 3, 3 + 3)') == math.log(6, 6)

    assert e.parse('log(13, 4) + 10 * 3') == math.log(13, 4) + 10 * 3
    assert e.parse('log10(3)') == math.log(3, 10)
    assert e.parse('ln(3)') == math.log(3, math.e)
    assert e.parse('log     (3, 3)') == math.log(3, 3)

    assert e.parse('sqrt(9)') == math.sqrt(9)
    assert e.parse('sqrt(9 + 3)') == math.sqrt(9 + 3)
    assert e.parse('sqrt(((((9)))))') == math.sqrt(9)
    assert e.parse('sqrt(---- 9 * 3)') == math.sqrt(27)
    assert e.parse('root(9, 3)') == 9 ** (1 / 3)

    assert e.parse('abs(-3)') == abs(-3)
    assert e.parse('abs(-3) - abs(3 + 3 - 9)') == abs(-3) - abs(3 + 3 - 9)

    assert e.parse('arcsin(0.5)') == math.asin(0.5)
    assert e.parse('e') == math.e
