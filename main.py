# -*- coding: utf-8 -*-

from optparse import OptionParser
from model import database as db
from model import tbl_odoo10 as tbl10, tbl_odoo8 as tbl8
from transfers import (crm_lead_transfer, partners_transfer,
                       crm_phonecall_transfer, product_transfer, sales_transfer)


def prepare_app():
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option('-1', '--config1', dest='config1', default=None,
                      help='Параметры подключения Odoo v8')
    parser.add_option('-2', '--config2', dest='config2', default=None,
                      help='Параметры подключения Odoo v10')
    (options, args) = parser.parse_args()
    parser.destroy()

    dal8 = db.DataAccessLayer()
    dal10 = db.DataAccessLayer()
    user1, pass1, address1, database1 = options.config1.split(",")
    user2, pass2, address2, database2 = options.config2.split(",")

    dal8.connect(user1, pass1, address1, database1)
    dal10.connect(user2, pass2, address2, database2)
    return dal8.session, dal10.session


session1, session2 = prepare_app()

# Переносим Клиентов
partners_transfer.do_partners_transfer(session1, session2)
# Переносим контактов клиентов
partners_transfer.do_partners_contacts_transfer(session1, session2)
# Переносим предложения
crm_lead_transfer.do_crm_lead_transfer(session1, session2)
# Переносим Звонки
crm_phonecall_transfer.do_crm_phonecall_transfer(session1, session2)
# Переносим Продукты
product_transfer.do_product_template_transfer(session1, session2)
# Переносим Заказы продаж
sales_transfer.do_sales_transfer(session1, session2)