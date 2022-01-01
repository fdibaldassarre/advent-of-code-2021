#!/usr/bin/env python3


POSSIBLE_VARIABLES = {'x', 'y', 'z', 'w'}
TYPE_VAR = 0
TYPE_CON = 1
TYPE_EXPR = 2


class Evaluable:
    def __init__(self, evtype):
        self.evtype = evtype


class Constant(Evaluable):
    def __init__(self, value):
        super().__init__(TYPE_CON)
        self.value = value
        self.min_value = value
        self.max_value = value

    def print(self):
        return str(self.value)

    def eval(self, variables):
        return self.value


class Variable(Evaluable):
    def __init__(self, vid):
        super().__init__(TYPE_VAR)
        self.vid = vid
        self.min_value = 1
        self.max_value = 9

    def print(self):
        return "input" + str(self.vid)

    def eval(self, variables):
        if variables[self.vid] is None:
            print("Cannot eval", self.vid, variables)
            raise Exception("asd")
        return variables[self.vid]


class Expression(Evaluable):
    def __init__(self, op_type, left, right):
        super().__init__(TYPE_EXPR)
        self.op_type = op_type
        self.left = left
        self.right = right
        self.min_value, self.max_value = self._get_min_max()

    def _get_min_max(self):
        if self.op_type == "add":
            return self.left.min_value + self.right.min_value, self.left.max_value + self.right.max_value
        elif self.op_type == "div":
            return int_div(self.left.min_value, self.right.max_value), int_div(self.left.max_value, self.right.min_value)
        elif self.op_type == "mul":
            return self.left.min_value * self.right.min_value, self.left.max_value * self.right.max_value
        elif self.op_type == "mod":
            return 0, self.right.max_value
        elif self.op_type == "eql":
            return 0, 1
        else:
            raise Exception("Invalid operation " + self.op_type)

    def _get_base_eval(self):
        if self.left.min_value == self.left.max_value and self.right.min_value == self.right.max_value:
            left = self.left.min_value
            right = self.right.min_value
            return left, right
        else:
            return None

    def _eval(self, left, right):
        if self.op_type == "add":
            return left + right
        elif self.op_type == "div":
            return int_div(left, right)
        elif self.op_type == "mul":
            return left * right
        elif self.op_type == "eql":
            return 1 if left == right else 0
        elif self.op_type == "mod":
            return left % right
        else:
            raise Exception("Invalid operation")

    def simplify(self):
        instant_eval = self._get_base_eval()
        if instant_eval is not None:
            return Constant(self._eval(*instant_eval))
        if self.op_type == "add":
            if self.left.evtype == TYPE_CON and self.left.value == 0:
                return self.right
            elif self.right.evtype == TYPE_CON and self.right.value == 0:
                return self.left
            else:
                return self
        elif self.op_type == "mul":
            if self.left.evtype == TYPE_CON and self.left.value == 0:
                return Constant(0)
            elif self.right.evtype == TYPE_CON and self.right.value == 0:
                return Constant(0)
            elif self.left.evtype == TYPE_CON and self.left.value == 1:
                return self.right
            elif self.right.evtype == TYPE_CON and self.right.value == 1:
                return self.left
            else:
                return self
        elif self.op_type == "div":
            if self.left.evtype == TYPE_CON and self.left.value == 0:
                return Constant(0)
            if self.right.evtype == TYPE_CON and self.right.value == 1:
                return self.left
            else:
                return self
        elif self.op_type == "mod":
            if self.left.evtype == TYPE_CON and self.left.value == 0:
                return Constant(0)
            else:
                return self
        elif self.op_type == "eql":
            interval_min = max(self.left.min_value, self.right.min_value), min(self.right.max_value, self.left.max_value)
            if interval_min[0] > interval_min[1]:
                # Always false
                return Constant(0)
            else:
                return self
        else:
            raise Exception("Invalid operation")

    def print(self):
        if self.op_type == "eql":
            return "(1 if {x} == {y} else 0)".format(x=self.left.print(), y=self.right.print())
        else:
            return "({x} {op_type} {y})".format(x=self.left.print(), y=self.right.print(), op_type=self.op_type)

    def eval(self, variables):
        left = self.left.eval(variables)
        right = self.right.eval(variables)
        if self.op_type == "add":
            return left + right
        elif self.op_type == "mul":
            return left * right
        elif self.op_type == "div":
            return int_div(left, right)
        elif self.op_type == "mod":
            return left % right
        elif self.op_type == "eql":
            return 1 if left == right else 0


class EqlCondition:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def print(self):
        return "{x} == {y}".format(x=self.left.print(), y=self.right.print())

    def eval(self, variables):
        left = self.left.eval(variables)
        right = self.right.eval(variables)
        return left == right


class UnEqlCondition:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def print(self):
        return "{x} != {y}".format(x=self.left.print(), y=self.right.print())

    def eval(self, variables):
        left = self.left.eval(variables)
        right = self.right.eval(variables)
        return left != right


