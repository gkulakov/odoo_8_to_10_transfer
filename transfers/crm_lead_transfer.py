# -*- coding: utf-8 -*-
from model import tbl_odoo8 as tbl8
from model import tbl_odoo10 as tbl10
from model.database import logger


def do_crm_lead_transfer(session1, session2):
    """
    Теперь переносим Предложения
    """

    session2.execute('''
    DO $$
        BEGIN
            BEGIN
                ALTER TABLE public.crm_lead ADD COLUMN id_ INT;
            EXCEPTION
                WHEN duplicate_column THEN RAISE NOTICE 'column id_ already exists in crm_lead.';
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

    stage_dict = {
        x: session2.query(tbl10.crm_stage.id).filter(
            tbl10.crm_stage.probability == name
        ).first()[0]
        for x, name
        in session1.query(tbl8.crm_case_stage.id,
                          tbl8.crm_case_stage.probability).all()
    }

    records = session1.query(tbl8.crm_lead) \
        .filter(tbl8.crm_lead.active.is_(True)) \
        .all()

    vals = [value for value,
            in session2.query(tbl10.res_partner.id_).all()]

    for rec in records:
        if rec.partner_id in vals:
            lead = tbl10.crm_lead()
            lead.id_ = rec.id
            lead.name = rec.name
            lead.active = rec.active
            lead.planned_revenue = rec.planned_revenue
            lead.probability = rec.probability
            if rec.partner_id:
                lead.partner_id = session2.query(tbl10.res_partner.id) \
                    .filter(tbl10.res_partner.id_ == rec.partner_id) \
                    .first()[0]
            if rec.company_id:
                lead.company_id = company_dict[rec.company_id]
            lead.email_from = rec.email_from
            lead.phone = rec.phone
            lead.mobile = rec.mobile
            if rec.user_id:
                lead.user_id = user_dict[rec.user_id]
            if rec.section_id:
                lead.team_id = team_dict[rec.section_id]
            lead.description = rec.description
            lead.next_activity_id = 3
            lead.title_action = rec.title_action
            lead.date_action = rec.date_action
            lead.date_deadline = rec.date_deadline
            lead.priority = rec.priority
            lead.partner_name = rec.partner_name
            lead.street = rec.street
            lead.street2 = rec.street2
            lead.city = rec.city
            lead.zip_ = rec.zip_
            lead.contact_name = rec.contact_name
            lead.function = rec.function
            lead.fax = rec.fax
            lead.opt_out = True
            lead.type = rec.type
            lead.create_date = rec.create_date
            if rec.stage_id:
                lead.stage_id = stage_dict[rec.stage_id]

            session2.add(lead)
    session2.commit()
    logger.info("Leads transfer compete.")
