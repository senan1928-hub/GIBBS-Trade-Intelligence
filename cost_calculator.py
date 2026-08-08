def calculate_landed_cost(
    exw_fob_unit_price,
    quantity,
    sea_freight=0.0,
    insurance=0.0,
    customs_duty_percent=5.0,
    inland_transport=0.0,
    storage_port_fees=0.0,
    admin_expenses=0.0,
    desired_margin_percent=15.0
):
    """
    حاسبة احترافية لحساب تكلفة الاستيراد الواصلة (Landed Cost) وسعر البيع المقترح.
    
    المعادلات المالية المستخدمة:
    1. CIF Value = Total Factory Price + Sea Freight + Insurance
    2. Customs Duty = CIF Value * (Customs % / 100)
    3. Total Landed Cost = Total Factory Price + Freight + Insurance + Customs + Inland + Storage + Admin
    4. Cost per Ton = Total Landed Cost / Quantity
    5. Cost per KG = Cost per Ton / 1000
    6. Suggested Total Selling Price = Total Landed Cost / (1 - Margin % / 100)
    """
    raw_material_total = exw_fob_unit_price * quantity
    cif_value = raw_material_total + sea_freight + insurance
    customs_amount = cif_value * (customs_duty_percent / 100.0)
    
    # التكلفة الإجمالية الواصلة
    total_landed_cost = (
        raw_material_total + 
        sea_freight + 
        insurance + 
        customs_amount + 
        inland_transport + 
        storage_port_fees + 
        admin_expenses
    )
    
    # تكلفة الطن والكيلو
    cost_per_ton = total_landed_cost / quantity if quantity > 0 else 0.0
    cost_per_kg = cost_per_ton / 1000.0 if quantity > 0 else 0.0
    
    # حساب سعر البيع المقترح والربح المستهدف
    if desired_margin_percent < 100:
        suggested_selling_price_total = total_landed_cost / (1 - (desired_margin_percent / 100.0))
    else:
        suggested_selling_price_total = total_landed_cost * (1 + (desired_margin_percent / 100.0))
        
    suggested_price_per_ton = suggested_selling_price_total / quantity if quantity > 0 else 0.0
    expected_profit = suggested_selling_price_total - total_landed_cost
    
    return {
        "raw_material_total": raw_material_total,
        "cif_value": cif_value,
        "customs_amount": customs_amount,
        "total_landed_cost": total_landed_cost,
        "cost_per_ton": cost_per_ton,
        "cost_per_kg": cost_per_kg,
        "suggested_selling_price_total": suggested_selling_price_total,
        "suggested_price_per_ton": suggested_price_per_ton,
        "expected_profit": expected_profit,
        "desired_margin_percent": desired_margin_percent
    }