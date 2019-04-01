# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import *
from sqlalchemy import ForeignKey as FKey

Base = declarative_base()


class res_country(Base):
    """Страны"""
    __tablename__ = 'res_country'
    id = Column(Integer, primary_key=True)
    address_format = Column(Text)
    code = Column(String(2))
    create_date = Column(DateTime)
    create_uid = Column(Integer)
    write_date = Column(DateTime)
    write_uid = Column(Integer)
    currency_id = Column(Integer)
    image = Column(Binary)
    name = Column(String)
    phone_code = Column(Integer)


class res_country_state(Base):
    """Страны"""
    __tablename__ = 'res_country_state'
    id = Column(Integer, primary_key=True)
    code = Column(String(3))
    country_id = Column(Integer, FKey('res_country.id'), index=True)
    create_date = Column(DateTime)
    create_uid = Column(Integer)
    write_date = Column(DateTime)
    write_uid = Column(Integer)
    name = Column(String)


class res_partner(Base):
    """Клиенты"""
    __tablename__ = 'res_partner'
    id = Column(Integer, primary_key=True)
    id_ = Column(Integer, index=True)
    name = Column(String, nullable=False)
    company_id = Column(Integer, FKey('res_company.id'), index=True)
    comment = Column(Text)
    website = Column(String)
    create_date = Column(DateTime)
    color = Column(Integer)
    active = Column(Boolean)
    street = Column(String)
    supplier = Column(Boolean)
    city = Column(String)
    display_name = Column(String)
    zip = Column(String(24))
    title = Column(Integer)
    country_id = Column(Integer)
    commercial_company_name = Column(String)  # Only in v10
    parent_id = Column(Integer, FKey('res_partner.id'), index=True)
    company_name = Column(String)  # Only in v10
    employee = Column(Boolean)
    ref = Column(String)
    email = Column(String)
    is_company = Column(Boolean)
    function = Column(String)
    lang = Column(String)
    fax = Column(String)
    street2 = Column(String)
    barcode = Column(String)
    phone = Column(String)
    write_date = Column(DateTime)
    date = Column(Date)
    tz = Column(String(64))
    write_uid = Column(Integer, FKey('res_users.id'), index=True)
    customer = Column(Boolean)
    create_uid = Column(Integer, FKey('res_users.id'), index=True)
    credit_limit = Column(Float)
    user_id = Column(Integer, FKey('res_users.id'), index=True)
    mobile = Column(String)
    type = Column(String)
    partner_share = Column(Boolean)  # Only in v10
    vat = Column(String)
    state_id = Column(Integer)
    commercial_partner_id = Column(Integer)
    notify_email = Column(String, nullable=False)
    message_last_post = Column(DateTime)
    opt_out = Column(Boolean)
    message_bounce = Column(Integer)
    signup_type = Column(String)
    signup_expiration = Column(DateTime)
    signup_token = Column(String)
    team_id = Column(Integer)  # section_id in v8
    calendar_last_notif_ack = Column(DateTime)
    invoice_warn = Column(String, nullable=False)  # Only in v10
    debit_limit = Column(Numeric)  # Float in v8
    last_time_entries_checked = Column(DateTime)  # Only in v10
    invoice_warn_msg = Column(Text)  # Only in v10
    sale_warn = Column(String, nullable=False)  # Only in v10
    sale_warn_msg = Column(Text)  # Only in v10
    picking_warn = Column(String, nullable=False)  # Only in v10
    picking_warn_msg = Column(Text)  # Only in v10
    purchase_warn = Column(String, nullable=False)  # Only in v10
    purchase_warn_msg = Column(Text)  # Only in v10
    kpp = Column(String(9))
    okpo = Column(String(14))
    inn = Column(String(128))  # vat in v8 Надо увеличить до 128
    # website_meta_keywords = Column(String)
    # website_meta_description = Column(Text)
    # website_meta_title = Column(String)
    # website_published = Column(Boolean)
    # website_short_description = Column(Text)
    # website_description = Column(Text)
    date_transfer = Column(Date)  # Only in v10
    last_call = Column(Date)
    is_overdue = Column(Boolean)
    last_proposals = Column(Date)  # Дата закрытия последнего предложения

    # ean13 = Column(String(13))
    # image = Column(Binary)
    # use_parent_address = Column(Boolean)
    # image_medium = Column(Binary)
    # image_small = Column(Binary)
    # birthdate = Column(String)
    # cm_user_taxpayerID = Column(String(40))
    # last_reconciliation_date = Column(DateTime)
    # site_customer = Column(Boolean)
    # speaker = Column(Boolean)
    # latest_followup_level_id_without_lit = Column(Integer)
    # payment_next_action_date = Column(Date)
    # latest_followup_level_id = Column(Integer)
    # payment_next_action = Column(Text)
    # payment_note = Column(Text)
    # payment_responsible_id = Column(Integer)
    # last_call_overdue = Column(Boolean)
    # last_quotation_overdue = Column(Boolean)


