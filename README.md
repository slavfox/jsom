# JSOM - not quite JSON, but close enough

`jsom` is a simple and quick Python 3.7+ parser for terribly broken JSON.

## Installation

`$ pip install jsom`

## Usage

`jsom` works like this:

```python
>>> import jsom
>>> broken_json = "{\"foo\": {bar: 1, 'baz':,}, bar: 1, baz: [1,2,3,],}")
>>> jsom.JsomParser(ignore_warnings=jsom.ALL_WARNINGS).loads(broken_json)
{'foo': {'bar': 1, 'baz': None}, 'bar': 1, 'baz': [1, 2, 3]}
```

`jsom` happily gobbles up the following:
* unquoted keys and values
* single-quoted strings
* trailing commas
* empty values in objects

By default, it will warn you whenever it sees one of those, but still parse it.

Warnings are annoying, though, and to make matters worse, they slow the 
parser down - so just pass in the list of warnings you want `jsom` to be quiet
about in the `ignore_warnings` parameter:
```
parser = JsomParser(
    ignore_warnings=[jsom.SINGLE_QUOTED_STRING, jsom.EMPTY_OBJECT_VALUE]
)
```
Or, if you prefer, just tell it to shut up completely, by passing in 
`jsom.ALL_WARNINGS`.

## LICENSE

`jsom` is distributed under the terms of the **Do What The Fuck You Want To 
Public License (WTFPL)**:

```
        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
                    Version 2, December 2004 

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 

 Everyone is permitted to copy and distribute verbatim or modified 
 copies of this license document, and changing it is allowed as long 
 as the name is changed. 

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

  0. You just DO WHAT THE FUCK YOU WANT TO.
```