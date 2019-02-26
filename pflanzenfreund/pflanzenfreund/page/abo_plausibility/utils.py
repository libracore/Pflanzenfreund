# -*- coding: utf-8 -*-
# Copyright (c) 2017-2018, libracore and contributors
# License: AGPL v3. See LICENCE

from __future__ import unicode_literals
import frappe
from frappe import throw, _, utils
from frappe.utils.background_jobs import enqueue
from erpnext.controllers.sales_and_purchase_return import make_return_doc

@frappe.whitelist()
def start_background_jop(mod=None, start=None, end=None):
	args = {
		'mod': mod,
		'start': start,
		'end': end
	}
	enqueue("pflanzenfreund.pflanzenfreund.page.abo_plausibility.utils.start_checking", queue='long', job_name=mod, timeout=3000, **args)

@frappe.whitelist()
def read_log(mod):
	result = []
	if mod == "Deaktivierte Kunden":
		try:
			seen_status = frappe.db.sql("""SELECT `seen` FROM `tababo plausibility log` WHERE `name` = 'Deaktivierte Kunden'""", as_list=True)[0][0]
		except:
			return 'not found'
		print(seen_status)
		if seen_status != 1:
			raw_result = frappe.db.sql("""SELECT `result` FROM `tababo plausibility log` WHERE `name` = 'Deaktivierte Kunden'""", as_list=True)[0][0]
			update_seen = frappe.db.sql("""UPDATE `tababo plausibility log` SET `seen` = '1' WHERE `name` = 'Deaktivierte Kunden'""", as_list=True)
		else:
			return "abort"
	if mod == "Aktivierte Kunden ohne Werbe-Sperre mit Kundenkarte":
		try:
			seen_status = frappe.db.sql("""SELECT `seen` FROM `tababo plausibility log` WHERE `name` = 'Aktivierte Kunden ohne Werbe-Sperre mit Kundenkarte'""", as_list=True)[0][0]
		except:
			return 'not found'
		if seen_status != 1:
			raw_result = frappe.db.sql("""SELECT `result` FROM `tababo plausibility log` WHERE `name` = 'Aktivierte Kunden ohne Werbe-Sperre mit Kundenkarte'""", as_list=True)[0][0]
			update_seen = frappe.db.sql("""UPDATE `tababo plausibility log` SET `seen` = '1' WHERE `name` = 'Aktivierte Kunden ohne Werbe-Sperre mit Kundenkarte'""", as_list=True)
		else:
			return "abort"
	if mod == "Aktivierte Kunden ohne Werbe-Sperre ohne Kundenkarte":
		try:
			seen_status = frappe.db.sql("""SELECT `seen` FROM `tababo plausibility log` WHERE `name` = 'Aktivierte Kunden ohne Werbe-Sperre ohne Kundenkarte'""", as_list=True)[0][0]
		except:
			return 'not found'
		if seen_status != 1:
			raw_result = frappe.db.sql("""SELECT `result` FROM `tababo plausibility log` WHERE `name` = 'Aktivierte Kunden ohne Werbe-Sperre ohne Kundenkarte'""", as_list=True)[0][0]
			update_seen = frappe.db.sql("""UPDATE `tababo plausibility log` SET `seen` = '1' WHERE `name` = 'Aktivierte Kunden ohne Werbe-Sperre ohne Kundenkarte'""", as_list=True)
		else:
			return "abort"
	if mod == "Aktivierte Kunden mit Werbe-Sperre":
		try:
			seen_status = frappe.db.sql("""SELECT `seen` FROM `tababo plausibility log` WHERE `name` = 'Aktivierte Kunden mit Werbe-Sperre'""", as_list=True)[0][0]
		except:
			return 'not found'
		if seen_status != 1:
			raw_result = frappe.db.sql("""SELECT `result` FROM `tababo plausibility log` WHERE `name` = 'Aktivierte Kunden mit Werbe-Sperre'""", as_list=True)[0][0]
			update_seen = frappe.db.sql("""UPDATE `tababo plausibility log` SET `seen` = '1' WHERE `name` = 'Aktivierte Kunden mit Werbe-Sperre'""", as_list=True)
		else:
			return "abort"
	__result = raw_result.split("*/****")
	for _result in __result:
		_result = _result.split("*/*")
		result.append(_result)
	return result

