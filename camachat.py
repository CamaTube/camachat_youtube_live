# Creata da Luigi Cama[Tube] 
# Seguimi su https://www.youtube.com/@camatubeofficial 

from flask import Flask, render_template, jsonify, request, send_from_directory, make_response
from flask_cors import CORS
from chat_downloader import ChatDownloader, sites
import json
import sqlite3
import re
import datetime
import emoji
import requests
import os

timestampattuale = int(datetime.datetime.now().timestamp())

app = Flask(__name__)
# app = Flask(__name__, static_folder='.', static_url_path='') # per rendere visibili tutti i file nella root, ma vede anche il codice python, non lo processa

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

# Definisci la route per servire le miniature
@app.route('/thumb/<path:filename>')
def serve_image(filename):
    return send_from_directory('thumb', filename)

# Definisci la route per servire css
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename)

# Definisci la route per servire font awesome
@app.route('/webfonts/<path:filename>')
def serve_webfonts(filename):
    return send_from_directory('webfonts', filename)

@app.route('/verifica_chat')
def verifica_chat():

    global chat
    
    # Verifichiamo il formato corretto dell'ID video di Youtube
    idlive = request.args.get('idlive', 0)

    verifica_idlive = ''
    status = ''
    title = ''
    live_chat_replay = ''
    video = None

    if idlive:

        verifica_idlive = re.match(pattern, idlive)
        
        if verifica_idlive:

            idlive = str(verifica_idlive.group(1))

            try:
                
                url = 'https://www.youtube.com/watch?v=' + idlive                

                chat = ChatDownloader().get_chat(url, message_types=[
                    'viewer_engagement_message',
                    'paid_message',
                    'ticker_paid_message_item',
                    'text_message', 
                    'paid_sticker',
                    'ticker_paid_sticker_item',
                    'sponsorships_gift_purchase_announcement',
                    'ticker_sponsor_item',
                    'membership_item',
                    'banner',
                    'banner_header',
                    'donation_announcement',
                    'purchased_product_message'
                ])  

                if chat:
                    # Verifichiamo se è una live in tempo reale o registrata (past / live)
                    video = sites.YouTubeChatDownloader().get_video_data(idlive)

                    if video:
                        status = video['status']
                        title = video['title']
                        if status=='past':
                            live_chat_replay = video['continuation_info']['Live chat replay']

                    # Salviamo i dati della live per poterla recuperare offline
                    conn = sqlite3.connect('CamaTube.db')
                    cursor = conn.cursor()

                    try: 
                        # Salva live
                        cursor.execute('INSERT INTO live (idlive, idchannel, titolo) VALUES (?,?,?)', (idlive, video['author_id'], title))
                        conn.commit()

                    except sqlite3.Error as e:
                        #print("Errore insert SQlite:", e)
                        pass

                    try: 

                        # Aggiungi canale ai preferiti
                        cursor.execute('INSERT INTO canali (idchannel, titolo) VALUES (?,?)', (video['author_id'], video['author']))
                        conn.commit()

                    except sqlite3.Error as e:
                        #print("Errore insert SQlite:", e)
                        pass
                    
                    cursor.close
                    conn.close()

                    return jsonify({'response': 3, 'idlive': idlive, 'status': status, 'title': title, 'live_chat_replay': live_chat_replay})  # chat pronta                                                      

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

    print('Connessione')

    global chat
    idlive = request.args.get('idlive', 0)
    
    for message in chat:
  
        if message['message_type']!='viewer_engagement_message':

            importo = ''
            header_primary_text = ''
            header_secondary_text = ''
            timestamp = ''

            if message['message_type']=='paid_message':
                if message.get('money', {}).get('text') is not None:
                    importo = message['money']['text']

            if message['message_type']=='membership_item': 
                if 'header_primary_text' in message:
                    header_primary_text = message['header_primary_text'] 
                if 'header_secondary_text' in message:
                    header_secondary_text =  message['header_secondary_text']    

            if 'timestamp' in message:
                timestamp = convert_timestamp(message['timestamp'])           

            author_name = message['author']['name'] if message['author']['name'] else "Anonymous"
            thumb = message['author']['images'][2]['url']
            image = message['author']['id'] + '.jpg'
            scarica_immagine(thumb, image)

            if message['message_id']:

                try: 
                    sqlchat(idlive, message['message_id'], message['author']['id'], author_name, message['message'], timestamp, image, str(message['message_type']), importo, header_primary_text, header_secondary_text)
                
                except sqlite3.Error as e:
                    #print("Errore try insert SQlite:", e)
                    pass

    return jsonify({'response': 3}) # connessione chat avviata        


