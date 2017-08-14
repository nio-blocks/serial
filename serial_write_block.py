import serial

from nio.block.base import Block
from nio.properties import VersionProperty, StringProperty, \
    IntProperty, Property


class SerialWrite(Block):

    """ Write to  a serial port """

    version = VersionProperty('0.1.0')
    port = StringProperty(title='Port', default='/dev/ttyS0')
    baudrate = IntProperty(title='Baud Rate', default=9600)
    write_data = Property(title='Data to Write',
                          default='{{ $data }}')

    def __init__(self):
        super().__init__()
        self._serial = None

    def configure(self, context):
        super().configure(context)
        self._serial = serial.Serial(self.port(), self.baudrate())

    def process_signals(self, signals):
        for signal in signals:
            self._write(signal)
        self.notify_signals(signals)

    def _write(self, signal):
        data = None
        try:
            data = self.write_data(signal)
        except:
            self.logger.exception('Failed to evaluate write_data')
        if data:
            try:
                self._serial.write(data)
            except serial.SerialTimeoutException:
                self.logger.error('Failed writing to serial port')
            finally:
                self._serial.flush()
