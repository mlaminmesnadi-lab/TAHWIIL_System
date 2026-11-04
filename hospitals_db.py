import json

# قاعدة بيانات المستشفيات والأقسام المتاحة وسعة الأسرّة
HOSPITALS_DATABASE = [
    {
        "hospital_id": "H-01",
        "name": "EPH Tébessa (مستشفى العالية صالح - تبسة)",
        "city": "Tébessa",
        "departments": {
            "Emergency": {"available_beds": 8, "status": "Active"},
            "ICU": {"available_beds": 1, "status": "Limited"},  # أسرّة عناية مركزة محدودة جداً
            "Cardiology": {"available_beds": 4, "status": "Active"}
        }
    },
    {
        "hospital_id": "H-02",
        "name": "CHU Annaba (المركز الاستشفائي الجامعي - عنابة)",
        "city": "Annaba",
        "departments": {
            "Emergency": {"available_beds": 20, "status": "Active"},
            "ICU": {"available_beds": 5, "status": "Active"},    # قدرة أكبر على استقبال الحالات الحرجة
            "Cardiology": {"available_beds": 12, "status": "Active"}
        }
    }
]