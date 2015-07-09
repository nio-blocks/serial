import serial
from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import VersionProperty, StringProperty, \
    IntProperty


@Discoverable(DiscoverableType.block)
class SerialRead(Block):

    """ Read from a serial port """

    version = VersionProperty('0.1.0')
    port = StringProperty(title='Port', default='/dev/ttyS0')
    baudrate = IntProperty(title='Baud Rate', default=9600)
    timeout = IntProperty(title='Number of Bytes to Read', default=16)
    num_bytes = IntProperty(title='Number of Bytes to Read', default=16)

    def __init__(self):
        super().__init__()
        self.ser = None

    def configure(self, context):
        super().configure(context)
        self.ser = serial.Serial(
            self.port, self.baudrate, timeout=self.timeout)

    def process_signals(self, signals, input_id='default'):
        for signal in signals:
            self._read(signal)
        self.notify_signals(signals, output_id='default')

    def _read(self, signal):
        read = self.ser.read(self.num_bytes)
        signal.serial_read = read
