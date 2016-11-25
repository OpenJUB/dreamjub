from . import operators as ops
"""This module holds QBuilder."""

class QBuilder(object):
    """Generates a Django Q object from a PreJSPy filter JSON object"""

    def translate(self, filter_obj):
        if not filter:
            raise ValueError("Filter was empty")

        # Get filter type
        try:
            obj_type = filter_obj['type']
        except KeyError:
            raise ValueError("Filter has no type")

        # Decide what to do based on filter type
        if obj_type == ops.BIN_TYPE:
            return self._generate_binary(filter_obj)

        elif obj_type == ops.UN_TYPE:
            return self._generate_unary(filter_obj)

        elif obj_type in [ops.IDENTITY_TYPE, ops.STRING_TYPE]:
            return self._generate_literal(filter_obj)

        else:
            raise NotImplementedError("Invalid filter type: " + obj_type)

    def _generate_binary(self, filter_obj):
        try:
            left = filter_obj['left']
            right = filter_obj['right']
            filter_type = filter_obj['operator']
        except KeyError as e:
            raise ValueError("Filter is incomplete: " + str(e))

        try:
            op = ops.BIN_OPS[filter_type]
        except KeyError:
            raise ValueError("Unknown binary expression: " + filter_type)

        return op(self.translate(left), self.translate(right))

    def _generate_unary(self, filter_obj):
        raise NotImplementedError

    def _generate_literal(self, literal):
        try:
            if literal['type'] == ops.IDENTITY_TYPE:
                return literal['name']
            elif literal['type'] == ops.STRING_TYPE:
                return literal['value']
            else:
                raise NotImplementedError
        except KeyError:
            raise ValueError("Invalid literal: " + literal)