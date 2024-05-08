from flask import Flask, jsonify, render_template
import jsondr
import os

app = Flask(__name__)

@app.route('/<path:url_path>', methods=['GET'])
def extract(url_path):
    # Construct the full URL from the sanitized path
    full_url = 'http://' + url_path

    try:
        result = jsondr.extract_content(full_url)
    except Exception as e:
        return jsonify({"error": f"Invalid URL format: {str(e)}"}), 400

    return jsonify(result)

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
