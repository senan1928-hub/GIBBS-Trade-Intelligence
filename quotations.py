from connection import get_connection

def add_quotation(request_id, supplier_id, unit_price, currency="USD", production_lead_time="", payment_terms="", incoterms="FOB"):
    """تسجيل عرض سعر جديد مقدم من مورد لطلب شراء محدد"""
    query = """
        INSERT INTO quotations (request_id, supplier_id, unit_price, currency, production_lead_time, payment_terms, incoterms)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (request_id, supplier_id, unit_price, currency, production_lead_time, payment_terms, incoterms))
        conn.commit()
        return cursor.lastrowid


def get_quotations_by_request(request_id):
    """جلب جميع عروض الأسعار المرتبطة بطلب شراء محدد مجمعة مع تقييم المورد"""
    query = """
        SELECT 
            q.id,
            s.company_name AS supplier_name,
            s.country AS supplier_country,
            s.rating AS supplier_rating,
            q.unit_price,
            q.currency,
            q.production_lead_time,
            q.payment_terms,
            q.incoterms,
            q.status,
            q.created_at
        FROM quotations q
        JOIN suppliers s ON q.supplier_id = s.id
        WHERE q.request_id = ?
        ORDER BY q.unit_price ASC
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (request_id,))
        return [dict(row) for row in cursor.fetchall()]


def get_all_quotations():
    """جلب كافة عروض الأسعار المسجلة في النظام"""
    query = """
        SELECT 
            q.id,
            q.request_id,
            c.company_name AS customer_name,
            p.trade_name AS product_name,
            s.company_name AS supplier_name,
            q.unit_price,
            q.currency,
            q.incoterms,
            q.created_at
        FROM quotations q
        JOIN purchase_requests pr ON q.request_id = pr.id
        JOIN customers c ON pr.customer_id = c.id
        JOIN products p ON pr.product_id = p.id
        JOIN suppliers s ON q.supplier_id = s.id
        ORDER BY q.id DESC
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]