class res_users(Base):
    """Клиенты"""
    __tablename__ = 'res_users'
    id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    login = Column(String(64))
    password = Column(String)
    company_id = Column(Integer, FKey('res_company.id'), index=True)
    partner_id = Column(Integer, FKey('res_partner.id'), index=True)
    create_uid = Column(Integer, FKey('res_users.id'), index=True)
    create_date = Column(DateTime)
    share = Column(Boolean)
    action_id = Column(Integer)
    write_date = Column(DateTime)
    write_uid = Column(Integer, FKey('res_users.id'), index=True)
    signature = Column(Text)
    password_crypt = Column(String)
    alias_id = Column(Integer, nullable=False)

    menu_id = Column(Integer)
    login_date = Column(Date)
    display_groups_suggestions = Column(Boolean)
    default_section_id = Column(Integer)
    facsimile = Column(Binary)
    display_employees_suggestions = Column(Boolean)
    google_calendar_token_validity = Column(DateTime)
    google_calendar_rtoken = Column(String)
    google_calendar_last_sync_date = Column(DateTime)
    google_calendar_token = Column(String)
    google_calendar_cal_id = Column(String)
    karma = Column(Integer)


class res_company(Base):
    """Компании"""
    __tablename__ = 'res_company'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True)
    account_no = Column(String)
    accountant_id = Column(Integer, FKey('res_users.id'), index=True)
    accounts_code_digits = Column(Integer)
    anglo_saxon_accounting = Column(Boolean)
    auto_currency_up = Column(Boolean)
    bank_account_code_prefix = Column(String)
    cash_account_code_prefix = Column(String)
    chart_template_id = Column(Integer)
    chief_id = Column(Integer, FKey('res_users.id'), index=True)
    company_registry = Column(String)
    create_date = Column(DateTime)
    create_uid = Column(Integer, FKey('res_users.id'), index=True)
    write_date = Column(DateTime)
    write_uid = Column(Integer, FKey('res_users.id'), index=True)
    currency_exchange_journal_id = Column(Integer)
    currency_id = Column(Integer)
    custom_footer = Column(Boolean)
    email = Column(String)
    expects_chart_of_accounts = Column(Boolean)
    fiscalyear_last_day = Column(Integer, nullable=False)
    fiscalyear_last_month = Column(Integer, nullable=False)
    fiscalyear_lock_date = Column(Date)
    font = Column(Integer)
    internal_transit_location_id = Column(Integer)
    logo_web = Column(Binary)
    manufacturing_lead = Column(Float)
    overdue_msg = Column(Text)
    paperformat_id = Column(Integer)
    parent_id = Column(Integer, FKey('res_company.id'), index=True)
    partner_id = Column(Integer, FKey('res_partner.id'), index=True)
    period_lock_date = Column(Date)
    phone = Column(String)
    po_double_validation = Column(String)
    po_double_validation_amount = Column(Numeric)
    po_lead = Column(Float)
    po_lock = Column(String)
    print_anywhere = Column(Boolean)
    print_facsimile = Column(Boolean)
    print_stamp = Column(Boolean)
    propagation_minimum_delta = Column(Integer)
    property_stock_account_input_categ_id = Column(Integer)
    property_stock_account_output_categ_id = Column(Integer)
    property_stock_valuation_account_id = Column(Integer)
    #  skip rml
    sale_note = Column(Text)
    security_lead = Column(Float)
    sequence = Column(Integer)
    stamp = Column(Binary)
    tax_calculation_rounding_method = Column(String)
    transfer_account_id = Column(Integer)


class crm_team(Base):
    """Команды продаж"""
    __tablename__ = 'crm_team'
    id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    alias_id = Column(Integer)
    color = Column(Integer)
    company_id = Column(Integer, FKey('res_company.id'), index=True)
    create_date = Column(DateTime)
    create_uid = Column(Integer, FKey('res_users.id'), index=True)
    write_date = Column(DateTime)
    write_uid = Column(Integer, FKey('res_users.id'), index=True)
    invoiced_target = Column(Integer)
    message_last_post = Column(DateTime)
    name = Column(String, nullable=False)
    reply_to = Column(String)
    resource_calendar_id = Column(Integer)
    use_invoices = Column(Boolean)
    use_leads = Column(Boolean)
    use_opportunities = Column(Boolean)
    use_quotations = Column(Boolean)
    user_id = Column(Integer, FKey('res_users.id'), index=True)


