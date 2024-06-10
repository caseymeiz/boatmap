
ecg_lead_schema = {
    "type": "array",
    "items": {"type": "number"}
}

ecg = {
    "type": "object",
    "properties": {
        "t": {
            "type": "array",
            "items": {"type": "number"}
        },
        "ecg": {
            "type": "object",
            "properties": {
                "I": ecg_lead_schema,
                "II": ecg_lead_schema,
                "III": ecg_lead_schema,
                "aVR": ecg_lead_schema,
                "aVL": ecg_lead_schema,
                "aVF": ecg_lead_schema,
                "V1": ecg_lead_schema,
                "V2": ecg_lead_schema,
                "V3": ecg_lead_schema,
                "V4": ecg_lead_schema,
                "V5": ecg_lead_schema,
                "V6": ecg_lead_schema,
            },
            "required": ["I", "II", "III", "aVR", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
        }
    },
    "required": ["t", "ecg"]
}
