import os
from pathlib import Path

# المسار الرئيسي للمشروع
BASE_DIR = Path(__file__).resolve().parent

# معلومات التطبيق الأساسية
APP_NAME = "GIBBS Trade Intelligence"
APP_SHORT_NAME = "GTI"
APP_VERSION = "1.0.0"

# مسارات المجلدات والقواعد
DB_PATH = r"D:\GIBBS Trade Intelligence\database.db"
UPLOADS_DIR = BASE_DIR / "uploads"
EXPORTS_DIR = BASE_DIR / "exports"
REPORTS_DIR = BASE_DIR / "reports"
ASSETS_DIR = BASE_DIR / "assets"

# إعدادات النظام وتتبع الأخطاء
DEBUG = True
LOG_LEVEL = "INFO"
LOG_FILE = BASE_DIR / "app.log"

# التأكد من وجود المجلدات الأساسية
for path in [UPLOADS_DIR, EXPORTS_DIR, REPORTS_DIR, ASSETS_DIR]:
    path.mkdir(parents=True, exist_ok=True)