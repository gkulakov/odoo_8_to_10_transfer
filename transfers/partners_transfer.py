# -*- coding: utf-8 -*-
from model import tbl_odoo8 as tbl8
from model import tbl_odoo10 as tbl10
from model.database import logger
from sqlalchemy import or_


def do_partners_transfer(session1, session2):
    """
    Перенос клиентов без контактов
    """

    session2.execute('''
    DO $$
        BEGIN
            BEGIN
                ALTER TABLE public.res_partner ADD COLUMN id_ INT;
            EXCEPTION
                WHEN duplicate_column THEN RAISE NOTICE 'column id_ already exists in res_partner.';
            END;
        END;
    $$
    ''')
    session2.commit()

    session2.execute('''
    BEGIN;

    ALTER TABLE "public"."res_partner" 
    ALTER COLUMN "inn" TYPE Character Varying( 128 );
    
    COMMIT;
    ''')

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

    records = session1.query(tbl8.res_partner) \
        .filter(tbl8.res_partner.parent_id.is_(None),
                tbl8.res_partner.active.is_(True),
                or_(tbl8.res_partner.customer.is_(True),
                    tbl8.res_partner.supplier.is_(True))) \
        .all()

    for rec in records:
        partner = tbl10.res_partner()
        partner.id_ = rec.id
        partner.name = rec.name
        partner.display_name = rec.display_name
        partner.street = rec.street
        partner.street2 = rec.street2
        partner.city = rec.city
        partner.is_company = rec.is_company
        partner.website = rec.website,
        partner.phone = rec.phone
        partner.mobile = rec.mobile
        partner.fax = rec.fax
        partner.email = rec.email
        partner.kpp = rec.kpp
        partner.okpo = rec.okpo
        partner.create_date = rec.create_date
        partner.last_call = rec.last_call
        partner.last_proposals = rec.last_proposals
        partner.inn = rec.vat  # В Odoo 10 нужно увеличить поле до 128
        partner.type = rec.type
        partner.function = rec.function
        partner.comment = rec.comment
        partner.date_transfer = rec.date
        partner.customer = rec.customer
        partner.supplier = rec.supplier
        partner.active = True
        if not rec.notify_email:
            partner.notify_email = "always"
        else:
            partner.notify_email = rec.notify_email
        partner.invoice_warn = "no-message"
        partner.sale_warn = "no-message"
        partner.picking_warn = "no-message"
        partner.purchase_warn = "no-message"
        partner.lang = "ru_RU"
        partner.opt_out = False
        partner.partner_share = True
        partner.message_bounce = 0
        partner.is_overdue = rec.is_overdue
        partner.employee = rec.employee
        partner.tz = rec.tz
        partner.commercial_company_name = rec.display_name
        if rec.user_id:
            partner.user_id = user_dict[rec.user_id]
        if rec.section_id:
            partner.team_id = team_dict[rec.section_id]
        if rec.company_id:
            partner.company_id = company_dict[rec.company_id]
        session2.add(partner)
        session2.flush()
        partner.commercial_partner_id = partner.id
    session2.commit()
    logger.info("Partners transfer compete.")


def do_partners_contacts_transfer(session1, session2):
    """
    Перенос контактов
    """

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

    records = session1.query(tbl8.res_partner) \
        .filter(~tbl8.res_partner.parent_id.is_(None),
                tbl8.res_partner.active.is_(True)) \
        .all()

    vals = [value for value, in session2.query(tbl10.res_partner.id_).all()]

    for rec in records:
        if rec.parent_id in vals:
            partner = tbl10.res_partner()
            partner.parent_id = session2.query(tbl10.res_partner.id).filter(
                tbl10.res_partner.id_ == rec.parent_id).first()[0]
            partner.id_ = rec.id
            partner.name = rec.name
            partner.display_name = rec.display_name
            partner.street = rec.street
            partner.street2 = rec.street2
            partner.city = rec.city
            partner.is_company = rec.is_company
            partner.website = rec.website,
            partner.phone = rec.phone
            partner.mobile = rec.mobile
            partner.fax = rec.fax
            partner.email = rec.email
            partner.kpp = rec.kpp
            partner.okpo = rec.okpo
            partner.create_date = rec.create_date
            partner.last_call = rec.last_call
            partner.last_proposals = rec.last_proposals
            partner.inn = rec.vat
            partner.type = rec.type
            partner.function = rec.function
            partner.comment = rec.comment
            partner.date_transfer = rec.date
            partner.customer = rec.customer
            partner.supplier = rec.supplier
            partner.active = True
            if not rec.notify_email:
                partner.notify_email = "always"
            else:
                partner.notify_email = rec.notify_email
            partner.invoice_warn = "no-message"
            partner.sale_warn = "no-message"
            partner.picking_warn = "no-message"
            partner.purchase_warn = "no-message"
            partner.lang = "ru_RU"
            partner.opt_out = False
            partner.partner_share = True
            partner.message_bounce = 0
            partner.is_overdue = rec.is_overdue
            partner.employee = rec.employee
            partner.tz = rec.tz
            partner.commercial_company_name = rec.display_name
            if rec.user_id:
                partner.user_id = user_dict[rec.user_id]
            if rec.section_id:
                partner.team_id = team_dict[rec.section_id]
            if rec.company_id:
                partner.company_id = company_dict[rec.company_id]
            session2.add(partner)
            session2.flush()
            partner.commercial_partner_id = partner.id
    session2.commit()
    logger.info("Contacts transfer compete.")
