import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email(to_email, subject, body_html, attachment_bytes=None, attachment_filename="Report.pdf", smtp_config=None):
    """
    إرسال بريد إلكتروني احترافي تلقائياً مع إمكانية إرفاق ملفات PDF
    
    :param to_email: البريد الإلكتروني المستهدف (مورد أو عميل)
    :param subject: عنوان الرسالة
    :param body_html: نص الرسالة بتنسيق HTML
    :param attachment_bytes: ملف المرفق في الذاكرة (BytesIO)
    :param attachment_filename: اسم ملف المرفق
    :param smtp_config: قاموس يحتوي على إعدادات الخادم (Host, Port, Email, Password)
    """
    
    # 1. إذا لم تتوفر إعدادات SMTP حقيقية، نقوم بمحاكاة الإرسال (Simulation Mode)
    if not smtp_config or not smtp_config.get("smtp_server"):
        print("\n📧 [حالة محاكاة الإرسال - Simulation Mode]")
        print(f"📩 إلى: {to_email}")
        print(f"📌 الموضوع: {subject}")
        print(f"📎 المرفقات: {attachment_filename if attachment_bytes else 'بدون مرفقات'}")
        print("✅ تم إرسال البريد إفتراضياً بنجاح! (ربط SMTP الحقيقي جاهز عند إدخال البيانات)\n")
        return True, "تم إرسال البريد في وضع المحاكاة بنجاح!"

    # 2. الإرسال الفعلي عبر سيرفر SMTP
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_config.get("sender_email")
        msg['To'] = to_email
        msg['Subject'] = subject

        # إضافة نص الرسالة HTML
        msg.attach(MIMEText(body_html, 'html'))

        # إضافة المرفق إن وجد
        if attachment_bytes:
            part = MIMEApplication(attachment_bytes.getvalue(), Name=attachment_filename)
            part['Content-Disposition'] = f'attachment; filename="{attachment_filename}"'
            msg.attach(part)

        # الاتصال بالسيرفر والإرسال
        server = smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port'])
        server.starttls()
        server.login(smtp_config['sender_email'], smtp_config['sender_password'])
        server.send_message(msg)
        server.quit()
        
        return True, f"تم إرسال البريد الإلكتروني بنجاح إلى {to_email}"
        
    except Exception as e:
        return False, f"فشل إرسال البريد الإلكتروني: {str(e)}"


def generate_rfq_email_template(supplier_name, product_name, quantity, unit):
    """
    توليد قالب بريد إلكتروني أنيق لطلب عرض سعر (RFQ) موجه للمورد
    """
    html_content = f"""
    <div style="direction: rtl; font-family: Arial, sans-serif; padding: 20px; border: 1px solid #E5E7EB; border-radius: 8px;">
        <h2 style="color: #1E3A8A;">GIBBS Trade Intelligence</h2>
        <p>عزيزنا المورد <b>{supplier_name}</b>،</p>
        <p>تحية طيبة وبعد،،</p>
        <p>يرجى التكرم بتزويدنا بأفضل عرض سعر متاح للمادة التالية وفقاً للمواصفات أدناه:</p>
        
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr style="background-color: #F8FAFC;">
                <td style="padding: 10px; border: 1px solid #CBD5E1;"><b>المنتج المطلوبة:</b></td>
                <td style="padding: 10px; border: 1px solid #CBD5E1;">{product_name}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #CBD5E1;"><b>الكمية المطلوبة:</b></td>
                <td style="padding: 10px; border: 1px solid #CBD5E1;">{quantity} {unit}</td>
            </tr>
        </table>
        
        <p>يرجى تضمين شروط التسليم (Incoterms)، مدة الإنتاج، وشروط الدفع المتاحة لديك.</p>
        <p>شاكرين ومقدرين حسن تعاونكم معنا.</p>
        <hr style="border: 0; border-top: 1px solid #E5E7EB;">
        <p style="font-size: 12px; color: #64748B;">تم إرسال هذا البريد تلقائياً عبر نظام GTI الذكي.</p>
    </div>
    """
    return html_content