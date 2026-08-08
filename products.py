from connection import get_connection

def add_product(trade_name, chemical_name="", cas_number="", hs_code="", un_number="", specifications="", packaging="", origin_country=""):
    """إضافة منتج كيميائي جديد"""
    query = """
        INSERT INTO products (trade_name, chemical_name, cas_number, hs_code, un_number, specifications, packaging, origin_country)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (trade_name, chemical_name, cas_number, hs_code, un_number, specifications, packaging, origin_country))
        conn.commit()
        return cursor.lastrowid

def get_all_products():
    """جلب جميع المنتجات الكيميائية"""
    query = "SELECT * FROM products ORDER BY id DESC"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

def get_product_by_id(product_id):
    """جلب منتج محدد بواسطة الرقم التعريفي"""
    query = "SELECT * FROM products WHERE id = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (product_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
def delete_supplier(supplier_id):
    """حذف مورد من قاعدة البيانات"""
    query = "DELETE FROM suppliers WHERE id = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (supplier_id,))
        conn.commit()
        return cursor.rowcount > 0