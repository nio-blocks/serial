from unittest.mock import patch
from collections import defaultdict
from nio.common.signal.base import Signal
from nio.util.support.block_test_case import NIOBlockTestCase
from ..serial_read_block import SerialRead


class TestSerialRead(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        # This will keep a list of signals notified for each output
        self.last_notified = defaultdict(list)

    def signals_notified(self, signals, output_id='default'):
        self.last_notified[output_id].extend(signals)

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
        self.assertDictEqual(self.last_notified['default'][0].to_dict(),
                             {
                                 'my': 'signal',
                                 'serial_read': 'sample response'
                             })
