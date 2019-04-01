# -*- coding: utf-8 -*-
from model import tbl_odoo8 as tbl8
from model import tbl_odoo10 as tbl10
from model.database import logger


def do_crm_phonecall_transfer(session1, session2):
    """
    Теперь переносим звонки
    """

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

    records = session1.query(tbl8.crm_phonecall) \
        .filter(tbl8.crm_phonecall.active.is_(True)) \
        .all()

    vals = [value for value,
            in session2.query(tbl10.res_partner.id_).all()]

    for rec in records:
        if rec.partner_id in vals:
            phonecall = tbl10.crm_phonecall()
            # phonecall.id_ = rec.id
            phonecall.name = rec.name
            phonecall.active = rec.active
            phonecall.create_date = rec.create_date
            phonecall.partner_phone = rec.partner_phone
            phonecall.date = rec.date
            phonecall.duration = rec.duration
            if rec.partner_id:
                phonecall.partner_id = session2.query(tbl10.res_partner.id) \
                    .filter(tbl10.res_partner.id_ == rec.partner_id) \
                    .first()[0]
            phonecall.partner_mobile = rec.partner_mobile
            if rec.opportunity_id:
                phonecall.opportunity_id = session2.query(tbl10.crm_lead.id) \
                    .filter(tbl10.crm_lead.id_ == rec.opportunity_id) \
                    .first()[0]
            phonecall.description = rec.description
            if rec.user_id:
                phonecall.user_id = user_dict[rec.user_id]
            if rec.section_id:
                phonecall.team_id = team_dict[rec.section_id]
            phonecall.priority = rec.priority
            phonecall.state = rec.state
            phonecall.message_last_post = rec.message_last_post
            phonecall.email_from = rec.email_from

            session2.add(phonecall)
    session2.commit()
    logger.info("Phonecalls transfer compete.")
