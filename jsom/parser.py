from __future__ import annotations

from ast import literal_eval
from typing import Tuple, Dict, List, Union, Type, Callable, Any, IO, Iterable

# noinspection PyPackageRequirements
# PyCharm throws a fit here for some reason
from lark import Lark, Transformer, Token, v_args

from jsom.jsomwarnings import TrailingCommaInArray, TrailingCommaInObject, \
    SingleQuotedString, UnquotedString, EmptyObjectValue, JsomWarning
from jsom.transformer_methods import get_array_transformer, \
    get_identifier_transformer, \
    get_object_transformer, get_sqstring_transformer, \
    get_object_item_empty_transformer, JsomValue

jsom_grammar = r"""
?start: value

?value: object
      | array
      | NUMBER               -> number
      | "true"               -> true
      | "false"              -> false
      | "null"               -> null
      | string
      | identifier

array : "[" [value ("," value)*] [","] "]"

object : "{" [object_item ("," object_item)*] [","] "}"

object_item: string ":" value     -> object_item
           | identifier ":" value -> object_item
           | string ":"           -> object_item_empty
           | identifier ":"       -> object_item_empty

string: /"(\\\"|\\\\|[^"\n])*?"i?/ -> dqstring
      | /'(\\\'|\\\\|[^'\n])*?'i?/ -> sqstring

identifier: IDENTIFIER
IDENTIFIER:/\w+/

%import common.SIGNED_NUMBER -> NUMBER
%import common.WS
%ignore WS
"""


class _JsomTransformer(Transformer):
    @staticmethod
    def null(_: List): return None

    @staticmethod
    def true(_: List): return True

    @staticmethod
    def false(_: List): return False

    @staticmethod
    @v_args(inline=True)
    def number(token: Token) -> Union[float, int]:
        return literal_eval(token)

    @staticmethod
    @v_args(inline=True)
    def dqstring(token: Token) -> str:
        return literal_eval(token.replace(r'\/', '/'))

    object_item = tuple


class JsomParser:
    _transformers: Dict[
        str, Tuple[Type[JsomWarning], Callable[[JsomParser, bool],
                                               Callable[[Any, List], Any]]]
    ] = {
        'array': (TrailingCommaInArray, get_array_transformer),
        'object': (TrailingCommaInObject, get_object_transformer),
        'sqstring': (SingleQuotedString, get_sqstring_transformer),
        'identifier': (UnquotedString, get_identifier_transformer),
        'object_item_empty': (
            EmptyObjectValue, get_object_item_empty_transformer
        )
    }

    def __init__(self,
                 ignore_warnings: Iterable[Type[JsomWarning]] = (),
                 transform: bool = True):
        self.file = None

        transformer = _JsomTransformer()

        # Wtf, PyCharm, you suggest this way of declaring loop variable types
        # yourself.
        # noinspection PyUnusedLocal
        method_getter: Callable[[JsomParser, bool], Callable[[Any, List], Any]]
        for method, (warning, method_getter) in self._transformers.items():
            setattr(
                transformer,
                method,
                method_getter(
                    parser=self,
                    warnings=warning not in ignore_warnings
                )
            )

        self._parser = Lark(
            jsom_grammar,
            start='value',
            parser='lalr',
            lexer='standard',
            transformer=transformer if transform else None,
        )

    def loads(self, s: str) -> JsomValue:
        return self._parser.parse(s)

    def load(self, f: IO) -> JsomValue:
        if hasattr(f, "name"):
            self.file = f.name
        source = f.read()
        if source:
            parsed = self.loads(source)
        else:
            parsed = None
        self.file = None
        return parsed
