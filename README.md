SerialRead
==========

Read from a serial port

Properties
--------------

-   port (str): Serial port to read from
-   baudrate (int): Baud rate of serial port
-   timeout (int): Read timeout
-   num_bytes (int): Number of bytes to read

Dependencies
----------------

-   [pyserial](https://pypi.python.org/pypi/pyserial)

Commands
----------------
None

Input
-------
Any list of signals.

Output
---------
Same list of signals as input with new attribute *serial_read*.

-------------------------------------------------------------------------------

SerialWrite
===========

Write to a serial port

Properties
--------------

-   port (str): Serial port to read from
-   baudrate (int): Baud rate of serial port
-   write_data (exp): Data to write to serial port

Dependencies
----------------

-   [pyserial](https://pypi.python.org/pypi/pyserial)

Commands
----------------
None

Input
-------
Any list of signals.

Output
---------
Same list of signals as input.
