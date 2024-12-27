Il Tech Stack è stato in questo modo suddiviso:

Interfaccia Utente

La sua implementazione è avvenuta nella classe PortScannerGUI importando la libreria PyQt5, una libreria che consente di utilizzare il toolkit Qt5 con il linguaggio Python. La scelta di questa libreria è stata conveniente per lo sviluppo multipiattaforma, in quanto garantisce l’esecuzione del tool anche sul sistema operativo Windows senza modificare o adattare il codice scritto sul sistema operativo macOS. Inoltre, possiede un’ampia gamma di componenti grafici (come ad esempio QWidget, QPushButton, QTextEdit e QProgressBar) ed è open source rilasciato sotto licenza GPL.

Gestore e motore delle Scansioni

Nella classe Scanner sono presenti i metodi per la gestione e l’avvio di scansioni TCP/UDP. In questa classe è stata importata la libreria socket, essenziale per la comunicazione di rete e per poter inviare e ricevere pacchetti di informazioni. 
Nei metodi responsabili delle scansioni è stato impostato un timeout pari a 0,1 ms per rendere il software più performante e veloce ma meno affidabile sul risultato di una scansione UDP in quanto quest’ultimo non richiede che ci sia una connessione con il servizio in esecuzione. 
Per rendere l’output più dettagliato è stata creata una mappa (dizionario) che associa alcune porte comuni ai protocolli e servizi più noti.
 Le porte indicate sono: 20 per l’FTP Data Transfer, 21 per l’FTP generico, 22 per SSH, 23 per Telnet, 25 per SMTP, 53 per DNS, 80 per l’HTTP, 110 per il POP3, 143 per IMAP, 443 per HTTPS, 445 per SMB, 3306 per MySQL ed infine 3389 per RDP.

Modulo di Analisi, Report e Ordinamento

Nella classe Sorter è presente un metodo statico che consente di ordinare i risultati delle scansioni unicamente per porte aperte. 
Nella classe ExcelExporter è stata importata la libreria pandas per esportare i risultati della scansione in un file Excel di estensione .xlsx. Pandas si occupa di creare una tabella utile per studiare e approfondire i risultati ottenuti e presenta il modulo xlsxwriter per aggiungere formattazioni e migliorare la leggibilità del file.

Main

La classe Main è responsabile dell’avvio, dell’esecuzione e della chiusura della GUI.
In questa classe è stata importata la libreria sys per gestire degli aspetti runtime di Python e interagire con il sistema operativo. L’importazione di tale libreria è essenziale per la funzione resource_path, che determina il percorso assoluto delle risorse del tool come l’immagine dell’interfaccia e del logo dell’icona a seconda che il software sia in esecuzione come script o impacchettato in un file eseguibile.
