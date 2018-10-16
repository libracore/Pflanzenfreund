# -*- coding: utf-8 -*-
# Copyright (c) 2017-2018, libracore and contributors
# License: AGPL v3. See LICENCE

from __future__ import unicode_literals
import frappe
from frappe import throw, _, utils
from frappe.utils.background_jobs import enqueue

@frappe.whitelist()
def start_background_jop(mod=None, start=None, end=None):
	args = {
		'mod': mod,
		'start': start,
		'end': end
	}
	enqueue("pflanzenfreund.pflanzenfreund.page.abo_plausibility.utils.start_checking", queue='long', job_name=mod, timeout=1500, **args)

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
		seen_status = frappe.db.sql("""SELECT `seen` FROM `tababo plausibility log` WHERE `name` = 'Aktivierte Kunden ohne Werbe-Sperre mit Kundenkarte'""", as_list=True)[0][0]
		if seen_status != 1:
			raw_result = frappe.db.sql("""SELECT `result` FROM `tababo plausibility log` WHERE `name` = 'Aktivierte Kunden ohne Werbe-Sperre mit Kundenkarte'""", as_list=True)[0][0]
			update_seen = frappe.db.sql("""UPDATE `tababo plausibility log` SET `seen` = '1' WHERE `name` = 'Aktivierte Kunden ohne Werbe-Sperre mit Kundenkarte'""", as_list=True)
		else:
			return "abort"
	if mod == "Aktivierte Kunden ohne Werbe-Sperre ohne Kundenkarte":
		seen_status = frappe.db.sql("""SELECT `seen` FROM `tababo plausibility log` WHERE `name` = 'Aktivierte Kunden ohne Werbe-Sperre ohne Kundenkarte'""", as_list=True)[0][0]
		if seen_status != 1:
			raw_result = frappe.db.sql("""SELECT `result` FROM `tababo plausibility log` WHERE `name` = 'Aktivierte Kunden ohne Werbe-Sperre ohne Kundenkarte'""", as_list=True)[0][0]
			update_seen = frappe.db.sql("""UPDATE `tababo plausibility log` SET `seen` = '1' WHERE `name` = 'Aktivierte Kunden ohne Werbe-Sperre ohne Kundenkarte'""", as_list=True)
		else:
			return "abort"
	if mod == "Aktivierte Kunden mit Werbe-Sperre":
		seen_status = frappe.db.sql("""SELECT `seen` FROM `tababo plausibility log` WHERE `name` = 'Aktivierte Kunden mit Werbe-Sperre'""", as_list=True)[0][0]
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
		frappe.publish_realtime(event='msgprint', message='Der Background-Job für {0} wurde erfolgreich abgeschlossen, die Daten können nun analysiert werden.'.format(mod))
	
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
		frappe.publish_realtime(event='msgprint', message='Der Background-Job für {0} wurde erfolgreich abgeschlossen, die Daten können nun analysiert werden.'.format(mod))
	
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
		frappe.publish_realtime(event='msgprint', message='Der Background-Job für {0} wurde erfolgreich abgeschlossen, die Daten können nun analysiert werden.'.format(mod))
		
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
		frappe.publish_realtime(event='msgprint', message='Der Background-Job für {0} wurde erfolgreich abgeschlossen, die Daten können nun analysiert werden.'.format(mod))
		
def get_abos_of_customer(customer, werbesperre=False):
	if not werbesperre:
		abos = frappe.get_all("Pflanzenfreund Abo", {'customer': customer, 'docstatus': 1, 'end_date': (">=", utils.today()), 'abo_type': ("!=", "Geschenk-Abo")}, ["name"])
		geschenke = frappe.get_all("Pflanzenfreund Abo", {'customer': customer, 'docstatus': 1, 'end_date': (">=", utils.today()), 'abo_type': "Geschenk-Abo"}, ["name"])
	else:
		abos = frappe.get_all("Pflanzenfreund Abo", {'customer': customer, 'docstatus': 1, 'end_date': (">=", utils.today())}, ["name", "abo_type"])
		geschenke = []
	
	return abos, geschenke
	
