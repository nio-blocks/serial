from serial import SerialTimeoutException
from unittest.mock import patch

from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase

from ..serial_write_block import SerialWrite


class TestSerialWrite(NIOBlockTestCase):

    def test_default_write(self):
        blk = SerialWrite()
        with patch('serial.Serial'):
            self.configure_block(blk, {})
        blk.start()
        blk.process_signals([Signal({'data': 'd'})])
        blk.stop()
        blk._serial.write.assert_called_once_with('d')
        blk._serial.flush.assert_called_once_with()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'data': 'd'})

    def test_write_timeout(self):
        blk = SerialWrite()
        with patch('serial.Serial'):
            self.configure_block(blk, {})
        blk._serial.write.side_effect = SerialTimeoutException()
        blk.start()
        blk.process_signals([Signal({'data': 'd'})])
        blk.stop()
        blk._serial.write.assert_called_once_with('d')
        blk._serial.flush.assert_called_once_with()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'data': 'd'})

    def test_bad_write_data_expression(self):
        blk = SerialWrite()
        with patch('serial.Serial'):
            self.configure_block(blk, {'write_data': '{{bad}}'})
        blk.start()
        blk.process_signals([Signal({'data': 'd'})])
        blk.stop()
        self.assertEqual(0, blk._serial.write.call_count)
        self.assertEqual(0, blk._serial.flush.call_count)
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'data': 'd'})
