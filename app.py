import os
import json
import io
from flask import Flask, render_template, request, jsonify
from PIL import Image
import pytesseract

app = Flask(__name__)

# إعداد مسار محرك الكاميرا للسيرفر
if os.path.exists('/usr/bin/tesseract'):
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def load_data():
    # البحث عن ملف الـ 100 مرض في المجلد الرئيسي أو templates
    paths = ['diseases.json', os.path.join('templates', 'diseases.json')]
    for path in paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                continue
    return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    try:
        user_input = request.json.get('symptoms', '')
        all_diseases = load_data()
        results = [item for item in all_diseases if any(key in user_input for key in item["keys"])]
        if not results:
            return jsonify([{"disease": "غير محدد", "tests": "يرجى مراجعة طبيب بخت الرضا."}])
        return jsonify(results)
    except Exception as e:
        return jsonify([{"disease": "خطأ", "tests": str(e)}])

@app.route('/scan', methods=['POST'])
def scan():
    if 'image' not in request.files:
        return jsonify({"error": "لم يتم استلام صورة"})
    try:
        file = request.files['image']
        img = Image.open(io.BytesIO(file.read()))
        # محاولة قراءة النص من الروشتة
        text = pytesseract.image_to_string(img, lang='eng')
        return jsonify({"extracted_text": text if text.strip() else "النص غير واضح"})
    except Exception:
        return jsonify({"extracted_text": "خدمة الكاميرا سيعاد تفعيلها قريباً"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)