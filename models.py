from connection import get_connection
def create_tables():
    """إنشاء جميع جداول قاعدة البيانات والعلاقات بينها إذا لم تكن موجودة"""
    
    queries = [
        # 1. جدول المستخدمين (Users)
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'Admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,

        # 2. جدول العملاء (Customers)
        """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            contact_person TEXT,
            email TEXT,
            phone TEXT,
            whatsapp TEXT,
            country TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,

        # 3. جدول الموردين (Suppliers)
        """
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            country TEXT,
            city TEXT,
            contact_person TEXT,
            email TEXT,
            whatsapp TEXT,
            website TEXT,
            rating REAL DEFAULT 0.0,
            response_speed TEXT,
            quality_rating TEXT,
            production_lead_time TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,

        # 4. جدول المنتجات الكيميائية (Products)
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trade_name TEXT NOT NULL,
            chemical_name TEXT,
            cas_number TEXT,
            hs_code TEXT,
            un_number TEXT,
            specifications TEXT,
            packaging TEXT,
            origin_country TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,

        # 5. جدول طلبات الشراء (Purchase Requests)
        """
        CREATE TABLE IF NOT EXISTS purchase_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT DEFAULT 'TON',
            specifications TEXT,
            delivery_date DATE,
            destination_country TEXT,
            destination_port TEXT,
            status TEXT DEFAULT 'New', -- New, In Progress, Quoted, Closed, Cancelled
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
        );
        """,

        # 6. جدول عروض أسعار الموردين (Quotations / RFQs)
        """
        CREATE TABLE IF NOT EXISTS quotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            supplier_id INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            currency TEXT DEFAULT 'USD',
            production_lead_time TEXT,
            payment_terms TEXT,
            incoterms TEXT, -- FOB, CIF, EXW, etc.
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES purchase_requests (id) ON DELETE CASCADE,
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id) ON DELETE CASCADE
        );
        """,

        # 7. جدول الصفقات (Deals)
        """
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            quotation_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            supplier_id INTEGER NOT NULL,
            deal_value REAL NOT NULL,
            commission_rate REAL DEFAULT 0.0,
            commission_amount REAL DEFAULT 0.0,
            net_profit REAL DEFAULT 0.0,
            status TEXT DEFAULT 'In Progress', -- In Progress, Shipped, Completed, Cancelled
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES purchase_requests (id),
            FOREIGN KEY (quotation_id) REFERENCES quotations (id),
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
        );
        """,

        # 8. جدول الشحنات (Shipments)
        """
        CREATE TABLE IF NOT EXISTS shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deal_id INTEGER NOT NULL,
            shipping_company TEXT,
            container_number TEXT,
            bill_of_lading TEXT,
            etd DATE, -- Estimated Time of Departure
            eta DATE, -- Estimated Time of Arrival
            loading_port TEXT,
            discharge_port TEXT,
            status TEXT DEFAULT 'Preparing', -- Preparing, On Board, Arrived, Cleared
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (deal_id) REFERENCES deals (id) ON DELETE CASCADE
        );
        """,

        # 9. جدول المستندات (Documents)
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deal_id INTEGER,
            document_type TEXT NOT NULL, -- Quotation, PO, Invoice, BL, SDS, COA
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (deal_id) REFERENCES deals (id) ON DELETE CASCADE
        );
        """,

        # 10. جدول إعدادات النظام (Settings)
        """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            description TEXT
        );
        """
    ]

    with get_connection() as conn:
        cursor = conn.cursor()
        for query in queries:
            cursor.execute(query)
        conn.commit()
    
    print("✅ تم إنشاء جميع جداول قاعدة البيانات بنجاح مع العلاقات والمرجعيات!")

if __name__ == "__main__":
    create_tables()