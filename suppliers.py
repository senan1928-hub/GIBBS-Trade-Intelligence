from connection import get_connection

def add_supplier(company_name, country="", city="", contact_person="", email="", whatsapp="", website="", rating=0.0, notes=""):
    """إضافة مورد جديد"""
    query = """
        INSERT INTO suppliers (company_name, country, city, contact_person, email, whatsapp, website, rating, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (company_name, country, city, contact_person, email, whatsapp, website, rating, notes))
        conn.commit()
        return cursor.lastrowid

def get_all_suppliers():
    """جلب قائمة جميع الموردين"""
    query = "SELECT * FROM suppliers ORDER BY id DESC"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

def get_supplier_by_id(supplier_id):
    """جلب بيانات مورد بواسطة الرقم التعريفي"""
    query = "SELECT * FROM suppliers WHERE id = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (supplier_id,))
        row = cursor.fetchone()
        return dict(row) if row else None