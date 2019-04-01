# -*- coding: utf-8 -*-
from model import tbl_odoo8 as tbl8
from model import tbl_odoo10 as tbl10
from model.database import logger


def do_product_template_transfer(session1, session2):
    """
    Теперь переносим шаблоны товаров
    """
    session2.execute('''
    DO $$
    BEGIN
        BEGIN
            ALTER TABLE public.product_template ADD COLUMN id_ INT;
        EXCEPTION
            WHEN duplicate_column 
            THEN RAISE NOTICE 'column id_ already exists in product_template.';
        END;
    END;
    $$
    ''')
    session2.commit()

    company_dict = {
        x: session2.query(tbl10.res_company.id).filter(
            tbl10.res_company.name.like(name)
        ).first()[0]
        for x, name
        in session1.query(tbl8.res_company.id, tbl8.res_company.name).all()
    }

    supp = session2.query(tbl10.res_partner.id) \
        .filter(tbl10.res_partner.name.like("Поставщик по умолчанию")) \
        .first()[0]

    records = session1.query(tbl8.product_template) \
        .filter(tbl8.product_template.active.is_(True)) \
        .all()

    for rec in records:
        prod_tmp = tbl10.product_template()
        prod_tmp.id_ = rec.id
        prod_tmp.name = rec.name
        prod_tmp.active = rec.active
        prod_tmp.create_date = rec.create_date
        prod_tmp.write_date = rec.write_date
        prod_tmp.sale_ok = rec.sale_ok
        prod_tmp.purchase_ok = rec.purchase_ok
        prod_tmp.can_be_expensed = rec.hr_expense_ok
        prod_tmp.type = rec.type
        prod_tmp.categ_id = 1  # All
        prod_tmp.list_price = 0.0
        if rec.company_id:
            prod_tmp.company_id = company_dict[rec.company_id]
        prod_tmp.uom_id = rec.uom_id
        prod_tmp.uom_po_id = rec.uom_po_id
        prod_tmp.purchase_method = 'purchase'
        prod_tmp.purchase_requisition = 'rfq'
        prod_tmp.invoice_policy = 'order'
        prod_tmp.sale_line_warn = 'no-message'
        prod_tmp.purchase_line_warn = 'no-message'
        prod_tmp.tracking = 'none'
        prod_tmp.weight = 0.0
        prod_tmp.volume = 0
        prod_tmp.rental = False
        prod_tmp.track_service = 'manual'
        prod_tmp.expense_policy = 'no'
        prod_tmp.sale_delay = 0
        prod_tmp.produce_delay = 0
        prod_tmp.warranty = 0
        prod_tmp.sequence = 1

        session2.add(prod_tmp)
        session2.flush()

        prod_prod = tbl10.product_product()
        prod_prod.product_tmpl_id = prod_tmp.id
        prod_prod.active = True

        session2.add(prod_prod)

        prod_supp = tbl10.product_supplierinfo()
        prod_supp.company_id = prod_tmp.company_id
        prod_supp.currency_id = 31  # Rub
        prod_supp.delay = 0
        prod_supp.min_qty = 0.0
        prod_supp.name = supp
        prod_supp.price = 0.0
        prod_supp.product_tmpl_id = prod_tmp.id

        session2.add(prod_supp)

        prod_route1 = tbl10.stock_route_product()
        prod_route1.product_id = prod_tmp.id
        prod_route1.route_id = 1  # Make To Order

        session2.add(prod_route1)

        prod_route2 = tbl10.stock_route_product()
        prod_route2.product_id = prod_tmp.id
        prod_route2.route_id = 5  # Buy

        session2.add(prod_route2)

    session2.commit()
    logger.info("Products transfer compete.")

