SerialRead
==========

Read from a serial port

Properties
--------------

-   Port (str): Serial port to read from
-   Baud Rate (int): Baud rate of serial port
-   Timeout (int): Read timeout in seconds
-   Number of Bytes to Read (int): Number of bytes to read

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
Same list of signals as input with new attribute `serial_read`.

-------------------------------------------------------------------------------

SerialWrite
===========

Write to a serial port

Properties
--------------

-   Port (str): Serial port to read from
-   Baud Rate (int): Baud rate of serial port
-   Data to Write (exp): Data to write to serial port

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

-------------------------------------------------------------------------------

SerialDelimitedRead
===========

Read from serial port until delimiter(s) found

Properties
--------------

-   Port (str): Serial port to read from
-   Baud Rate (int): Baud rate of serial port
-   Delimiter 1 (str): Hex code of first delimiter, default `0D`
-   Delimiter 2 (str): Hex code of second delimiter, unused if blank

Dependencies
----------------

-   [pyserial](https://pypi.python.org/pypi/pyserial)

Commands
----------------
None

Input
-------
None

Output
---------
For each line read, terminated by delimiter(s), a signal is notified with the 
attribute `serial_read` and the bytes read.
