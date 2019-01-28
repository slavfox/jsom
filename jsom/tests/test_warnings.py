import unittest

from jsom import JsomParser, SINGLE_QUOTED_STRING, UNQUOTED_STRING, \
    EMPTY_OBJECT_VALUE, TRAILING_COMMA_IN_OBJECT, TRAILING_COMMA_IN_ARRAY, \
    ALL_WARNINGS


class TestWarnings(unittest.TestCase):
    def setUp(self):
        self.parser = JsomParser()

    def test_single_quoted_string_warning(self):
        with self.assertWarns(SINGLE_QUOTED_STRING):
            self.assertDictEqual(
                self.parser.loads("{\"foo\": 'bar'}"),
                {"foo": "bar"}
            )
        with self.assertWarns(SINGLE_QUOTED_STRING):
            self.assertEqual(
                self.parser.loads("'foo'"),
                "foo"
            )
        with self.assertWarns(SINGLE_QUOTED_STRING):
            self.assertListEqual(
                self.parser.loads("['foo', 'bar', 'baz']"),
                ["foo", "bar", "baz"]
            )

    def test_empty_value_warning(self):
        with self.assertWarns(EMPTY_OBJECT_VALUE):
            self.assertDictEqual(
                self.parser.loads("{\"foo\":, \"bar\": 1}"),
                {"foo": None, "bar": 1}
            )
            self.assertDictEqual(
                self.parser.loads("{\"foo\":}"),
                {"foo": None}
            )

    def test_unquoted_string_warning(self):
        with self.assertWarns(UNQUOTED_STRING):
            self.assertDictEqual(
                self.parser.loads("{foo: bar, baz: IRanOutOfPlaceholders}"),
                {"foo": "bar", "baz": "IRanOutOfPlaceholders"}
            )

    def test_trailing_comma_in_array_warning(self):
        with self.assertWarns(TRAILING_COMMA_IN_ARRAY):
            self.assertListEqual(
                self.parser.loads("[1, 2, 3,]"),
                [1, 2, 3]
            )

    def test_trailing_comma_in_object_warning(self):
        with self.assertWarns(TRAILING_COMMA_IN_OBJECT):
            self.assertDictEqual(
                self.parser.loads('{"foo": 1, "bar": "baz",}'),
                {"foo": 1, "bar": "baz"}
            )

    def test_same_result_without_warnings(self):
        parser_no_warnings = JsomParser(ignore_warnings=ALL_WARNINGS)
        broken_json = r"""
        {"foo": {bar: 1, 'baz':,},
         bar: 1,
         baz: [1,2,3,],        
        }
        """
        with self.assertWarns(tuple(ALL_WARNINGS)):
            parse_with_warnings = self.parser.loads(broken_json)
        self.assertDictEqual(
            parse_with_warnings,
            parser_no_warnings.loads(broken_json)
        )


if __name__ == '__main__':
    unittest.main()