def check_aktivierte_kunden(start, end):
	results = []
	filters = {'disabled': ("=", 0)}
	if start:
		filters['modified'] = (">=", start)
	if end:
		filters['modified'] = ("<=", end)
	
	inactive_customers = frappe.get_all("Customer", filters, ["name"])
	
	for customer in inactive_customers:
		if customer.name != 'Administrator' and customer.name != 'Guest':
			abos, geschenke = get_abos_of_customer(customer.name)
			for abo in abos:
				results.append(['Der Kunde {0} besitzt das Abonnement {1}, obwohl der Kunde Deaktiviert ist.'.format(customer.name, abo.name), 'Das Abonnement stornieren.', 'storno', customer.name, abo.name])
			
			for geschenk in geschenke:
				results.append(['Der Kunde {0} hat das Abonnement {1} verschenkt, ist selber aber deaktiviert.'.format(customer.name, geschenk.name), 'Das Geschenk-Abo in ein Gratis-Abo umwandeln.', 'geschenk_gratis', customer.name, geschenk.name])
			
	return results
	
def check_deaktivierte_kunden(start, end):
	results = []
	filters = {'disabled': ("=", 1)}
	if start:
		filters['modified'] = (">=", start)
	if end:
		filters['modified'] = ("<=", end)
	
	inactive_customers = frappe.get_all("Customer", filters, ["name"])
	
	for customer in inactive_customers:
		if customer.name != 'Administrator' and customer.name != 'Guest':
			abos, geschenke = get_abos_of_customer(customer.name)
			for abo in abos:
				results.append(['Der Kunde {0} besitzt das Abonnement {1}, obwohl der Kunde Deaktiviert ist.'.format(customer.name, abo.name), 'Das Abonnement stornieren.', 'storno', customer.name, abo.name])
			
			for geschenk in geschenke:
				results.append(['Der Kunde {0} hat das Abonnement {1} verschenkt, ist selber aber deaktiviert.'.format(customer.name, geschenk.name), 'Das Geschenk-Abo in ein Gratis-Abo umwandeln.', 'geschenk_gratis', customer.name, geschenk.name])
			
	return results
	
def check_aktivierte_kunden_mit_werbe_sperre(start, end):
	results = []
	filters = {'disabled': ("=", 0), 'code_05': ("=", "1")}
	if start:
		filters['modified'] = (">=", start)
	if end:
		filters['modified'] = ("<=", end)
	
	customers = frappe.get_all("Customer", filters, ["name"])
	
	for customer in customers:
		if customer.name != 'Administrator' and customer.name != 'Guest':
			abos, geschenke = get_abos_of_customer(customer.name, werbesperre=True)
			for abo in abos:
				if abo.abo_type != "Geschenk-Abo" and abo.abo_type != "Jahres-Abo" and abo.abo_type != "Probe-Abo":
					results.append(['Der Kunde {0} besitzt das Abonnement {1}, hat aber eine Werbe-Sperre'.format(customer.name, abo.name), 'Das Abonnement stornieren', 'storno', customer.name, abo.name])
			
	return results
	
def aktivierte_kunden_ohne_werbe_sperre_mit_kundenkarte(start, end):
	results = []
	filters = {'disabled': ("=", 0), 'code_05': ("!=", "1"), 'karte': 'J'}
	if start:
		filters['modified'] = (">=", start)
	if end:
		filters['modified'] = ("<=", end)
	
	customers = frappe.get_all("Customer", filters, ["name"])
	
	for customer in customers:
		if customer.name != 'Administrator' and customer.name != 'Guest':
			jahr_qty = 0
			probe_qty = 0
			geschenk_qty = 0
			kk_qty = 0
			jahr_qty = get_abo_or_qty(customer.name, "Jahres-Abo")
			probe_qty = get_abo_or_qty(customer.name, "Probe-Abo")
			geschenk_qty = get_abo_or_qty(customer.name, "Geschenk-Abo")
			
			if jahr_qty > 0 or probe_qty > 0 or geschenk_qty > 0:
				#abfrage aller KK abos und vorschlagen für stornierung
				abos = get_abo_or_qty(customer.name, "Kundenkarten-Abo (KK)", qty=False)
				for abo in abos:
					results.append(['Der Kunde {0} besitzt ein Kundenkarten-Abo (KK) ({1}), hat aber bereits bezahlte Abonnemente'.format(customer.name, abo.name), 'Das Abonnement stornieren', 'storno', customer.name, abo.name])
			else:
				#abfrage ob kk abo, wenn nein vorschlag für erstellung
				kk_qty = 0
				kk_qty = get_abo_or_qty(customer.name, "Kundenkarten-Abo (KK)")
				if kk_qty == 0:
					results.append(['Der Kunde {0} besitzt eine Kundenkarte, hat aber weder bezahlte Abonnemente noch ein Kundenkarten-Abo (KK)'.format(customer.name), 'Ein Kundenkarten-Abo (KK) anlegen', 'anlage_kk', customer.name, 'Kundenkarten-Abo (KK)'])
				if kk_qty > 1:
					results.append(['Der Kunde {0} besitzt mehere Kundenkarten-Abo (KK)'.format(customer.name), 'Alle bis auf ein Kundenkarten-Abo (KK) stornieren', 'none', customer.name, 'none'])
	return results
	
