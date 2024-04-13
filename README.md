# CamaChat for Youtube Live
### *CamaChat è un'applicazione Python creata sia per chi dirige live (Youtubers) che per chi le segue (Followers). Permette di monitorare e visualizzare la chat live di un video YouTube, sia in corso che registrata, filtrando i messaggi per utente.*

## Funzioni principali
1. Ingrandimento del testo della chat
2. Elenco utenti chattaroli
3. Filtraggio messaggi per uno o più utenti
4. Data e ora dei messaggi
5. Ordinamento messaggi per data e ora crescente o decrescente
6. Conteggio messaggi in chat
7. Video Youtube
8. Chat Youtube per chattare

## Come funziona
L'applicazione utilizza il framework Flask che grazie al WebServer Nijia consente l'avvio in locale della pagina web index.html. Lo script camachat.py si occupa di intermediare le varie richieste, prelevando i dati da Youtube tramite API v1 con l'ausilio del modulo Python chat-downloader e registrando i dati sul DB SQlite presente nella cartella.

'''python
cursor.execute('INSERT INTO chat (idlive, idmessaggio, autore, messaggio, data, thumb) VALUES (?,?,?,?,?,?)', (idlive, idmessaggio, autore, messaggio, data_messaggio,thumb))


Per qualsiasi esigenza è possibile aprire e consultare il database con il software: https://github.com/sqlitebrowser/sqlitebrowser

> **Attenzione:** Se modifichi i campi delle tabelle o qualsiasi altro dato, l'applicazione potrebbe bloccarsi


## Come avviare l'applicazione
- Avviare il file camachat_start.bat
Si aprirà il prompt e si installerà il necessario, solo nella cartella che avete scaricato. Non sarà installato altro nel vostro computer.
Al termine si aprirà il browser predefinito alla pagina: localhost:5000

## L'applicazione è stata testata con
- Windows 10 e Windows 11
- Python 3.2
- Chrome, Firefoz, Opera

## 
        
