import json
import os

def calculate_NEWS2(
    heart_rate: int, 
    oxygen_saturation: int, 
    temperature: float, 
    systolic_bp: int, 
    respiratory_rate: int,  # معدل التنفس أساسي ولا غنى عنه
    consciousness: str      # مستوى الوعي (A : awar, V : Voice, P :Pain, U: Unresponsive)
) -> str: 
    
    score = 0 
    
    # 1. تقييم معدل التنفس (Respiratory Rate) 
    if respiratory_rate <= 8 or respiratory_rate >= 25:
        score += 3
    elif 9 <= respiratory_rate <= 11:
        score += 1
    elif 12 <= respiratory_rate <= 20:
        score += 0  # نطاق طبيعي آمن
    elif 21 <= respiratory_rate <= 24:
        score += 2

    # 2. تقييم تشبع الأكسجين (Oxygen Saturation - Scale 1)
    if oxygen_saturation <= 91:
        score += 3
    elif 92 <= oxygen_saturation <= 93:
        score += 2
    elif 94 <= oxygen_saturation <= 95:
        score += 1
    else:
        score += 0  # 96% فأكثر طبيعي

    # 3. تقييم مستوى الوعي (Consciousness - AVPU Scale)
    if consciousness.upper() != "A":
        score += 3  # (V: Voice, P: Pain, U: Unresponsive)
    else:
        score += 0  # تنبه كامل

    # 4. تقييم درجة الحرارة (Temperature)
    if temperature <= 35.0:
        score += 3
    elif 35.1 <= temperature <= 36.0:
        score += 1
    elif 36.1 <= temperature <= 38.0:
        score += 0  # نطاق طبيعي
    elif 38.1 <= temperature <= 39.0:
        score += 1
    elif temperature >= 39.1:
        score += 2

    # 5. تقييم ضغط الدم الانقباضي (Systolic Blood Pressure)
    if systolic_bp <= 90:
        score += 3
    elif 91 <= systolic_bp <= 100:
        score += 2
    elif 101 <= systolic_bp <= 110:
        score += 1
    elif 111 <= systolic_bp <= 219:
        score += 0  # نطاق طبيعي
    elif systolic_bp >= 220:
        score += 3

    # 6. تقييم معدل ضربات القلب (Heart Rate)
    if heart_rate <= 40 or heart_rate >= 131:
        score += 3
    elif 41 <= heart_rate <= 50 or 111 <= heart_rate <= 130:
        score += 1
    elif 51 <= heart_rate <= 90:
        score += 0  # نطاق طبيعي
    elif 91 <= heart_rate <= 110:
        score += 1

    # 7. تحديد مستوى الخطورة بناءً على المجموع النهائي للنقاط
    if score >= 7:
        urgency_level = "Critical Risk (Emergency Escalation Required)"
    elif score >= 5:
        urgency_level = "High Risk (Urgent Clinical Review Required)"
    elif score >= 1:
        urgency_level = "Low/Medium Risk (Increased Monitoring)"
    else:
        urgency_level = "Normal (Routine Monitoring)"

    # إرجاع النتيجة بصيغة JSON
    return json.dumps({
        "NEWS2_Score": score, 
        "emergency_status": urgency_level 
    })


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////:


    # استيراد مكتبة os للتحقق من وجود الملفات في النظام

def load_and_validate_hospitals(file_path: str) -> list:
    """
    دالة لتحميل بيانات المستشفيات من ملف JSON وتطبيق برمجية دفاعية صارمة
    للتحقق من سلامة وصحة البيانات قبل اعتمادها في النظام.
    """
    
    # 1. التحقق من وجود الملف فعلياً في مسار المشروع
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The hospitals file does not exist at the specified path: {file_path}")
# ******
    # 2. فتح الملف وقراءته مع حماية ضد الملفات المعطوبة
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)  # محاولة ترجمة محتوى الملف إلى هيكل بيانات Python
        except json.JSONDecodeError:
            raise ValueError("Structural error: The JSON file is corrupted or has an invalid syntax (Syntax Error).")
