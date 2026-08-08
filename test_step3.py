from connection import get_connection
from customers import add_customer, get_all_customers
from suppliers import add_supplier, get_all_suppliers
from products import add_product, get_all_products
from deals import create_deal, get_all_deals

def create_dummy_request_and_quotation(customer_id, supplier_id, product_id):
    """
    إنشاء طلب شراء وعرض سعر تجريبيين بالاعتماد على الهيكلية 
    الموجودة مسبقاً في قاعدة البيانات (models.py) بدون إعادة إنشاء الجداول.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. إنشاء طلب شراء في جدول purchase_requests
        cursor.execute("""
            INSERT INTO purchase_requests (customer_id, product_id, quantity)
            VALUES (?, ?, ?)
        """, (customer_id, product_id, 25))
        req_id = cursor.lastrowid

        # 2. إنشاء عرض سعر في جدول quotations (مع الحقل الإجباري unit_price)
        cursor.execute("""
            INSERT INTO quotations (request_id, supplier_id, unit_price)
            VALUES (?, ?, ?)
        """, (req_id, supplier_id, 820.0))
        quot_id = cursor.lastrowid

        conn.commit()
        return req_id, quot_id

def run_tests():
    print("🚀 بدء اختبار الخطوة الثالثة (Business Logic)...")

    # 1. اختبار العملاء
    c_id = add_customer("شركة سابك", "علي أحمد", "ali@sabic.com", country="السعودية")
    print(f"✅ تم إضافة العميل بمعرف: {c_id}")

    # 2. اختبار الموردين
    s_id = add_supplier("Sinopec Chemical", country="الصين", rating=4.8)
    print(f"✅ تم إضافة المورد بمعرف: {s_id}")

    # 3. اختبار المنتجات
    p_id = add_product("Caustic Soda Flakes", "Sodium Hydroxide", cas_number="1310-73-2")
    print(f"✅ تم إضافة المنتج بمعرف: {p_id}")

    # 4. إنشاء طلب وعرض سعر حقيقيين وفق المخطط
    req_id, quot_id = create_dummy_request_and_quotation(c_id, s_id, p_id)

    # 5. اختبار الصفقات
    d_id = create_deal(
        request_id=req_id,
        quotation_id=quot_id,
        customer_id=c_id,
        supplier_id=s_id,
        deal_value=50000.0,
        commission_rate=5.0
    )
    print(f"✅ تم إضافة الصفقة بمعرف: {d_id}")

    print("\n📊 ملخص البيانات في قاعدة البيانات:")
    print(f"- إجمالي العملاء: {len(get_all_customers())}")
    print(f"- إجمالي الموردين: {len(get_all_suppliers())}")
    print(f"- إجمالي المنتجات: {len(get_all_products())}")
    print(f"- إجمالي الصفقات: {len(get_all_deals())}")
    print("\n🎉 جميع عمليات الخطوة الثالثة تعمل بنجاح 100%!")

if __name__ == "__main__":
    run_tests()