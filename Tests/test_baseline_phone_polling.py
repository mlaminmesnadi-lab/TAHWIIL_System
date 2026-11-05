import unittest
import json
import os
from functions import simulate_baseline_phone_polling
from hospitals_db import HOSPITALS_DATABASE
class testbaselinephonepolling(unittest.TestCase):
 def test_baseline_phone_polling(self):
        """Task 5 Test: Calculating the baseline time for sequential telephone communication"""
        from functions import simulate_baseline_phone_polling
        
        # في البيانات الافتراضية، المستشفى الأول (تبسة) تخصص ICU أسرّته 0 (فشل الاتصال به أولاً)
        # المستشفى الثاني (عنابة) تخصص ICU أسرّته 3 (تم النجاح عنده في المحاولة الثانية)
        result = simulate_baseline_phone_polling(HOSPITALS_DATABASE, "ICU")
        
        # المحاولات: مستشفيان (2 * 2 = 4 دقائق مكالمات) + زمن نقل عنابة (120 دقيقة) = 124 دقيقة
        self.assertEqual(result["status"], "Success")
        self.assertEqual(result["hospitals_checked"], 2)
        self.assertEqual(result["phone_calls_time_minutes"], 4)
        self.assertEqual(result["total_baseline_time_minutes"], 124)

        

if __name__ == "__main__":
    unittest.main()