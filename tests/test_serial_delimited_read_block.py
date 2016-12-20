from threading import Event
from unittest.mock import patch
from nio.block.terminals import DEFAULT_TERMINAL
from nio.testing.block_test_case import NIOBlockTestCase
from ..serial_delimited_read_block import SerialDelimitedRead


class ReadEvent(SerialDelimitedRead):

    def __init__(self, event):
        super().__init__()
        self._event = event

    def notify_signals(self, signals):
        super().notify_signals(signals)
        self._event.set()


class TestSerialDelimitedReadBlock(NIOBlockTestCase):

    def test_one_delimiter_readline(self):
        e = Event()
        blk = ReadEvent(e)
        self.configure_block(blk, {
            'delim1': '0d',
            'delim2': ''
        })
        with patch('serial.Serial'):
            blk.start()
        blk._com.read.side_effect = [
            b'l', b'l', b'o', b'\r', \
            b'h', b'e', b'l', b'l', b'o', b'\r'
        ]
        # wait for notify_signals
        e.wait(1.5)
        blk.stop()
        self.assert_num_signals_notified(1, blk)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(), {
                'serial_read': b'hello\r'
            }
        )

    def test_two_delimiters_readline(self):
        e = Event()
        blk = ReadEvent(e)
        self.configure_block(blk, {
            'delim1': '0d',
            'delim2': '0a'
        })
        with patch('serial.Serial'):
            blk.start()
        blk._com.read.side_effect = [
            b'l', b'l', b'o', b'\r', b'\n', \
            b'h', b'e', b'l', b'l', b'o', b'\r', b'\n'
        ]
        # wait for notify_signals
        e.wait(1.5)
        blk.stop()
        self.assert_num_signals_notified(1, blk)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(), {
                'serial_read': b'hello\r\n'
            }
        )

    def test_one_delimiter_readline_fail(self):
        e = Event()
        blk = ReadEvent(e)
        self.configure_block(blk, {
            'delim1': '0d',
            'delim2': ''
        })
        with patch('serial.Serial'):
            blk.start()
        blk._com.read.side_effect = [
            b'l', b'l', b'o', b'\r', \
            b'h', b'e', b'l', b'l', b'o'
        ]
        # wait for notify_signals
        e.wait(1.5)
        blk.stop()
        self.assert_num_signals_notified(0, blk)

    def test_two_delimiter_readline_fail(self):
        e = Event()
        blk = ReadEvent(e)
        self.configure_block(blk, {
            'delim1': '0d',
            'delim2': '0a'
        })
        with patch('serial.Serial'):
            blk.start()
        blk._com.read.side_effect = [
            b'l', b'l', b'o', b'\r', b'\n', \
            b'h', b'e', b'l', b'l', b'o', b'\r'
        ]
        # wait for notify_signals
        e.wait(1.5)
        blk.stop()
        self.assert_num_signals_notified(0, blk)
        