def start_checking(mod=None, start=None, end=None):
	if mod == "Deaktivierte Kunden":
		delete = frappe.db.sql("""DELETE FROM `tababo plausibility log` WHERE `name` = 'Deaktivierte Kunden'""", as_list=True)
		string_array = ""
		for item in check_deaktivierte_kunden(start, end):
			sub_string_array = ""
			for sub_item in item:
				sub_string_array += str(sub_item) + "*/*"
			string_array += sub_string_array + "***"
		new_log = frappe.get_doc({
			"doctype": "abo plausibility log",
			"type": "Deaktivierte Kunden",
			"result": string_array or "empty"
		})
		new_log.insert()
		frappe.db.commit()
	
	if mod == "Aktivierte Kunden mit Werbe-Sperre":
		delete = frappe.db.sql("""DELETE FROM `tababo plausibility log` WHERE `name` = 'Aktivierte Kunden mit Werbe-Sperre'""", as_list=True)
		string_array = ""
		for item in check_aktivierte_kunden_mit_werbe_sperre(start, end):
			sub_string_array = ""
			for sub_item in item:
				sub_string_array += str(sub_item) + "*/*"
			string_array += sub_string_array + "***"
		new_log = frappe.get_doc({
			"doctype": "abo plausibility log",
			"type": "Aktivierte Kunden mit Werbe-Sperre",
			"result": string_array or "empty"
		})
		new_log.insert()
		frappe.db.commit()
	
	if mod == "Aktivierte Kunden ohne Werbe-Sperre mit Kundenkarte":
		delete = frappe.db.sql("""DELETE FROM `tababo plausibility log` WHERE `name` = 'Aktivierte Kunden ohne Werbe-Sperre mit Kundenkarte'""", as_list=True)
		string_array = ""
		for item in aktivierte_kunden_ohne_werbe_sperre_mit_kundenkarte(start, end):
			sub_string_array = ""
			for sub_item in item:
				sub_string_array += str(sub_item) + "*/*"
			string_array += sub_string_array + "***"
		new_log = frappe.get_doc({
			"doctype": "abo plausibility log",
			"type": "Aktivierte Kunden ohne Werbe-Sperre mit Kundenkarte",
			"result": string_array or "empty"
		})
		new_log.insert()
		frappe.db.commit()
		
	if mod == "Aktivierte Kunden ohne Werbe-Sperre ohne Kundenkarte":
		delete = frappe.db.sql("""DELETE FROM `tababo plausibility log` WHERE `name` = 'Aktivierte Kunden ohne Werbe-Sperre ohne Kundenkarte'""", as_list=True)
		string_array = ""
		for item in aktivierte_kunden_ohne_werbe_sperre_ohne_kundenkarte(start, end):
			sub_string_array = ""
			for sub_item in item:
				sub_string_array += str(sub_item) + "*/*"
			string_array += sub_string_array + "***"
		new_log = frappe.get_doc({
			"doctype": "abo plausibility log",
			"type": "Aktivierte Kunden ohne Werbe-Sperre ohne Kundenkarte",
			"result": string_array or "empty"
		})
		new_log.insert()
		frappe.db.commit()
	
	message = 'Der Background-Job für {0} wurde erfolgreich abgeschlossen, die Daten können nun analysiert werden.'.format(mod)
	frappe.publish_realtime(event='msgprint',message=message,user=frappe.session.user)
		
