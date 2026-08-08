from connection import get_connection

def add_customer(company_name, contact_person="", email="", phone="", whatsapp="", country="", address=""):
    """إضافة عميل جديد"""
    query = """
        INSERT INTO customers (company_name, contact_person, email, phone, whatsapp, country, address)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (company_name, contact_person, email, phone, whatsapp, country, address))
        conn.commit()
        return cursor.lastrowid

def get_all_customers():
    """جلب قائمة جميع العملاء"""
    query = "SELECT * FROM customers ORDER BY id DESC"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

def get_customer_by_id(customer_id):
    """جلب بيانات عميل بواسطة الرقم التعريفي"""
    query = "SELECT * FROM customers WHERE id = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (customer_id,))
        row = cursor.fetchone()
        return dict(row) if row else None