# Creata da Luigi Cama[Tube] 
# 13 Aprile 2024 
# Seguimi su https://www.youtube.com/@camatubeofficial 


from flask import Flask, render_template, jsonify, request, send_from_directory, make_response
from flask_cors import CORS
from chat_downloader import ChatDownloader, sites
import json
import sqlite3
import re
import datetime
import emoji

app = Flask(__name__)
CORS(app)

pattern = re.compile(r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})')
chat = None

@app.route('/')
def index():

    response = make_response(render_template('index.html'))
    response.headers['X-Frame-Options'] = 'ALLOW-FROM localhost'
    return response

# Definisci la route per servire i file JavaScript
@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

@app.route('/verifica_chat')
def verifica_chat():

    global chat
    
    # Verifichiamo il formato corretto dell'ID video di Youtube
    idlive = request.args.get('idlive', 0)
    verifica_idlive = ''

    if idlive:
        verifica_idlive = re.match(pattern, idlive)
        
        if verifica_idlive:

            try:
                
                url = 'https://www.youtube.com/watch?v=' + str(verifica_idlive.group(1))
                chat = ChatDownloader().get_chat(url, message_groups=['all'], message_types=['text_message'])   

                if chat:
                    return jsonify({'response': str(verifica_idlive.group(1))})  # chat pronta                    

            except:
                #print("Errore: il video non è disponibile.")
                return jsonify({'response': 2})  # video non trovato
        else:
            #print('idlive errato')
            return jsonify({'response': 1}) # idlive errato
        
    else:
            #print('idlive errato')
            return jsonify({'response': 0}) # idlive errato
    
@app.route('/connessione_chat')
def connessione_chat():

    global chat
    idlive = request.args.get('idlive', 0)

    for message in chat:    
   
        if message['message_type']!='viewer_engagement_message':

            importo = ''
            header_primary_text = ''
            header_secondary_text = ''

            if message['message_type']=='paid_message':
                importo = message['money']['text']

            if message['message_type']=='membership_item': 
                header_primary_text = message['header_primary_text'] 
                header_secondary_text =  message['header_secondary_text']               

            author_name = message['author']['name'] if message['author']['name'] else "Anonymous"
            thumb = message['author']['images'][2]['url']

            if message['message_id']:

                try: 
                    sqlchat(idlive, message['message_id'], message['author']['id'], author_name, message['message'], convert_timestamp(message['timestamp']), thumb, str(message['message_type']), importo, header_primary_text, header_secondary_text)
                
                except sqlite3.Error as e:
                    #print("Errore try insert SQlite:", e)
                    pass

    return jsonify({'response': 3}) # connessione chat avviata        


def riconnetti_chat(idlive):

    global chat
    
    if idlive:
        
        try:
                
            url = 'https://www.youtube.com/watch?v=' + idlive
            chat = ChatDownloader().get_chat(url, message_groups=['all'], message_types=['text_message']) 

            for message in chat:

                if message['message_type']!='viewer_engagement_message':

                    importo = ''
                    header_primary_text = ''
                    header_secondary_text = ''

                    if message['message_type']=='paid_message':
                        importo = message['money']['text']

                    if message['message_type']=='membership_item': 
                        header_primary_text = message['header_primary_text'] 
                        header_secondary_text =  message['header_secondary_text']               

                    author_name = message['author']['name'] if message['author']['name'] else "Anonymous"
                    thumb = message['author']['images'][2]['url']

                    if message['message_id']:

                        try: 
                            sqlchat(idlive, message['message_id'], message['author']['id'], author_name, message['message'], convert_timestamp(message['timestamp']), thumb, str(message['message_type']), importo, header_primary_text, header_secondary_text)
                        
                        except sqlite3.Error as e:
                            #print("Errore try insert SQlite:", e)
                            pass

        except:
            #print("Errore: il video non è disponibile.")
            pass

      
# Preleviamo i messaggi dal db
@app.route('/aggiorna_messaggi')
def aggiorna_messaggi():

    global chat
    idlive = request.args.get('idlive', 0)

    if chat is None:
        riconnetti_chat(idlive)

    # Connessione al database SQLite
    conn = sqlite3.connect('CamaTube.db')
    cursor = conn.cursor()

    # Esempio: Query per selezionare tutti i dati dalla tabella
    query = "SELECT * FROM chat WHERE idlive=? ORDER BY data"
    cursor.execute(query, (idlive,))
    rows = cursor.fetchall()

    # Converti i dati in una lista di dizionari
    data = []
    for row in rows:

        if isinstance(row[5], str):
            emoji_txt = emoji.emojize(row[5])
        else:
            emoji_txt = ""

        data.append({
            'idmessaggio': row[2],
            'idchannel': row[3],
            'autore': row[4],
            'messaggio': emoji_txt,
            'data': row[6],
            'thumb': row[7],
            'tipo': row[8],
            'importo': row[9],
            'header_primary_text': row[10],
            'header_secondary_text': row[11]
        })

    # Formatta i dati come JSON
    json_data = json.dumps(data, indent=4)

    # Chiudi la connessione al database
    cursor.close
    conn.close()

    # Rispondiamo alla richiesta della pagine web restituendo i nuovi messaggi
    return json_data       

# Salviamo i messaggi nel db e gli utenti
def sqlchat(idlive, idmessaggio, idchannel, autore, messaggio, data_messaggio, thumb, tipo, importo, header_primary_text, header_secondary_text):

    # Connessione al database
    conn = sqlite3.connect('CamaTube.db')
    cursor = conn.cursor()

    try: 
        # Salva messaggi
        cursor.execute('INSERT INTO chat (idlive, idmessaggio, idchannel, autore, messaggio, data, thumb, tipo, importo, header_primary_text, header_secondary_text) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (idlive, idmessaggio, idchannel, autore, messaggio, data_messaggio, thumb, tipo, importo, header_primary_text, header_secondary_text))
        conn.commit()

    except sqlite3.Error as e:
        #print("Errore insert SQlite:", e)
        pass

    try: 
       
        # Salva utenti
        cursor.execute('INSERT INTO utenti (idchannel, utente, livello, stato, preferito, thumb) VALUES (?,?,?,?,?,?)', (idchannel, autore, 1, 1, 0, thumb))
        conn.commit()

    except sqlite3.Error as e:
        #print("Errore insert SQlite:", e)
        pass
    
    cursor.close
    conn.close()

def convert_timestamp(ts):

    # Converti i microsecondi in secondi dividendo per 1 milione
    timestamp_seconds = ts / 1000000

    # Converti il timestamp in una data e ora leggibile
    data_ora = datetime.datetime.fromtimestamp(timestamp_seconds, datetime.timezone.utc)

    # Formatta la data e l'ora per visualizzare solo i secondi
    return data_ora.strftime('%Y-%m-%dT%H:%M:%SZ')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

