import serial
from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import VersionProperty, StringProperty, \
    IntProperty, ExpressionProperty


@Discoverable(DiscoverableType.block)
class SerialWrite(Block):

    """ Write to  a serial port """

    version = VersionProperty('0.1.0')
    port = StringProperty(title='Port', default='/dev/ttyS0')
    baudrate = IntProperty(title='Baud Rate', default=9600)
    write_data = ExpressionProperty(title='Data to Write',
                                     default='{{ $data }}')

    def __init__(self):
        super().__init__()
        self.ser = None

    def configure(self, context):
        super().configure(context)
        self.ser = serial.Serial(self.port, self.baudrate)

    def process_signals(self, signals, input_id='default'):
        for signal in signals:
            self._write(signal)
        self.notify_signals(signals, output_id='default')

    def _write(self, signal):
        data = None
        try:
            data = self.write_data(signal)
        except:
            self._logger.exception('Failed to evaluate write_data')
        if data:
            try:
                self.ser.write(data)
            except serial.SerialTimeoutException:
                self._logger.error('Failed writing to serial port')
            finally:
                self.ser.flush()
