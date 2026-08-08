import sqlite3
import sys
from pathlib import Path

# إضافة المجلد الرئيسي للمسار لتسهيل استيراد config
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import DB_PATH

def get_connection():
    """
    إنشاء اتصال مع قاعدة البيانات SQLite.
    row_factory تمكننا من التعامل مع النتائج كـ Dictionaries (أسماء الأعمدة بدلاً من الأرقام).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # تفعيل قيود المفاتيح الأجنبية (Foreign Keys)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn