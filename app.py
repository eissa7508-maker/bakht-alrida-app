from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# قاعدة بيانات مؤسسة بخت الرضا الشاملة
medical_data = [
    {
        "keys": ["امساك", "اسفل فتحة الشرج", "شرج", "بواسير", "الم عند الاخراج"],
        "disease": "احتمال بواسير أو شق شرجي",
        "tests": "فحص سريري لدى جراح عام + فحص براز لاستبعاد مسببات الإمساك."
    },
    {
        "keys": ["انتفاخ", "كراكر", "غازات", "نفخه", "مغص قولون"],
        "disease": "القولون العصبي (IBS)",
        "tests": "فحص براز مجهري (Stool Analysis) لاستبعاد الطفيليات."
    },
    {
        "keys": ["حرقان", "حموضه", "لوعه", "فم المعده", "الم معده"],
        "disease": "التهاب المعدة أو الجرثومة",
        "tests": "فحص جرثومة المعدة (H.Pylori Antigen) واختبار النفس."
    },
    {
        "keys": ["جنبي اليمين", "تحت الاضلاع", "مراره"],
        "disease": "احتمال حصوات أو التهاب المرارة",
        "tests": "أشعة تلفزيونية (ألتراساوند) على البطن + وظائف كبد (ALT, AST)."
    },
    {
        "keys": ["طشاش", "دوار", "زغلله", "ارهاق"],
        "disease": "أنيميا (فقر دم)",
        "tests": "فحص صورة دم كاملة (CBC) وفحص مخزون حديد (Ferritin)."
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    user_input = data.get('text', '').lower()
    results = []

    for item in medical_data:
        if any(key in user_input for key in item["keys"]):
            results.append({
                "disease": item["disease"],
                "tests": item["tests"]
            })

    if not results:
        results.append({
            "disease": "لم يتم التعرف بدقة",
            "tests": "يرجى مراجعة طبيب بخت الرضا للفحص السريري العام."
        })
    
    return jsonify(results)

import os

if __name__ == '__main__':
    # Render بيحتاج المنفذ ده عشان يفتح الموقع للجمهور
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)