def get_abos_of_customer(customer, werbesperre=False):
	if not werbesperre:
		abos = frappe.get_all("Pflanzenfreund Abo", {'customer': customer, 'docstatus': 1, 'end_date': (">=", utils.today()), 'abo_type': ("!=", "Geschenk-Abo")}, ["name"])
		geschenke = frappe.get_all("Pflanzenfreund Abo", {'customer': customer, 'docstatus': 1, 'end_date': (">=", utils.today()), 'abo_type': "Geschenk-Abo"}, ["name"])
	else:
		abos = frappe.get_all("Pflanzenfreund Abo", {'customer': customer, 'docstatus': 1, 'end_date': (">=", utils.today())}, ["name", "abo_type"])
		geschenke = []
	
	return abos, geschenke
	
def check_aktivierte_kunden(start, end):
	max_results = 1000
	control_results = 0
	results = []
	filters = {'disabled': ("=", 0)}
	if start:
		filters['modified'] = (">=", start)
	if end:
		filters['modified'] = ("<=", end)
	
	inactive_customers = frappe.get_all("Customer", filters, ["name"])
	
	for customer in inactive_customers:
		if control_results == max_results:
			break
		if customer.name != 'Administrator' and customer.name != 'Guest':
			abos, geschenke = get_abos_of_customer(customer.name)
			for abo in abos:
				results.append(['Der Kunde <a href="/desk#Form/Customer/{0}">{0}</a> besitzt das Abonnement <a href="/desk#Form/Pflanzenfreund Abo/{1}">{1}</a>, obwohl der Kunde Deaktiviert ist.'.format(customer.name, abo.name), 'Das Abonnement stornieren.', 'storno', customer.name, abo.name])
				control_results += 1
				if control_results == max_results:
					break
			for geschenk in geschenke:
				results.append(['Der Kunde {0} hat das Abonnement {1} verschenkt, ist selber aber deaktiviert.'.format(customer.name, geschenk.name), 'Das Geschenk-Abo in ein Gratis-Abo umwandeln.', 'geschenk_gratis', customer.name, geschenk.name])
				control_results += 1
				if control_results == max_results:
					break
	return results
	
def check_deaktivierte_kunden(start, end):
	max_results = 1000
	control_results = 0
	results = []
	filters = {'disabled': ("=", 1)}
	if start:
		filters['modified'] = (">=", start)
	if end:
		filters['modified'] = ("<=", end)
	
	inactive_customers = frappe.get_all("Customer", filters, ["name"])
	
	for customer in inactive_customers:
		if control_results == max_results:
			break
		if customer.name != 'Administrator' and customer.name != 'Guest':
			abos, geschenke = get_abos_of_customer(customer.name)
			for abo in abos:
				results.append(['Der Kunde {0} besitzt das Abonnement {1}, obwohl der Kunde Deaktiviert ist.'.format(customer.name, abo.name), 'Das Abonnement stornieren.', 'storno', customer.name, abo.name])
				control_results += 1
				if control_results == max_results:
					break
			for geschenk in geschenke:
				results.append(['Der Kunde {0} hat das Abonnement {1} verschenkt, ist selber aber deaktiviert.'.format(customer.name, geschenk.name), 'Das Geschenk-Abo in ein Gratis-Abo umwandeln.', 'geschenk_gratis', customer.name, geschenk.name])
				control_results += 1
				if control_results == max_results:
					break
	return results
	
def check_aktivierte_kunden_mit_werbe_sperre(start, end):
	max_results = 1000
	control_results = 0
	results = []
	filters = {'disabled': ("=", 0), 'code_05': ("=", "1")}
	if start:
		filters['modified'] = (">=", start)
	if end:
		filters['modified'] = ("<=", end)
	
	customers = frappe.get_all("Customer", filters, ["name"])
	
	for customer in customers:
		if control_results == max_results:
			break
		if customer.name != 'Administrator' and customer.name != 'Guest':
			abos, geschenke = get_abos_of_customer(customer.name, werbesperre=True)
			for abo in abos:
				if abo.abo_type != "Geschenk-Abo" and abo.abo_type != "Jahres-Abo" and abo.abo_type != "Probe-Abo" and abo.abo_type != "VIP-Abo":
					results.append(['Der Kunde {0} besitzt das Abonnement {1}, hat aber eine Werbe-Sperre'.format(customer.name, abo.name), 'Das Abonnement stornieren', 'storno', customer.name, abo.name])
					control_results += 1
					if control_results == max_results:
						break
	return results
	
