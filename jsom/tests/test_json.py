import json
import unittest

from jsom import JsomParser

# from:
# https://json.org/JSON_checker/test/pass1.json
# https://json.org/JSON_checker/test/pass2.json
# https://json.org/JSON_checker/test/pass3.json
JSON1 = r'''
[
    "JSON Test Pattern pass1",
    {"object with 1 member":["array with 1 element"]},
    {},
    [],
    -42,
    true,
    false,
    null,
    {
        "integer": 1234567890,
        "real": -9876.543210,
        "e": 0.123456789e-12,
        "E": 1.234567890E+34,
        "":  23456789012E66,
        "zero": 0,
        "one": 1,
        "space": " ",
        "quote": "\"",
        "backslash": "\\",
        "controls": "\b\f\n\r\t",
        "slash": "/ & \/",
        "alpha": "abcdefghijklmnopqrstuvwyz",
        "ALPHA": "ABCDEFGHIJKLMNOPQRSTUVWYZ",
        "digit": "0123456789",
        "special": "`1~!@#$%^&*()_+-={':[,]}|;.</>?",
        "hex": "\u0123\u4567\u89AB\uCDEF\uabcd\uef4A",
        "true": true,
        "false": false,
        "null": null,
        "array":[  ],
        "object":{  },
        "address": "50 St. James Street",
        "url": "http://www.JSON.org/",
        "comment": "// /* <!-- --",
        "# -- --> */": " ",
        " s p a c e d " :[1,2 , 3
,
4 , 5        ,          6           ,7        ],"compact": [1,2,3,4,5,6,7],
        "jsontext": "{\"object with 1 member\":[\"array with 1 element\"]}",
        "quotes": "&#34; \u0022 %22 0x22 034 &#x22;",
        "\/\\\"\uCAFE\uBABE\uAB98\uFCDE\ubcda\uef4A\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?"
: "A key can be any string"
    },
    0.5 ,98.6
,
99.44
,
1066,
1e1,
0.1e1,
1e-1,
1e00,2e+00,2e-00
,"rosebud"]
'''

JSON2 = r'''
[[[[[[[[[[[[[[[[[[["Not too deep"]]]]]]]]]]]]]]]]]]]
'''

JSON3 = r'''
{
    "JSON Test Pattern pass3": {
        "The outermost value": "must be an object or array.",
        "In this test": "It is an object."
    }
}
'''


class TestJson(unittest.TestCase):
    def setUp(self):
        self.parser = JsomParser()

    def test_parsing_valid_json(self):
        self.assertListEqual(
            json.loads(JSON1),
            self.parser.loads(JSON1)
        )
        self.assertListEqual(
            json.loads(JSON2),
            self.parser.loads(JSON2)
        )
        self.assertDictEqual(
            json.loads(JSON3),
            self.parser.loads(JSON3)
        )

    def test_multiline_strings(self):
        self.assertDictEqual(
            self.parser.loads('{"foo": "bar\nbaz"}'),
            {"foo": "bar\nbaz"}
        )

    def test_stray_backslash(self):
        self.assertDictEqual(
            self.parser.loads(r'{"foo": "bar"}\\'),
            {"foo": "bar"}
        )
