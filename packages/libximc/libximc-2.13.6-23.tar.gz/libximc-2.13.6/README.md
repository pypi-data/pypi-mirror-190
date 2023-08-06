# Cross-platform package for managing XIMC devices

>Libximc is a thread-safe, cross-platform library for working with 8SMC4-USB and 8SMC5-USB controllers.

>Libximc manages the equipment using interfaces: USB 2.0., RS232 and Ethernet, also uses a common and proven virtual serial port interface, so you can work with motor control modules through this library under Windows and Linux.

>The libximc library supports connecting and disconnecting devices on the fly. No more than one instance of the control program can work with one device at any time - multiple access of control programs to the same device is not allowed.

## Installation

- Pip update
    ```bash
    python3 -m pip install --upgrade pip
    ```
- Installation
    ```bash
    python3 -m pip install libximc
    ```
- Checking the installation
    ```python
    import libximc
    if libximc.lib is not None:
        print("Installation successful")
    ```

## Example of using the library
```python
from libximc import *
from ctypes import *

# Open a virtual controller
device_id = lib.open_device("xi-emu:///testdevice.bin")
print("Device id: " + repr(device_id))

# Checking the current position
x_pos = get_position_t()
result = lib.get_position(device_id, byref(x_pos))
print("Result: " + repr(result))
if result == Result.Ok:
    print("Position: {0} steps, {1} microsteps".format(x_pos.Position, x_pos.uPosition))

# Offset by 1000 steps
DeltaPosition = 1000
uDeltaPosition = 0
result = lib.command_movr(device_id, DeltaPosition,  uDeltaPosition)

# Checking the current position
result = lib.get_position(device_id, byref(x_pos))
print("Result: " + repr(result))
if result == Result.Ok:
    print("Position: {0} steps, {1} microsteps".format(x_pos.Position, x_pos.uPosition))

lib.close_device(byref(cast(device_id, POINTER(c_int))))
```

## Additional information
[Software download page](https://files.xisupport.com/Software.en.html)

[Programmer manual](https://libximc.xisupport.com/doc-en/)

[User manual](https://doc.xisupport.com/en/8smc5-usb/)
