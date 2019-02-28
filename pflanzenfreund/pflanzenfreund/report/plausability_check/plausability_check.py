# Copyright (c) 2013, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import today

def execute(filters=None):
	columns, data = [], []
	if filters.abfrage == 'Deaktivierte Kunden':
		columns = ["Kunde:Link/Customer", "Kundennamen:Data", "Status", "Jahres-Abos:Int", "Probe-Abos:Int", "Geschenk-Abos:Int", "KK-Abos:Int", "OK-Abos:Int", "Gratis-Abos:Int", "VIP-Abos:Int"]
		limit = ''
		if filters.bis > 0:
			if filters.von > 0:
				limit = ' LIMIT {bis} OFFSET {von}'.format(von=filters.von, bis=filters.bis)
			else:
				limit = ' LIMIT {bis}'.format(bis=filters.bis)
		customers = frappe.db.sql("""SELECT
										`name`,
										`customer_name`
									FROM `tabCustomer`
									WHERE
										`disabled` = 1
									ORDER BY `modified` DESC{limit}""".format(limit=limit), as_dict=True)
									
		for customer in customers:
			jahres_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Jahres-Abo'
												AND `end_date` >= '{today}'""".format(customer=customer.name, today=today()), as_list=True)[0][0]
												
			probe_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Probe-Abo'
												AND `end_date` >= '{today}'""".format(customer=customer.name, today=today()), as_list=True)[0][0]
												
			geschenk_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Geschenk-Abo'
												AND `end_date` >= '{today}'""".format(customer=customer.name, today=today()), as_list=True)[0][0]
												
			kk_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Kundenkarten-Abo (KK)'""".format(customer=customer.name), as_list=True)[0][0]
												
			ok_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Kunden-Abo (OK)'""".format(customer=customer.name), as_list=True)[0][0]
												
			gratis_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Gratis-Abo'""".format(customer=customer.name), as_list=True)[0][0]
												
			vip_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'VIP-Abo'""".format(customer=customer.name), as_list=True)[0][0]
												
			
			
			log = []
			log.append(customer.name)
			log.append(customer.customer_name)
			log.append("Deaktiviert")
			log.append(jahres_abos)
			log.append(probe_abos)
			log.append(geschenk_abos)
			log.append(kk_abos)
			log.append(ok_abos)
			log.append(gratis_abos)
			log.append(vip_abos)
			
			data.append(log)
			
	if filters.abfrage == 'Kunden mit WS':
		columns = ["Kunde:Link/Customer", "Kundennamen:Data", "Status", "KK-Abos:Int", "OK-Abos:Int", "Gratis-Abos:Int", "VIP-Abos:Int"]
		limit = ''
		if filters.bis > 0:
			if filters.von > 0:
				limit = ' LIMIT {bis} OFFSET {von}'.format(von=filters.von, bis=filters.bis)
			else:
				limit = ' LIMIT {bis}'.format(bis=filters.bis)
			
		customers = frappe.db.sql("""SELECT
										`name`,
										`customer_name`
									FROM `tabCustomer`
									WHERE
										`disabled` = 0
										AND `code_05` = '1'
									ORDER BY `modified` DESC{limit}""".format(limit=limit), as_dict=True)
									
		for customer in customers:
			kk_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Kundenkarten-Abo (KK)'""".format(customer=customer.name), as_list=True)[0][0]
												
			ok_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Kunden-Abo (OK)'""".format(customer=customer.name), as_list=True)[0][0]
												
			gratis_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Gratis-Abo'""".format(customer=customer.name), as_list=True)[0][0]
												
			vip_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'VIP-Abo'""".format(customer=customer.name), as_list=True)[0][0]
												
			
			
			log = []
			log.append(customer.name)
			log.append(customer.customer_name)
			log.append("Mit WS")
			log.append(kk_abos)
			log.append(ok_abos)
			log.append(gratis_abos)
			log.append(vip_abos)
			
			data.append(log)
	
	
	if filters.abfrage == 'Kunden mit Kundenkarte':
		columns = ["Kunde:Link/Customer", "Kundennamen:Data", "Status", "Jahres-Abos:Int", "Probe-Abos:Int", "Geschenk-Abos:Int", "KK-Abos:Int", "OK-Abos:Int", "Gratis-Abos:Int", "VIP-Abos:Int"]
		limit = ''
		if filters.bis > 0:
			if filters.von > 0:
				limit = ' LIMIT {bis} OFFSET {von}'.format(von=filters.von, bis=filters.bis)
			else:
				limit = ' LIMIT {bis}'.format(bis=filters.bis)
		customers = frappe.db.sql("""SELECT
										`name`,
										`customer_name`
									FROM `tabCustomer`
									WHERE
										`disabled` = 0
										AND `karte` = 'J'
										AND `code_05` = '1'
									ORDER BY `modified` DESC{limit}""".format(limit=limit), as_dict=True)
									
		for customer in customers:
			jahres_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Jahres-Abo'
												AND `end_date` >= '{today}'""".format(customer=customer.name, today=today()), as_list=True)[0][0]
												
			probe_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Probe-Abo'
												AND `end_date` >= '{today}'""".format(customer=customer.name, today=today()), as_list=True)[0][0]
												
			geschenk_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Geschenk-Abo'
												AND `end_date` >= '{today}'""".format(customer=customer.name, today=today()), as_list=True)[0][0]
												
			kk_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Kundenkarten-Abo (KK)'""".format(customer=customer.name), as_list=True)[0][0]
												
			ok_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Kunden-Abo (OK)'""".format(customer=customer.name), as_list=True)[0][0]
												
			gratis_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Gratis-Abo'""".format(customer=customer.name), as_list=True)[0][0]
												
			vip_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'VIP-Abo'""".format(customer=customer.name), as_list=True)[0][0]
												
			
			
			log = []
			log.append(customer.name)
			log.append(customer.customer_name)
			log.append("Mit Kundenkarte")
			log.append(jahres_abos)
			log.append(probe_abos)
			log.append(geschenk_abos)
			log.append(kk_abos)
			log.append(ok_abos)
			log.append(gratis_abos)
			log.append(vip_abos)
			
			data.append(log)
			
			
	if filters.abfrage == 'Kunden ohne Kundenkarte':
		columns = ["Kunde:Link/Customer", "Kundennamen:Data", "Status", "Jahres-Abos:Int", "Probe-Abos:Int", "Geschenk-Abos:Int", "KK-Abos:Int", "OK-Abos:Int", "Gratis-Abos:Int", "VIP-Abos:Int"]
		limit = ''
		if filters.bis > 0:
			if filters.von > 0:
				limit = ' LIMIT {bis} OFFSET {von}'.format(von=filters.von, bis=filters.bis)
			else:
				limit = ' LIMIT {bis}'.format(bis=filters.bis)
		customers = frappe.db.sql("""SELECT
										`name`,
										`customer_name`
									FROM `tabCustomer`
									WHERE
										`disabled` = 0
										AND `karte` != 'J'
										AND `code_05` = '1'
									ORDER BY `modified` DESC{limit}""".format(limit=limit), as_dict=True)
									
		for customer in customers:
			jahres_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Jahres-Abo'
												AND `end_date` >= '{today}'""".format(customer=customer.name, today=today()), as_list=True)[0][0]
												
			probe_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Probe-Abo'
												AND `end_date` >= '{today}'""".format(customer=customer.name, today=today()), as_list=True)[0][0]
												
			geschenk_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Geschenk-Abo'
												AND `end_date` >= '{today}'""".format(customer=customer.name, today=today()), as_list=True)[0][0]
												
			kk_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Kundenkarten-Abo (KK)'""".format(customer=customer.name), as_list=True)[0][0]
												
			ok_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Kunden-Abo (OK)'""".format(customer=customer.name), as_list=True)[0][0]
												
			gratis_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'Gratis-Abo'""".format(customer=customer.name), as_list=True)[0][0]
												
			vip_abos = frappe.db.sql("""SELECT
												COUNT(`name`)
											FROM `tabPflanzenfreund Abo`
											WHERE
												`docstatus` = 1
												AND `customer` = '{customer}'
												AND `abo_type` = 'VIP-Abo'""".format(customer=customer.name), as_list=True)[0][0]
												
			
			
			log = []
			log.append(customer.name)
			log.append(customer.customer_name)
			log.append("Ohne Kundenkarte")
			log.append(jahres_abos)
			log.append(probe_abos)
			log.append(geschenk_abos)
			log.append(kk_abos)
			log.append(ok_abos)
			log.append(gratis_abos)
			log.append(vip_abos)
			
			data.append(log)
	# columns = ["Kunde", "Kundennamen", "Deaktiviert", "Werbe-Sperre", "Kundenkarte", "Anz. Jahres-Abos"]
	# customers = frappe.db.sql("""SELECT
									# `name`,
									# `customer_name`,
									# `disabled`,
									# `code_05`,
									# `karte`
								# FROM `tabCustomer`""", as_dict=True)
								
	# for customer in customers:
		# jahres_abos = frappe.db.sql("""SELECT
											# COUNT(`name`)
										# FROM `tabPflanzenfreund Abo`
										# WHERE
											# `docstatus` = 1
											# AND `customer` = '{customer}'
											# AND `abo_type` = 'Jahres-Abo'
											# AND `end_date` >= '2019-01-01'""".format(customer=customer.name), as_list=True)[0][0]
											
		
		
		# log = []
		# log.append(customer.name)
		# log.append(customer.customer_name)
		# log.append(customer.disabled)
		# log.append(customer.code_05)
		# log.append(customer.karte)
		# log.append(jahres_abos)
		
		# data.append(log)
	return columns, data
