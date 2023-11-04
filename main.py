from pymodbus.client import ModbusSerialClient

# colori per lo stato
green = "\033[30;42m"
red = "\033[0;31m"
no_color = "\033[0m"

while True:
    serial_port485_252 = ModbusSerialClient(
        method='rtu',
        port='COM5',
        stopbits=1,
        bytesize=8,
        parity='N',
        baudrate=19200,
        timeout=1,
        debug=True
    )

    serial_port485_rele = ModbusSerialClient(
        method='rtu',
        port='COM7',
        stopbits=1,
        bytesize=8,
        parity='N',
        baudrate=9600,
        timeout=1,
        debug=True
    )

    try:
        # Apri la connessione seriale
        serial_port485_252.connect()
        serial_port485_rele.connect()

        # Scrivi il valore 1 nel registro 115
        serial_port485_252.write_register(115, 1, slave=1)

        # Scrivi il valore 1 nel registro 400
        serial_port485_252.write_register(400, 1, slave=1)

        # Relè ON
        serial_port485_rele.write_coil(1, True, slave=100)

        # Leggi stato IN1 sulla scheda relè
        state_of_input = serial_port485_rele.read_discrete_inputs(0, 8, slave=100)

        if state_of_input.bits[0] == True:
            print(f"{green}Collaudo OK")
        else:
            print(f"{red}Errore, uscita non funziona.")

    except Exception as e:
        print(f"Errore: {str(e)}")

    finally:
        serial_port485_252.close()
        serial_port485_rele.close()

        # Ripetere ciclo premendo Enter
    input(f"{no_color}Premi Enter per ripetere il ciclo...")