def aktivierte_kunden_ohne_werbe_sperre_mit_kundenkarte(start, end):
	max_results = 1000
	control_results = 0
	results = []
	filters = {'disabled': ("=", 0), 'code_05': ("!=", "1"), 'karte': 'J'}
	if start:
		filters['modified'] = (">=", start)
	if end:
		filters['modified'] = ("<=", end)
	
	customers = frappe.get_all("Customer", filters, ["name"])
	
	for customer in customers:
		if control_results == max_results:
			break
		if customer.name != 'Administrator' and customer.name != 'Guest':
			jahr_qty = 0
			probe_qty = 0
			geschenk_qty = 0
			kk_qty = 0
			ok_qty = 0
			
			jahr_qty, probe_qty, geschenk_qty, kk_qty, ok_qty = get_abo_qty_sql(customer.name)
			
			#jahr_qty = get_abo_or_qty(customer.name, "Jahres-Abo")
			#probe_qty = get_abo_or_qty(customer.name, "Probe-Abo")
			#geschenk_qty = get_abo_or_qty(customer.name, "Geschenk-Abo")
			
			if jahr_qty > 0 or probe_qty > 0 or geschenk_qty > 0:
				#abfrage aller KK abos und vorschlagen für stornierung
				#abos = get_abo_or_qty(customer.name, "Kundenkarten-Abo (KK)", qty=False)
				abos = frappe.get_all("Pflanzenfreund Abo", {'customer': customer.name, 'docstatus': 1, 'end_date': (">=", utils.today()), 'abo_type': "Kundenkarten-Abo (KK)"}, ["name"])
				for abo in abos:
					results.append(['Der Kunde {0} besitzt ein Kundenkarten-Abo (KK) ({1}), hat aber bereits bezahlte Abonnemente'.format(customer.name, abo.name), 'Das Abonnement stornieren', 'storno', customer.name, abo.name])
					control_results += 1
					if control_results == max_results:
						break
			else:
				#abfrage ob kk abo, wenn nein vorschlag für erstellung
				#kk_qty = 0
				#kk_qty = get_abo_or_qty(customer.name, "Kundenkarten-Abo (KK)")
				if kk_qty == 0:
					results.append(['Der Kunde {0} besitzt eine Kundenkarte, hat aber weder bezahlte Abonnemente noch ein Kundenkarten-Abo (KK)'.format(customer.name), 'Ein Kundenkarten-Abo (KK) anlegen', 'anlage_kk', customer.name, 'Kundenkarten-Abo (KK)'])
					control_results += 1
					if control_results == max_results:
						break
				if kk_qty > 1:
					results.append(['Der Kunde {0} besitzt mehere Kundenkarten-Abo (KK)'.format(customer.name), 'Alle bis auf ein Kundenkarten-Abo (KK) stornieren', 'none', customer.name, 'none'])
					control_results += 1
					if control_results == max_results:
						break
			if ok_qty > 0:
				#abfrage aller OK abos und vorschlagen für stornierung
				#abos = get_abo_or_qty(customer.name, "Kunden-Abo (OK)", qty=False)
				abos = frappe.get_all("Pflanzenfreund Abo", {'customer': customer.name, 'docstatus': 1, 'end_date': (">=", utils.today()), 'abo_type': "Kunden-Abo (OK)"}, ["name"])
				for abo in abos:
					results.append(['Der Kunde {0} besitzt ein Kunden-Abo (OK) ({1}), hat aber eine Kundenkarte'.format(customer.name, abo.name), 'Das Abonnement stornieren', 'storno', customer.name, abo.name])
					control_results += 1
					if control_results == max_results:
						break
	return results
	
