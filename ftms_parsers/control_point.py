from enum import Enum
from collections import namedtuple
import time


class FTMS_CP_Response_Code(Enum):
    SUCCESS = 0x01
    NOT_SUPPORTED = 0x02
    INCORRECT_PARAMETER = 0x03
    OPERATION_FAILED = 0x04
    CONTROL_NOT_PERMITTED = 0x05


class FTMS_CP_OpCode(Enum):
    REQUEST_CONTROL = 0x00
    RESET = 0x01
    SET_TARGET_SPEED = 0x02
    START_OR_RESUME = 0x07
    STOP_OR_PAUSE = 0x08
    RESPONSE_CODE = 0x80


def form_ftms_control_command(opcode: FTMS_CP_OpCode, parameter: int = 0):
    if opcode == FTMS_CP_OpCode.REQUEST_CONTROL:
        return b"\x00"
    elif opcode == FTMS_CP_OpCode.RESET:
        return b"\x01"
    elif opcode == FTMS_CP_OpCode.SET_TARGET_SPEED:
        # parameter: uint16, 0.01km/h
        return b"\x02" + parameter.to_bytes(2, "little", signed=False)
    elif opcode == FTMS_CP_OpCode.START_OR_RESUME:
        # parameter: 01=stop, 02=pause
        return b"\x07"
    elif opcode == FTMS_CP_OpCode.STOP_OR_PAUSE:
        return b"\x08" + parameter.to_bytes(2, "little", signed=False)
    elif opcode == FTMS_CP_OpCode.RESPONSE_CODE:
        return b"\x80"
    else:
        raise ValueError("Invalid opcode")


ControlPointResponse = namedtuple("ControlPointResponse", ["request_code_enum", "result_code_enum"])


def parse_cp_response(message: bytearray) -> ControlPointResponse:
    request_code_enum = FTMS_CP_OpCode(message[1])
    result_code_enum = FTMS_CP_Response_Code(message[2])
    return ControlPointResponse(request_code_enum, result_code_enum)
