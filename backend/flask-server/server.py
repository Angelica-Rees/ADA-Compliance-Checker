from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS
from errors import validate_doc_structure,validate_img_tags,validate_links,validate_headings
app = Flask(__name__)
CORS(app) 

@app.route('/analyze-html', methods=['POST'])
def analyze_html():
    data = request.get_json()
    if not data or 'html' not in data:
        return jsonify({"error": "Invalid request. 'html' key is required."}), 400

    html_content = data['html']

    soup = BeautifulSoup(html_content, 'html.parser')
    error_list = []

    doc_errors = validate_doc_structure(soup)
    error_list = error_list + doc_errors

    img_errors = validate_img_tags(soup)
    error_list = error_list + img_errors

    links_errors = validate_links(soup)
    error_list = error_list + links_errors

    headings_errors = validate_headings(soup)
    error_list = error_list + headings_errors
    
    return jsonify(error_list) 


if __name__ == "__main__":
    app.run(debug=True)