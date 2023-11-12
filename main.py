import serial.tools.list_ports
from pymodbus.client import ModbusSerialClient
import subprocess

# I colori per le notifiche
green = "\033[30;42m"
red = "\x1b[30;41m"
no_color = "\033[0m"

# I parametri iniziali per la connessione seriale
selected_port_relay = None
selected_port_252 = None

# Lista delle porte COM disponibili
while True:
    com_ports = [port.device for port in serial.tools.list_ports.comports()]

    if not com_ports:
        print("Nessuna porta COM trovata.")
        input("Premi 'Enter' per aggiornare la lista delle porte...")
    else:
        print("Porte COM disponibili:")
        for i, port in enumerate(com_ports):
            print(f"{i + 1}. {port}")
        break
# Seleziona la porta COM per ELA252
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
# Seleziona la porta COM per la scheda relè
while True:
    try:
        selection = int(input("Seleziona il numero della porta COM desiderata per scheda relè: ")) - 1
        if 0 <= selection < len(com_ports):
            selected_port_relay = com_ports[selection]
            break
        else:
            print("Selezione non valida. Inserisci un numero valido.")
    except ValueError:
        print("Inserisci un numero valido.")

# Main
while True:
    # Imposta i parametri per la connessione seriale
    serial_port485_252 = ModbusSerialClient(
        method='rtu',
        port=selected_port_252,
        stopbits=1,
        bytesize=8,
        parity='N',
        baudrate=19200,
        timeout=1,
    )

    serial_port485_relay = ModbusSerialClient(
        method='rtu',
        port=selected_port_relay,
        stopbits=1,
        bytesize=8,
        parity='N',
        baudrate=9600,
        timeout=1,
    )

    try:
        # Apri la connessione seriale
        serial_port485_252.connect()
        serial_port485_relay.connect()

        # Apri file .bat per caricare FW, se non esiste - prosegui.
        try:
            FlashMagic = subprocess.run(['flash.bat'])
        except FileNotFoundError:
            pass

        # Relè OFF
        serial_port485_relay.write_coil(1, False, slave=100)

        # Verifica se uscita della scheda ELA252 è in corto
        response_of_input_corto_uscita252 = serial_port485_relay.read_discrete_inputs(0, 8, slave=100)
        # DEBUG, per vedere entrata scheda relè
        # print(f"Entrata scheda relè {response_of_input_corto_uscita252.bits}")

        # Relè ON
        serial_port485_relay.write_coil(1, True, slave=100)

        # Scrivi il valore 1 nel registro 115
        serial_port485_252.write_register(115, 1, slave=1)

        # verifica lo stato del registro 115 nella variabile
        response_reg115 = serial_port485_252.read_holding_registers(115, 1, slave=1)
        # DEBUG, per vedere se è stato scritto correttamente
        # print(f"Registro 115 {response_reg115.registers[0]}")

        # Scrivi il valore 1 nel registro 400
        serial_port485_252.write_register(400, 1, slave=1)

        # Aggiungi lo stato del registro 400 nella variabile
        response_reg400 = serial_port485_252.read_holding_registers(400, 1, slave=1)
        # DEBUG, per vedere se è stato scritto correttamente
        # print(f"Registro 400 {response_reg400.registers[0]}")

        # Aggiungi lo stato di ingresso 1 sulla scheda relè nella variablie
        response_of_input = serial_port485_relay.read_discrete_inputs(0, 8, slave=100)

        # Verifica se ci sono stati errori nella scrittura dei registri
        ErroreCortoUscita252 = response_of_input_corto_uscita252.bits[0] != False
        ErroreRegistro115 = response_reg115.registers[0] != 1
        ErroreRegistro400 = response_reg400.registers[0] != 1
        ErroreUscita = response_of_input.bits[0] != True

        if ErroreRegistro115 or ErroreRegistro400 or ErroreUscita or ErroreCortoUscita252:
            if ErroreRegistro115:
                print(f"{red}Impossibile scrivere nel registro 115.{no_color}")
            if ErroreRegistro400:
                print(f"{red}Impossibile scrivere nel registro 400.{no_color}")
            if ErroreUscita:
                print(f"{red}Errore, uscita non funziona.{no_color}")
            if ErroreCortoUscita252:
                print(f"{red}Corto uscita della scheda ELA252.{no_color}")
        else:
            print(f"{green}Collaudo OK.{no_color}")

    except Exception as e:
        print(f"Errore: {str(e)}")

    finally:
        serial_port485_252.close()
        serial_port485_relay.close()

    # Ripetere ciclo premendo Enter
    input(f"{no_color}Premi 'Enter' per ripetere")
