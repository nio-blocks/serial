from .serial_base import SerialBase
from nio.properties import VersionProperty, Property


class SerialWrite(SerialBase):

    """ Write to  a serial port """

    version = VersionProperty("0.2.0")
    write_data = Property(title='Data to Write', default='{{ $data }}')

    def process_signals(self, signals):
        for signal in signals:
            self._write(signal)
        self.notify_signals(signals)

    def _write(self, signal):
        data = self.write_data(signal)
        try:
            self.execute_with_retry(self._serial.write, data)
        finally:
            # Attempt to flush the serial connection after a write
            try:
                self._serial.flush()
            except Exception:
                pass
