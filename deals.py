from connection import get_connection

def create_deal(customer_id, supplier_id, deal_value, commission_rate, request_id=None, quotation_id=None):
    """
    إنشاء صفقة جديدة مع حساب العمولة والربح التلقائي.
    ملاحظة: جعلنا request_id و quotation_id اختياريين (القيمة الافتراضية None)
    لتجنب خطأ FOREIGN KEY constraint failed عند الاختبار قبل وجود طلبات أو عروض أسعار.
    """
    commission_amount = deal_value * (commission_rate / 100.0)
    net_profit = commission_amount

    query = """
        INSERT INTO deals (request_id, quotation_id, customer_id, supplier_id, deal_value, commission_rate, commission_amount, net_profit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (request_id, quotation_id, customer_id, supplier_id, deal_value, commission_rate, commission_amount, net_profit))
        conn.commit()
        return cursor.lastrowid

def get_all_deals():
    """جلب جميع الصفقات"""
    query = "SELECT * FROM deals ORDER BY id DESC"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]