# def get_abo_or_qty(customer, abotype, qty=True):
	# abos = frappe.get_all("Pflanzenfreund Abo", {'customer': customer, 'docstatus': 1, 'end_date': (">=", utils.today()), 'abo_type': ("=", abotype)}, ["name"])
	# if qty:
		# abo_qty = len(abos)
		# return abo_qty
	# else:
		# return abos
		
def get_abo_qty_sql(customer):
	results = frappe.db.sql("""SELECT (SELECT COUNT(`name`) FROM `tabPflanzenfreund Abo` WHERE `customer` = '{0}' AND `docstatus` = '1' AND `abo_type` = 'Jahres-Abo' AND `end_date` >= {1}),
		(SELECT COUNT(`name`) FROM `tabPflanzenfreund Abo` WHERE `customer` = '{0}' AND `docstatus` = '1' AND `abo_type` = 'Probe-Abo' AND `end_date` >= {1}),
		(SELECT COUNT(`name`) FROM `tabPflanzenfreund Abo` WHERE `donee` = '{0}' AND `docstatus` = '1' AND `abo_type` = 'Geschenk-Abo' AND `end_date` >= {1}),
		(SELECT COUNT(`name`) FROM `tabPflanzenfreund Abo` WHERE `customer` = '{0}' AND `docstatus` = '1' AND `abo_type` = 'Kundenkarten-Abo (KK)'),
		(SELECT COUNT(`name`) FROM `tabPflanzenfreund Abo` WHERE `customer` = '{0}' AND `docstatus` = '1' AND `abo_type` = 'Kunden-Abo (OK)')""".format(customer, utils.today()), as_list=True)[0]
	return results[0], results[1], results[2], results[3], results[4]

def aktivierte_kunden_ohne_werbe_sperre_ohne_kundenkarte(start, end):
	max_results = 1000
	control_results = 0
	results = []
	filters = {'disabled': ("=", 0), 'code_05': ("!=", "1"), 'karte': ("!=", "J")}
	if start:
		filters['modified'] = (">=", start)
	if end:
		filters['modified'] = ("<=", end)
	
	customers = frappe.get_all("Customer", filters, ["name"])
	
	for customer in customers:
		if control_results == max_results:
			break
		if customer.name != 'Administrator' and customer.name != 'Guest':
			jahr_qty = 0
			probe_qty = 0
			geschenk_qty = 0
			ok_qty = 0
			kk_qty = 0
			
			jahr_qty, probe_qty, geschenk_qty, kk_qty, ok_qty = get_abo_qty_sql(customer.name)
			
			#jahr_qty = get_abo_or_qty(customer.name, "Jahres-Abo")
			#probe_qty = get_abo_or_qty(customer.name, "Probe-Abo")
			#geschenk_qty = get_abo_or_qty(customer.name, "Geschenk-Abo")
			
			if jahr_qty > 0 or probe_qty > 0 or geschenk_qty > 0:
				#abfrage aller OK abos und vorschlagen für stornierung
				#abos = get_abo_or_qty(customer.name, "Kunden-Abo (OK)", qty=False)
				abos = frappe.get_all("Pflanzenfreund Abo", {'customer': customer.name, 'docstatus': 1, 'end_date': (">=", utils.today()), 'abo_type': "Kunden-Abo (OK)"}, ["name"])
				for abo in abos:
					results.append(['Der Kunde {0} besitzt ein Kunden-Abo (OK) ({1}), hat aber bereits bezahlte Abonnemente'.format(customer.name, abo.name), 'Das Abonnement stornieren', 'storno', customer.name, abo.name])
					control_results += 1
					if control_results == max_results:
						break
			else:
				#abfrage ob ok abo, wenn nein vorschlag für erstellung
				#ok_qty = 0
				#ok_qty = get_abo_or_qty(customer.name, "Kunden-Abo (OK)")
				if ok_qty == 0:
					results.append(['Der Kunde {0} besitzt keine Kundenkarte, hat aber weder bezahlte Abonnemente noch ein Kunden-Abo (OK)'.format(customer.name), 'Ein Kunden-Abo (OK) anlegen', 'anlage_ok', customer.name, 'Kunden-Abo (OK)'])
					control_results += 1
					if control_results == max_results:
						break
				if ok_qty > 1:
					results.append(['Der Kunde {0} besitzt mehere Kunden-Abo (OK)'.format(customer.name), 'Alle bis auf ein Kunden-Abo (OK) stornieren', 'none', customer.name, 'none'])
					control_results += 1
					if control_results == max_results:
						break
			if kk_qty > 0:
				abos = frappe.get_all("Pflanzenfreund Abo", {'customer': customer.name, 'docstatus': 1, 'end_date': (">=", utils.today()), 'abo_type': "Kundenkarten-Abo (KK)"}, ["name"])
				for abo in abos:
					results.append(['Der Kunde {0} besitzt ein Kundenkarten-Abo (KK) ({1}), hat aber keine Kundenkarte'.format(customer.name, abo.name), 'Das Abonnement stornieren', 'storno', customer.name, abo.name])
					control_results += 1
					if control_results == max_results:
						break
	return results
	

