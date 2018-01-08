SerialDelimitedRead
===================
For each line read, terminated by delimiter(s), a signal is notified with the attribute `serial_read` and the bytes read.

Properties
----------
- **baud**: Baud rate of the serial port.
- **delim1**: First delimiter.
- **delim2**: Optional second delimiter.
- **port**: Serial port to read.

Inputs
------
None

Outputs
-------
- **default**: For each input signal, a signal notified with the attribute `serial_read` and the bytes read.

Commands
--------
None

Dependencies
------------
-   [pyserial](https://pypi.python.org/pypi/pyserial)

SerialRead
==========
Read from a serial port.

Properties
----------
- **baudrate**: Baud rate of serial port.
- **num_bytes**: Number of bytes to read from the serial port.
- **port**: Serial port to read.
- **timeout**: Read timeout in seconds.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: For each input signal, a signal notifies with the attribute `serial_read` and the bytes read.

Commands
--------
None

Dependencies
------------
-   [pyserial](https://pypi.python.org/pypi/pyserial)

SerialWrite
===========
Write to a serial port.

Properties
----------
- **baudrate**: Baud rate of serial port.
- **port**: Serial port to write.
- **write_data**: Data to write.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: The same list of signals.

Commands
--------
None

Dependencies
------------
-   [pyserial](https://pypi.python.org/pypi/pyserial)

