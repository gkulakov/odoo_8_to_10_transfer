# -*- coding: utf-8 -*-
from model import tbl_odoo8 as tbl8
from model import tbl_odoo10 as tbl10
from model.database import logger


def do_sales_transfer(session1, session2):
    """
    Перенос заказов продаж
    """
    session2.execute('''
    BEGIN;
    
    -- CHANGE "NULLABLE" OF "FIELD "product_id" --------------------
    ALTER TABLE "public"."sale_order_line" 
    ALTER COLUMN "product_id" DROP NOT NULL;
    -- -------------------------------------------------------------
    
    COMMIT;
    ''')
    session2.commit()

    company_dict = {
        x: session2.query(tbl10.res_company.id).filter(
            tbl10.res_company.name.like(name)
        ).first()[0]
        for x, name
        in session1.query(tbl8.res_company.id, tbl8.res_company.name).all()
    }

    user_dict = {
        x: session2.query(tbl10.res_users.id).filter(
            tbl10.res_users.login.like(name)
        ).first()[0]
        for x, name
        in session1.query(tbl8.res_users.id, tbl8.res_users.login).all()
    }

    team_dict = {
        x: session2.query(tbl10.crm_team.id).filter(
            tbl10.crm_team.name.like(name)
        ).first()[0]
        for x, name
        in session1.query(tbl8.crm_case_section.id,
                          tbl8.crm_case_section.complete_name).all()
    }
    records = session1.query(tbl8.sale_order) \
        .filter(tbl8.sale_order.state.notin_(['draft','cancel'])) \
        .all()

    for rec in records:
        so = tbl10.sale_order()
        so.name = rec.name
        so.partner_id = session2.query(tbl10.res_partner.id).filter(
            tbl10.res_partner.id_ == rec.partner_id
        ).first()[0]
        so.partner_invoice_id = so.partner_id
        so.partner_shipping_id = so.partner_id
        if rec.entity_for_proc:
            so.entity_for_proc = session2.query(tbl10.sintez_legal_entity.id).filter(
            tbl10.sintez_legal_entity.name == rec.legal_entity.name
        ).first()[0]
        so.matching_scheme_date = rec.matching_scheme_date
        so.required_shipment_date = rec.contract_shipment_date
        so.shipment_date = rec.shipment_date
        if rec.warehouse_id:
            so.warehouse_id = session2.query(tbl10.stock_warehouse.id).filter(
                tbl10.stock_warehouse.code.like(rec.warehouse.code)
            ).first()[0]
        so.picking_policy = rec.picking_policy
        if rec.user_id:
            so.user_id = user_dict[rec.user_id]
        if rec.section_id:
            so.team_id = team_dict[rec.section_id]
        if rec.company_id:
            so.company_id = company_dict[rec.company_id]
        so.origin = rec.origin
        so.create_date = rec.create_date
        so.date_order = rec.date_order
        so.note = rec.note
        so.amount_untaxed = rec.amount_untaxed
        so.amount_tax = rec.amount_tax
        so.amount_total = rec.amount_total
        so.state = 'done'
        so.message_last_post = rec.message_last_post
        so.pricelist_id = 1
        so.confirmation_date = rec.date_confirm
        so.write_date = rec.write_date
        so.picking_policy = rec.picking_policy
        so.shipped = rec.shipped

        session2.add(so)
        session2.flush()

        for sol in rec.so_lines:
            if sol.state in ['confirmed', 'done']:
                new_sol = tbl10.sale_order_line()
                new_sol.product_id = None
                new_sol.product_uom_qty = sol.product_uom_qty
                new_sol.qty_delivered = sol.product_uom_qty
                new_sol.qty_invoiced = sol.product_uom_qty
                new_sol.price_unit = sol.price_unit
                new_sol.price_subtotal = sol.price_unit * sol.product_uom_qty
                new_sol.price_total = new_sol.price_subtotal
                new_sol.name = sol.name
                new_sol.customer_lead = 0.0
                new_sol.product_uom = sol.product_uom
                new_sol.currency_id = 31
                new_sol.qty_to_invoice = 0.0
                new_sol.customer_lead = 0.0
                new_sol.price_tax = 0.0
                new_sol.state = 'sale'
                new_sol.order_partner_id = so.partner_id
                new_sol.discount = 0.0
                new_sol.salesman_id = so.user_id
                new_sol.invoice_status = 'invoiced'
                new_sol.price_reduce_taxexcl = sol.price_unit
                new_sol.price_reduce_taxinc = sol.price_unit
                new_sol.price_reduce = sol.price_unit

                new_sol.order_id = so.id
                session2.add(new_sol)

    session2.commit()
    logger.info("Sales transfer compete.")