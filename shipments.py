from connection import get_connection

def add_shipment(deal_id, shipping_company="", container_number="", bill_of_lading="", etd="", eta="", loading_port="", discharge_port="", status="Preparing"):
    """تسجيل شحنة جديدة مربوطة بصفقة محددة"""
    query = """
        INSERT INTO shipments (deal_id, shipping_company, container_number, bill_of_lading, etd, eta, loading_port, discharge_port, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (deal_id, shipping_company, container_number, bill_of_lading, etd, eta, loading_port, discharge_port, status))
        conn.commit()
        return cursor.lastrowid


def get_all_shipments():
    """جلب جميع الشحنات مع تفاصيل الصفقات والعملاء والموردين المرتبطين بها"""
    query = """
        SELECT s.*, d.deal_value, c.company_name as customer_name, sup.company_name as supplier_name
        FROM shipments s
        LEFT JOIN deals d ON s.deal_id = d.id
        LEFT JOIN customers c ON d.customer_id = c.id
        LEFT JOIN suppliers sup ON d.supplier_id = sup.id
        ORDER BY s.id DESC
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]


def update_shipment_status(shipment_id, new_status):
    """تحديث حالة الشحنة (تحت التحضير، على متن السفينة، وصلت، تم التخليص)"""
    query = "UPDATE shipments SET status = ? WHERE id = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (new_status, shipment_id))
        conn.commit()
        return cursor.rowcount > 0