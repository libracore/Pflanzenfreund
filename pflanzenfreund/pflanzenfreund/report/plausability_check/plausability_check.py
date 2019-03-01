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

	
@frappe.whitelist()
def remove_all_abos(kunden):
	import json
	if isinstance(kunden, basestring):
		kunden = json.loads(kunden)
	#frappe.throw(str(kunden))
	#idx = 1
	for kunde in kunden:
		#frappe.publish_realtime('remove_all_abos_task', {"progress": [idx, len(kunden)]}, user=frappe.session.user)
		#idx = idx + 1
		abos = frappe.db.sql("""SELECT `name` FROM `tabPflanzenfreund Abo` WHERE `customer` = '{kunde}' AND `docstatus` = 1""".format(kunde=kunde), as_dict=True)
		for _abo in abos:
			abo = frappe.get_doc("Pflanzenfreund Abo", _abo.name)
			abo.cancel()
	return "OK"
	
@frappe.whitelist()
def remove_all_abos_ws_affected(kunden):
	import json
	if isinstance(kunden, basestring):
		kunden = json.loads(kunden)
	#frappe.throw(str(kunden))
	#idx = 1
	for kunde in kunden:
		#frappe.publish_realtime('remove_all_abos_task', {"progress": [idx, len(kunden)]}, user=frappe.session.user)
		#idx = idx + 1
		abos = frappe.db.sql("""SELECT `name` FROM `tabPflanzenfreund Abo` WHERE `customer` = '{kunde}' AND `docstatus` = 1 AND `abo_type` IN ('Gratis-Abo', 'VIP-Abo', 'Kundenkarten-Abo (KK)', 'Kunden-Abo (OK)')""".format(kunde=kunde), as_dict=True)
		for _abo in abos:
			abo = frappe.get_doc("Pflanzenfreund Abo", _abo.name)
			abo.cancel()
	return "OK"
	
