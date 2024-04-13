# CamaChat for Youtube Live
### *CamaChat è un'applicazione Python creata sia per chi dirige live (Youtubers) che per chi le segue (Followers). Permette di monitorare e visualizzare la chat live di un video YouTube, sia in corso che registrata, filtrando i messaggi per utente. Non richiede credenziali Youtube, perché legge solo dati pubblici.*

> **Seguimi su Youtube:** Trovi queste e altre idee sul mio canale Youtube: https://www.youtube.com/@camatubeofficial

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/25634VCkR9g/0.jpg)](https://www.youtube.com/watch?v=25634VCkR9g)


## Funzioni principali
1. Ingrandimento del testo della chat
2. Elenco utenti chattaroli
3. Filtraggio messaggi per uno o più utenti
4. Ordinamento messaggi per data e ora crescente o decrescente
5. Conteggio messaggi in chat

**Funzioni che è possibile attivare e disattivare**
6. Data e ora dei messaggi
7. Video Youtube (lo puoi spostare, ridimensionare, mostrare o nascondere)
8. Chat Youtube per chattare (la puoi mostrare o nascondere)

## Come funziona
L'applicazione utilizza il framework Flask che grazie al WebServer Nijia consente l'avvio in locale della pagina web index.html. Lo script camachat.py si occupa di intermediare le varie richieste, prelevando i dati da Youtube tramite API v1 con l'ausilio del modulo Python chat-downloader e registrando i dati sul DB SQlite presente nella cartella principale, come nell'esempio seguente:

```python
cursor.execute('INSERT INTO chat (idlive, idmessaggio, autore, messaggio, data, thumb) VALUES (?,?,?,?,?,?)',
(idlive, idmessaggio, autore, messaggio, data_messaggio,thumb))
```


Per qualsiasi esigenza è possibile aprire e consultare il database con il software: https://github.com/sqlitebrowser/sqlitebrowser

> **Attenzione:** Se modifichi i campi delle tabelle o qualsiasi altro dato, l'applicazione potrebbe bloccarsi


## Come avviare l'applicazione
- Scaricate il file zip e unzippate la cartella dove preferite
- Avviare il file camachat_start.bat
- Si aprirà il prompt e si avvierà subito l'applicazione. Non sarà installato nulla nel vostro computer, in quanto Python 3.12 Embed e le librerie necessarie sono incluse nella cartella
![Prompt CamaChat](/images/camachat_prompt.png "")

- Al termine si aprirà il browser alla pagina: localhost:5000
- Copiate e incollare l'URL del video live
![Inserisci url video live Youtube](/images/camachat_url.png "")

Se il video è disponibile e la chat è pubblica, apparirà la chat.

## Devi sapere che
- Se la live è terminata, CamaChat scaricherà tutti i messaggi (ma proprio tutti). Dovrai attendere il tempo necessario affinchè possa scaricare tutta la chat.
- Se la live è in tempo reale, CamaChat scaricherà gli ultimi 80 messaggi. Se la chat contenevà più di 80 messaggi, una volta terminata la live, potrai ricollegarti alla live registrata per recuperare i primi messaggi.
- Se perdi la connessione durante la live e sei obbligato ad aggiornare la pagina web di CamaChat o a riavviare il tuo PC, una volta ristabilità la connessione con la live, potrai recuperare i messaggi che avevi già scaricato nel database locale.

## Esempio di live terminata ma disponibile al pubblico (la chat di Youtube è disattivata)
![Live registrata](/images/camachat_liverec.png "")

## Esempio di live in tempo reale
![Live in tempo reale](/images/camachat_live.png "")

## Elenco utenti in chat con campo di ricerca
![Live in tempo reale](/images/camachat_utenti.png "")

## Messaggi di un solo utente selezionato
![Live in tempo reale](/images/camachat_utente.png "")

## Messaggi di più utenti selezionati
![Live in tempo reale](/images/camachat_utentiselezionati.png "")

## L'applicazione è stata testata con
- Windows 10 e Windows 11 (X64)
- Python 3.12
- Chrome, Firefox, Opera
- Risoluzione schermo 1920x1080

        