def sammel_bereinigung(_stornos, _umwandlungen, _anlagen_kk, _anlagen_ok):
	stornos = _stornos.split("**+**")
	umwandlungen = _umwandlungen.split("**+**")
	anlagen_kk = _anlagen_kk.split("**+**")
	anlagen_ok = _anlagen_ok.split("**+**")
	#throw(_stornos)
	for storno in stornos:
		try:
			customer, abo = storno.split("**-**")
			storno_bereinigung(customer, abo)
		except:
			continue
			
	for umwandlung in umwandlungen:
		try:
			customer, abo = umwandlung.split("**-**")
			umwandlungen_bereinigung(customer, abo)
		except:
			continue
		
	for anlagen_kk_item in anlagen_kk:
		if len(anlagen_kk_item) > 4:
			anlagen_kk_bereinigung(anlagen_kk_item)
		
	for anlagen_ok_item in anlagen_ok:
		if len(anlagen_ok_item) > 4:
			anlagen_ok_bereinigung(anlagen_ok_item)
		
	#return stornos, umwandlungen, anlagen_kk, anlagen_ok
	message = 'Der Background-Job Sammel Bereinigung wurde erfolgreich abgeschlossen, die Daten sind nun bereinigt.'
	frappe.publish_realtime(event='msgprint',message=message,user=frappe.session.user)
	
@frappe.whitelist()
def sammel_bereinigung_background(stornos, umwandlungen, anlagen_kk, anlagen_ok):
	args = {
		'_stornos': stornos,
		'_umwandlungen': umwandlungen,
		'_anlagen_kk': anlagen_kk,
		'_anlagen_ok': anlagen_ok
	}
	enqueue("pflanzenfreund.pflanzenfreund.page.abo_plausibility.utils.sammel_bereinigung", queue='long', job_name='Sammel Bereinigung', timeout=3000, **args)
	#return "background"
	
