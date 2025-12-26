from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
import requests
import os
from authlib.integrations.flask_client import OAuth

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..'), static_url_path='/')
app.secret_key = 'your_secret_key_here'  # Change to a random secret key

oauth = OAuth(app)
# oauth.register(
#     name='google',
#     client_id='your_google_client_id',  # Replace with your Google Client ID
#     client_secret='your_google_client_secret',  # Replace with your Google Client Secret
#     server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
#     client_kwargs={'scope': 'openid email profile'}
# )

# Replace with your actual Groq API key
GROQ_API_KEY = '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'

# Replace with your actual Google Gemini API key if using Gemini
GOOGLE_API_KEY = 'your_google_api_key_here'

@app.route('/')
def index():
    # if 'user' not in session:
    #     return send_from_directory('..', 'login.html')  # Assuming you have a login.html
    return send_from_directory('..', 'index.html')

# @app.route('/login')
# def login():
#     redirect_uri = url_for('authorize', _external=True)
#     return oauth.google.authorize_redirect(redirect_uri)

# @app.route('/authorize')
# def authorize():
#     token = oauth.google.authorize_access_token()
#     user = oauth.google.parse_id_token(token)
#     session['user'] = user
#     return redirect('/')

# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect('/')

# @app.route('/user')
# def user():
#     if 'user' in session:
#         return jsonify(session['user'])
#     return jsonify({})

# @app.route('/profile')
# def profile():
#     if 'user' not in session:
#         return redirect('/login')
#     return send_from_directory('..', 'profile.html')

@app.route('/chat', methods=['POST'])
def chat():
    # if 'user' not in session:
    #     return jsonify({'response': 'Please log in first.'})
    # Rest of the code
    data = request.get_json()
    user_message = data.get('message', '')
    model = data.get('model', 'llama-3.3-70b-versatile')  # Default model

    if not user_message:
        return jsonify({'response': 'Please provide a message.'})

    if model == 'gemini-1.5-flash':
        # Call Google Gemini API
        if not GOOGLE_API_KEY or GOOGLE_API_KEY == 'your_google_api_key_here':
            return jsonify({'response': 'Google API key not set.'})
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GOOGLE_API_KEY}'
        payload = {
            'contents': [
                {
                    'parts': [
                        {'text': 'You are a helpful assistant. Provide concise, informative responses in a friendly tone, using bullet points for lists when appropriate. ' + user_message}
                    ]
                }
            ]
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            assistant_message = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'response': assistant_message})
        except requests.exceptions.RequestException as e:
            return jsonify({'response': f'Error: {str(e)}'})
    else:
        # Call Groq API
        url = 'https://api.groq.com/openai/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': model,
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant. Provide concise, informative responses in a friendly tone, using bullet points for lists when appropriate.'},
                {'role': 'user', 'content': user_message}
            ],
            'max_completion_tokens': 1000
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            assistant_message = result['choices'][0]['message']['content']
            return jsonify({'response': assistant_message})
        except requests.exceptions.RequestException as e:
            return jsonify({'response': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(port=5000, debug=False)