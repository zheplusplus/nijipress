from UserDict import UserDict


class Node(UserDict):
    def __init__(self, node_type, **kwargs):
        UserDict.__init__(self, type=node_type, **kwargs)

    def first(self):
        return None


class Name(Node):
    def __init__(self, name):
        Node.__init__(self, 'name', name=name)

    def first(self):
        return self['name']


class PreUnaryOp(Node):
    def __init__(self, op, rhs):
        Node.__init__(self, 'preu', op=op, rhs=rhs)

    def first(self):
        return self['op']


class BinaryOp(Node):
    def __init__(self, node_type, op, lhs, rhs):
        Node.__init__(self, node_type, op=op, lhs=lhs, rhs=rhs)

    def first(self):
        return self['lhs'].first()


def additive_binary(op, lhs, rhs):
    return BinaryOp('add', op, lhs, rhs)


def multiplication(lhs, rhs):
    return BinaryOp('mul', None, lhs, rhs)


def division(lhs, rhs):
    return Node('div', lhs=lhs, rhs=rhs)


def relation_op(op, lhs, rhs):
    return BinaryOp('rel', op, lhs, rhs)


class Equation(Node):
    def __init__(self, first, operators, tails):
        Node.__init__(self, 'eq', first=first, ops=operators, tails=tails)

    def first(self):
        return self['first'].first()


class Subscript(Node):
    def __init__(self, name, sub):
        Node.__init__(self, 'sub', name=name, sub=sub)

    def first(self):
        return self['name'].first()


class Exponentiation(Node):
    def __init__(self, base, exponent):
        Node.__init__(self, 'exp', base=base, exponent=exponent)

    def first(self):
        return self['base'].first()


def absolute_value(value):
    return Node('abs', value=value)


def root(degree, number):
    return Node('root', degree=degree, number=number)


def square_root(number):
    return root(Name('2'), number)


class Function(Node):
    def __init__(self, callee, args):
        Node.__init__(self, 'func', callee=callee, args=args)

    def first(self):
        return self['callee'].first()


def set_node(elements, restrict):
    return Node('set', elements=elements, restrict=restrict)


class QuadraticStruct(Node):
    def __init__(self, name, form):
        Node.__init__(self, 'quad', name=name, form=form)

    def first(self):
        return self['name'].first()


class CongruentModulo(Node):
    def __init__(self, mod_chain, last_expr, last_op, mod):
        Node.__init__(self, 'comod', mod_chain=mod_chain, last_expr=last_expr,
                      last_op=last_op, mod=mod)

    def first(self):
        return self['mod_chain'][0].first()


def expr_tuple(elements):
    return Node('tuple', elements=elements)
