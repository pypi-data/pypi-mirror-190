import operator

opdict = {
    "+": operator.add,
    "concat": operator.concat,  # also + in Python
    "in": operator.contains,
    "/": operator.truediv,
    "//": operator.floordiv,
    "&": operator.and_,
    "^": operator.xor,
    "~": operator.invert,
    "|": operator.or_,
    "**": operator.pow,
    "is": operator.is_,
    "is not": operator.is_not,
    "=": operator.setitem,
    "del": operator.delitem,
    "[]": operator.getitem,
    "<<": operator.lshift,
    "%": operator.mod,
    "*": operator.mul,
    "@": operator.matmul,
    "neg": operator.neg,  # also -
    "not": operator.not_,
    "pos": operator.pos, # also +
    ">>": operator.rshift,
    "-": operator.sub,
    "truth": operator.truth,
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
    ">=": operator.ge,
    ">": operator.gt,
    "+=": operator.iadd,
    "&=": operator.iand,
    "iconcat": operator.iconcat, # also +=
    "//=": operator.ifloordiv,
    "<<=": operator.ilshift,
    "%=": operator.imod,
    "*=": operator.imul,
    "@=": operator.imatmul,
    "|=": operator.ior,
    "**=": operator.ipow,
    ">>=": operator.irshift,
    "-=": operator.isub,
    "/=": operator.itruediv,
    "^=": operator.ixor,
}


def doops(op=None, *args, **kwargs):
    def _print_all():
        for key, item in opdict.items():
            print(f"Operator: {str(key).ljust(10)}\nFunction: {item.__name__}")
            help(item)
            print("_______________________")

    if not op:
        _print_all()
    else:
        try:
            opi = opdict.__getitem__(op)
        except KeyError as fe:
            _print_all()
            print("Operator not found!")
            raise fe

        return opi(*args, **kwargs)
