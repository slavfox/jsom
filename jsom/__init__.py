from jsom.jsomwarnings import TrailingCommaInArray, TrailingCommaInObject, \
    SingleQuotedString, UnquotedString, EmptyObjectValue, JsomWarning

from jsom.parser import JsomParser

__all__ = [
    'SINGLE_QUOTED_STRING', 'UNQUOTED_STRING', 'TRAILING_COMMA_IN_ARRAY',
    'TRAILING_COMMA_IN_OBJECT', 'EMPTY_OBJECT_VALUE', 'ALL_WARNINGS',
    'JsomParser'
]

SINGLE_QUOTED_STRING = SingleQuotedString
UNQUOTED_STRING = UnquotedString
TRAILING_COMMA_IN_ARRAY = TrailingCommaInArray
TRAILING_COMMA_IN_OBJECT = TrailingCommaInObject
EMPTY_OBJECT_VALUE = EmptyObjectValue

ALL_WARNINGS = tuple(w for _, (w, _) in JsomParser._transformers.items())
