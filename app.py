import streamlit as st
import pandas as pd

# استيراد كافة الخدمات والنماذج
from models import create_tables
from customers import add_customer, get_all_customers
from suppliers import add_supplier, get_all_suppliers
from products import add_product, get_all_products
from deals import create_deal, get_all_deals
from purchase_requests import add_purchase_request, get_all_purchase_requests
from quotations import add_quotation, get_quotations_by_request, get_all_quotations
from cost_calculator import calculate_landed_cost
from excel_service import export_to_excel
from pdf_service import generate_deal_pdf
from email_service import send_email
from shipments import add_shipment, get_all_shipments, update_shipment_status
from ai_assistant import get_best_supplier_for_product, simulate_shipping_impact, get_analytics_summary, ask_gti_ai
from auth import login_user, init_users_table
from auth import login_user, init_users_table, change_password

# 1. تهيئة وقواعد البيانات والجدول الأمني
create_tables()
init_users_table()

# 2. إعدادات الصفحة
st.set_page_config(
    page_title="GIBBS Trade Intelligence",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. التنسيق والاتجاه العربي
st.markdown("""
    <style>
    .main-header {
        font-size: 26px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: right;
        padding-bottom: 10px;
        border-bottom: 2px solid #E5E7EB;
        margin-bottom: 20px;
    }
    .stApp {
        direction: rtl;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# 4. إدارة الجلسة ونظام تسجيل الدخول (Session State)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_info"] = None

# --- شاشة تسجيل الدخول المربعة الحصينة ---
if not st.session_state["logged_in"]:
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🧪 GIBBS Trade Intelligence</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>تسجيل الدخول للنظام</h4>", unsafe_allow_html=True)
        st.divider()
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")
            submit = st.form_submit_button("تسجيل الدخول", use_container_width=True)
            
            if submit:
                user = login_user(username.strip(), password.strip())
                if user:
                    st.session_state["logged_in"] = True
                    st.session_state["user_info"] = user
                    st.success("✅ تم تسجيل الدخول بنجاح!")
                    st.rerun()
                else:
                    st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة.")
    st.stop()


# --- القائمة الجانبية بعد تسجيل الدخول ---
user = st.session_state["user_info"]

st.sidebar.title("🧪 GIBBS Trade Intelligence")
st.sidebar.markdown(f"👤 **المستخدم:** {user['username']} (`{user['role']}`)")

if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state["logged_in"] = False
    st.session_state["user_info"] = None
    st.rerun()

# --- نموذج تغيير كلمة المرور ---
with st.sidebar.expander("🔑 تغيير كلمة المرور"):
    with st.form("change_pwd_form", clear_on_submit=True):
        old_pwd = st.text_input("كلمة المرور الحالية", type="password")
        new_pwd = st.text_input("كلمة المرور الجديدة", type="password")
        confirm_pwd = st.text_input("تأكيد كلمة المرور", type="password")
        
        submit_pwd = st.form_submit_button("حفظ كلمة المرور", use_container_width=True)
        
        if submit_pwd:
            if new_pwd != confirm_pwd:
                st.error("⚠️ كلمة المرور الجديدة غير متطابقة.")
            else:
                success, msg = change_password(user['username'], old_pwd, new_pwd)
                if success:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "الانتقال السريع إلى الشاشة:",
    [
        "📊 لوحة التحكم",
        "👥 إدارة العملاء",
        "🏭 إدارة الموردين",
        "🧪 المنتجات الكيميائية",
        "📑 طلبات الشراء",
        "⚖️ مقارنة العروض",
        "🤝 إدارة الصفقات",
        "🚢 متابعة الشحنات",
        "🧮 حاسبة التكلفة",
        "🤖 مساعد الذكاء الاصطناعي",
        "📈 التحليلات والتقارير"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("GTI System v1.0 - Secured Enterprise")


# --- 1. لوحة التحكم ---
if menu == "📊 لوحة التحكم":
    st.markdown("<div class='main-header'>📊 لوحة التحكم الرئيسية والذكاء التجاري</div>", unsafe_allow_html=True)
    
    customers_list = get_all_customers()
    suppliers_list = get_all_suppliers()
    products_list = get_all_products()
    deals_list = get_all_deals()
    shipments_list = get_all_shipments()

    active_shipments = [s for s in shipments_list if s['status'] != 'Cleared']
    total_deal_value = sum([d['deal_value'] for d in deals_list]) if deals_list else 0.0
    total_commission = sum([d['commission_amount'] for d in deals_list]) if deals_list else 0.0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("إجمالي العملاء", len(customers_list))
    col2.metric("إجمالي الموردين", len(suppliers_list))
    col3.metric("إجمالي المنتجات", len(products_list))
    col4.metric("الشحنات النشطة", len(active_shipments), f"من إجمالي {len(shipments_list)}")

    st.divider()

    m_col1, m_col2 = st.columns(2)
    m_col1.metric("إجمالي قيمة الصفقات", f"${total_deal_value:,.2f}")
    m_col2.metric("إجمالي العمولات والأرباح", f"${total_commission:,.2f}")

    st.subheader("🔔 التنبيهات وإشعار اللوجستيات")
    if active_shipments:
        for s in active_shipments:
            st.warning(f"🚢 **شحنة نشطة #{s['id']}**: الحاوية `{s['container_number']}` الخاصة بالعميل **{s['customer_name']}** - الحالة الحالية: **{s['status']}** (وصول متوقع ETA: {s['eta']})")
    else:
        st.success("✅ جميع الشحنات في حالة ممتازة ومكتملة ولا توجد تنبيهات تأخير حالياً.")

    st.divider()
    st.subheader("أحدث الصفقات المسجلة")
    if deals_list:
        st.dataframe(pd.DataFrame(deals_list), use_container_width=True)
    else:
        st.info("لا توجد صفقات مسجلة بعد في قاعدة البيانات.")


# --- 2. إدارة العملاء ---
elif menu == "👥 إدارة العملاء":
    st.markdown("<div class='main-header'>👥 إدارة العملاء (Customers)</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ إضافة عميل جديد", "📋 قائمة العملاء المسجلين"])
    
    with tab1:
        with st.form("add_customer_form", clear_on_submit=True):
            company_name = st.text_input("اسم الشركة *")
            contact_person = st.text_input("الشخص المسؤول")
            col_a, col_b = st.columns(2)
            email = col_a.text_input("البريد الإلكتروني")
            phone = col_b.text_input("الهاتف")
            whatsapp = col_a.text_input("واتساب")
            country = col_b.text_input("الدولة")
            address = st.text_area("العنوان")
            
            submitted = st.form_submit_button("حفظ العميل")
            if submitted:
                if company_name.strip():
                    c_id = add_customer(company_name, contact_person, email, phone, whatsapp, country, address)
                    st.success(f"✅ تم إضافة العميل بنجاح! رقم التعريف: {c_id}")
                else:
                    st.error("⚠️ يرجى إدخال اسم الشركة.")
                    
    with tab2:
        customers = get_all_customers()
        if customers:
            st.dataframe(pd.DataFrame(customers), use_container_width=True)
            excel_file = export_to_excel(customers, sheet_name="Customers")
            st.download_button(
                label="📥 تصدير قائمة العملاء إلى Excel",
                data=excel_file,
                file_name="GTI_Customers_List.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("لا يوجد عملاء مسجلون حالياً.")


# --- 3. إدارة الموردين ---
elif menu == "🏭 إدارة الموردين":
    st.markdown("<div class='main-header'>🏭 إدارة الموردين (Suppliers)</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ إضافة مورد جديد", "📋 قائمة الموردين المسجلين"])
    
    with tab1:
        with st.form("add_supplier_form", clear_on_submit=True):
            company_name = st.text_input("اسم شركة المورد *")
            col_a, col_b = st.columns(2)
            country = col_a.text_input("الدولة")
            city = col_b.text_input("المدينة")
            contact_person = st.text_input("جهة الاتصال")
            email = col_a.text_input("البريد الإلكتروني")
            whatsapp = col_b.text_input("واتساب")
            website = st.text_input("الموقع الإلكتروني")
            rating = st.slider("تقييم المورد", 1.0, 5.0, 4.0, 0.1)
            notes = st.text_area("ملاحظات")
            
            submitted = st.form_submit_button("حفظ المورد")
            if submitted:
                if company_name.strip():
                    s_id = add_supplier(company_name, country, city, contact_person, email, whatsapp, website, rating, notes)
                    st.success(f"✅ تم إضافة المورد بنجاح! رقم التعريف: {s_id}")
                else:
                    st.error("⚠️ يرجى إدخال اسم شركة المورد.")
                    
    with tab2:
        suppliers = get_all_suppliers()
        if suppliers:
            st.dataframe(pd.DataFrame(suppliers), use_container_width=True)
        else:
            st.info("لا يوجد موردون مسجلون حالياً.")


# --- 4. إدارة المنتجات ---
elif menu == "🧪 المنتجات الكيميائية":
    st.markdown("<div class='main-header'>🧪 المنتجات الكيميائية (Products)</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ إضافة منتج جديد", "📋 قائمة المنتجات المسجلة"])
    
    with tab1:
        with st.form("add_product_form", clear_on_submit=True):
            trade_name = st.text_input("الاسم التجاري للمادة *")
            chemical_name = st.text_input("الاسم الكيميائي")
            col_a, col_b, col_c = st.columns(3)
            cas_number = col_a.text_input("CAS Number")
            hs_code = col_b.text_input("HS Code")
            un_number = col_c.text_input("UN Number")
            packaging = col_a.text_input("التعبئة")
            origin_country = col_b.text_input("بلد المنشأ")
            specifications = st.text_area("المواصفات الفنية")
            
            submitted = st.form_submit_button("حفظ المنتج")
            if submitted:
                if trade_name.strip():
                    p_id = add_product(trade_name, chemical_name, cas_number, hs_code, un_number, specifications, packaging, origin_country)
                    st.success(f"✅ تم إضافة المنتج بنجاح! رقم التعريف: {p_id}")
                else:
                    st.error("⚠️ يرجى إدخال الاسم التجاري.")
                    
    with tab2:
        products = get_all_products()
        if products:
            st.dataframe(pd.DataFrame(products), use_container_width=True)
        else:
            st.info("لا توجد منتجات مسجلة حالياً.")


# --- 5. طلبات الشراء ---
elif menu == "📑 طلبات الشراء":
    st.markdown("<div class='main-header'>📑 طلبات الشراء (Purchase Requests)</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ تسجيل طلب شراء جديد", "📋 قائمة الطلبات الواردة"])
    
    customers = get_all_customers()
    products = get_all_products()
    
    with tab1:
        if not customers or not products:
            st.warning("⚠️ يجب إضافة عميل واحد ومنتج واحد على الأقل قبل تسجيل طلب شراء.")
        else:
            cust_dict = {c['company_name']: c['id'] for c in customers}
            prod_dict = {p['trade_name']: p['id'] for p in products}
            
            with st.form("add_request_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                selected_customer = col1.selectbox("اختر العميل *", list(cust_dict.keys()))
                selected_product = col2.selectbox("اختر المنتج *", list(prod_dict.keys()))
                
                col_a, col_b = st.columns(2)
                quantity = col_a.number_input("الكمية المطلوبة *", min_value=0.1, value=100.0, step=10.0)
                unit = col_b.selectbox("الوحدة", ["TON", "KG", "IBC", "DRUM", "CONTAINER"])
                
                col_c, col_d = st.columns(2)
                destination_country = col_c.text_input("الدولة الهدف / الوجهة")
                destination_port = col_d.text_input("الميناء المستهدف")
                
                delivery_date = st.date_input("موعد التسليم المتوقع")
                specifications = st.text_area("مواصفات خاصة أو شروط إضافية")
                
                submitted = st.form_submit_button("تسجيل طلب الشراء")
                if submitted:
                    req_id = add_purchase_request(
                        customer_id=cust_dict[selected_customer],
                        product_id=prod_dict[selected_product],
                        quantity=quantity,
                        unit=unit,
                        specifications=specifications,
                        delivery_date=str(delivery_date),
                        destination_country=destination_country,
                        destination_port=destination_port
                    )
                    st.success(f"✅ تم تسجيل طلب الشراء بنجاح! رقم الطلب: #{req_id}")

    with tab2:
        requests_list = get_all_purchase_requests()
        if requests_list:
            st.dataframe(pd.DataFrame(requests_list), use_container_width=True)
        else:
            st.info("لا توجد طلبات شراء مسجلة حالياً.")


# --- 6. مقارنة العروض ---
elif menu == "⚖️ مقارنة العروض":
    st.markdown("<div class='main-header'>⚖️ منصة مقارنة عروض الأسعار والذكاء التجاري</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([
        "📊 شاشة المقارنة التحليلية", 
        "➕ تسجيل عرض سعر جديد", 
        "📋 جميع العروض المسجلة"
    ])
    
    requests_list = get_all_purchase_requests()
    suppliers_list = get_all_suppliers()
    
    with tab1:
        if not requests_list:
            st.info("لا توجد طلبات شراء مسجلة لمقارنة عروضها حالياً.")
        else:
            req_options = {f"طلب #{r['id']} - العميل: {r['customer_name']} | المنتج: {r['product_name']} ({r['quantity']} {r['unit']})": r['id'] for r in requests_list}
            selected_req_label = st.selectbox("اختر طلب الشراء لعرض عروض الموردين المتاحة:", list(req_options.keys()))
            selected_req_id = req_options[selected_req_label]
            
            quotes = get_quotations_by_request(selected_req_id)
            st.divider()
            
            if not quotes:
                st.warning("⚠️ لا توجد عروض أسعار مسجلة لهذا الطلب حتى الآن.")
            else:
                st.subheader("💡 مؤشرات تحليلية سريعة")
                best_price_quote = min(quotes, key=lambda x: x['unit_price'])
                best_rating_quote = max(quotes, key=lambda x: x['supplier_rating'])
                
                m1, m2, m3 = st.columns(3)
                m1.metric("أقل سعر وحدة", f"${best_price_quote['unit_price']:,.2f} {best_price_quote['currency']}", f"المورد: {best_price_quote['supplier_name']}")
                m2.metric("أعلى مورد تقييماً", f"⭐ {best_rating_quote['supplier_rating']:.1f} / 5.0", best_rating_quote['supplier_name'])
                m3.metric("إجمالي العروض المقدمة", f"{len(quotes)} عروض")
                
                st.subheader("📋 جدول المقارنة الشامل بين الموردين")
                df_quotes = pd.DataFrame(quotes)
                df_display = df_quotes[[
                    'supplier_name', 'supplier_country', 'supplier_rating', 
                    'unit_price', 'currency', 'incoterms', 
                    'production_lead_time', 'payment_terms'
                ]].copy()
                
                df_display.columns = [
                    "المورد", "الدولة", "التقييم", 
                    "سعر الوحدة", "العملة", "شرط التسليم (Incoterms)", 
                    "مدة الإنتاج", "شروط الدفع"
                ]
                st.dataframe(df_display, use_container_width=True)

    with tab2:
        if not requests_list or not suppliers_list:
            st.warning("⚠️ يجب وجود طلب شراء واحد ومورد واحد على الأقل لتسجيل عرض سعر.")
        else:
            req_dict = {f"طلب #{r['id']} - {r['customer_name']} ({r['product_name']})": r['id'] for r in requests_list}
            supp_dict = {s['company_name']: s['id'] for s in suppliers_list}
            
            with st.form("add_quotation_form_tab2", clear_on_submit=True):
                selected_req = st.selectbox("اختر طلب الشراء المستهدف *", list(req_dict.keys()))
                selected_supp = st.selectbox("اختر المورد *", list(supp_dict.keys()))
                
                col_a, col_b = st.columns(2)
                unit_price = col_a.number_input("سعر الوحدة *", min_value=0.01, value=500.0, step=10.0)
                currency = col_b.selectbox("العملة", ["USD", "EUR", "CNY", "SAR"])
                
                col_c, col_d = st.columns(2)
                incoterms = col_c.selectbox("شرط التسليم (Incoterms)", ["FOB", "CIF", "CFR", "EXW", "DDP"])
                production_lead_time = col_d.text_input("مدة الإنتاج (مثال: 15 يوماً)")
                
                payment_terms = st.text_input("شروط الدفع (مثال: 30% Advance, 70% LC)")
                
                submitted = st.form_submit_button("حفظ عرض السعر")
                if submitted:
                    q_id = add_quotation(
                        request_id=req_dict[selected_req],
                        supplier_id=supp_dict[selected_supp],
                        unit_price=unit_price,
                        currency=currency,
                        production_lead_time=production_lead_time,
                        payment_terms=payment_terms,
                        incoterms=incoterms
                    )
                    st.success(f"✅ تم تسجيل عرض السعر بنجاح! رقم العرض: #{q_id}")

    with tab3:
        all_q = get_all_quotations()
        if all_q:
            st.dataframe(pd.DataFrame(all_q), use_container_width=True)
        else:
            st.info("لا توجد عروض أسعار مسجلة حالياً.")


# --- 7. إدارة الصفقات ---
elif menu == "🤝 إدارة الصفقات":
    st.markdown("<div class='main-header'>🤝 إدارة الصفقات والعمولات (Deals Management)</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ إغلاق وإنشاء صفقة جديدة", "📋 قائمة الصفقات الحالية والتصدير"])
    
    requests_list = get_all_purchase_requests()
    suppliers_list = get_all_suppliers()
    customers_list = get_all_customers()
    quotations_list = get_all_quotations()
    
    with tab1:
        if not requests_list or not quotations_list:
            st.warning("⚠️ يجب تسجيل طلب شراء وعرض سعر واحد على الأقل قبل إنشاء صفقة.")
        else:
            req_dict = {f"طلب #{r['id']} - العميل: {r['customer_name']} | المنتج: {r['product_name']}": r['id'] for r in requests_list}
            supp_dict = {s['company_name']: s['id'] for s in suppliers_list}
            cust_dict = {c['company_name']: c['id'] for c in customers_list}
            
            with st.form("create_deal_form", clear_on_submit=True):
                st.subheader("📝 تفاصيل الصفقة والعملاء")
                
                selected_req_label = st.selectbox("اختر طلب الشراء المرتبط بالصفقة *", list(req_dict.keys()))
                selected_req_id = req_dict[selected_req_label]
                
                col_a, col_b = st.columns(2)
                selected_cust_name = col_a.selectbox("العميل المشترِي *", list(cust_dict.keys()))
                selected_supp_name = col_b.selectbox("المورد المورد *", list(supp_dict.keys()))
                
                st.subheader("💰 القيم المالية والعمولات")
                col_c, col_d = st.columns(2)
                deal_value = col_c.number_input("القيمة الإجمالية للصفقة ($) *", min_value=1.0, value=10000.0, step=500.0)
                commission_rate = col_d.number_input("نسبة عمولة الشركة (%) *", min_value=0.1, max_value=50.0, value=5.0, step=0.5)
                
                est_commission = deal_value * (commission_rate / 100.0)
                st.info(f"💡 معاينة الحسابات: قيمة العمولة المستحقة = **${est_commission:,.2f}** | صافي الربح التقديري = **${est_commission:,.2f}**")
                
                submitted = st.form_submit_button("إغلاق وحفظ الصفقة")
                if submitted:
                    quotation_id = quotations_list[0]['id'] if quotations_list else 1
                    
                    deal_id = create_deal(
                        request_id=selected_req_id,
                        quotation_id=quotation_id,
                        customer_id=cust_dict[selected_cust_name],
                        supplier_id=supp_dict[selected_supp_name],
                        deal_value=deal_value,
                        commission_rate=commission_rate
                    )
                    st.success(f"🎉 تم تسجيل الصفقة بنجاح! رقم الصفقة المرجعي: #{deal_id}")

    with tab2:
        deals = get_all_deals()
        if deals:
            total_deals_val = sum(d['deal_value'] for d in deals)
            total_comm_val = sum(d['commission_amount'] for d in deals)
            
            m1, m2, m3 = st.columns(3)
            m1.metric("عدد الصفقات المسجلة", f"{len(deals)} صفقات")
            m2.metric("إجمالي قيمة الصفقات", f"${total_deals_val:,.2f}")
            m3.metric("إجمالي أرباح العمولات", f"${total_comm_val:,.2f}")
            
            st.divider()
            st.subheader("📊 جدول الصفقات المكتملة والقائمة")
            df_deals = pd.DataFrame(deals)
            st.dataframe(df_deals, use_container_width=True)
            
            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                st.subheader("📥 تصدير السجل (Excel)")
                excel_file = export_to_excel(deals, sheet_name="Deals_Summary")
                st.download_button(
                    label="تنزيل كافة الصفقات (Excel)",
                    data=excel_file,
                    file_name="GTI_Deals_Summary.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
            with col_exp2:
                st.subheader("📄 تصدير وإرسال تقرير صفقة (PDF)")
                deal_ids = [d['id'] for d in deals]
                selected_deal_id = st.selectbox("اختر رقم الصفقة:", deal_ids)
                selected_deal_data = next((d for d in deals if d['id'] == selected_deal_id), None)
                
                if selected_deal_data:
                    pdf_file = generate_deal_pdf(selected_deal_data)
                    st.download_button(
                        label=f"تنزيل تقرير الصفقة #{selected_deal_id} (PDF)",
                        data=pdf_file,
                        file_name=f"GTI_Deal_Report_{selected_deal_id}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    st.markdown("---")
                    target_email = st.text_input("أدخل البريد الإلكتروني للمستلم:", value="client@example.com")
                    if st.button("📧 إرسال تقرير الصفقة إلكترونياً تلقائياً", use_container_width=True):
                        email_body = f"<h3>مرفق لكم تقرير ملخص الصفقة الرسمية #{selected_deal_id}</h3><p>شكراً لتعاملكم مع GTI.</p>"
                        success, msg = send_email(
                            to_email=target_email,
                            subject=f"GTI - Official Deal Report #{selected_deal_id}",
                            body_html=email_body,
                            attachment_bytes=pdf_file,
                            attachment_filename=f"GTI_Deal_Report_{selected_deal_id}.pdf"
                        )
                        if success:
                            st.success(f"✅ {msg}")
                        else:
                            st.error(f"❌ {msg}")
        else:
            st.info("لا توجد صفقات مسجلة حالياً.")


# --- 8. متابعة الشحنات ---
elif menu == "🚢 متابعة الشحنات":
    st.markdown("<div class='main-header'>🚢 متابعة الشحنات والعمليات اللوجستية (Shipment Tracking)</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ تسجيل شحنة جديدة", "📋 جدول تتبع الشحنات القائمة"])
    
    deals_list = get_all_deals()
    
    with tab1:
        if not deals_list:
            st.warning("⚠️ يجب إنشاء صفقة واحدة على الأقل قبل تسجيل شحنة جديدة.")
        else:
            deal_dict = {f"صفقة #{d['id']} - قيمة: ${d['deal_value']:,.2f}": d['id'] for d in deals_list}
            
            with st.form("add_shipment_form", clear_on_submit=True):
                selected_deal = st.selectbox("اختر الصفقة المرتبطة بالطلب *", list(deal_dict.keys()))
                
                col_a, col_b = st.columns(2)
                shipping_company = col_a.text_input("شركة الشحن (مثال: Maersk, MSC, COSCO)")
                container_number = col_b.text_input("رقم الحاوية (Container No.)")
                
                col_c, col_d = st.columns(2)
                bill_of_lading = col_c.text_input("رقم بوليصة الشحن (B/L Number)")
                status = col_d.selectbox("حالة الشحنة الحالية", ["Preparing", "On Board", "Arrived", "Cleared"])
                
                col_e, col_f = st.columns(2)
                loading_port = col_e.text_input("ميناء التحميل (Loading Port)")
                discharge_port = col_f.text_input("ميناء التفريغ (Discharge Port)")
                
                col_g, col_h = st.columns(2)
                etd = col_g.date_input("تاريخ المغادرة المتوقع (ETD)")
                eta = col_h.date_input("تاريخ الوصول المتوقع (ETA)")
                
                submitted = st.form_submit_button("تسجيل الشحنة")
                if submitted:
                    shipment_id = add_shipment(
                        deal_id=deal_dict[selected_deal],
                        shipping_company=shipping_company,
                        container_number=container_number,
                        bill_of_lading=bill_of_lading,
                        etd=str(etd),
                        eta=str(eta),
                        loading_port=loading_port,
                        discharge_port=discharge_port,
                        status=status
                    )
                    st.success(f"✅ تم تسجيل الشحنة بنجاح! رقم المتابعة اللوجستي: #{shipment_id}")

    with tab2:
        shipments = get_all_shipments()
        if shipments:
            st.dataframe(pd.DataFrame(shipments), use_container_width=True)
            
            st.divider()
            st.subheader("🔄 تحديث حالة شحنة قائمة")
            col_sel, col_stat = st.columns(2)
            s_ids = [s['id'] for s in shipments]
            selected_s_id = col_sel.selectbox("اختر رقم الشحنة لتحديث حالتها:", s_ids)
            new_s_status = col_stat.selectbox("الحالة الجديدة:", ["Preparing", "On Board", "Arrived", "Cleared"])
            
            if st.button("تحديث الحالة الآن"):
                update_shipment_status(selected_s_id, new_s_status)
                st.success(f"✅ تم تحديث حالة الشحنة #{selected_s_id} إلى ({new_s_status}) بنجاح!")
                st.rerun()
        else:
            st.info("لا توجد شحنات مسجلة حالياً.")


# --- 9. حاسبة التكلفة ---
elif menu == "🧮 حاسبة التكلفة":
    st.markdown("<div class='main-header'>🧮 حاسبة تكلفة الاستيراد وتحديد سعر البيع (Landed Cost Calculator)</div>", unsafe_allow_html=True)
    
    st.info("💡 أدخل عناصر التكلفة المختلفة للحصول على التكلفة النهائية للطن وسعر البيع المقترح وهامش الربح المتوقع.")
    
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.subheader("📦 البيانات الأساسية وسعر المصنع")
        quantity = st.number_input("الكمية المطلوبة (بالأطنان)", min_value=1.0, value=20.0, step=1.0)
        exw_fob_unit_price = st.number_input("سعر الطن من المصنع ($ EXW / FOB)", min_value=0.0, value=850.0, step=10.0)
        
        st.subheader("🚢 اللوجستيات والشحن")
        sea_freight = st.number_input("إجمالي الشحن البحري ($)", min_value=0.0, value=1800.0, step=50.0)
        insurance = st.number_input("تكلفة التأمين البحري ($)", min_value=0.0, value=150.0, step=10.0)
        
    with col_input2:
        st.subheader("🏛️ الجمارك والمصاريف المحلية")
        customs_duty_percent = st.number_input("نسبة الجمرك (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
        inland_transport = st.number_input("النقل الداخلي ($)", min_value=0.0, value=400.0, step=20.0)
        storage_port_fees = st.number_input("مصاريف الميناء والتخزين ($)", min_value=0.0, value=300.0, step=20.0)
        admin_expenses = st.number_input("المصروفات الإدارية والخدمية ($)", min_value=0.0, value=200.0, step=20.0)
        
        st.subheader("🎯 هامش الربح المستهدف")
        desired_margin_percent = st.slider("نسبة هامش الربح المطلوبة (%)", min_value=1.0, max_value=50.0, value=15.0, step=0.5)
        
    st.divider()
    
    res = calculate_landed_cost(
        exw_fob_unit_price=exw_fob_unit_price,
        quantity=quantity,
        sea_freight=sea_freight,
        insurance=insurance,
        customs_duty_percent=customs_duty_percent,
        inland_transport=inland_transport,
        storage_port_fees=storage_port_fees,
        admin_expenses=admin_expenses,
        desired_margin_percent=desired_margin_percent
    )
    
    st.subheader("📊 نتائج تحليل التكلفة والربحية")
    
    res_col1, res_col2, res_col3, res_col4 = st.columns(4)
    res_col1.metric("التكلفة الإجمالية الواصلة", f"${res['total_landed_cost']:,.2f}")
    res_col2.metric("تكلفة الطن الواصل", f"${res['cost_per_ton']:,.2f} / طن")
    res_col3.metric("تكلفة الكيلوجرام الواصل", f"${res['cost_per_kg']:,.3f} / كجم")
    res_col4.metric("قيمة الجمارك المقدرة", f"${res['customs_amount']:,.2f}")
    
    st.divider()
    
    profit_col1, profit_col2, profit_col3 = st.columns(3)
    profit_col1.metric("سعر البيع الإجمالي المقترح", f"${res['suggested_selling_price_total']:,.2f}")
    profit_col2.metric("سعر بيع الطن المقترح للعميل", f"${res['suggested_price_per_ton']:,.2f} / طن")
    profit_col3.metric("صافي الربح المتوقع", f"${res['expected_profit']:,.2f}", f"هامش {res['desired_margin_percent']}%")


# --- 10. مساعد الذكاء الاصطناعي ---
elif menu == "🤖 مساعد الذكاء الاصطناعي":
    st.markdown("<div class='main-header'>🤖 مساعد GTI للذكاء التجاري والاستعلامات الذكية</div>", unsafe_allow_html=True)
    
    st.info("💡 يمكنك طرح أسئلة استراتيجية على النظام لتحليل بيانات الموردين، تقييم هَامش الربح، ومحاكاة مخاطر السوق.")
    
    tab1, tab2 = st.tabs(["🎯 استفسارات الموردين والمنتجات", "📉 محاكاة أثر ارتفاع أسعار الشحن"])
    
    products_list = get_all_products()
    deals_list = get_all_deals()
    
    with tab1:
        st.subheader("🔍 استعلام المورد الأفضل")
        if not products_list:
            st.warning("⚠️ يرجى إضافة منتجات وعروض أسعار أولاً لتشغيل التحليل.")
        else:
            p_dict = {p['trade_name']: p['id'] for p in products_list}
            selected_prod_name = st.selectbox("اختر المنتج الكيميائي المطلوب تحليله:", list(p_dict.keys()))
            
            if st.button("تحليل واقتراح أفضل مورد"):
                answer = ask_gti_ai("best_supplier", {"product_id": p_dict[selected_prod_name]})
                st.markdown(answer)
                
    with tab2:
        st.subheader("🚢 محاكاة حساسية أسعار الشحن البحري")
        if not deals_list:
            st.warning("⚠️ لا توجد صفقات حالية للمحاكاة.")
        else:
            deal_options = {f"صفقة #{d['id']} - قيمة ${d['deal_value']:,.2f}": d for d in deals_list}
            selected_d_label = st.selectbox("اختر الصفقة:", list(deal_options.keys()))
            selected_d = deal_options[selected_d_label]
            
            shipping_inc = st.slider("نسبة الزيادة المتوقعة في أسعار الشحن (%)", 1.0, 50.0, 15.0, 1.0)
            
            if st.button("تشغيل سناريو المحاكاة"):
                answer = ask_gti_ai("shipping_sensitivity", {
                    "deal_value": selected_d['deal_value'],
                    "current_profit": selected_d['net_profit'],
                    "increase_pct": shipping_inc
                })
                st.markdown(answer)


# --- 11. التحليلات والتقارير ---
elif menu == "📈 التحليلات والتقارير":
    st.markdown("<div class='main-header'>📈 التحليلات الإحصائية وتقرير الذكاء التجاري</div>", unsafe_allow_html=True)
    
    summary = get_analytics_summary()
    
    col1, col2 = st.columns(2)
    col1.metric("متوسط نسبة العمولة للشركة", f"{summary['avg_commission_rate']:.2f}%")
    col2.metric("متوسط قيمة الصفقات", f"${summary['avg_deal_value']:,.2f}")
    
    st.divider()
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("🔥 المنتجات الأكثر طلباً")
        if summary['top_products']:
            st.dataframe(pd.DataFrame(summary['top_products']), use_container_width=True)
        else:
            st.info("لا توجد بيانات كافية حول طلبات المنتجات.")
            
    with col_b:
        st.subheader("⭐ الموردون الأبرز تقييماً")
        if summary['top_suppliers']:
            st.dataframe(pd.DataFrame(summary['top_suppliers']), use_container_width=True)
        else:
            st.info("لا توجد بيانات كافية حول الموردين.")