from unittest.mock import patch
from collections import defaultdict
from nio.common.signal.base import Signal
from nio.util.support.block_test_case import NIOBlockTestCase
from ..serial_write_block import SerialWrite


class TestSerialWrite(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        # This will keep a list of signals notified for each output
        self.last_notified = defaultdict(list)

    def signals_notified(self, signals, output_id='default'):
        self.last_notified[output_id].extend(signals)

    def test_default_write(self):
        blk = SerialWrite()
        with patch('serial.Serial'):
            self.configure_block(blk, {})
        blk.start()
        blk.process_signals([Signal({'data': 'd'})])
        blk.stop()
        blk.ser.write.assert_called_once_with('d')
        blk.ser.flush.assert_called_once_with()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(self.last_notified['default'][0].to_dict(),
                             {
                                 'data': 'd'
                             })
