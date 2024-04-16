# CamaChat for Youtube Live
### *CamaChat è un'applicazione Python creata per chi dirige o segue live su Youtube. Uno strumento per Youtubers e per i loro followers che permette di visualizzare la chat live di un video YouTube, filtrando i messaggi per utente e altre utilità. Non richiede credenziali Youtube, perché legge solo dati pubblici. Può essere utilizzata sia per le live in tempo reale che per quelle registrate.*

> **Seguimi su Youtube:** Trovi queste e altre idee sul mio canale Youtube: https://www.youtube.com/@camatubeofficial

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/25634VCkR9g/0.jpg)](https://www.youtube.com/watch?v=25634VCkR9g)


## Funzioni principali
1. Ingrandimento del testo della chat.
2. Elenco e totale utenti chattaroli.
3. Filtraggio messaggi per uno o più utenti.
4. Ordinamento messaggi per data e ora crescente o decrescente.
5. Conteggio messaggi in chat.
6. Data e ora dei messaggi (la puoi mostrare o nascondere).
7. Video Youtube (lo puoi spostare, ridimensionare, mostrare o nascondere).
8. Chat Youtube per chattare (la puoi mostrare o nascondere).
9. Le immagini degli utenti sono cliccabili: puoi visionare il loro canale.

## Come funziona
L'applicazione utilizza il framework Flask, il quale, grazie al WebServer Ninja, consente l'avvio in locale della pagina web index.html. Lo script camachat.py si occupa di intermediare le varie richieste, prelevando i dati da YouTube tramite l'API v1 con l'ausilio del modulo Python chat-downloader e registrando i dati nel database SQLite presente nella cartella principale, come nell'esempio seguente:

```python
cursor.execute('INSERT INTO chat (idlive, idmessaggio, autore, messaggio, data, thumb) VALUES (?,?,?,?,?,?)',
(idlive, idmessaggio, autore, messaggio, data_messaggio,thumb))
```


Per qualsiasi esigenza è possibile aprire e consultare il database locale con il software: https://github.com/sqlitebrowser/sqlitebrowser

> **Attenzione:** Se modifichi i campi delle tabelle o qualsiasi altro dato, l'applicazione potrebbe bloccarsi


## Come avviare l'applicazione
- Scarica il file zip e aprilo dove preferisci. Non necessita di installazione.
- Avvia il file camachat_start.bat
- Si aprirà il prompt di Windows e si avvierà subito l'applicazione. Non sarà installato nulla nel tuo computer, in quanto Python 3.12 Embed e le librerie necessarie sono incluse nella cartella.
![Prompt CamaChat](/images/camachat_prompt.png "")

- Al termine si aprirà il browser alla pagina: localhost:5000
- Copia e incolla l'URL del video live nella schermata di avvio.
![Inserisci url video live Youtube](/images/camachat_url.png "")

Se il video è disponibile e la chat è pubblica, dopo qualche secondo appariranno i primi messaggi.

## Devi sapere che
- Se la live è terminata, CamaChat scaricherà tutti i messaggi (ma proprio tutti). Dovrai attendere il tempo necessario affinchè possa scaricare tutta la chat.
- Se la live è in tempo reale e ti sei collegato in ritardo, CamaChat potrebbe non scaricare i primi messaggi. Tuttavia, una volta terminata la live, potrai ricollegarti alla live registrata per recuperare quelli persi.
- Se perdi la connessione durante la live o sei obbligato ad aggiornare la pagina web di CamaChat o devi riavviare il tuo PC, una volta ristabilità la connessione con la live, potrai recuperare tutti i messaggi che avevi già scaricato nel database locale.

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

## Prossimi aggiornamenti
È stato divertente realizzare questa prima versione di CamaChat e ho altre idee su come potenziarla. Spero presto di poterle condividere sul mio canale YouTube. Ti invito a seguirmi per essere avvisato sulle novità. Se anche tu vuoi contribuire a migliorarla, scrivimi a info@camatube.com o modifica il codice a tuo piacimento e mostrami il risultato. :)
        
