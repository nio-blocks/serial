from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import VersionProperty, StringProperty, \
    IntProperty


@Discoverable(DiscoverableType.block)
class SerialRead(Block):

    """ Read from a serial port """

    version = VersionProperty('0.1.0')
    port = StringProperty(title='Port', default='/dev/ttyS0')
    baudrate = IntProperty(title='Baud Rate', default=9600)

    def process_signals(self, signals, input_id='default'):
        for signal in signals:
            pass
        self.notify_signals(signals, output_id='default')