def get_abo_or_qty(customer, abotype, qty=True):
	abos = frappe.get_all("Pflanzenfreund Abo", {'customer': customer, 'docstatus': 1, 'end_date': (">=", utils.today()), 'abo_type': ("=", abotype)}, ["name"])
	if qty:
		abo_qty = len(abos)
		return abo_qty
	else:
		return abos

def aktivierte_kunden_ohne_werbe_sperre_ohne_kundenkarte(start, end):
	results = []
	filters = {'disabled': ("=", 0), 'code_05': ("!=", "1"), 'karte': ("!=", "J")}
	if start:
		filters['modified'] = (">=", start)
	if end:
		filters['modified'] = ("<=", end)
	
	customers = frappe.get_all("Customer", filters, ["name"])
	
	for customer in customers:
		if customer.name != 'Administrator' and customer.name != 'Guest':
			jahr_qty = 0
			probe_qty = 0
			geschenk_qty = 0
			ok_qty = 0
			jahr_qty = get_abo_or_qty(customer.name, "Jahres-Abo")
			probe_qty = get_abo_or_qty(customer.name, "Probe-Abo")
			geschenk_qty = get_abo_or_qty(customer.name, "Geschenk-Abo")
			
			if jahr_qty > 0 or probe_qty > 0 or geschenk_qty > 0:
				#abfrage aller OK abos und vorschlagen für stornierung
				abos = get_abo_or_qty(customer.name, "Kunden-Abo (OK)", qty=False)
				for abo in abos:
					results.append(['Der Kunde {0} besitzt ein Kunden-Abo (OK) ({1}), hat aber bereits bezahlte Abonnemente'.format(customer.name, abo.name), 'Das Abonnement stornieren', 'storno', customer.name, abo.name])
			else:
				#abfrage ob ok abo, wenn nein vorschlag für erstellung
				ok_qty = 0
				ok_qty = get_abo_or_qty(customer.name, "Kunden-Abo (OK)")
				if ok_qty == 0:
					results.append(['Der Kunde {0} besitzt keine Kundenkarte, hat aber weder bezahlte Abonnemente noch ein Kunden-Abo (OK)'.format(customer.name), 'Ein Kunden-Abo (OK) anlegen', 'anlage_ok', customer.name, 'Kunden-Abo (OK)'])
				if ok_qty > 1:
					results.append(['Der Kunde {0} besitzt mehere Kunden-Abo (OK)'.format(customer.name), 'Alle bis auf ein Kunden-Abo (OK) stornieren', 'none', customer.name, 'none'])
	return results
	
@frappe.whitelist()
def sammel_bereinigung(stornos, umwandlungen, anlagen_kk, anlagen_ok):
	return stornos, umwandlungen, anlagen_kk, anlagen_ok
	
@frappe.whitelist()
def storno_bereinigung(customer, abo):
	return customer, abo
	
@frappe.whitelist()
def umwandlungen_bereinigung(customer, abo):
	return customer, abo
	
@frappe.whitelist()
def anlagen_kk_bereinigung(customer):
	return customer
	
@frappe.whitelist()
def anlagen_ok_bereinigung(customer):
	return customer