from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

API_KEY = 'YOUR_RIOT_GAMES_API_KEY'

VALID_REGIONS = ['na', 'euw', 'eun', 'kr', 'jp', 'ap', 'sea']

@app.route('/rank', methods=['GET'])
def get_rank():
    region = request.args.get('region')
    riot_id = request.args.get('riot_id')
    tagline = request.args.get('tagline')

    if not region or not riot_id or not tagline:
        return jsonify({'error': 'Please provide region, riot_id, and tagline'}), 400

    if region not in VALID_REGIONS:
        return jsonify({'error': f'Invalid region. Valid regions are: {", ".join(VALID_REGIONS)}'}), 400

    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_id}/{tagline}"
    headers = {
        'X-Riot-Token': API_KEY
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        try:
            error_message = response.json().get('status', {}).get('message', 'An unknown error occurred')
        except ValueError:
            error_message = 'An unknown error occurred'
        return jsonify({'error': error_message}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