@frappe.whitelist()
def remove_abos_on_case_kk(case1, case2, case3, case4, winter_ed=0, feb_ed=0, mar_ed=0, apr_ed=0, may_ed=0, jun_ed=0, summer_ed=0, sept_ed=0, okt_ed=0, nov_ed=0):
	import json
	if isinstance(case1, basestring):
		case1 = json.loads(case1)
	if isinstance(case2, basestring):
		case2 = json.loads(case2)
	if isinstance(case3, basestring):
		case3 = json.loads(case3)
	if isinstance(case4, basestring):
		case4 = json.loads(case4)
	#frappe.throw(str(kunden))
	#idx = 1
	for kunde in case1:
		#frappe.publish_realtime('remove_all_abos_task', {"progress": [idx, len(kunden)]}, user=frappe.session.user)
		#idx = idx + 1
		abos = frappe.db.sql("""SELECT `name` FROM `tabPflanzenfreund Abo` WHERE `customer` = '{kunde}' AND `docstatus` = 1 AND `abo_type` IN ('Gratis-Abo', 'VIP-Abo', 'Kundenkarten-Abo (KK)', 'Kunden-Abo (OK)')""".format(kunde=kunde), as_dict=True)
		for _abo in abos:
			abo = frappe.get_doc("Pflanzenfreund Abo", _abo.name)
			abo.cancel()
			
	for kunde in case2:
		#frappe.publish_realtime('remove_all_abos_task', {"progress": [idx, len(kunden)]}, user=frappe.session.user)
		#idx = idx + 1
		abos = frappe.db.sql("""SELECT `name` FROM `tabPflanzenfreund Abo` WHERE `customer` = '{kunde}' AND `docstatus` = 1 AND `abo_type` = 'Kundenkarten-Abo (KK)'""".format(kunde=kunde), as_dict=True)
		for _abo in abos:
			abo = frappe.get_doc("Pflanzenfreund Abo", _abo.name)
			abo.cancel()
	
	#ANLAGE KK ABO!!!!	
	for kunde in case3:
		adresse = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `parenttype` = 'Address' AND `parentfield` = 'links' AND `idx` = '1' AND `link_doctype` = 'Customer' AND `link_name` = '{kunde}'""".format(kunde=kunde), as_list=True)[0][0]
		abo = frappe.new_doc("Pflanzenfreund Abo")
		abo.update({
				"customer": kunde,
				"customer_address": adresse,
				"abo_type": "Kundenkarten-Abo (KK)",
				"start_date": today(),
				"set_ed_manual": 1,
				"winter_ed": winter_ed,
				"feb_ed": feb_ed,
				"mar_ed": mar_ed,
				"apr_ed": apr_ed,
				"may_ed": may_ed,
				"jun_ed": jun_ed,
				"summer_ed": summer_ed,
				"sept_ed": sept_ed,
				"oct_ed": okt_ed,
				"nov_ed": nov_ed
			})
		abo.insert(ignore_permissions=True)
		abo.submit()
			
	for kunde in case4:
		#frappe.publish_realtime('remove_all_abos_task', {"progress": [idx, len(kunden)]}, user=frappe.session.user)
		#idx = idx + 1
		abos = frappe.db.sql("""SELECT `name` FROM `tabPflanzenfreund Abo` WHERE `customer` = '{kunde}' AND `docstatus` = 1 AND `abo_type` = 'Kunden-Abo (OK)'""".format(kunde=kunde), as_dict=True)
		for _abo in abos:
			abo = frappe.get_doc("Pflanzenfreund Abo", _abo.name)
			abo.cancel()
	return "OK"
	
@frappe.whitelist()
def remove_abos_on_case_ok(case1, case2, case3, case4, winter_ed=0, feb_ed=0, mar_ed=0, apr_ed=0, may_ed=0, jun_ed=0, summer_ed=0, sept_ed=0, okt_ed=0, nov_ed=0):
	import json
	if isinstance(case1, basestring):
		case1 = json.loads(case1)
	if isinstance(case2, basestring):
		case2 = json.loads(case2)
	if isinstance(case3, basestring):
		case3 = json.loads(case3)
	if isinstance(case4, basestring):
		case4 = json.loads(case4)
	#frappe.throw(str(kunden))
	#idx = 1
	for kunde in case1:
		#frappe.publish_realtime('remove_all_abos_task', {"progress": [idx, len(kunden)]}, user=frappe.session.user)
		#idx = idx + 1
		abos = frappe.db.sql("""SELECT `name` FROM `tabPflanzenfreund Abo` WHERE `customer` = '{kunde}' AND `docstatus` = 1 AND `abo_type` IN ('Gratis-Abo', 'VIP-Abo', 'Kundenkarten-Abo (KK)', 'Kunden-Abo (OK)')""".format(kunde=kunde), as_dict=True)
		for _abo in abos:
			abo = frappe.get_doc("Pflanzenfreund Abo", _abo.name)
			abo.cancel()
			
	for kunde in case2:
		#frappe.publish_realtime('remove_all_abos_task', {"progress": [idx, len(kunden)]}, user=frappe.session.user)
		#idx = idx + 1
		abos = frappe.db.sql("""SELECT `name` FROM `tabPflanzenfreund Abo` WHERE `customer` = '{kunde}' AND `docstatus` = 1 AND `abo_type` = 'Kunden-Abo (OK)'""".format(kunde=kunde), as_dict=True)
		for _abo in abos:
			abo = frappe.get_doc("Pflanzenfreund Abo", _abo.name)
			abo.cancel()
	
	#ANLAGE KK ABO!!!!	
	for kunde in case3:
		adresse = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `parenttype` = 'Address' AND `parentfield` = 'links' AND `idx` = '1' AND `link_doctype` = 'Customer' AND `link_name` = '{kunde}'""".format(kunde=kunde), as_list=True)[0][0]
		abo = frappe.new_doc("Pflanzenfreund Abo")
		abo.update({
				"customer": kunde,
				"customer_address": adresse,
				"abo_type": "Kunden-Abo (OK)",
				"start_date": today(),
				"set_ed_manual": 1,
				"winter_ed": winter_ed,
				"feb_ed": feb_ed,
				"mar_ed": mar_ed,
				"apr_ed": apr_ed,
				"may_ed": may_ed,
				"jun_ed": jun_ed,
				"summer_ed": summer_ed,
				"sept_ed": sept_ed,
				"oct_ed": okt_ed,
				"nov_ed": nov_ed
			})
		abo.insert(ignore_permissions=True)
		abo.submit()
			
	for kunde in case4:
		#frappe.publish_realtime('remove_all_abos_task', {"progress": [idx, len(kunden)]}, user=frappe.session.user)
		#idx = idx + 1
		abos = frappe.db.sql("""SELECT `name` FROM `tabPflanzenfreund Abo` WHERE `customer` = '{kunde}' AND `docstatus` = 1 AND `abo_type` = 'Kundenkarten-Abo (KK)'""".format(kunde=kunde), as_dict=True)
		for _abo in abos:
			abo = frappe.get_doc("Pflanzenfreund Abo", _abo.name)
			abo.cancel()
	return "OK"