class crm_stage(Base):
    """Стадия предложения"""
    __tablename__ = 'crm_stage'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime)
    create_uid = Column(Integer, FKey('res_users.id'), index=True)
    write_date = Column(DateTime)
    write_uid = Column(Integer, FKey('res_users.id'), index=True)
    fold = Column(Boolean)
    legend_priority = Column(Text)
    name = Column(String, nullable=False)
    on_change = Column(Boolean)
    probability = Column(Float)
    requirements = Column(Text)
    sequence = Column(Integer)
    team_id = Column(Integer)


class crm_lead(Base):
    """Предложения"""
    __tablename__ = 'crm_lead'
    id = Column(Integer, primary_key=True)
    id_ = Column(Integer, index=True)
    active = Column(Boolean)
    campaign_id = Column(Integer)
    city = Column(String)
    color = Column(Integer)
    company_id = Column(Integer, FKey('res_company.id'), index=True)
    company = relationship(
        'res_company', foreign_keys='crm_lead.company_id')
    contact_name = Column(String)
    country_id = Column(Integer)
    create_date = Column(DateTime)
    create_uid = Column(Integer, FKey('res_users.id'), index=True)
    write_date = Column(DateTime)
    write_uid = Column(Integer, FKey('res_users.id'), index=True)
    date_action = Column(Date, index=True)
    date_action_last = Column(DateTime)
    date_action_next = Column(DateTime)
    date_closed = Column(DateTime)
    date_conversion = Column(DateTime)  # New in 10
    date_deadline = Column(Date)
    date_last_stage_update = Column(DateTime)
    date_open = Column(DateTime)
    day_close = Column(Numeric)
    day_open = Column(Numeric)
    description = Column(Text)
    email_cc = Column(Text)
    email_from = Column(String)
    fax = Column(String)
    function = Column(String)
    lost_reason = Column(Integer)  # New in 10
    medium_id = Column(Integer)
    message_bounce = Column(Integer)
    message_last_post = Column(DateTime)
    mobile = Column(String)
    name = Column(String, nullable=False, index=True)
    next_activity_id = Column(Integer)  # New in 10
    opt_out = Column(Boolean)
    partner_id = Column(Integer, FKey('res_partner.id'), index=True)
    partner = relationship(
        'res_partner', foreign_keys='crm_lead.partner_id')
    partner_name = Column(String)
    phone = Column(String)
    planned_revenue = Column(Float)
    priority = Column(String)
    probability = Column(Float)
    referred = Column(String)
    source_id = Column(Integer)
    stage_id = Column(Integer, FKey('crm_stage.id'), index=True)
    stage = relationship(
        'crm_stage', foreign_keys='crm_lead.stage_id')
    state_id = Column(Integer)
    street = Column(String)
    street2 = Column(String)
    team_id = Column(Integer, FKey('crm_team.id'), index=True)
    team = relationship(
        'crm_team', foreign_keys='crm_lead.team_id')
    title = Column(Integer)
    title_action = Column(String)
    type = Column(String)
    user_id = Column(Integer, FKey('res_users.id'), index=True)
    user = relationship(
        'res_users', foreign_keys='crm_lead.user_id')
    zip_ = Column(String, name="zip")


class crm_phonecall(Base):
    """Звонки"""
    __tablename__ = 'crm_phonecall'
    id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    campaign_id = Column(Integer)  # new in 10
    company_id = Column(Integer, FKey('res_company.id'), index=True)
    company = relationship(
        'res_company', foreign_keys='crm_phonecall.company_id')
    create_date = Column(DateTime)
    create_uid = Column(Integer, FKey('res_users.id'), index=True)
    write_date = Column(DateTime)
    write_uid = Column(Integer, FKey('res_users.id'), index=True)
    date = Column(DateTime)
    date_action_last = Column(DateTime)
    date_action_next = Column(DateTime)
    date_closed = Column(DateTime)
    date_open = Column(DateTime)
    description = Column(Text)
    duration = Column(Float)
    email_from = Column(String)
    medium_id = Column(Integer)
    message_last_post = Column(DateTime)
    name = Column(String, nullable=False)
    opportunity_id = Column(Integer)
    partner_id = Column(Integer, FKey('res_partner.id'), index=True)
    partner = relationship(
        'res_partner', foreign_keys='crm_phonecall.partner_id')
    partner_mobile = Column(String)
    partner_phone = Column(String)
    priority = Column(String)
    source_id = Column(Integer)
    state = Column(String)
    team_id = Column(Integer, FKey('crm_team.id'), index=True)
    team = relationship(
        'crm_team', foreign_keys='crm_phonecall.team_id')
    user_id = Column(Integer, FKey('res_users.id'), index=True)
    user = relationship(
        'res_users', foreign_keys='crm_phonecall.user_id')


