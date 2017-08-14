SerialDelimitedRead
===================

For each line read, terminated by delimiter(s), a signal is notified with the attribute `serial_read` and the bytes read.

Properties
----------
- **baud**: Baud rate of the serial port
- **delim1**: First delimiter
- **delim2**: Optional second delimiter
- **port**: Serial port to read from

Inputs
------

Outputs
-------

For each line read, terminated by delimiter(s), a signal is notified with the
attribute `serial_read` and the bytes read.

Commands
--------

Dependencies
------------
-   [pyserial](https://pypi.python.org/pypi/pyserial)


SerialRead
==========

Read from a serial port

Properties
----------
- **baudrate**: Baud rate of the serial port
- **num_bytes**: Number of bytes to read from the serial port
- **port**: Serial port to read from
- **timeout**: Read timeout in seconds

Inputs
------

Any list of signals.

Outputs
-------

For each input signal, a signal notifies with the attribute `serial_read` and the bytes read

Commands
--------

Dependencies
------------
-   [pyserial](https://pypi.python.org/pypi/pyserial)


SerialWrite
===========

Write to a serial port

Properties
----------
- **baudrate**: Baud rate of the serial port
- **port**: Serial port to write to
- **write_data**: Data to write

Inputs
------

Any list of signals

Outputs
-------

Same list of signals as input.

Commands
--------

Dependencies
------------
-   [pyserial](https://pypi.python.org/pypi/pyserial)
