calculate_NEWS2 = {
    'type': 'function',
    'function': {
        'name': 'calculate_NEWS2',
        'description': "Calculating the patient's health risk score (NEWS2 score) based on key vital signs to determine the appropriate level of medical intervention.",
        'parameters': {
            'type': 'object',
            'properties': {
                'heart_rate': {
                    'type': 'integer',
                    'description': 'Heart rate (beats per minute)'
                },
                'oxygen_saturation': {
                    'type': 'integer',
                    'description': 'Blood oxygen saturation level (percentage %)'
                },
                'temperature': {
                    'type': 'number',
                    'description': 'Body temperature (in degrees Celsius)'
                },
                'systolic_bp': {
                    'type': 'integer',
                    'description': 'Systolic blood pressure (mmHg)'
                },
                'respiratory_rate': {
                    'type': 'integer',
                    'description': 'Respiratory rate (breaths per minute)'
                },
                'consciousness': {
                    'type': 'string',
                    'description': 'Level of consciousness(V: Voice, P: Pain, U: Unresponsive)'
                }
            },
            'required': [
                'heart_rate', 
                'oxygen_saturation', 
                'temperature', 
                'systolic_bp', 
                'respiratory_rate', 
                'consciousness'
            ],
        },
    },
}


load_and_validate_hospitals = {
    'type': 'function',
    'function': {
        'name': 'load_and_validate_hospitals',
        'description': 'Reading the JSON file for the hospital database and verifying the integrity and validity of its data structure before using it in routing operations.' ,
        'parameters': {
            'type': 'object',
            'properties': {
                'file_path': {
                    'type': 'string',
                    'description':'Path to the JSON file for the hospital database (e.g., hospitals.json)'
                }
            },
            'required': ['file_path'],
        },
    },
}


select_best_hospital = {
    'type': 'function',
    'function': {
        'name': 'select_best_hospital',
        'description': 'Search for and select the most suitable hospital from the database based on the required medical specialty and bed availability, while minimizing geographical transit time.',
        'parameters': {
            'type': 'object',
            'properties': {
                'required_specialty': {
                    'type': 'string',
                    'description': 'The medical specialty required for the case (e.g., ICU, Emergency, or Cardiology)'
                },
                'hospitals_data': {
                    'type': 'array',
                    'description': 'List of hospital data available for searching',
                    'items': {
                        'type': 'object'
                    }
                }
            },
            'required': ['required_specialty', 'hospitals_data'],
        },
    },
}


simulate_baseline_phone_polling = {
    'type': 'function',
    'function': {
        'name': 'simulate_baseline_phone_polling',
        'description': 'Simulating the traditional sequential telephone-based process in hospitals to calculate the total time elapsed (call durations + transfer time) required to secure an available bed.',
        'parameters': {
            'type': 'object',
            'properties': {
                'hospitals_data': {
                    'type': 'array',
                    'description': 'List of hospitals to be visited in sequence',
                    'items': {
                        'type': 'object'
                    }
                },
                'required_specialty': {
                    'type': 'string',
                    'description': 'The medical specialty to be examined (e.g., ICU or Emergency)'
                }
            },
            'required': ['hospitals_data', 'required_specialty'],
        },
    },
}

# تعريف قائمة المخططات الشاملة لجميع الأدوات لاستخدامها مباشرة في وكيل Ollama
tools_definitions = [
    calculate_NEWS2,
    load_and_validate_hospitals,
    select_best_hospital,
    simulate_baseline_phone_polling
]