@frappe.whitelist()
def storno_bereinigung(customer, abo):
	to_storno = frappe.get_doc("Pflanzenfreund Abo", abo)
	customer = frappe.get_doc("Customer", to_storno.customer)
	disable_status = False
	if customer.disabled == 1:
		disable_status = True
		enable_customer = frappe.db.sql("""UPDATE `tabCustomer` SET `disabled` = '0' WHERE `name` = '{0}'""".format(to_storno.customer), as_list=True)
	
	to_storno.add_comment('Comment', 'Dieses Abo wurde automatisiert storniert')
	linked_sales_invoices = frappe.db.sql("""SELECT `name` FROM `tabSales Invoice` WHERE `pflanzenfreund_abo` = '{0}'""".format(to_storno.name), as_list=True)
	remove_links_in_sales_invoice = frappe.db.sql("""UPDATE `tabSales Invoice` SET `pflanzenfreund_abo` = null WHERE `pflanzenfreund_abo` = '{0}'""".format(to_storno.name), as_list=True)
	for _sales_invoice in linked_sales_invoices:
		sales_invoice = frappe.get_doc("Sales Invoice", _sales_invoice[0])
		sales_invoice.add_comment('Comment', 'Diese Rechnung wurde automatisiert storniert/gutgeschrieben')
		reurn_invoice = make_return_doc("Sales Invoice", sales_invoice.name)
		reurn_invoice.insert()
		reurn_invoice.add_comment('Comment', 'Diese Gutschrift wurde automatisiert erstellt')
		reurn_invoice.submit()
		frappe.db.commit()
	to_storno.cancel()
	frappe.db.commit()
	
	if disable_status:
		disable_customer = frappe.db.sql("""UPDATE `tabCustomer` SET `disabled` = '1' WHERE `name` = '{0}'""".format(to_storno.customer), as_list=True)
	
	return customer, abo
	
	
@frappe.whitelist()
def umwandlungen_bereinigung(customer, abo):
	old_abo = frappe.get_doc("Pflanzenfreund Abo", abo)
	new_abo = frappe.get_doc({
		"doctype": "Pflanzenfreund Abo",
		"customer": old_abo.donee,
		"customer_address": old_abo.donee_address,
		"abo_type": "Gratis-Abo",
		"start_date": old_abo.start_date,
		"end_date": old_abo.end_date,
		"jan_ed": old_abo.jan_ed,
		"feb_ed": old_abo.feb_ed,
		"mar_ed": old_abo.mar_ed,
		"apr_ed": old_abo.apr_ed,
		"may_ed": old_abo.may_ed,
		"jun_ed": old_abo.jun_ed,
		"jul_ed": old_abo.jul_ed,
		"aug_ed": old_abo.aug_ed,
		"sept_ed": old_abo.sept_ed,
		"oct_ed": old_abo.oct_ed,
		"nov_ed": old_abo.nov_ed,
		"dec_ed": old_abo.dec_ed,
		"winter_ed": old_abo.winter_ed,
		"summer_ed": old_abo.summer_ed,
		"set_ed_manual": old_abo.set_ed_manual
	})
	new_abo.insert()
	new_abo.submit()
	frappe.db.commit()
	old_abo.add_comment('Comment', 'Dieses Abo wurde automatisiert storniert und in ein Gratis-Abo ({0}) umgewandelt'.format(new_abo.name))
	new_abo.add_comment('Comment', 'Dieses Abo wurde automatisiert erstellt, basierend auf dem Geschenk-Abo {0}'.format(old_abo.name))
	remove_links_in_sales_invoice = frappe.db.sql("""UPDATE `tabSales Invoice` SET `pflanzenfreund_abo` = null WHERE `pflanzenfreund_abo` = '{0}'""".format(old_abo.name), as_list=True)
	old_abo.cancel()
	
	return new_abo
	
@frappe.whitelist()
def anlagen_kk_bereinigung(customer):
	address = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `parenttype` = 'Address' AND `link_name` = '{0}' ORDER BY `idx` ASC LIMIT 1""".format(customer), as_list=True)[0][0]
	new_kk_abo = frappe.get_doc({
		"doctype": "Pflanzenfreund Abo",
		"customer": customer,
		"customer_address": address,
		"abo_type": "Kundenkarten-Abo (KK)",
		"start_date": utils.today(),
		"end_date": ''
	})
	new_kk_abo.update(get_editions(kk=True))
	new_kk_abo.insert()
	new_kk_abo.submit()
	frappe.db.commit()
	new_kk_abo.add_comment('Comment', 'Dieses Abo wurde automatisiert angelegt')
	return new_kk_abo
	
@frappe.whitelist()
def anlagen_ok_bereinigung(customer):
	address = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `parenttype` = 'Address' AND `link_name` = '{0}' ORDER BY `idx` ASC LIMIT 1""".format(customer), as_list=True)[0][0]
	new_ok_abo = frappe.get_doc({
		"doctype": "Pflanzenfreund Abo",
		"customer": customer,
		"customer_address": address,
		"abo_type": "Kunden-Abo (OK)",
		"start_date": utils.today(),
		"end_date": ''
	})
	new_ok_abo.update(get_editions(ok=True))
	new_ok_abo.insert()
	new_ok_abo.submit()
	frappe.db.commit()
	new_ok_abo.add_comment('Comment', 'Dieses Abo wurde automatisiert angelegt')
	return new_ok_abo
	