#********
    # 3. التحقق من أن هيكل البيانات الرئيسي عبارة عن مصفوفة (قائمة مستشفيات)
    if not isinstance(data, list):
        raise ValueError("Structural error: The file content must be a list (array) containing the hospitals.")

    # 4. المرور على كل مستشفى لفحص وتدقيق حقوله الداخلية
    for hospital in data:
        # قائمة الحقول الإلزامية التي يجب أن توجد في كل مستشفى
        mandatory_fields = ["hospital_id", "name", "city", "transfer_time_minutes", "departments", "updated_at"]
        
        for field in mandatory_fields:
            if field not in hospital:
                raise ValueError(f"Data error: A required field '{field}' is missing in the data for one of the hospitals.")

        # 5. التحقق من المنطق الجغرافي: زمن النقل لا يمكن أن يكون رقماً سالباً
        if hospital["transfer_time_minutes"] < 0:
            raise ValueError(f"Data error: Transit time cannot be negative at the hospital: {hospital.get('name', 'Unknown')}.")

        # 6. المرور على أقسام المستشفى والتحقق من أسرّتها
        departments = hospital.get("departments", {})
        for dept_name, dept_info in departments.items():
            
            # التأكد من وجود حقل الأسرّة المتاحة داخل القسم
            if "available_beds" not in dept_info:
                raise ValueError(f"Data error: The number of available beds is undefined in the '{dept_name}' department of hospital {hospital['name']}.")
            
            # التحقق من المنطق الطبي: عدد الأسرّة لا يمكن أن يكون سالباً أبداً
            if dept_info["available_beds"] < 0:
                raise ValueError(f"Data error: The number of beds cannot be negative in department '{dept_name}' at hospital {hospital['name']}.")

    # إذا اجتازت البيانات كافة شروط الفحص بنجاح، يتم إرجاعها للاستخدام
    return data


def select_best_hospital(required_specialty: str, hospitals_data: list) -> str:
    """
    دالة اختيار المستشفى الأنسب بناءً على:
    1. توفر التخصص المطلوب.
    2. وجود أسرّة شاغرة (> 0).
    3. تطبيق قاعدة الترتيب: أقصر زمن نقل أولاً، ثم الأكثر أسرّة في حال التساوي.
    4. إن لم يوجد مستشفى مناسب، تُعيد عبارة "لا يوجد" بوضوح دون اختلاق أي اختيار.
    """
    
    suitable_hospitals = []  # قائمة مؤقتة لتخزين المستشفيات التي تطابق الشروط

    # 1. المرور على قائمة المستشفيات المتاحة
    for hospital in hospitals_data:
        departments = hospital.get("departments", {})
        
        # الشرط الأول: هل التخصص المطلوب موجود ضمن أقسام هذا المستشفى؟
        if required_specialty in departments:
            available_beds = departments[required_specialty].get("available_beds", 0)
            
            # الشرط الثاني: هل يوجد سرير واحد على الأقل شاغر في هذا التخصص؟
            if available_beds > 0:
                # إذا توفرت الشروط، نضيف المستشفى إلى قائمة الترشيح مع كامل تفاصيله
                suitable_hospitals.append({
                    "hospital_name": hospital["name"],
                    "city": hospital["city"],
                    "ward": required_specialty,
                    "available_beds": available_beds,
                    "transfer_time_minutes": hospital["transfer_time_minutes"],
                    "updated_at": hospital["updated_at"]
                })

    # الشرط الرابع: إذا كانت قائمة الترشيح فارغة تماماً (لا توجد أسرّة أو تخصصات متاحة)
    if not suitable_hospitals:
        return "لا يوجد"

    # الشرط الثالث: اختيار الأفضل باستخدام مفتاح مزدوج في الترتيب (أقصر زمن نقل، ثم الأكبر أسرّة)
    best_match = min(
        suitable_hospitals, 
        key=lambda x: (x["transfer_time_minutes"], -x["available_beds"])
    )

    # تغليف النتيجة النهائية الناجحة في هيكل JSON منظم لكي يستهلكه الوكيل الذكي (AI Agent)
    return json.dumps({
        "status": "Success",
        "selected_hospital": best_match["hospital_name"],
        "city": best_match["city"],
        "ward": best_match["ward"],
        "available_beds": best_match["available_beds"],
        "transfer_time_minutes": best_match["transfer_time_minutes"],
        "updated_at": best_match["updated_at"]
    }, ensure_ascii=False)  # لضمان بقاء الحروف والأصوات العربية واضحة دون أي تشفير