def riconnetti_chat(idlive):

    print('Riconnessione')

    global chat
    
    if idlive:
        
        try:
                
            url = 'https://www.youtube.com/watch?v=' + idlive
            chat = ChatDownloader().get_chat(url, message_types=[
                'viewer_engagement_message',
                'paid_message',
                'ticker_paid_message_item',
                'text_message', 
                'paid_sticker',
                'ticker_paid_sticker_item',
                'sponsorships_gift_purchase_announcement',
                'ticker_sponsor_item',
                'membership_item',
                'banner',
                'banner_header',
                'donation_announcement',
                'purchased_product_message'
            ])   
            
            for message in chat:

                if message['message_type']!='viewer_engagement_message':

                    importo = ''
                    header_primary_text = ''
                    header_secondary_text = ''
                    timestamp = ''

                    if message['message_type']=='paid_message':
                        if message.get('money', {}).get('text') is not None:
                            importo = message['money']['text']

                    if message['message_type']=='membership_item': 
                        if 'header_primary_text' in message:
                            header_primary_text = message['header_primary_text'] 
                        if 'header_secondary_text' in message:
                            header_secondary_text =  message['header_secondary_text']    

                    if 'timestamp' in message:
                        timestamp = convert_timestamp(message['timestamp'])              

                    author_name = message['author']['name'] if message['author']['name'] else "Anonymous"
                    thumb = message['author']['images'][2]['url']
                    image = message['author']['id'] + '.jpg'
                    scarica_immagine(thumb, image)

                    if message['message_id']:

                        try: 
                            sqlchat(idlive, message['message_id'], message['author']['id'], author_name, message['message'], timestamp, image, str(message['message_type']), importo, header_primary_text, header_secondary_text)
                        
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
    id = request.args.get('id', 0)

    if chat is None and id is None:
        riconnetti_chat(idlive)
        print('none')

    # Connessione al database SQLite
    conn = sqlite3.connect('CamaTube.db')
    cursor = conn.cursor()

    if id:
        query = "SELECT * FROM chat WHERE idlive=? and id>? ORDER BY data LIMIT 100"
        cursor.execute(query, (idlive,id,))
    else:
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
            'id': row[0],
            'idmessaggio': row[2],
            'idchannel': row[3],
            'autore': row[4],
            'messaggio': emoji_txt,
            'data': row[6],
            'thumb': rf"\thumb\{row[7]}?v={timestampattuale}",
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

# Preleviamo le live
@app.route('/elenco_live')
def elenco_live():

    idchannel = request.args.get('idchannel', 0)
    conn = sqlite3.connect('CamaTube.db')
    cursor = conn.cursor()

    if idchannel:
        # preleviamo elenco live da Youtube
        yt_live = sites.YouTubeChatDownloader().get_user_videos(idchannel,video_type='live')
        data = []
        for item in yt_live:

            data.append({
                'idlive': item['video_id'],
                'titolo': item['title'],
                'idchannel': idchannel,
                'canale': ''
            })

        json_data = json.dumps(data, indent=4)
        return json_data

    else:
        # preleviamo elenco live dal DB locale
        query = "SELECT live.*, canali.titolo FROM live LEFT JOIN canali ON live.idchannel = canali.idchannel ORDER BY titolo"
        cursor.execute(query)

    rows = cursor.fetchall()

    data = []
    for row in rows:

        data.append({
            'id': row[0],
            'idlive': row[1],
            'titolo': row[2],
            'idchannel': row[3],
            'canale': row[4]
        })

    json_data = json.dumps(data, indent=4)

    cursor.close
    conn.close()

    return json_data  

# Preleviamo le live scaricate dal db
@app.route('/elenco_canali')
def elenco_canali():

    conn = sqlite3.connect('CamaTube.db')
    cursor = conn.cursor()

    #query = "SELECT * FROM canali "
    query = "SELECT canali.*, live.idlive FROM canali LEFT JOIN (SELECT * FROM live group by idchannel) live ON live.idchannel = canali.idchannel ORDER BY titolo"
    cursor.execute(query)
    rows = cursor.fetchall()

    data = []
    for row in rows:

        data.append({
            'id': row[0],
            'idchannel': row[1],
            'titolo': row[2],
            'idlive' : row[3]
        })

    json_data = json.dumps(data, indent=4)
    print(json_data)

    cursor.close
    conn.close()

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

def scarica_immagine(url, nome_file):
    # Effettua la richiesta per scaricare l'immagine
    response = requests.get(url)
    
    # Verifica se la richiesta ha avuto successo (status code 200)
    if response.status_code == 200:
        # Crea la cartella se non esiste già
        if not os.path.exists("thumb"):
            os.makedirs("thumb")

        # Costruisci il percorso completo del file nella cartella "images"
        percorso_completo = os.path.join("thumb", nome_file)

        # Apre il file in modalità binaria e scrive i dati dell'immagine
        with open(percorso_completo, 'wb') as file:
            file.write(response.content)
        #print("Immagine scaricata con successo!")
    else:
        #print("Errore durante il download dell'immagine. Status code:", response.status_code)
        pass

def convert_timestamp(ts):

    # Converti i microsecondi in secondi dividendo per 1 milione
    timestamp_seconds = ts / 1000000

    # Converti il timestamp in una data e ora leggibile
    data_ora = datetime.datetime.fromtimestamp(timestamp_seconds, datetime.timezone.utc)

    # Formatta la data e l'ora per visualizzare solo i secondi
    return data_ora.strftime('%Y-%m-%dT%H:%M:%SZ')


if __name__ == '__main__':
    app.run(debug=True, port=5000)