class ConditionNode:
    def __init__(self, parent, cond=None):
        self.parent = parent
        self.cond = cond
        self.left = None
        self.right = None

    def addSplit(self, left, right):
        self.left = left
        self.right = right


def split(expression):
    if expression.op_type != "eql":
        raise RuntimeError("Cannot split!")
    return (EqlCondition(expression.left, expression.right), Constant(1)), \
           (UnEqlCondition(expression.left, expression.right), Constant(0))


def parse(input_file):
    data = list()
    with open(input_file, "r") as hand:
        for line in hand:
            data.append(line.strip().split(" "))
    return data


def get_value_var(symbol, closure):
    if symbol in POSSIBLE_VARIABLES:
        return closure[symbol]
    return Constant(int(symbol))


def sgn(a):
    return 1 if a >= 0 else -1


def int_div(a, b):
    return sgn(a) * sgn(b) * (abs(a) // abs(b))


class Executor:
    def __init__(self, operations):
        self.operations = operations

    def parse(self, external_closure, variables):
        closures = list()
        root = ConditionNode(None)
        closures.append((root, external_closure.copy()))
        input_id = 0
        for operation in self.operations:
            new_closures = list()
            input_read = False
            for cond, closure in closures:
                op_type = operation[0]
                if op_type == "inp":
                    var = operation[1]
                    closure[var] = variables[input_id]
                    input_read = True
                    new_closures.append((cond, closure))
                else:
                    x = operation[1]
                    y = operation[2]
                    y_val = get_value_var(y, closure)
                    op = Expression(op_type, closure[x], y_val)
                    simplified = op.simplify()
                    if simplified.evtype != TYPE_EXPR or simplified.op_type != "eql":
                        closure[x] = simplified
                        new_closures.append((cond, closure))
                    else:
                        left, right = split(simplified)
                        left_node = ConditionNode(cond, cond=left[0])
                        closure_left = closure.copy()
                        closure_left[x] = left[1]
                        new_closures.append((left_node, closure_left))
                        right_node = ConditionNode(cond, cond=right[0])
                        closure_right = closure.copy()
                        closure_right[x] = right[1]
                        new_closures.append((right_node, closure_right))
                        cond.addSplit(left_node, right_node)
            closures = new_closures
            if input_read:
                input_id += 1
        return root, closures


def solve(operations):
    initial_closure = {
        'x': Constant(0),
        'y': Constant(0),
        'z': Constant(0),
        'w': Constant(0)
    }
    variables = [Variable(i) for i in range(14)]
    executor = Executor(operations)
    cond_node, closures = executor.parse(initial_closure, variables)
    # Get the final formulas that can be evaluated to zero
    valid_final_conditions = list()
    valid_final_formulas = list()
    for condition, closure in closures:
        z_val = closure["z"]
        if z_val.min_value <= 0 <= z_val.max_value:
            valid_final_conditions.append(condition)
            valid_final_formulas.append(z_val)
    # There should be only one formula, and it should always be zero
    assert len(valid_final_conditions) == 1
    valid_final = valid_final_conditions.pop()
    final_formula = valid_final_formulas.pop()
    assert final_formula.print() == "0"

    valid_conditions = list()
    current = valid_final
    while current is not None:
        if current.cond is not None:
            valid_conditions.append(current.cond)
        current = current.parent
    valid_conditions.reverse()

    variables = [None] * 14
    results = set()
    for input0 in range(1, 10):
        variables[0] = input0
        for input1 in range(1, 10):
            variables[1] = input1
            for input2 in range(1, 10):
                variables[2] = input2
                for input3 in range(1, 10):
                    variables[3] = input3
                    if not valid_conditions[0].eval(variables):
                        continue
                    print("Check", input0, input1, input2, input3)
                    for input4 in range(1, 10):
                        variables[4] = input4
                        for input5 in range(1, 10):
                            variables[5] = input5
                            if not valid_conditions[1].eval(variables):
                                continue
                            for input6 in range(1, 10):
                                variables[6] = input6
                                for input7 in range(1, 10):
                                    variables[7] = input7
                                    for input8 in range(1, 10):
                                        variables[8] = input8
                                        for input9 in range(1, 10):
                                            variables[9] = input9
                                            if not valid_conditions[2].eval(variables):
                                                continue
                                            for input10 in range(1, 10):
                                                variables[10] = input10
                                                if not valid_conditions[3].eval(variables):
                                                    continue
                                                for input11 in range(1, 10):
                                                    variables[11] = input11
                                                    if not valid_conditions[4].eval(variables):
                                                        continue
                                                    for input12 in range(1, 10):
                                                        variables[12] = input12
                                                        if not valid_conditions[5].eval(variables):
                                                            continue
                                                        for input13 in range(1, 10):
                                                            variables[13] = input13
                                                            if not valid_conditions[6].eval(variables):
                                                                continue
                                                            results.add("".join(map(str, variables)))

    return max(results), min(results)


if __name__ == "__main__":
    data = parse("input")
    solution1, solution2 = solve(data)
    print("Solution 1: %s" % solution1)
    print("Solution 2: %s" % solution2)
