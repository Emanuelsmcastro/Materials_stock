import serial
import serial.tools.list_ports as serial_ports
from Utils.Console.console_manager import BeautifulPrint


def connection_serial(_port='COM3', _baud_rate=115200, _parity=serial.PARITY_EVEN,
                      _stop_bits=serial.STOPBITS_TWO, _timeout=0.05, _auto_detect_port=True):
    """
    The function will establish connection and returning it;
    :param _port: Port to connect to arduino;
    :param _baud_rate: Serial operating speed;
    :param _parity:Data Integrity Checker;
    :param _stop_bits: Stop A bit operating mode;
    :param _timeout: speed of sending and receiving data;
    :param _auto_detect_port: Will automatically detect an arduino port;
    :return: Return connection to arduino.
    """
    port_to_connect = _port
    auto_detect_port = _auto_detect_port
    BeautifulPrint().printer('Establishing connection')
    if auto_detect_port:
        ports = [port for port in serial_ports.comports()]
        for port in ports:
            if 'Arduino' in port.description:
                port_to_connect = port.name
    while True:
        try:
            ser = serial.Serial(port=port_to_connect,
                                baudrate=_baud_rate,
                                parity=_parity,
                                stopbits=_stop_bits,
                                timeout=_timeout)
        except serial.serialutil.SerialException:
            pass
        else:
            BeautifulPrint().printer(f'Connection established\nArduino {port_to_connect:<14}')
            break
    return ser


def read_serial_data(_serial):
    """
    The function will read serial information!
    """
    _data = _serial.readline().decode()
    return _data
