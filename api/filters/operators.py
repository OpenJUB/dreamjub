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


def nand_fn(x, y):
    return not_fn(and_fn(x, y))


# Django filters
def q_lambda(dj_filter="exact"):
    return lambda x, y: models.Q(**{x + '__' + dj_filter: y})


def not_eq(x, y):
    return not_fn(q_lambda()(x, y))

UNARY_OPS = {
    'not': not_fn,
    '!': not_fn,
    '~': not_fn
}

BIN_OPS = {
    # LOGICAL CONNECTIVES
    'and': and_fn, '&': and_fn, '&&': and_fn, '*': and_fn,

    'or': or_fn, '|': or_fn, '||': or_fn, '+': or_fn,

    'nand': nand_fn, '!&': nand_fn,

    'xor': xor_fn, '^': xor_fn,

    # FILTERS
    'equals': q_lambda(),
    'eq': q_lambda(),
    ':': q_lambda(),
    '=': q_lambda(),
    '==': q_lambda(),
    '===': q_lambda(),

    '!=': not_eq,

    'less than': q_lambda('lt'),
    '<': q_lambda('lt'),

    'less than or equal': q_lambda('lte'),
    '<=': q_lambda('lte'),
    '=<': q_lambda('lte'),

    'greater than': q_lambda('gt'),
    '>': q_lambda('gt'),

    'greater than or equal': q_lambda('gte'),
    '>=': q_lambda('gte'),
    '=>': q_lambda('gte'),

    'contains': q_lambda('contains'),
    '::': q_lambda('contains'),

    'matches': q_lambda('regex'),
    'unicorn': q_lambda('regex'),
    '@': q_lambda('regex')
}

COMPOUND_TYPE = 'Compound'
BIN_TYPE = 'BinaryExpression'
UN_TYPE = 'UnaryExpression'
IDENTITY_TYPE = 'Identifier'
STRING_TYPE = 'Literal'
