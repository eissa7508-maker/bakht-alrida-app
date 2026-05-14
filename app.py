import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# دالة ذكية لتحميل البيانات والتأكد من عدم وجود أخطاء
def load_data():
    try:
        # التأكد من وجود الملف في مجلد المشروع
        if os.path.exists('diseases.json'):
            with open('diseases.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    user_input = request.json.get('symptoms', '')
    all_diseases = load_data()
    results = []
    
    # محرك بحث مرن يطابق الكلمات المفتاحية في قاعدة البيانات
    if user_input:
        for item in all_diseases:
            if any(key in user_input for key in item["keys"]):
                results.append(item)
            
    # إذا لم يجد نتيجة، يوجه المستخدم للفحص السريري
    if not results:
        return jsonify([{"disease": "غير محدد بدقة", "tests": "يرجى مراجعة طبيب جامعة بخت الرضا للفحص السريري."}])
        
    return jsonify(results)

if __name__ == '__main__':
    # إعداد المنفذ ليتوافق مع منصة Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)