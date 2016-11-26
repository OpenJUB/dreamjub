from rest_framework import filters
import PreJsPy
from . import builder as qb
"""This module holds TLFilter."""


class TLFilter(filters.BaseFilterBackend):
    """A filter that parses complex queries into JSON, then into Django
    queries"""

    def filter_queryset(self, request, queryset, view):
        parser = PreJsPy.PreJsPy()
        builder = qb.QBuilder()

        query_str = request.GET.get('tl', default=None)

        if not query_str:
            return queryset

        filter_obj = parser.parse(query_str)
        q_obj = builder.translate(filter_obj)

        return queryset.filter(q_obj)
