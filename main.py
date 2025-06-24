# api bypass
from flask import Flask, jsonify, request
import requests
from urllib.parse import urlparse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/bypass', methods=['GET'])
def bypass_url():
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({"error": "Missing URL parameter"}), 400

        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()

        # Handle Pastebin URLs
        if 'pastebin.com' in domain:
            path_parts = parsed_url.path.strip('/').split('/')
            
            if len(path_parts) < 1:
                return jsonify({'error': 'URL không hợp lệ'}), 400

            paste_id = path_parts[-1]
            raw_url = f'https://pastebin.com/raw/{paste_id}'

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            try:
                response = requests.get(raw_url, headers=headers)
                response.raise_for_status()
                return jsonify({'result': response.text})
            except requests.exceptions.HTTPError:
                return jsonify({'error': 'Không tìm thấy paste hoặc paste không công khai'}), 404
            except requests.exceptions.RequestException as e:
                return jsonify({'error': f'Lỗi khi lấy dữ liệu: {str(e)}'}), 500

        # Handle Rekonise URLs
        elif 'rekonise.com' in domain:
            sPathname = parsed_url.path.strip('/')
            api_url = f"https://api.rekonise.com/social-unlocks/{sPathname}/unlock"

            response = requests.get(api_url)
            json_data = response.json()
            key = json_data.get("url")
            
            if response.status_code == 200:
                return jsonify({"result": key}), 200
            else:
                return jsonify({"error": "Failed to fetch unlock URL from API"}), 500

        else:
            return jsonify({"error": "URL không được hỗ trợ. Chỉ hỗ trợ pastebin.com và rekonise.com"}), 400

    except Exception as e:
        return jsonify({"error": "Lỗi xử lý URL"}), 500

@app.route('/', methods=['GET'])
def list_endpoints():
    endpoints = {
        "/api/bypasṣ?url=": "rekonise",
        "/api/bypass?url=": "pastebin bypass",
    }
    return jsonify(endpoints)
    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
