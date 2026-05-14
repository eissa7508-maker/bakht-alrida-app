import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# دالة تحميل بيانات الـ 100 مرض
def load_data():
    # بفتش على الملف في المجلد الرئيسي لمشروع بخت الرضا
    path = 'diseases.json'
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    try:
        # استلام الأعراض من المستخدم
        data = request.get_json()
        user_input = data.get('symptoms', '').lower()
        
        all_diseases = load_data()
        
        # فحص الأعراض ومقارنتها بالكلمات المفتاحية في الملف
        results = [
            item for item in all_diseases 
            if any(key.lower() in user_input for key in item.get("keys", []))
        ]
        
        if not results:
            return jsonify([{"disease": "غير محدد", "tests": "يرجى مراجعة طبيب جامعة بخت الرضا للفحص السريري."}])
            
        return jsonify(results)
    except Exception as e:
        return jsonify([{"disease": "خطأ في النظام", "tests": str(e)}])

if __name__ == '__main__':
    # إعداد المنفذ تلقائياً ليتناسب مع سيرفر Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)