class product_template(Base):
    """Шаблон продука"""
    __tablename__ = 'product_template'
    id = Column(Integer, primary_key=True)
    id_ = Column(Integer, index=True)
    active = Column(Boolean)
    can_be_expensed = Column(Boolean)  # New
    categ_id = Column(Integer, nullable=False)
    color = Column(Integer)
    company_id = Column(Integer, FKey('res_company.id'), index=True)
    company = relationship(
        'res_company', foreign_keys='product_template.company_id')
    create_date = Column(DateTime)
    create_uid = Column(Integer, FKey('res_users.id'), index=True)
    write_date = Column(DateTime)
    write_uid = Column(Integer, FKey('res_users.id'), index=True)
    default_code = Column(String)  # New
    description = Column(Text)
    description_picking = Column(Text)
    description_purchase = Column(Text)
    description_sale = Column(Text)
    expense_policy = Column(String)  # New
    invoice_policy = Column(String)  # New
    list_price = Column(Numeric)
    location_id = Column(Integer)
    message_last_post = Column(String)
    name = Column(String, nullable=False)
    produce_delay = Column(Float)
    purchase_line_warn = Column(String)  # New
    purchase_line_warn_msg = Column(Text)  # New
    purchase_method = Column(String)
    purchase_ok = Column(Boolean)
    purchase_requisition = Column(String)
    rental = Column(Boolean)
    sale_delay = Column(Float)
    sale_line_warn = Column(String)  # New
    sale_line_warn_msg = Column(Text)  # New
    sale_ok = Column(Boolean)
    sequence = Column(Integer)  # New
    track_service = Column(String)  # New
    tracking = Column(String)  # New
    type = Column(String)
    uom_id = Column(Integer)
    uom_po_id = Column(Integer)
    volume = Column(Float)
    warehouse_id = Column(Integer)  # New
    warranty = Column(Float)
    weight = Column(Numeric)


class product_product(Base):
    """Шаблон продука"""
    __tablename__ = 'product_product'
    id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    barcode = Column(String)
    create_date = Column(DateTime)
    create_uid = Column(Integer, FKey('res_users.id'), index=True)
    write_date = Column(DateTime)
    write_uid = Column(Integer, FKey('res_users.id'), index=True)
    default_code = Column(String)
    message_last_post = Column(DateTime)
    product_tmpl_id = Column(Integer)
    volume = Column(Float)
    weight = Column(Numeric)


class product_supplierinfo(Base):
    """Поставщики продукта"""
    __tablename__ = 'product_supplierinfo'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, FKey('res_company.id'), index=True)
    create_date = Column(DateTime)
    create_uid = Column(Integer, FKey('res_users.id'), index=True)
    write_date = Column(DateTime)
    write_uid = Column(Integer, FKey('res_users.id'), index=True)
    currency_id = Column(Integer, nullable=False)
    date_end = Column(Date)
    date_start = Column(Date)
    delay = Column(Integer, nullable=False)
    min_qty = Column(Float, nullable=False)
    name = Column(Integer, nullable=False)  # Supplier ID
    price = Column(Numeric, nullable=False)
    product_code = Column(String)
    product_id = Column(Integer)
    product_name = Column(String)
    product_tmpl_id = Column(Integer)
    sequence = Column(Integer)


class stock_route_product(Base):
    """Маршруты продукта"""
    __tablename__ = 'stock_route_product'
    product_id = Column(Integer, index=True, primary_key=True)
    route_id = Column(Integer, index=True, primary_key=True)


