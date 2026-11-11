import json
import ollama
from tools import calculate_NEWS2, select_best_hospital, tools_definitions
from hospitals_db import HOSPITALS_DATABASE 

def run_true_tahwil_agent(patient_data: dict, HOSPITALS_DATABASE: list) -> str:
    """
    True TAHWIL Agent: Configured with temperature=0 and strict system instructions 
    to force Llama 3.1 to execute native tool calls rather than outputting text descriptions.
    """

    vitals = patient_data.get("vitals", {})
    required_specialty = patient_data.get("required_specialty", "Emergency")
    
    # 1. تحديث رسالة النظام لتكون صارمة وتمنع الشرح النصي وتجبره على استخدام الأدوات
    messages = [
        {
            'role': 'system',
            'content': (
                'You are an intelligent medical coordination agent for the TAHWIL referral system. '
                'CRITICAL INSTRUCTION: You MUST use the provided tools (calculate_NEWS2 and select_best_hospital) directly. '
                'NEVER write text explaining what tools you want to call. Execute the tool calls immediately. '
                'After the tools return their results, synthesize a final professional medical referral report.'
            )
        },
        {
            'role': 'user',
            'content': f"Complete Patient Information:\n{json.dumps(patient_data, ensure_ascii=False)}\n\nAvailable Hospitals Database:\n{json.dumps(HOSPITALS_DATABASE, ensure_ascii=False)}"
        }
    ]

    # 2. إرسال الطلب مع ضبط temperature=0 لمنع النموذج من الثرثرة النصية
    response = ollama.chat(
        model='llama3.1',
        messages=messages,
        tools=tools_definitions,
        options={'temperature': 0}
    )

    # 3. حلقة استدعاء الأدوات الذاتية (Agent Tool-Calling Loop)
    while response.get('message', {}).get('tool_calls'):
        messages.append(response['message'])
        
        for tool_call in response['message']['tool_calls']:
            function_name = tool_call['function']['name']
            function_args = tool_call['function']['arguments']
            
            tool_result = None
            if function_name == 'calculate_NEWS2':
                tool_result = calculate_NEWS2(
                    heart_rate=int(vitals.get("heart_rate", 70)),
                    oxygen_saturation=int(vitals.get("spo2", 98)),
                    temperature=float(vitals.get("temperature", 37.0)),
                    systolic_bp=int(vitals.get("systolic_bp", 120)),
                    respiratory_rate=int(vitals.get("respiratory_rate", 16)),
                    consciousness=str(vitals.get("consciousness", "A"))
                )
            elif function_name == 'select_best_hospital':
                if not function_args.get('required_specialty'):
                    function_args['required_specialty'] = required_specialty
                if 'hospitals_data' not in function_args or not function_args['HOSPITALS_DATABASE']:
                    function_args['HOSPITALS_DATABASE'] = hospitals_database
                
                tool_result = select_best_hospital(**function_args)
            
            messages.append({
                'role': 'tool',
                'content': json.dumps(tool_result, ensure_ascii=False),
                'name': function_name
            })
            
        # استدعاء النموذج مرة أخرى بعد حصوله على نتائج الأدوات ليصوغ التقرير النهائي
        response = ollama.chat(
            model='llama3.1',
            messages=messages,
            tools=tools_definitions,
            options={'temperature': 0}
        )

    # 4. إرجاع التقرير النهائي الناتج عن تحليل الوكيل
    return response['message']['content']