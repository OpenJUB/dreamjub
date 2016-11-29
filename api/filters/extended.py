from rest_framework import filters
import PreJsPy
from . import builder as qb
"""This module holds TLFilter."""


class TLFilter(filters.BaseFilterBackend):
    """A filter that parses complex queries into JSON, then into Django
    queries"""

    def filter_queryset(self, request, queryset, view):
        parser = PreJsPy.PreJsPy()

        # Do not use the tertiary operator -- we do not need it
        parser.setTertiaryOperatorEnabled(False)

        # Set up the unary operators properly
        parser.setUnaryOperators([
            'not', '!', '~'
        ])

        parser.setBinaryOperators({
            # LOGICAL CONNECTIVES
            'and': 1, '&': 1, '&&': 1, '*': 1,
            'or': 1, '|': 1, '||': 1, '+': 1,
            'nand': 1, '!&': 1,
            'xor': 1, '^': 1,

            # Filters
            'equals': 2, ':': 2, '=': 2, '==': 2, '===': 2,
            'less than': 2, '<': 2,
            'less than or equal': 2, '<=': 2, '=<': 2,
            'greater than': 2, '>': 2,
            'greater than or equal': 2, '>=': 2, '=>': 2,
            'contains': 2, '::': 2,
            'matches': 2, 'unicorn': 2, '@': 2,
        })

        builder = qb.QBuilder()

        query_str = request.GET.get('tl', default=None)

        if not query_str:
            return queryset

        filter_obj = parser.parse(query_str)
        q_obj = builder.translate(filter_obj)

        return queryset.filter(q_obj)
