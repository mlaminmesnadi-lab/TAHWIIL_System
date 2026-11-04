{
  "patient_id": "",                         
  "vitals": {
    "respiratory_rate": "null",                # معدل التنفس (int)
    "spo2": "null",                            # نسبة الأكسجين (int)
    "spo2_scale": 1,                           # مقياس الأكسجين (القيمة الافتراضية 1)
    "on_oxygen": "false",                      # هل يتلقى أكسجين؟ (True أو False)
    "systolic_bp": "null",                     # ضغط الدم الانقباضي (int)
    "heart_rate": "null",                      # معدل ضربات القلب (integer)
    "consciousness": "",                       # مستوى الوعي حسب AVPU (مثلاً: "A", "V", "P", "U")
    "temperature": "null"                      # درجة الحرارة (Double for example : 38.5)
  },
  "sbar_context": {
    "situation": "",                         # وصف الموقف الطبي الحالي للمريض
    "background": "",                        # الخلفية الطبية والتاريخ المرضي
    "assessment": "",                        # التقييم السريري الأولي
    "recommendation": ""                     # التوصية أو طلب التحويل المطلوب
  },
  "required_specialty": ""                   # التخصص أو القسم المطلوب (مثلاً: "ICU", "Emergency", "Cardiology")
}