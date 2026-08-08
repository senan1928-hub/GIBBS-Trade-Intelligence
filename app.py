import streamlit as st
import pandas as pd
import json

# ==========================================
# 1. CORE BACKEND SERVICES
# ==========================================
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
from auth import login_user, init_users_table, change_password

# ==========================================
# 2. SYSTEM INITIALIZATION
# ==========================================
create_tables()
init_users_table()

st.set_page_config(
    page_title="GIBBS Trade Intelligence | Enterprise",
    page_icon="G",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 3. ENTERPRISE DESIGN SYSTEM (CSS)
# ==========================================
def inject_enterprise_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans Arabic', 'Inter', sans-serif !important;
    }
    .stApp {
        background-color: #F6F8FA;
        direction: rtl;
        text-align: right;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 1400px !important;
    }

    .gti-page-title {
        font-size: 32px;
        font-weight: 700;
        color: #0B1F33;
        margin-bottom: 4px;
    }
    .gti-page-subtitle {
        font-size: 15px;
        color: #64748B;
        margin-bottom: 32px;
        font-weight: 400;
    }
    .gti-section-title {
        font-size: 20px;
        font-weight: 600;
        color: #0F172A;
        margin: 24px 0 16px 0;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 8px;
    }

    [data-testid="stSidebar"] {
        background-color: #0B1F33 !important;
        border-left: 1px solid #071522;
    }
    [data-testid="stSidebar"] * {
        color: #CBD5E1 !important;
    }
    .gti-logo-container {
        padding: 10px 0 20px 0;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .gti-logo {
        font-size: 22px;
        font-weight: 700;
        color: #FFFFFF !important;
        letter-spacing: 1px;
    }
    .gti-logo-sub {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #16A6B6 !important;
        font-weight: 600;
    }

    .stButton > button {
        background-color: #164E78 !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 8px 24px !important;
        transition: background-color 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #0B1F33 !important;
    }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stNumberInput>div>div>input {
        border-radius: 6px;
        border: 1px solid #CBD5E1;
        background-color: #FFFFFF;
        color: #0F172A;
    }

    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .kpi-title {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748B;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .kpi-val {
        font-size: 32px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 8px;
    }
    .kpi-trend {
        font-size: 13px;
        font-weight: 500;
    }
    .trend-up { color: #15803D; }
    .trend-neutral { color: #2563A6; }

    .status-badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-critical { background: #FEF2F2; color: #C2413B; border: 1px solid #FECACA; }
    .badge-attention { background: #FEFCE8; color: #B7791F; border: 1px solid #FEF08A; }
    .badge-info { background: #EFF6FF; color: #2563A6; border: 1px solid #BFDBFE; }
    .badge-success { background: #F0FDF4; color: #15803D; border: 1px solid #BBF7D0; }

    .quote-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        position: relative;
    }
    .quote-card-best {
        border: 2px solid #2563A6;
        box-shadow: 0 4px 15px rgba(37, 99, 166, 0.1);
    }
    .quote-best-badge {
        position: absolute;
        top: -12px;
        left: 50%;
        transform: translateX(-50%);
        background: #2563A6;
        color: #FFFFFF;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .quote-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #F1F4F7;
        font-size: 14px;
    }
    .quote-row:last-child { border-bottom: none; }
    .quote-label { color: #64748B; }
    .quote-value { font-weight: 600; color: #0F172A; }

    .financial-panel {
        background: #0B1F33;
        color: #FFFFFF;
        border-radius: 12px;
        padding: 32px;
        height: 100%;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .fin-label { font-size: 13px; color: #94A3B8; margin-bottom: 4px; }
    .fin-value { font-size: 36px; font-weight: 700; color: #FFFFFF; margin-bottom: 24px; }
    .fin-value-accent { color: #16A6B6; }
    .fin-divider { height: 1px; background: rgba(255,255,255,0.1); margin: 24px 0; }
    </style>
    """, unsafe_allow_html=True)

inject_enterprise_css()

# ==========================================
# 4. SESSION MANAGEMENT & AUTHENTICATION
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_info"] = None

if not st.session_state["logged_in"]:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="font-size: 36px; font-weight: 700; color: #0B1F33; letter-spacing: -1px;">GIBBS</div>
            <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 3px; color: #164E78; font-weight: 600;">Trade Intelligence</div>
            <p style="color: #64748B; margin-top: 12px;">Enterprise Commercial Intelligence Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("اسم المستخدم (Username)")
            password = st.text_input("كلمة المرور (Password)", type="password")
            submit = st.form_submit_button("تسجيل الدخول", use_container_width=True)
            
            if submit:
                user = login_user(username.strip(), password.strip())
                if user:
                    st.session_state["logged_in"] = True
                    st.session_state["user_info"] = user
                    st.rerun()
                else:
                    st.error("بيانات الدخول غير صحيحة. يرجى المحاولة مرة أخرى.")
    st.stop()

# ==========================================
# 5. ENTERPRISE NAVIGATION (SIDEBAR)
# ==========================================
user = st.session_state["user_info"]

st.sidebar.markdown("""
<div class="gti-logo-container">
    <div class="gti-logo">GIBBS</div>
    <div class="gti-logo-sub">Trade Intelligence</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"<div style='font-size:12px; color:#94A3B8; margin-bottom:15px;'>المستخدم: <b>{user['username']}</b> (`{user['role']}`)</div>", unsafe_allow_html=True)

if st.sidebar.button("تسجيل الخروج", use_container_width=True):
    st.session_state["logged_in"] = False
    st.session_state["user_info"] = None
    st.rerun()

with st.sidebar.expander("تغيير كلمة المرور"):
    with st.form("change_pwd_form", clear_on_submit=True):
        old_pwd = st.text_input("كلمة المرور الحالية", type="password")
        new_pwd = st.text_input("كلمة المرور الجديدة", type="password")
        confirm_pwd = st.text_input("تأكيد كلمة المرور", type="password")
        if st.form_submit_button("حفظ كلمة المرور"):
            if new_pwd != confirm_pwd:
                st.error("كلمة المرور الجديدة غير متطابقة.")
            else:
                success, msg = change_password(user['username'], old_pwd, new_pwd)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "التنقل الرئيسي",
    [
        "لوحة التحكم التنفيذية",
        "إدارة العملاء",
        "استخبارات الموردين",
        "المنتجات الكيميائية",
        "طلبات الشراء",
        "مقارنة العروض",
        "إدارة الصفقات",
        "متابعة الشحنات",
        "حاسبة التكلفة الواصلة",
        "مساعد GTI الاستراتيجي",
        "التحليلات والتقارير"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("GTI System v2.0 - Secured Enterprise")


# ==========================================
# 6. APPLICATION MODULES
# ==========================================

if menu == "لوحة التحكم التنفيذية":
    st.markdown("<div class='gti-page-title'>لوحة التحكم التنفيذية</div>", unsafe_allow_html=True)
    st.markdown("<div class='gti-page-subtitle'>مركز الأداء التجاري والعمليات اللوجستية العالمية</div>", unsafe_allow_html=True)
    
    customers_list = get_all_customers()
    suppliers_list = get_all_suppliers()
    products_list = get_all_products()
    deals_list = get_all_deals()
    shipments_list = get_all_shipments()

    active_shipments = [s for s in shipments_list if s['status'] != 'Cleared']
    total_deal_value = sum([d['deal_value'] for d in deals_list]) if deals_list else 0.0
    total_commission = sum([d['commission_amount'] for d in deals_list]) if deals_list else 0.0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">إجمالي قيمة الصفقات</div>
            <div class="kpi-val">${total_deal_value:,.0f}</div>
            <div class="kpi-trend trend-up">الأداء المالي</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">إجمالي العمولات</div>
            <div class="kpi-val">${total_commission:,.0f}</div>
            <div class="kpi-trend trend-up">الإيرادات المحققة</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">الشحنات النشطة</div>
            <div class="kpi-val">{len(active_shipments)}</div>
            <div class="kpi-trend trend-neutral">قيد التنفيذ</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">الشبكة التجارية</div>
            <div class="kpi-val">{len(customers_list)} / {len(suppliers_list)}</div>
            <div class="kpi-trend trend-neutral">عملاء / موردين</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='gti-section-title'>مركز العمليات والمخاطر (Operations & Risk Center)</div>", unsafe_allow_html=True)
    if active_shipments:
        for s in active_shipments:
            severity = "badge-attention" if s['status'] == "Delayed" else "badge-info"
            st.markdown(f"""
            <div style="background: white; border: 1px solid #E2E8F0; padding: 16px; border-radius: 8px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span class="status-badge {severity}" style="margin-left: 12px;">{s['status']}</span>
                    <strong style="color: #0F172A; font-size: 15px;">شحنة رقم {s['id']}</strong>
                    <span style="color: #64748B; font-size: 14px; margin-right: 8px;">• الحاوية: {s['container_number']} • العميل: {s['customer_name']}</span>
                </div>
                <div style="text-align: left; font-size: 13px; color: #64748B;">
                    وصول متوقع (ETA): <strong style="color: #0F172A;">{s['eta']}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge badge-success">جميع الشحنات في حالة ممتازة ومكتملة ولا توجد تنبيهات تأخير حالياً.</div>', unsafe_allow_html=True)

    st.markdown("<div class='gti-section-title'>أحدث الصفقات المسجلة</div>", unsafe_allow_html=True)
    if deals_list:
        st.dataframe(pd.DataFrame(deals_list), use_container_width=True)
    else:
        st.info("لا توجد صفقات مسجلة بعد في النظام.")


elif menu == "إدارة العملاء":
    st.markdown("<div class='gti-page-title'>إدارة العملاء (Customer Workspace)</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ إنشاء ملف عميل", "📋 قاعدة بيانات العملاء"])
    
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
            
            if st.form_submit_button("حفظ ملف العميل"):
                if company_name.strip():
                    c_id = add_customer(company_name, contact_person, email, phone, whatsapp, country, address)
                    st.success(f"تم إنشاء ملف العميل بنجاح! رقم المعرف: {c_id}")
                else:
                    st.error("يرجى إدخال اسم الشركة.")
                    
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


elif menu == "استخبارات الموردين":
    st.markdown("<div class='gti-page-title'>استخبارات الموردين (Supplier Intelligence)</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ تسجيل مورد جديد", "📋 سجل استخبارات الموردين"])
    
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
            rating = st.slider("مؤشر التقييم التجاري", 1.0, 5.0, 4.0, 0.1)
            notes = st.text_area("ملاحظات استخباراتية")
            
            if st.form_submit_button("اعتماد وحفظ المورد"):
                if company_name.strip():
                    s_id = add_supplier(company_name, country, city, contact_person, email, whatsapp, website, rating, notes)
                    st.success(f"تم تسجيل المورد بنجاح! رقم المعرف: {s_id}")
                else:
                    st.error("يرجى إدخال اسم شركة المورد.")
                    
    with tab2:
        suppliers = get_all_suppliers()
        if suppliers:
            st.dataframe(pd.DataFrame(suppliers), use_container_width=True)
        else:
            st.info("لا يوجد موردون مسجلون حالياً.")


elif menu == "المنتجات الكيميائية":
    st.markdown("<div class='gti-page-title'>المنتجات الكيميائية (Chemical Portfolio)</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ إضافة منتج جديد", "📋 دليل المنتجات الكيميائية"])
    
    with tab1:
        with st.form("add_product_form", clear_on_submit=True):
            trade_name = st.text_input("الاسم التجاري للمادة *")
            chemical_name = st.text_input("الاسم الكيميائي")
            col_a, col_b, col_c = st.columns(3)
            cas_number = col_a.text_input("CAS Number")
            hs_code = col_b.text_input("HS Code")
            un_number = col_c.text_input("UN Number")
            packaging = col_a.text_input("طريقة التعبئة")
            origin_country = col_b.text_input("بلد المنشأ")
            specifications = st.text_area("المواصفات الفنية التفصيلية")
            
            if st.form_submit_button("حفظ المنتج في المحفظة"):
                if trade_name.strip():
                    p_id = add_product(trade_name, chemical_name, cas_number, hs_code, un_number, specifications, packaging, origin_country)
                    st.success(f"تم إضافة المنتج بنجاح! رقم المعرف: {p_id}")
                else:
                    st.error("يرجى إدخال الاسم التجاري.")
                    
    with tab2:
        products = get_all_products()
        if products:
            st.dataframe(pd.DataFrame(products), use_container_width=True)
        else:
            st.info("لا توجد منتجات مسجلة حالياً.")


elif menu == "طلبات الشراء":
    st.markdown("<div class='gti-page-title'>طلبات الشراء (Purchase Requests)</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ تسجيل طلب شراء جديد", "📋 قائمة الطلبات الواردة"])
    
    customers = get_all_customers()
    products = get_all_products()
    
    with tab1:
        if not customers or not products:
            st.warning("يجب إضافة عميل ومنتج واحد على الأقل قبل تسجيل طلب شراء.")
        else:
            cust_dict = {c['company_name']: c['id'] for c in customers}
            prod_dict = {p['trade_name']: p['id'] for p in products}
            
            with st.form("add_request_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                selected_customer = col1.selectbox("اختر العميل *", list(cust_dict.keys()))
                selected_product = col2.selectbox("اختر المنتج *", list(prod_dict.keys()))
                
                col_a, col_b = st.columns(2)
                quantity = col_a.number_input("الكمية المطلوبة *", min_value=0.1, value=100.0, step=10.0)
                unit = col_b.selectbox("الوحدة القياسية", ["TON", "KG", "IBC", "DRUM", "CONTAINER"])
                
                col_c, col_d = st.columns(2)
                destination_country = col_c.text_input("الدولة الوجهة")
                destination_port = col_d.text_input("الميناء المستهدف")
                
                delivery_date = st.date_input("موعد التسليم المتوقع")
                specifications = st.text_area("المواصفات الخاصة وشروط الإمداد")
                
                if st.form_submit_button("تسجيل طلب الشراء"):
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
                    st.success(f"تم تسجيل طلب الشراء بنجاح! رقم الطلب: #{req_id}")

    with tab2:
        requests_list = get_all_purchase_requests()
        if requests_list:
            st.dataframe(pd.DataFrame(requests_list), use_container_width=True)
        else:
            st.info("لا توجد طلبات شراء مسجلة حالياً.")


elif menu == "مقارنة العروض":
    st.markdown("<div class='gti-page-title'>مركز قرار المشتريات (Procurement Decision Center)</div>", unsafe_allow_html=True)
    st.markdown("<div class='gti-page-subtitle'>مقارنة عروض أسعار الموردين واتخاذ القرار الاستراتيجي الأفضل</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([
        "📊 مصفوفة المقارنة التحليلية", 
        "➕ تسجيل عرض سعر جديد", 
        "📋 سجل عروض الأسعار"
    ])
    
    requests_list = get_all_purchase_requests()
    suppliers_list = get_all_suppliers()
    
    with tab1:
        if not requests_list:
            st.info("لا توجد طلبات شراء مسجلة لمقارنة عروضها حالياً.")
        else:
            req_options = {f"طلب #{r['id']} - العميل: {r['customer_name']} | المنتج: {r['product_name']} ({r['quantity']} {r['unit']})": r['id'] for r in requests_list}
            selected_req_label = st.selectbox("اختر طلب الشراء لعرض تحليل الموردين:", list(req_options.keys()))
            selected_req_id = req_options[selected_req_label]
            
            quotes = get_quotations_by_request(selected_req_id)
            st.divider()
            
            if not quotes:
                st.warning("لا توجد عروض أسعار مسجلة لهذا الطلب حتى الآن.")
            else:
                best_quote = min(quotes, key=lambda x: (x['unit_price'], -x['supplier_rating']))
                
                cols = st.columns(len(quotes) if len(quotes) <= 3 else 3)
                for i, quote in enumerate(quotes):
                    is_best = (quote['id'] == best_quote['id'])
                    with cols[i % 3]:
                        card_class = "quote-card quote-card-best" if is_best else "quote-card"
                        best_badge = "<div class='quote-best-badge'>الخيار الاستراتيجي الأفضل</div>" if is_best else ""
                        
                        st.markdown(f"""
                        <div class="{card_class}">
                            {best_badge}
                            <div style="font-size:18px; font-weight:700; color:#0F172A; margin-bottom:4px;">{quote['supplier_name']}</div>
                            <div style="font-size:12px; color:#64748B; margin-bottom:20px;">
                                <span class="status-badge badge-info">تقييم المورد: {quote['supplier_rating']}/5.0</span>
                                <span style="margin-right:8px;">{quote['supplier_country']}</span>
                            </div>
                            
                            <div class="quote-row">
                                <span class="quote-label">سعر الوحدة</span>
                                <span class="quote-value" style="font-size:18px;">${quote['unit_price']:,.2f} <span style="font-size:11px; font-weight:normal;">{quote['currency']}</span></span>
                            </div>
                            <div class="quote-row">
                                <span class="quote-label">شرط التسليم</span>
                                <span class="quote-value">{quote['incoterms']}</span>
                            </div>
                            <div class="quote-row">
                                <span class="quote-label">فترة التوريد</span>
                                <span class="quote-value">{quote['production_lead_time']}</span>
                            </div>
                            <div class="quote-row">
                                <span class="quote-label">شروط الدفع</span>
                                <span class="quote-value">{quote['payment_terms']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

    with tab2:
        if not requests_list or not suppliers_list:
            st.warning("يجب وجود طلب شراء ومورد واحد على الأقل لتسجيل عرض سعر.")
        else:
            req_dict = {f"طلب #{r['id']} - {r['customer_name']} ({r['product_name']})": r['id'] for r in requests_list}
            supp_dict = {s['company_name']: s['id'] for s in suppliers_list}
            
            with st.form("add_quotation_form_tab2", clear_on_submit=True):
                selected_req = st.selectbox("اختر طلب الشراء *", list(req_dict.keys()))
                selected_supp = st.selectbox("اختر المورد *", list(supp_dict.keys()))
                
                col_a, col_b = st.columns(2)
                unit_price = col_a.number_input("سعر الوحدة *", min_value=0.01, value=500.0, step=10.0)
                currency = col_b.selectbox("العملة", ["USD", "EUR", "CNY", "SAR"])
                
                col_c, col_d = st.columns(2)
                incoterms = col_c.selectbox("شرط التسليم (Incoterms)", ["FOB", "CIF", "CFR", "EXW", "DDP"])
                production_lead_time = col_d.text_input("مدة الإنتاج (مثال: 15 يوماً)")
                
                payment_terms = st.text_input("شروط الدفع (مثال: 30% Advance, 70% LC)")
                
                if st.form_submit_button("حفظ عرض السعر"):
                    q_id = add_quotation(
                        request_id=req_dict[selected_req],
                        supplier_id=supp_dict[selected_supp],
                        unit_price=unit_price,
                        currency=currency,
                        production_lead_time=production_lead_time,
                        payment_terms=payment_terms,
                        incoterms=incoterms
                    )
                    st.success(f"تم تسجيل عرض السعر بنجاح! رقم المعرف: #{q_id}")

    with tab3:
        all_q = get_all_quotations()
        if all_q:
            st.dataframe(pd.DataFrame(all_q), use_container_width=True)
        else:
            st.info("لا توجد عروض أسعار مسجلة حالياً.")


elif menu == "إدارة الصفقات":
    st.markdown("<div class='gti-page-title'>إدارة الصفقات والعمولات (Deal Workspace)</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ إغلاق صفقة جديدة", "📋 قائمة الصفقات والتصدير"])
    
    requests_list = get_all_purchase_requests()
    suppliers_list = get_all_suppliers()
    customers_list = get_all_customers()
    quotations_list = get_all_quotations()
    
    with tab1:
        if not requests_list or not quotations_list:
            st.warning("يجب تسجيل طلب شراء وعرض سعر واحد على الأقل قبل إنشاء صفقة.")
        else:
            req_dict = {f"طلب #{r['id']} - العميل: {r['customer_name']} | المنتج: {r['product_name']}": r['id'] for r in requests_list}
            supp_dict = {s['company_name']: s['id'] for s in suppliers_list}
            cust_dict = {c['company_name']: c['id'] for c in customers_list}
            
            with st.form("create_deal_form", clear_on_submit=True):
                selected_req_label = st.selectbox("طلب الشراء المرتبط *", list(req_dict.keys()))
                selected_req_id = req_dict[selected_req_label]
                
                col_a, col_b = st.columns(2)
                selected_cust_name = col_a.selectbox("العميل المشتري *", list(cust_dict.keys()))
                selected_supp_name = col_b.selectbox("المورد المعتمد *", list(supp_dict.keys()))
                
                col_c, col_d = st.columns(2)
                deal_value = col_c.number_input("القيمة الإجمالية للصفقة ($) *", min_value=1.0, value=10000.0, step=500.0)
                commission_rate = col_d.number_input("نسبة عمولة الشركة (%) *", min_value=0.1, max_value=50.0, value=5.0, step=0.5)
                
                est_commission = deal_value * (commission_rate / 100.0)
                st.info(f"حسابات معاينة الصفقة: قيمة العمولة المتوقعة = ${est_commission:,.2f}")
                
                if st.form_submit_button("إغلاق وحفظ الصفقة"):
                    quotation_id = quotations_list[0]['id'] if quotations_list else 1
                    deal_id = create_deal(
                        request_id=selected_req_id,
                        quotation_id=quotation_id,
                        customer_id=cust_dict[selected_cust_name],
                        supplier_id=supp_dict[selected_supp_name],
                        deal_value=deal_value,
                        commission_rate=commission_rate
                    )
                    st.success(f"تم تسجيل الصفقة بنجاح! رقم الصفقة المرجعي: #{deal_id}")

    with tab2:
        deals = get_all_deals()
        if deals:
            total_deals_val = sum(d['deal_value'] for d in deals)
            total_comm_val = sum(d['commission_amount'] for d in deals)
            
            m1, m2, m3 = st.columns(3)
            m1.metric("إجمالي الصفقات", f"{len(deals)}")
            m2.metric("إجمالي قيمة الصفقات", f"${total_deals_val:,.2f}")
            m3.metric("إجمالي العمولات", f"${total_comm_val:,.2f}")
            
            st.divider()
            st.dataframe(pd.DataFrame(deals), use_container_width=True)
            
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                excel_file = export_to_excel(deals, sheet_name="Deals_Summary")
                st.download_button(
                    label="📥 تنزيل كافة الصفقات (Excel)",
                    data=excel_file,
                    file_name="GTI_Deals_Summary.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
            with col_exp2:
                deal_ids = [d['id'] for d in deals]
                selected_deal_id = st.selectbox("اختر رقم الصفقة لتصدير PDF/البريد:", deal_ids)
                selected_deal_data = next((d for d in deals if d['id'] == selected_deal_id), None)
                
                if selected_deal_data:
                    pdf_file = generate_deal_pdf(selected_deal_data)
                    st.download_button(
                        label=f"📄 تنزيل تقرير الصفقة #{selected_deal_id} (PDF)",
                        data=pdf_file,
                        file_name=f"GTI_Deal_Report_{selected_deal_id}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    target_email = st.text_input("البريد الإلكتروني للمستلم:", value="client@example.com")
                    if st.button("📧 إرسال تقرير الصفقة إلكترونياً", use_container_width=True):
                        email_body = f"<h3>مرفق لكم تقرير ملخص الصفقة الرسمية #{selected_deal_id}</h3><p>شكراً لتعاملكم مع GTI.</p>"
                        success, msg = send_email(
                            to_email=target_email,
                            subject=f"GTI - Official Deal Report #{selected_deal_id}",
                            body_html=email_body,
                            attachment_bytes=pdf_file,
                            attachment_filename=f"GTI_Deal_Report_{selected_deal_id}.pdf"
                        )
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)
        else:
            st.info("لا توجد صفقات مسجلة حالياً.")


elif menu == "متابعة الشحنات":
    st.markdown("<div class='gti-page-title'>متابعة الشحنات والعمليات اللوجستية (Shipment Control Center)</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ تسجيل شحنة جديدة", "📋 تتبع الشحنات القائمة"])
    
    deals_list = get_all_deals()
    
    with tab1:
        if not deals_list:
            st.warning("يجب إنشاء صفقة واحدة على الأقل قبل تسجيل شحنة جديدة.")
        else:
            deal_dict = {f"صفقة #{d['id']} - القيمة: ${d['deal_value']:,.2f}": d['id'] for d in deals_list}
            
            with st.form("add_shipment_form", clear_on_submit=True):
                selected_deal = st.selectbox("الصفقة المرتبطة *", list(deal_dict.keys()))
                
                col_a, col_b = st.columns(2)
                shipping_company = col_a.text_input("شركة الشحن")
                container_number = col_b.text_input("رقم الحاوية (Container No.)")
                
                col_c, col_d = st.columns(2)
                bill_of_lading = col_c.text_input("رقم بوليصة الشحن (B/L)")
                status = col_d.selectbox("الحالة الحالية", ["Preparing", "On Board", "Arrived", "Cleared"])
                
                col_e, col_f = st.columns(2)
                loading_port = col_e.text_input("ميناء التحميل")
                discharge_port = col_f.text_input("ميناء التفريغ")
                
                col_g, col_h = st.columns(2)
                etd = col_g.date_input("تاريخ المغادرة (ETD)")
                eta = col_h.date_input("تاريخ الوصول (ETA)")
                
                if st.form_submit_button("تسجيل الشحنة اللوجستية"):
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
                    st.success(f"تم تسجيل الشحنة بنجاح! رقم المتابعة: #{shipment_id}")

    with tab2:
        shipments = get_all_shipments()
        if shipments:
            st.dataframe(pd.DataFrame(shipments), use_container_width=True)
            
            st.divider()
            col_sel, col_stat = st.columns(2)
            s_ids = [s['id'] for s in shipments]
            selected_s_id = col_sel.selectbox("اختر رقم الشحنة لتحديث حالتها:", s_ids)
            new_s_status = col_stat.selectbox("الحالة الجديدة:", ["Preparing", "On Board", "Arrived", "Cleared"])
            
            if st.button("تحديث حالة الشحنة"):
                update_shipment_status(selected_s_id, new_s_status)
                st.success(f"تم تحديث حالة الشحنة #{selected_s_id} إلى ({new_s_status}) بنجاح!")
                st.rerun()
        else:
            st.info("لا توجد شحنات مسجلة حالياً.")


elif menu == "حاسبة التكلفة الواصلة":
    st.markdown("<div class='gti-page-title'>حاسبة التكلفة الواصلة (Landed Cost & Profitability)</div>", unsafe_allow_html=True)
    st.markdown("<div class='gti-page-subtitle'>نمذجة مالية حية لتكاليف الاستيراد وتسعير المبيعات</div>", unsafe_allow_html=True)
    
    col_input, col_results = st.columns([1.2, 1])
    
    with col_input:
        st.markdown("<div class='kpi-card' style='padding: 24px;'>", unsafe_allow_html=True)
        st.markdown("<div class='gti-section-title' style='margin-top:0;'>الافتراضات التجارية وسعر المصنع</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        quantity = c1.number_input("الكمية (طن MT)", value=100.0, step=10.0)
        exw_price = c2.number_input("سعر المصنع ($ EXW/FOB)", value=850.0, step=10.0)
        
        st.markdown("<div class='gti-section-title'>اللوجستيات والشحن البحري</div>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        freight = c3.number_input("إجمالي الشحن البحري ($)", value=1800.0, step=100.0)
        insurance = c4.number_input("التأمين ($)", value=150.0)
        
        st.markdown("<div class='gti-section-title'>الرسوم المحلية والجمارك</div>", unsafe_allow_html=True)
        c5, c6 = st.columns(2)
        duty = c5.number_input("نسبة الجمارك (%)", value=5.0, step=0.5)
        transport = c6.number_input("النقل الداخلي ($)", value=400.0)
        c7, c8 = st.columns(2)
        port_fees = c7.number_input("رسوم الميناء ($)", value=300.0)
        admin = c8.number_input("مصاريف إدارية ($)", value=200.0)
        
        st.markdown("<div class='gti-section-title'>المستهدف التجاري</div>", unsafe_allow_html=True)
        margin = st.slider("هامش الربح المستهدف (%)", 1.0, 40.0, 15.0)
        st.markdown("</div>", unsafe_allow_html=True)
        
    res = calculate_landed_cost(
        exw_fob_unit_price=exw_price, quantity=quantity, sea_freight=freight,
        insurance=insurance, customs_duty_percent=duty, inland_transport=transport,
        storage_port_fees=port_fees, admin_expenses=admin, desired_margin_percent=margin
    )
    
    with col_results:
        st.markdown(f"""
        <div class="financial-panel">
            <h3 style="color: #F1F4F7; font-size: 20px; font-weight: 600; margin-top: 0; margin-bottom: 32px;">الملخص المالي النهائي</h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
                <div>
                    <div class="fin-label">إجمالي التكلفة الواصلة</div>
                    <div class="fin-value">${res['total_landed_cost']:,.2f}</div>
                </div>
                <div>
                    <div class="fin-label">التكلفة الواصلة / طن</div>
                    <div class="fin-value fin-value-accent">${res['cost_per_ton']:,.2f}</div>
                </div>
            </div>
            
            <div class="fin-divider"></div>
            
            <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 16px; margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <span style="color: #94A3B8; font-size: 14px;">قيمة الجمارك المقدرة</span>
                    <span style="color: #FFFFFF; font-weight: 600;">${res['customs_amount']:,.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94A3B8; font-size: 14px;">الهامش المستهدف</span>
                    <span style="color: #FFFFFF; font-weight: 600;">{margin}%</span>
                </div>
            </div>
            
            <div style="background: #15803D; border-radius: 8px; padding: 20px;">
                <div class="fin-label" style="color: #BBF7D0;">سعر البيع المقترح / طن</div>
                <div class="fin-value" style="margin-bottom: 16px;">${res['suggested_price_per_ton']:,.2f}</div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 16px;">
                    <span style="color: #BBF7D0; font-size: 14px; font-weight: 600;">صافي الربح المتوقع</span>
                    <span style="background: white; color: #15803D; padding: 4px 12px; border-radius: 4px; font-weight: 700; font-size: 16px;">${res['expected_profit']:,.2f}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


elif menu == "مساعد GTI الاستراتيجي":
    st.markdown("<div class='gti-page-title'>مساعد GTI للاستخبارات والقرار الذكي</div>", unsafe_allow_html=True)
    st.markdown("<div class='gti-page-subtitle'>محرك تحليلي متقدم لتقييم الموردين، الهوامش، والمحاكاة اللوجستية</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🎯 استخبارات الموردين والمنتجات", "📉 محاكاة حساسية الشحن البحري"])
    
    products_list = get_all_products()
    deals_list = get_all_deals()
    
    with tab1:
        if not products_list:
            st.warning("يرجى إضافة منتجات وعروض أسعار أولاً لتشغيل التحليل الاستراتيجي.")
        else:
            p_dict = {p['trade_name']: p['id'] for p in products_list}
            selected_prod_name = st.selectbox("اختر المنتج الكيميائي للتحليل:", list(p_dict.keys()))
            
            if st.button("تشغيل تحليل المورد الأفضل"):
                answer = ask_gti_ai("best_supplier", {"product_id": p_dict[selected_prod_name]})
                st.markdown(answer)
                
    with tab2:
        if not deals_list:
            st.warning("لا توجد صفقات حالية للمحاكاة.")
        else:
            deal_options = {f"صفقة #{d['id']} - القيمة: ${d['deal_value']:,.2f}": d for d in deals_list}
            selected_d_label = st.selectbox("اختر الصفقة المستهدفة:", list(deal_options.keys()))
            selected_d = deal_options[selected_d_label]
            
            shipping_inc = st.slider("نسبة الزيادة المتوقعة في أسعار الشحن (%)", 1.0, 50.0, 15.0, 1.0)
            
            if st.button("تشغيل سيناريو محاكاة المخاطر"):
                answer = ask_gti_ai("shipping_sensitivity", {
                    "deal_value": selected_d['deal_value'],
                    "current_profit": selected_d['net_profit'],
                    "increase_pct": shipping_inc
                })
                st.markdown(answer)


elif menu == "التحليلات والتقارير":
    st.markdown("<div class='gti-page-title'>التحليلات الإحصائية وتقارير الذكاء التجاري</div>", unsafe_allow_html=True)
    
    summary = get_analytics_summary()
    
    col1, col2 = st.columns(2)
    col1.metric("متوسط نسبة العمولة للشركة", f"{summary['avg_commission_rate']:.2f}%")
    col2.metric("متوسط قيمة الصفقات", f"${summary['avg_deal_value']:,.2f}")
    
    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='gti-section-title'>المنتجات الأكثر طلباً</div>", unsafe_allow_html=True)
        if summary['top_products']:
            st.dataframe(pd.DataFrame(summary['top_products']), use_container_width=True)
        else:
            st.info("لا توجد بيانات كافية حول طلبات المنتجات.")
            
    with col_b:
        st.markdown("<div class='gti-section-title'>الموردون الأبرز تقييماً</div>", unsafe_allow_html=True)
        if summary['top_suppliers']:
            st.dataframe(pd.DataFrame(summary['top_suppliers']), use_container_width=True)
        else:
            st.info("لا توجد بيانات كافية حول الموردين.")