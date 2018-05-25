from .serial_base import SerialBase
from nio.properties import VersionProperty, IntProperty


class SerialRead(SerialBase):

    """ Read from a serial port """

    version = VersionProperty("0.2.0")
    num_bytes = IntProperty(title='Number of Bytes to Read', default=16)

    def process_signals(self, signals):
        for signal in signals:
            self._read(signal)
        self.notify_signals(signals)

    def _read(self, signal):
        num_bytes = self.num_bytes()
        self.logger.debug("Reading {} bytes".format(num_bytes))
        read = self.execute_with_retry(self._serial.read, num_bytes)
        signal.serial_read = read

    def before_retry(self, *args, **kwargs):
        """ Reconnect our serial connection before retrying """
        self.reconnect_serial()
