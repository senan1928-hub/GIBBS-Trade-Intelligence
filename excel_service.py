import pandas as pd
import io

def export_to_excel(data_list, sheet_name="Report"):
    """
    تحويل قائمة البيانات أو DataFrame إلى ملف Excel في الذاكرة لتنزيله فوراً عبر Streamlit
    """
    if isinstance(data_list, list):
        df = pd.DataFrame(data_list)
    else:
        df = data_list

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    output.seek(0)
    return output