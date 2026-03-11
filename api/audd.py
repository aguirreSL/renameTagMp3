import os
import requests

def identify_song(file_path):
    """Send an audio file to AudD API for recognition."""
    api_key = os.getenv('AUDD_API_KEY')
    if not api_key:
        print("AUDD_API_KEY is not set in .env")
        return None
        
    url = 'https://api.audd.io/'
    data = {'api_token': api_key, 'return': 'title,artist'}
    
    try:
        with open(file_path, 'rb') as audio_file:
            files = {'file': audio_file}
            response = requests.post(url, data=data, files=files)
        result = response.json()
        if result.get('status') == 'success' and result.get('result'):
            return result['result']
        return None
    except Exception as e:
        print(f"Error identifying song: {e}")
        return None
