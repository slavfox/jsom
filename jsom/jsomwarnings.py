from abc import ABC, abstractmethod


class JsomWarning(RuntimeWarning, ABC):
    def __init__(self, line, column, near=None, file=None):
        self.line = line
        self.column = column
        self.near = near
        self.file = file

    def __str__(self):
        message = f"{self.message} at line {self.line}, column {self.column}"
        if self.near:
            import inspect
            i = inspect.stack()
            message += f" (near \"...{self.near}...\")"
        if self.file:
            message += f" in file {self.file}"
        return message

    @property
    @abstractmethod
    def message(self):
        ...


class TrailingCommaInArray(JsomWarning):
    message = "Trailing comma in array"


class TrailingCommaInObject(JsomWarning):
    message = "Trailing comma in object"


class SingleQuotedString(JsomWarning):
    message = "Single-quoted string"


class UnquotedString(JsomWarning):
    message = "Unquoted string"


class EmptyObjectValue(JsomWarning):
    message = "Empty value"
