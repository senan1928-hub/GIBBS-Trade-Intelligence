from connection import get_connection

def add_purchase_request(customer_id, product_id, quantity, unit="TON", specifications="", delivery_date=None, destination_country="", destination_port=""):
    """تسجيل طلب شراء جديد من عميل"""
    query = """
        INSERT INTO purchase_requests (customer_id, product_id, quantity, unit, specifications, delivery_date, destination_country, destination_port)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (customer_id, product_id, quantity, unit, specifications, delivery_date, destination_country, destination_port))
        conn.commit()
        return cursor.lastrowid


def get_all_purchase_requests():
    """جلب جميع طلبات الشراء دمجمًا معها اسم العميل واسم المنتج"""
    query = """
        SELECT 
            pr.id,
            c.company_name AS customer_name,
            p.trade_name AS product_name,
            pr.quantity,
            pr.unit,
            pr.specifications,
            pr.delivery_date,
            pr.destination_country,
            pr.destination_port,
            pr.status,
            pr.created_at
        FROM purchase_requests pr
        JOIN customers c ON pr.customer_id = c.id
        JOIN products p ON pr.product_id = p.id
        ORDER BY pr.id DESC
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]


def update_request_status(request_id, new_status):
    """تحديث حالة طلب الشراء (New, In Progress, Quoted, Closed, Cancelled)"""
    query = "UPDATE purchase_requests SET status = ? WHERE id = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (new_status, request_id))
        conn.commit()
        return cursor.rowcount > 0