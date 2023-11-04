from pymodbus.client import ModbusSerialClient
import serial.tools.list_ports

# I colori per le notifiche
green = "\033[30;42m"
red = "\x1b[30;41m"
no_color = "\033[0m"

# Ottieni la lista delle porte COM disponibili
com_ports = [port.device for port in serial.tools.list_ports.comports()]

if not com_ports:
    print("Nessuna porta COM trovata.")
else:
    print("Porte COM disponibili:")
    for i, port in enumerate(com_ports):
        print(f"{i + 1}. {port}")

    while True:
        try:
            selection = int(input("Seleziona il numero della porta COM desiderata per ELA252: ")) - 1
            if 0 <= selection < len(com_ports):
                selected_port_252 = com_ports[selection]
                break
            else:
                print("Selezione non valida. Inserisci un numero valido.")
        except ValueError:
            print("Inserisci un numero valido.")
    while True:
        try:
            selection = int(input("Seleziona il numero della porta COM desiderata per scheda relè: ")) - 1
            if 0 <= selection < len(com_ports):
                selected_port_rele = com_ports[selection]
                break
            else:
                print("Selezione non valida. Inserisci un numero valido.")
        except ValueError:
            print("Inserisci un numero valido.")

# Main
while True:
    serial_port485_252 = ModbusSerialClient(
        method='rtu',
        port=selected_port_252,
        stopbits=1,
        bytesize=8,
        parity='N',
        baudrate=19200,
        timeout=1,
        debug=True
    )

    serial_port485_rele = ModbusSerialClient(
        method='rtu',
        port=selected_port_rele,
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