def get_editions(ok=False, kk=False):
	today = utils.today()
	year, month, day = today.split('-')
	if int(day) > 15:
		month = str(int(month) + 1)
		if int(month) > 12:
			month = str(1)
	
	if ok:
		if month == '1':
			editions = {
				"feb_ed": 1,
				"summer_ed": 1
			}
			return editions
			
		if month == '2':
			editions = {
				"mar_ed": 1,
				"sept_ed": 1
			}
			return editions
			
		if month == '3':
			editions = {
				"apr_ed": 1,
				"oct_ed": 1
			}
			return editions
			
		if month == '4':
			editions = {
				"may_ed": 1,
				"nov_ed": 1
			}
			return editions
			
		if month == '5':
			editions = {
				"jun_ed": 1,
				"winter_ed": 1
			}
			return editions
			
		if month == '6':
			editions = {
				"summer_ed": 1,
				"feb_ed": 1
			}
			return editions
			
		if month == '7':
			editions = {
				"sept_ed": 1,
				"mar_ed": 1
			}
			return editions
			
		if month == '8':
			editions = {
				"apr_ed": 1,
				"oct_ed": 1
			}
			return editions
			
		if month == '9':
			editions = {
				"may_ed": 1,
				"nov_ed": 1
			}
			return editions
			
		if month == '10':
			editions = {
				"jun_ed": 1,
				"winter_ed": 1
			}
			return editions
			
		if month == '11':
			editions = {
				"summer_ed": 1,
				"feb_ed": 1
			}
			return editions
			
		if month == '12':
			editions = {
				"sept_ed": 1,
				"mar_ed": 1
			}
			return editions
	
	if kk:
		if month == '1':
			editions = {
				"feb_ed": 1,
				"sept_ed": 1,
				"may_ed": 1
			}
			return editions
			
		if month == '2':
			editions = {
				"mar_ed": 1,
				"oct_ed": 1,
				"jun_ed": 1
			}
			return editions
			
		if month == '3':
			editions = {
				"apr_ed": 1,
				"nov_ed": 1,
				"summer_ed": 1
			}
			return editions
			
		if month == '4':
			editions = {
				"may_ed": 1,
				"winter_ed": 1,
				"sept_ed": 1
			}
			return editions
			
		if month == '5':
			editions = {
				"jun_ed": 1,
				"feb_ed": 1,
				"oct_ed": 1
			}
			return editions
			
		if month == '6':
			editions = {
				"summer_ed": 1,
				"mar_ed": 1,
				"nov_ed": 1
			}
			return editions
			
		if month == '7':
			editions = {
				"sept_ed": 1,
				"apr_ed": 1,
				"winter_ed": 1
			}
			return editions
			
		if month == '8':
			editions = {
				"sept_ed": 1,
				"mar_ed": 1,
				"nov_ed": 1
			}
			return editions
			
		if month == '9':
			editions = {
				"oct_ed": 1,
				"may_ed": 1,
				"feb_ed": 1
			}
			return editions
			
		if month == '10':
			editions = {
				"nov_ed": 1,
				"jun_ed": 1,
				"mar_ed": 1
			}
			return editions
			
		if month == '11':
			editions = {
				"winter_ed": 1,
				"summer_ed": 1,
				"apr_ed": 1
			}
			return editions
			
		if month == '12':
			editions = {
				"feb_ed": 1,
				"oct_ed": 1,
				"may_ed": 1
			}
			return editions
