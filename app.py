import os
import json
from flask import Flask, render_template, request, jsonify
from PIL import Image
import pytesseract
import io

app = Flask(__name__)

# دالة تحميل البيانات (تأكد أن الملف في المجلد الرئيسي)
def load_data():
    try:
        with open('diseases.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

@app.route('/')
def home():
    return render_template('index.html')

# 1. نظام الفحص النصي (القديم المطوّر)
@app.route('/check', methods=['POST'])
def check():
    user_input = request.json.get('symptoms', '')
    all_diseases = load_data()
    results = [item for item in all_diseases if any(key in user_input for key in item["keys"])]
    return jsonify(results if results else [{"disease": "غير محدد", "tests": "راجع طبيب بخت الرضا"}])

# 2. نظام الكاميرا الجديد (OCR)
@app.route('/scan', methods=['POST'])
def scan():
    if 'image' not in request.files:
        return jsonify({"error": "لم يتم استلام صورة"})
    
    file = request.files['image']
    img = Image.open(io.BytesIO(file.read()))
    
    # تحويل الصورة لنص (بيدعم الإنجليزية لأسماء الأدوية والفحوصات)
    extracted_text = pytesseract.image_to_string(img, lang='eng')
    
    return jsonify({"extracted_text": extracted_text})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)