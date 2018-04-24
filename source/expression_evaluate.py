import math
import random
import sys
import inspect
from decimal import Decimal
from enum import Enum

precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 's': 4, 'c': 4, 't': 4}

class TrigMode(Enum):
    RADIAN = 1
    DEGREE = 2

def tan(num):
    return math.sin(num) / math.cos(num)

def factorial(num):
    result = 1
    if num // 1 != num:
        raise Exception()
    for i in range(1, int(num) + 1):
        result *= i
    return result

def permutation(n, k):
    result = 1
    for i in range(int(n - k + 1), int(n + 1)):
        result *= i
    return result

def do_optor(opr1, opr2, opt):
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

def do_func(func):
    def do(self, sign):
        num = self.single_num()
        if self.trig_mode == TrigMode.DEGREE:
            if func.__name__ in ('eval_sin', 'eval_cos', 'eval_tan'):
                num = num * math.pi / 180
            elif func.__name__ in ('eval_arcsin', 'eval_arccos', 'eval_arctan'):
                return func(num) * sign * 180
        elif func.__name__ in ('eval_Ran', 'eval_root', 'eval_P', 'eval_C', 'eval_log'):
            base = self.single_num()
            return func(num, base) * sign
        return func(num) * sign
    return do

def assign_decorator(cls, func):
    for method_name in dir(cls):
        attr = getattr(cls, method_name)
        if callable(attr) and not (method_name.endswith('__') or method_name.startswith('__')):
            attr = staticmethod(func(attr))
            setattr(cls, method_name, attr)


class EvalFunc:
    def eval_Ran(num, base):
        return random.randint(num, base)

    def eval_sqr(num):
        return pow(num, 2)

    def eval_abs(num):
        return abs(num)

    def eval_root(num, base):
        return num ** (1 / base)

    def eval_sqrt(num):
        return num ** 0.5

    def eval_log(num, base):
        return math.log(num, base)

    def eval_log10(num):
        return math.log10(num)

    def eval_ln(num):
        return math.log(num, math.e)

    def eval_sin(num):
        return math.sin(num)

    def eval_cos(num):
        return math.cos(num)

    def eval_tan(num):
        return math.sin(num) / math.cos(num)

    def eval_arcsin(num):
        return math.asin(num)

    def eval_arccos(num):
        return math.acos(num)

    def eval_arctan(num):
        return math.atan(num)

    def eval_P(n, k):
        return permutation(n, k)

    def eval_C(n, k):
        return permutation(n, k) // factorial(k)

assign_decorator(EvalFunc, do_func)

class ExpressionEvaluator:
    def __init__(self, trig_mode=TrigMode.RADIAN):
        self.trig_mode = trig_mode
        self.ans = 0

    def parse(self, text):
        self.text = text
        self.i = 0
        self.ans = self.evaluate_expr()
        return self.ans

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

    def single_num(self):
        while self.i < len(self.text) and self.text[self.i] == ' ':
            self.i += 1
        return self.evaluate_expr()

    def evaluate_expr(self):
        optor, oprant = [], []
        while self.i < len(self.text) and self.text[self.i] == ' ':
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
                    oprant.append(do_optor(oprant.pop(), oprant.pop(), optor.pop()))
                optor.append(token)
            elif token == '!':
                oprant.append(factorial(oprant.pop()))
            elif token == '%':
                oprant.append(oprant.pop() / 100)
            elif token == ')':
                break
            elif token == ',':
                self.i += 1
                break
            elif token != ' ':
                sign = self.get_sign(oprant, optor)
                if token == '(':
                    self.i += 1
                    oprant.append(self.evaluate_expr() * sign)
                elif token == 'e':
                    oprant.append(math.e * sign)
                elif token == 'p':
                    self.i += 1
                    oprant.append(math.pi * sign)
                else:
                    func = ''
                    while self.text[self.i] != '(':
                        if self.text[self.i] != ' ':
                            func += self.text[self.i]
                        self.i += 1
                    self.i += 1
                    method = 'eval_' + func
                    oprant.append(getattr(EvalFunc, method)(self, sign))
            self.i += 1
        while optor:
            oprant.append(do_optor(oprant.pop(), oprant.pop(), optor.pop()))
        return oprant[0]


if __name__ == '__main__':
    e = ExpressionEvaluator()

    print(e.parse('Ran(10,100)'))
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
    assert e.parse('(1 + 2) * 5') == (1+2) * 5 * 1.0
    assert e.parse('(1 + 3) * (2 + 3)') == (1+3) * (2+3) * 1.0
    assert e.parse('((1 + 2) * 5 + 2) * 9') == ((1+2) * 5 + 2) * 9 * 1.0

    # More complex Test
    assert e.parse('(1.2 + 5.4) * 3 + 2 * (1 + 2)') == (1.2+5.4) * 3 + 2 * (1+2) * 1.0

    # Test for exponential
    assert e.parse('3 ^ 4') == 3 ** 4 * 1.0
    assert e.parse('5 * 3 ^ 4') == 5 * 3 ** 4 * 1.0
    assert e.parse('3 ^ (2 + 2)') == 3 ** (2+2) * 1.0

    assert e.parse('3 + +--3') == 3 + +--3 * 1.0
    assert e.parse('45 + 45') == 45 + 45 * 1.0

    assert e.parse('sin(cos(10)) + 1') == math.sin(math.cos(10)) + 1
    assert e.parse('sin(3 + 2) * tan(5 - --9 * 2)') == math.sin(3 + 2) * tan(5 - --9 * 2) * 1.0
    assert e.parse('sin(sin(sin(3 + 2)))') == math.sin(math.sin(math.sin(3 + 2))) * 1.0
    assert e.parse('sin(((3 + 3) * 3 + 3) * 3)') == math.sin(((3 + 3) * 3 + 3) * 3) * 1.0
    assert e.parse('sin(-3)') == math.sin(-3)

    assert e.parse('3 - -(3 + 5)') == 3.0 - -(3+5) * 1.0
    assert e.parse('-(3 + 5)') == -(3+5) * 1.0
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

    assert e.parse('root(2, 2)') == 2 ** 0.5
    assert e.parse('P(16, 3)') == 3360
    assert e.parse('P(10, 2)') == 90
    assert e.parse('C(16, 3)') == 560
