# ELA252_Collaudo
Collaudo scheda ELA252 tramite protocollo Modbus su RS485

Packages to install:

pip install pymodbus

pip install pymodbus[serial]

Il programma ha due modalità di collaudo:
1. Carica FW e poi esegue il collaudo (Per usare questa modalità bisogna creare file "flash.bat" vicino eseguibile)
2. Esegue il collaudo senza caricare FW


In alcuni casi su Windows 10 non funzionano i colori su CMD, per attivare bisogna creare un file di registo e lanciarlo:

Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Console]
"VirtualTerminalLevel"=dword:00000001
