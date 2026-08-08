import hashlib
import os
from connection import get_connection

def hash_password(password: str, salt: bytes = None) -> tuple:
    """تشفير كلمة المرور باستخدام Salt عشوائي"""
    if not salt:
        salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return pwd_hash.hex(), salt.hex()


def verify_password(stored_hash: str, stored_salt: str, password_attempt: str) -> bool:
    """التحقق من صحة محاولة تسجيل الدخول"""
    salt = bytes.fromhex(stored_salt)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password_attempt.encode('utf-8'), salt, 100000)
    return pwd_hash.hex() == stored_hash


def init_users_table():
    """تحديث وإنشاء جدول المستخدمين وتجهيز الحساب الافتراضي"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. التحقق مما إذا كان الجدول القديم موجوداً وبحاجة لتحديث الهيكل
        cursor.execute("PRAGMA table_info(users);")
        columns = [column[1] for column in cursor.fetchall()]

        # إذا كان الجدول موجوداً ولكن بدون حقل password_hash، نقوم بإعادة بنائه
        if columns and "password_hash" not in columns:
            cursor.execute("DROP TABLE users;")
            conn.commit()

        # 2. إنشاء جدول المستخدمين بالمواصفات الأمنية الجديدة
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT DEFAULT 'Admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(query)
        conn.commit()

        # 3. إنشاء حساب المدير الافتراضي إذا لم يكن موجوداً
        cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
        if not cursor.fetchone():
            h, s = hash_password("admin123")
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, salt, role) VALUES (?, ?, ?, ?, ?)",
                ("admin", "admin@gibbs.com", h, s, "Admin")
            )
            conn.commit()


def login_user(username, password):
    """التحقق من بيانات الدخول وإرجاع معلومات المستخدم عند النجاح"""
    init_users_table()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user:
            user_dict = dict(user)
            if verify_password(user_dict['password_hash'], user_dict['salt'], password):
                return user_dict
    return None
def change_password(username, old_password, new_password):
    """تغيير كلمة المرور للمستخدم"""
    # 1. التحقق من صحة كلمة المرور القديمة
    user = login_user(username, old_password)
    if not user:
        return False, "كلمة المرور القديمة غير صحيحة."

    # 2. التحقق من طول كلمة المرور الجديدة
    if len(new_password.strip()) < 6:
        return False, "يجب أن تتكون كلمة المرور الجديدة من 6 خانات على الأقل."

    # 3. تشفير كلمة المرور الجديدة والتحديث في قاعدة البيانات
    new_hash, new_salt = hash_password(new_password.strip())
    query = "UPDATE users SET password_hash = ?, salt = ? WHERE username = ?"
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (new_hash, new_salt, username))
        conn.commit()

    return True, "تم تغيير كلمة المرور بنجاح!"