class sale_order(Base):
    """Заказ продаж"""
    __tablename__ = 'sale_order'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime)
    create_uid = Column(Integer, FKey('res_users.id'), index=True)
    write_date = Column(DateTime)
    write_uid = Column(Integer, FKey('res_users.id'), index=True)
    amount_tax = Column(Numeric)
    amount_total = Column(Numeric)
    amount_untaxed = Column(Numeric)
    campaign_id = Column(Integer)  # New in 10
    client_order_ref = Column(String)
    # close_order_date = Column(Date)
    # cm_recured_date = Column(Date)
    company_id = Column(Integer, FKey('res_company.id'), index=True)
    company = relationship(
        'res_company', foreign_keys='sale_order.company_id')
    # contract_production_time = Column(Integer)
    # contract_shipment_date = Column(Date)
    # date_confirm = Column(Date)
    confirmation_date = Column(Date)
    date_order = Column(DateTime, nullable=False)
    entity_for_proc = Column(Integer, FKey('sintez_legal_entity.id'), index=True)
    legal_entity = relationship(
        'sintez_legal_entity', foreign_keys='sale_order.entity_for_proc')
    fiscal_position_id = Column(Integer)
    incoterm = Column(Integer)
    invoice_status = Column(String)
    matching_scheme_date = Column(Date)
    medium_id = Column(Integer)  # New in 10
    message_last_post = Column(DateTime)
    name = Column(String, index=True, nullable=False)
    note = Column(Text)
    opportunity_id = Column(Integer)  # New in 10
    # order_policy = Column(String)
    # order_procurement_confirmed = Column(Boolean)
    origin = Column(String)
    partner_id = Column(Integer, nullable=False)
    partner_invoice_id = Column(Integer, nullable=False)
    partner_shipping_id = Column(Integer, nullable=False)
    payment_term_id = Column(Integer)
    picking_policy = Column(String, nullable=False)
    # prepayments_date = Column(Date)
    pricelist_id = Column(Integer, nullable=False)
    procurement_group_id = Column(Integer)
    project_id = Column(Integer)
    required_shipment_date = Column(Date)
    shipment_date = Column(Date)
    shipped = Column(Boolean)
    so_lines = relationship("sale_order_line")
    source_id = Column(Integer)
    state = Column(String)
    team_id = Column(Integer)
    user_id = Column(Integer, FKey('res_users.id'), index=True)
    user = relationship(
        'res_users', foreign_keys='sale_order.user_id')
    validity_date = Column(Date)
    warehouse_id = Column(Integer, nullable=False)


class sale_order_line(Base):
    """Позиция заказа продаж"""
    __tablename__ = 'sale_order_line'
    id = Column(Integer, primary_key=True)
    # address_allotment_id = Column(Integer)
    # client_product_name = Column(String)
    company_id = Column(Integer, FKey('res_company.id'), index=True)
    company = relationship(
        'res_company', foreign_keys='sale_order_line.company_id')
    # contract_production_time = Column(Integer)
    # contract_shipment_date = Column(Date)
    create_date = Column(DateTime)
    create_uid = Column(Integer, FKey('res_users.id'), index=True)
    write_date = Column(DateTime)
    write_uid = Column(Integer, FKey('res_users.id'), index=True)
    # delay = Column(Float)
    currency_id = Column(Integer)  # New in 10
    customer_lead = Column(Float, nullable=False)  # New in 10
    discount = Column(Numeric)
    # invoiced = Column(Boolean)
    invoice_status = Column(String)  # New in 10
    layout_category_id = Column(Integer)  # New in 10
    layout_category_sequence = Column(Integer)  # New in 10
    name = Column(Text, nullable=False)
    order_id = Column(Integer, FKey('sale_order.id'), index=True)
    order = relationship(
        'sale_order', foreign_keys='sale_order_line.order_id')
    order_partner_id = Column(Integer)
    price_reduce = Column(Numeric)
    price_reduce_taxexcl = Column(Numeric)
    price_reduce_taxinc = Column(Numeric)
    price_subtotal = Column(Numeric)
    price_tax = Column(Numeric)
    price_total = Column(Numeric)
    price_unit = Column(Numeric, nullable=False)
    product_id = Column(Integer, nullable=False)
    product_packaging = Column(Integer)
    product_uom = Column(Integer)
    product_uom_qty = Column(Numeric)
    # product_uos = Column(Integer)
    # product_uos_qty = Column(Numeric)
    # requisition_required = Column(Boolean)
    qty_delivered = Column(Numeric)
    qty_invoiced = Column(Numeric)
    qty_to_invoice = Column(Numeric)
    route_id = Column(Integer)
    salesman_id = Column(Integer)
    sequence = Column(Integer)
    state = Column(String)
    # th_weight = Column(Numeric)

class sintez_legal_entity(Base):
    """Компания для выставления счетов"""
    __tablename__ = 'sintez_legal_entity'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime)
    create_uid = Column(Integer, FKey('res_users.id'), index=True)
    write_date = Column(DateTime)
    write_uid = Column(Integer, FKey('res_users.id'), index=True)
    name = Column(String)


class stock_warehouse(Base):
    """Склад"""
    __tablename__ = 'stock_warehouse'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
