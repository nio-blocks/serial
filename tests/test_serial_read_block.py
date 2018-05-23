from unittest.mock import patch

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

    def test_reconnect_on_error(self):
        """ Make sure a serial reconnection happens on an error reading """
        blk = SerialRead()
        with patch('serial.Serial') as mock_serial:
            self.configure_block(blk, {})

            # Our serial read will raise an exception first, then give bytes
            blk._serial.read.side_effect = [Exception, b"123"]
            blk.start()
            blk.process_signals([Signal({'my': 'signal'})])
            blk.stop()
            # We should see two connections to the serial port
            self.assertEqual(mock_serial.call_count, 2)
            # and 1 close attempt for the retry, one when stopping
            self.assertEqual(blk._serial.close.call_count, 2)
            # Ultimately we get our data out too, hooray!
            self.assert_num_signals_notified(1)
            self.assertDictEqual(
                self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
                {'my': 'signal', 'serial_read': b'123'})
