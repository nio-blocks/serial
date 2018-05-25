import serial

from nio.util.discovery import not_discoverable
from nio.block.base import Block
from nio.block.mixins import Retry
from nio.command import command
from nio.properties import StringProperty, IntProperty


@not_discoverable
@command("reconnect_serial")
@command("disconnect_serial")
class SerialBase(Retry, Block):

    """ Read from a serial port """

    port = StringProperty(title='Port', default='/dev/ttyS0')
    baudrate = IntProperty(title='Baud Rate', default=9600)
    timeout = IntProperty(title='Timeout', default=1)

    def __init__(self):
        super().__init__()
        self._serial = None

    def configure(self, context):
        super().configure(context)
        self.reconnect_serial()

    def reconnect_serial(self):
        self.disconnect_serial()
        port = self.port()
        baud = self.baudrate()
        self.logger.info("Connecting to serial port {}, baud: {}".format(
            port, baud))
        self._serial = serial.Serial(port, baud, timeout=self.timeout())
        # Return for the command
        return {"status": "connected"}

    def disconnect_serial(self):
        """ Attempt to close the existing serial connection, if we can"""
        if self._serial:
            try:
                self.logger.info("Closing serial connection")
                self._serial.close()
            except Exception:
                self.logger.info("Error closing serial connection, continuing")
                pass
        # Return for the command
        return {"status": "disconnected"}

    def stop(self):
        self.disconnect_serial()
        super().stop()

    def before_retry(self, *args, **kwargs):
        """ Reconnect our serial connection before retrying """
        self.reconnect_serial()
