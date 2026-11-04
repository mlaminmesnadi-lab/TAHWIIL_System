import unittest
import json
import os
from functions import load_and_validate_hospitals
from functions import select_best_hospital

class TestHospitalManager(unittest.TestCase):

    def setUp(self):
        """إعداد بيانات افتراضية سليمة للاستخدام في اختبارات التوجيه"""
        self.valid_hospitals_data = [
            {
                "hospital_id": "H-01",
                "name": "مستشفى تبسة",
                "city": "Tébessa",
                "transfer_time_minutes": 15,
                "departments": {
                    "ICU": {"available_beds": 0},  # ممتلئ
                    "Emergency": {"available_beds": 5}
                },
                "updated_at": "2026-11-03T08:00:00Z"
            },
            {
                "hospital_id": "H-02",
                "name": "مستشفى عنابة الجامعي",
                "city": "Annaba",
                "transfer_time_minutes": 120,
                "departments": {
                    "ICU": {"available_beds": 3},  # متاح ولكن أبعد زمنياً
                    "Emergency": {"available_beds": 10}
                },
                "updated_at": "2026-11-03T07:30:00Z"
            },
            {
                "hospital_id": "H-03",
                "name": "مستشفى سوق أهراس",
                "city": "Souk Ahras",
                "transfer_time_minutes": 45,
                "departments": {
                    "ICU": {"available_beds": 2},  # متاح وأقرب من عنابة
                    "Emergency": {"available_beds": 4}
                },
                "updated_at": "2026-11-03T06:15:00Z"
            }
        ]

    def test_select_best_hospital_success(self):
        """اختيار المستشفى الأنسب بناءً على أقصر زمن نقل وتوفر السرير لـ ICU"""
        result_json = select_best_hospital("ICU", self.valid_hospitals_data)
        result = json.loads(result_json)
        
        # المستشفى المتوقع: مستشفى سوق أهراس (لان زمن نقله 45 دقيقة وله سرير، مقارنة بعنابة 120 دقيقة، وتبسة ممتلئ 0)
        self.assertEqual(result["status"], "Success")
        self.assertEqual(result["selected_hospital"], "مستشفى سوق أهراس")
        self.assertEqual(result["transfer_time_minutes"], 45)

    def test_select_hospital_specialty_missing(self):
        """إذا طلب تخصص غير موجود نهائياً في أي مستشفى -> يجب أن يعيد 'لا يوجد'"""
        result = select_best_hospital("Pediatrics", self.valid_hospitals_data)
        self.assertEqual(result, "لا يوجد")

    def test_select_hospital_all_full(self):
        """إذا كانت كل المستشفيات ممتلئة في التخصص المطلوب -> يجب أن يعيد 'لا يوجد'"""
        # نعدل بيانات مؤقتة بحيث تصبح أسرّة ICU صفراً في الجميع
        for h in self.valid_hospitals_data:
            if "ICU" in h["departments"]:
                h["departments"]["ICU"]["available_beds"] = 0
                
        result = select_best_hospital("ICU", self.valid_hospitals_data)
        self.assertEqual(result, "لا يوجد")

    def test_validation_missing_field(self):
        """اختبار البرمجة الدفاعية: ملف به حقل مفقود -> يطلق استثناء ValueError"""
        corrupted_data = [
            {
                "hospital_id": "H-99",
                "name": "مستشفى ناقص الحقول",
                # حقل city و transfer_time_minutes مفقودان عمداً
                "departments": {"ICU": {"available_beds": 2}},
                "updated_at": "2026-11-03T00:00:00Z"
            }
        ]
        file_path = "test_corrupted_1.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(corrupted_data, f)

        with self.assertRaises(ValueError):
            load_and_validate_hospitals(file_path)

        if os.path.exists(file_path):
            os.remove(file_path)

    def test_validation_negative_beds(self):
        """اختبار البرمجة الدفاعية: عدد أسرّة بالسالب -> يطلق استثناء ValueError"""
        corrupted_data = [
            {
                "hospital_id": "H-100",
                "name": "مستشفى سلبي",
                "city": "Tébessa",
                "transfer_time_minutes": 10,
                "departments": {
                    "ICU": {"available_beds": -3}  # سرير بالسالب (خطأ منطقي)
                },
                "updated_at": "2026-11-03T00:00:00Z"
            }
        ]
        file_path = "test_corrupted_2.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(corrupted_data, f)

        with self.assertRaises(ValueError):
            load_and_validate_hospitals(file_path)

        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    unittest.main()