import pandas as pd
from connection import get_connection

def get_best_supplier_for_product(product_id):
    """
    تحليل واستخراج أفضل مورد لمنتج محدد بناءً على قاعدة عروض الأسعار وتقييم الموردين
    """
    query = """
        SELECT q.*, s.company_name as supplier_name, s.rating as supplier_rating, s.country as supplier_country
        FROM quotations q
        JOIN suppliers s ON q.supplier_id = s.id
        JOIN purchase_requests pr ON q.request_id = pr.id
        WHERE pr.product_id = ?
        ORDER BY q.unit_price ASC, s.rating DESC
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (product_id,))
        rows = cursor.fetchall()
        if rows:
            best = dict(rows[0])
            return {
                "supplier_name": best["supplier_name"],
                "unit_price": best["unit_price"],
                "currency": best["currency"],
                "rating": best["supplier_rating"],
                "country": best["supplier_country"],
                "incoterms": best["incoterms"]
            }
    return None


def simulate_shipping_impact(current_profit, total_deal_value, shipping_increase_percentage):
    """
    حساب محاكاة أثر ارتفاع تكاليف الشحن على هامش الربح
    """
    additional_shipping_cost = total_deal_value * (shipping_increase_percentage / 100.0)
    new_profit = current_profit - additional_shipping_cost
    new_margin = (new_profit / total_deal_value * 100.0) if total_deal_value > 0 else 0.0
    
    return {
        "additional_cost": additional_shipping_cost,
        "new_profit": max(new_profit, 0.0),
        "new_margin": max(new_margin, 0.0)
    }


def get_analytics_summary():
    """
    جلب مؤشرات التحليل الشامل لأداء الموردين والعملاء والمنتجات
    """
    with get_connection() as conn:
        # أكثر المنتجات طلباً
        top_products_query = """
            SELECT p.trade_name, COUNT(pr.id) as total_requests, SUM(pr.quantity) as total_quantity
            FROM purchase_requests pr
            JOIN products p ON pr.product_id = p.id
            GROUP BY p.id
            ORDER BY total_requests DESC
            LIMIT 5
        """
        df_top_products = pd.read_sql_query(top_products_query, conn)

        # الموردون الأسرع وأعلى تقييماً
        top_suppliers_query = """
            SELECT company_name, country, rating
            FROM suppliers
            ORDER BY rating DESC
            LIMIT 5
        """
        df_top_suppliers = pd.read_sql_query(top_suppliers_query, conn)

        # إحصائيات الصفقات والعمولات
        avg_commission_query = "SELECT AVG(commission_rate) as avg_comm, AVG(deal_value) as avg_deal FROM deals"
        df_stats = pd.read_sql_query(avg_commission_query, conn)
        avg_comm = df_stats.iloc[0]['avg_comm'] if not df_stats.empty and df_stats.iloc[0]['avg_comm'] else 0.0
        avg_deal = df_stats.iloc[0]['avg_deal'] if not df_stats.empty and df_stats.iloc[0]['avg_deal'] else 0.0

    return {
        "top_products": df_top_products.to_dict(orient="records"),
        "top_suppliers": df_top_suppliers.to_dict(orient="records"),
        "avg_commission_rate": avg_comm,
        "avg_deal_value": avg_deal
    }


def ask_gti_ai(question_key, params=None):
    """
    محرك إجابة الاستفسارات الذكية المباشرة
    """
    params = params or {}
    
    if question_key == "best_supplier":
        product_id = params.get("product_id")
        best = get_best_supplier_for_product(product_id)
        if best:
            return f"💡 **التحليل الذكي:** أفضل مورد متاح لهذا المنتج هو **{best['supplier_name']}** ({best['country']}) بسعر وحدة **${best['unit_price']:,.2f} {best['currency']}** وبتقييم **⭐ {best['rating']:.1f}/5.0**."
        return "⚠️ لا تتوفر عروض أسعار مسجلة لهذا المنتج حالياً لتحديد المورد الأفضل."

    elif question_key == "shipping_sensitivity":
        deal_val = params.get("deal_value", 10000.0)
        curr_profit = params.get("current_profit", 500.0)
        increase_pct = params.get("increase_pct", 15.0)
        
        sim = simulate_shipping_impact(curr_profit, deal_val, increase_pct)
        return f"📊 **محاكاة مخاطر الشحن:** في حال ارتفاع سعر الشحن بنسبة **{increase_pct}%**، سترتفع التكلفة بمقدار **${sim['additional_cost']:,.2f}**، وسينخفض صافي الربح إلى **${sim['new_profit']:,.2f}** (هامش ربح جديد: **{sim['new_margin']:.2f}%**)."
    
    return "الاستفسار غير معروف."