import base64
from typing import Any, Dict

class MachineType(str):
    def as_bytes(cls) -> bytes:
        return base64.b64decode(cls.content, validate=True)

    def as_str(cls) -> str:
        return cls.as_bytes().decode()
    
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(format="machine_type")
        
    @classmethod
    def __get_validators__(cls) -> Any:  # type: ignore
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> "MachineType":
        if isinstance(value, MachineType):
            return value
        elif isinstance(value, str):
            return MachineType(value)
        elif isinstance(value, (bytes, bytearray, memoryview)):
            return MachineType(base64.b64encode(value).decode())
        else:
            raise Exception("Wrong type")
