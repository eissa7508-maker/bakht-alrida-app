import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def load_data():
    # بنجرب نقرأ الملف من المجلد الرئيسي
    path1 = 'diseases.json'
    # وبنجرب نقرأه لو لسه تائه جوه templates
    path2 = os.path.join('templates', 'diseases.json')
    
    target_path = path1 if os.path.exists(path1) else path2
    
    try:
        if os.path.exists(target_path):
            with open(target_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except:
        return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    user_input = request.json.get('symptoms', '')
    all_diseases = load_data()
    results = []
    
    if user_input:
        for item in all_diseases:
            if any(key in user_input for key in item["keys"]):
                results.append(item)
            
    if not results:
        return jsonify([{"disease": "لم يتم العثور على نتيجة", "tests": "يرجى مراجعة طبيب بخت الرضا للفحص."}])
        
    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)