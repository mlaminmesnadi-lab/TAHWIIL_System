import json
from agent00 import run_true_tahwil_agent  
from hospitals_db import HOSPITALS_DATABASE



# 2. تعريف عينة بيانات المريض التجريبي
sample_patient_data = {
    "patient_id": "P-99887",
    "vitals": {
        "respiratory_rate": 26,
        "spo2": 88,
        "spo2_scale": 1,
        "on_oxygen": "true",
        "systolic_bp": 95,
        "heart_rate": 125,
        "consciousness": "V",
        "temperature": 39.1
    },
    "sbar_context": {
        "situation": "A patient suffering from acute shortness of breath, low oxygen saturation, and a high fever.",
        "background": "A medical history of chronic respiratory diseases.",
        "assessment": "A critical condition requiring urgent intensive care (ICU) and continuous monitoring.",
        "recommendation": "Request for immediate transfer to the intensive care unit."
    },
    "required_specialty": "ICU"
}

if __name__ == "__main__":
    print("=== Starting the Intelligent Agent Test (TAHWIL Agent Test) ===")
    print(f"Managing the patient's condition: {sample_patient_data['patient_id']}...\n")
    
    try:
        # استدعاء الوكيل مع تمرير المتغيرين المعرفين أعلاه بوضوح
        final_report = run_true_tahwil_agent(sample_patient_data, HOSPITALS_DATABASE)
        
        print("\n--- Final Agent Report ---")
        print(final_report)
        print("----------------------------")
        
    except Exception as e:
        print(f"⚠️ An error occurred while running the proxy: {e}")
        print("Ensure that the Ollama service is running locally and that the llama3.1 model is loaded and available.")