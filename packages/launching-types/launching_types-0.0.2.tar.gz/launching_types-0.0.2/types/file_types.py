import base64
from typing import Any, Dict

class File(dict):
    name: str = ""
    content: bytes
    def __init__(cls, content, name):
        cls.name = name
        cls.content = content
        
    def as_bytes(cls) -> bytes:
        # return base64.b64decode(cls.content, validate=True)
        return cls.content

    def as_str(cls) -> str:
        # return cls.as_bytes().decode()
        return cls.content.decode()
    
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(format="file_path")
        
    @classmethod
    def __get_validators__(cls) -> Any:  # type: ignore
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> "File":
        if isinstance(value, File):
            return value
        elif isinstance(value, str):
            return File(content=value)
        elif isinstance(value, dict):
            return File(**value)
        else:
            raise Exception("Wrong type")


class FileContent(str):
    def as_bytes(self) -> bytes:
        return base64.b64decode(self, validate=True)

    def as_str(self) -> str:
        return self.as_bytes().decode()

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(format="byte")

    @classmethod
    def __get_validators__(cls) -> Any:  # type: ignore
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> "FileContent":
        if isinstance(value, FileContent):
            return value
        elif isinstance(value, str):
            return FileContent(value)
        elif isinstance(value, (bytes, bytearray, memoryview)):
            return FileContent(base64.b64encode(value).decode())
        else:
            raise Exception("Wrong type")
