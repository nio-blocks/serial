import serial
from threading import Thread
import time
from nio.block.base import Block
from nio.signal.base import Signal
from nio.properties import Property, IntProperty, VersionProperty


class SerialDelimitedRead(Block):

    version = VersionProperty('0.1.0')
    delim1 = Property(title='Delimiter 1, Hex', default='0D')
    delim2 = Property(title='Delimiter 2, Hex (optional)', default='')
    port = Property(title='Port', default='/dev/ttyUSB0')
    baud = IntProperty(title='Baud Rate', default=115200)

    def __init__(self):
        super().__init__()
        self._com = None
        self._timeout = 0.05
        self._eol = b''
        self._kill = False

    def start(self):
        super().start()
        self._eol = bytes.fromhex(self.delim1()) + bytes.fromhex(self.delim2())
        self._com = serial.Serial(self.port(), self.baud())
        # Read some large amount of bytes to clear the buffer
        self.logger.debug('flush')
        self._com.timeout = 0.15
        self._com.read(100) # TODO: properly flush buffer at start
        self._com.timeout = self._timeout
        self.logger.debug('done with flush')
        # Read from com port in new thread
        self._thread = Thread(target=self._read_thread)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._kill = True
        super().stop()

    def _read_thread(self):
        sleep_time = 0.002
        # Discard first line. it may be incomplete.
        time.sleep(1)
        self._readline()
        # Read until block stops
        while not self._kill:
            signals = []
            self.logger.debug('read_thread loop')
            start = time.time()
            self.logger.debug('start time: {}'.format(start))
            line = self._readline()
            if line and line[-len(self._eol):] == self._eol:
                self.logger.debug('prepare signal')
                try:
                    signals.append(Signal({"serial_read": line}))
                    self.notify_signals(signals)
                except:
                    self.logger.exception('error preparing signal')
                    self.notify_signals(signals)
            else:
                self.logger.debug('did not read a valid line: {}'.format(line))
            try:
                self.logger.debug('try sleep')
                time.sleep(sleep_time - (time.time() - start))
                self.logger.debug('wake up!')
            except ValueError:
                self.logger.debug('sleep error')
                pass

    def _readline(self):
        self.logger.debug('readline')
        return_value = b''
        latest_byte = b''
        while return_value[-len(self._eol):] != self._eol and not self._kill:
            # latest_byte = self._com.read(1)
            try:
                latest_byte = self._com.read(1)
            except:
                self.logger.exception(
                    "Serial read failed: aborting readline"
                )
                return
            return_value += latest_byte
        self.logger.debug('line read: {}'.format(return_value))
        return return_value
