
from collections import namedtuple

from ftms_parsers import (
    parse_ftm_status,
    parse_cp_response,
    form_ftms_control_command,
    FTMS_CP_OpCode,
)

# read: Supported Speed Range
ftms_speed_range_char_id = "00002ad4-0000-1000-8000-00805f9b34fb"
# notify: Fitness Machine Status
ftm_status_char_id = "00002ada-0000-1000-8000-00805f9b34fb"
# (write, indicate): Fitness Machine Control Point
ftms_control_point_char_id = "00002ad9-0000-1000-8000-00805f9b34fb"




speed_range = namedtuple(
    "SupportedSpeedRange",
    ["min_speed", "max_speed", "min_increment"],
)


def _parse_speed_range(message: bytearray):
    minimum_speed = int.from_bytes(message[0:2], "little")
    maximum_speed = int.from_bytes(message[2:4], "little")
    minimum_speed_increment = int.from_bytes(message[4:6], "little")
    return speed_range(minimum_speed, maximum_speed, minimum_speed_increment)


class FitnessMachineService:
    def __init__(self, client):
        self._client = client
        self._cp_response_callback = None
        self._ftm_status_callback = None

    
    async def get_speed_range (self):
        message = await self._client.read_gatt_char(ftms_speed_range_char_id)
        return _parse_speed_range(message)
    
    async def get_ftm_status (self):
        message = await self._client.read_gatt_char(ftm_status_char_id)
        return parse_ftm_status(message)


    
    # === NOTIFY Characteristics ===
    # ====== Fitness Machine Status ======
    async def enable_ftm_status_notify(self) -> None:
        await self._client.start_notify( ftm_status_char_id, self._ftm_status_notification_handler )

    async def disable_ftm_status_notify(self):
        await self._client.stop_notify(ftm_status_char_id)

    def set_ftm_status_handler(self, callback):
        self._ftm_status_callback = callback

    def _ftm_status_notification_handler(self, sender, data):
        if self._ftm_status_callback is not None:
            self._ftm_status_callback(parse_ftm_status(data))



    # === WRITE/INDICATE Characteristics ===
    # ====== Fitness Machine Control Point ======
    async def enable_cp_indicate(self) -> None:
        await self._client.start_notify(
            ftms_control_point_char_id,
            self._cp_response_handler,
        )

    async def disable_cp_indicate(self):
        await self._client.stop_notify(
            ftms_control_point_char_id
        )

    def set_control_point_response_handler(self, callback):
        self._cp_response_callback = callback

    def _cp_response_handler(
        self, sender, data
    ):  # pylint: disable=unused-argument
        if self._cp_response_callback is not None:
            self._cp_response_callback(parse_cp_response(data))

    async def request_control(self) -> None:
        message = form_ftms_control_command(FTMS_CP_OpCode.REQUEST_CONTROL)
        await self._client.write_gatt_char(
            ftms_control_point_char_id, message, False
        )

    async def reset(self) -> None:
        message = form_ftms_control_command(FTMS_CP_OpCode.RESET)
        await self._client.write_gatt_char(
            ftms_control_point_char_id, message, False
        )


    async def set_target_speed(self, speed: int) -> None:
        message = form_ftms_control_command(
            FTMS_CP_OpCode.SET_TARGET_SPEED, int(speed)
        )
        await self._client.write_gatt_char(
            ftms_control_point_char_id, message, False
        )
        
    async def stop_treadmill(self) -> None:
        message = form_ftms_control_command(FTMS_CP_OpCode.STOP_OR_PAUSE, 1)
        await self._client.write_gatt_char(
            ftms_control_point_char_id, message, False
            )
        
    async def pause_treadmill(self) -> None:
        message = form_ftms_control_command(FTMS_CP_OpCode.STOP_OR_PAUSE, 2)
        await self._client.write_gatt_char(
            ftms_control_point_char_id, message, False
            )
