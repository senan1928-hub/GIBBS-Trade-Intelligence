import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_deal_pdf(deal_info):
    """
    إنشاء ملخص صفقة رسمية بملف PDF احترافي
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    story = []

    # 1. العنوان الرئيسي
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1, # Center
        spaceAfter=20
    )
    story.append(Paragraph("GIBBS Trade Intelligence", title_style))
    story.append(Paragraph("Official Deal Summary Report", styles['Heading2']))
    story.append(Spacer(1, 15))

    # 2. بناء بيانات الجدول
    table_data = [
        ["Field Description", "Value"],
        ["Deal ID", f"#{deal_info.get('id', 'N/A')}"],
        ["Customer ID", str(deal_info.get('customer_id', 'N/A'))],
        ["Supplier ID", str(deal_info.get('supplier_id', 'N/A'))],
        ["Total Deal Value", f"${deal_info.get('deal_value', 0):,.2f}"],
        ["Commission Rate", f"{deal_info.get('commission_rate', 0)}%"],
        ["Commission Amount", f"${deal_info.get('commission_amount', 0):,.2f}"],
        ["Net Profit", f"${deal_info.get('net_profit', 0):,.2f}"],
        ["Deal Status", str(deal_info.get('status', 'In Progress'))],
        ["Created Date", str(deal_info.get('created_at', 'N/A'))]
    ]

    t = Table(table_data, colWidths=[200, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 30))
    story.append(Paragraph("Generated automatically by GTI System", styles['Italic']))

    doc.build(story)
    buffer.seek(0)
    return buffer