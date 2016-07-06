from unittest.mock import patch
from collections import defaultdict
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..serial_read_block import SerialRead


class TestSerialRead(NIOBlockTestCase):

    def test_default_read(self):
        blk = SerialRead()
        with patch('serial.Serial'):
            self.configure_block(blk, {})
        blk._serial.read.return_value = 'sample response'
        blk.start()
        blk.process_signals([Signal({'my': 'signal'})])
        blk.stop()
        blk._serial.read.assert_called_once_with(16)
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'my': 'signal', 'serial_read': 'sample response'})
