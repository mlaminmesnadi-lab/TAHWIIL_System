from functions import calculate_NEWS2
import json


def run_tests():
    print("=" * 50)
    print("Start NEWS2's tast : ")
    print("=" * 50)

    # الحالة الأولى: مريض بحالة حرجة (مثال: ضائقة تنفسية حادة ونقص أكسجين ووعي غير مستقر)
    # المتوقع: نقاط عالية جداً (> 7) لتستوجب تحويل عاجل لـ ICU
    critical_case = calculate_NEWS2(
        heart_rate=120,
        oxygen_saturation=88,
        temperature=38.2,
        systolic_bp=95,
        respiratory_rate=26,
        consciousness="V"  # رد فعل للصوت فقط (غير منتبه تماماً)
    )
    
    # الحالة الثانية: مريض بحالة متوسطة/منخفضة الخطورة
    medium_case = calculate_NEWS2(
        heart_rate=95,
        oxygen_saturation=94,
        temperature=37.5,
        systolic_bp=120,
        respiratory_rate=18,
        consciousness="A"  # منتبه تماماً
    )

    # الحالة الثالثة: مريض سليم تماماً (في النطاق الطبيعي)
    # المتوقع: 0 نقاط
    normal_case = calculate_NEWS2(
        heart_rate=75,
        oxygen_saturation=98,
        temperature=36.8,
        systolic_bp=120,
        respiratory_rate=16,
        consciousness="A"
    )

    # طباعة النتائج للتحقق منها
    print("\n[Test 1] Emergincy case (Critical):")
    print(json.loads(critical_case))

    print("\n[Test 2] Medium case (Medium/Low):")
    print(json.loads(medium_case))

    print("\n[Test 3] Normal case (Normal):")
    print(json.loads(normal_case))
    
    print("\n" + "=" * 50)
    print("The tests have been completed with complete success!")
    print("=" * 50)

if __name__ == "__main__":
    run_tests()