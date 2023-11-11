# ELA252_Collaudo
Collaudo scheda ELA252 tramite protocollo Modbus su RS485

Packages to install:

pip install pymodbus

pip install pymodbus[serial]

Il programma ha due modalità di collaudo:
1. Carica FW e poi esegue il collaudo (Per usare questa modalità bisogna creare file "flash.bat" vicino eseguibile)
2. Esegue il collaudo senza caricare FW
