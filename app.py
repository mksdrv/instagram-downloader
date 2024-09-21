import os
import instaloader
from flask import Flask, jsonify, request

app = Flask(__name__)

# Initialisiere Instaloader
L = instaloader.Instaloader()

@app.route('/download', methods=['POST'])
def download_image():
    # Erwarte eine URL in der Anfrage
    data = request.json
    if 'url' not in data:
        return jsonify({'error': 'URL not provided'}), 400
    
    post_url = data['url']
    
    try:
        # Extrahiere den Post-Shortcode aus der URL
        shortcode = post_url.split("/")[-2]
        
        # Lade den Beitrag herunter
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # Lade das Bild herunter
        L.download_post(post, target='downloads')
        
        # Extrahiere die Bild-URL
        image_url = post.url
        
        # Antwort im JSON-Format
        return jsonify({'image_url': image_url}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Stelle sicher, dass der Ordner für die Downloads existiert
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)