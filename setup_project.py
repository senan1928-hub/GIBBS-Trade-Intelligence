import os

# المجلدات المطلوبة
directories = [
    "database",
    "core",
    "modules/customers",
    "modules/suppliers",
    "modules/products",
    "modules/deals",
    "modules/quotations",
    "modules/shipments",
    "modules/analytics",
    "modules/documents",
    "services",
    "ui/pages",
    "ui/components",
    "reports",
    "uploads",
    "exports",
    "assets/logo",
    "assets/icons",
    "assets/images",
    "tests",
    "backups"
]

# الملفات الأساسية
files = [
    "app.py",
    "config.py",
    "requirements.txt",
    "README.md",
    "database/connection.py",
    "database/models.py",
    "database/migrations.py",
    "core/constants.py",
    "core/helpers.py",
    "core/validators.py",
    "core/logger.py",
    "services/pdf_service.py",
    "services/excel_service.py",
    "services/email_service.py",
    "services/currency_service.py",
    "ui/dashboard.py"
]

# إنشاء المجلدات
for folder in directories:
    os.makedirs(folder, exist_ok=True)
    # إضافة ملف __init__.py لتسجيل المجلد كموديول بايثون
    init_file = os.path.join(folder, "__init__.py")
    if not os.path.exists(init_file):
        open(init_file, 'w').close()

# إنشاء الملفات
for file_path in files:
    if not os.path.exists(file_path):
        open(file_path, 'w').close()

print("✅ تم إنشاء هيكل مشروع GIBBS Trade Intelligence بنجاح!")