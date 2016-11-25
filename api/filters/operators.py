import operator
from django.db import models

"""This module holds all the logical and non-logical operators and static
definitions used in QBuilder."""


def not_impl(*args):
    raise NotImplementedError

# Binary logic expressions
and_fn = operator.and_
or_fn = operator.or_
not_fn = operator.invert


def xor_fn(x, y):
    return or_fn(and_fn(not_fn(x), y), and_fn(x, not_fn(y)))


# Django filters
def q_lambda(dj_filter="exact"):
    return lambda x, y: models.Q(**{x + '__' + dj_filter: y})


def not_eq(x, y):
    return not_fn(q_lambda()(x, y))

UNARY_OPS = {
    '-': not_impl,
    '!': not_fn,
    '~': not_fn,
    '+': not_impl
}

BIN_OPS = {
    '||': or_fn,
    '&&': and_fn,
    '|': or_fn,
    '^': xor_fn,
    '&': and_fn,
    '==': q_lambda(),
    '!=': not_eq,
    '===': q_lambda(),
    '!==': not_eq,
    '<': q_lambda('lt'),
    '>': q_lambda('gt'),
    '<=': q_lambda('lte'),
    '>=': q_lambda('gte'),

    '<<': not_impl,
    '>>': not_impl,
    '>>>': not_impl,
    '+': not_impl,
    '-': not_impl,
    '*': not_impl,
    '/': not_impl,
    '%': not_impl
}

BIN_TYPE = 'BinaryExpression'
UN_TYPE = 'UnaryExpression'
IDENTITY_TYPE = 'Identifier'
STRING_TYPE = 'Literal'
