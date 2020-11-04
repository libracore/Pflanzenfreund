# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe.utils.data import getdate

@frappe.whitelist(allow_guest=True)
def check_if_user_exist(mail):
	exist = frappe.db.sql("""SELECT COUNT(`name`) FROM `tabUser` WHERE `name` = '{mail}'""".format(mail=mail), as_list=True)[0][0]
	if exist == 1:
		return "existiert"
	else:
		return "neu"

@frappe.whitelist(allow_guest=True)
def create_address(vorname, nachname, mail, strasse, nummer, plz, ort, geschlecht, geburtsdatum):
	customer = create_customer(vorname, nachname, geschlecht)
	contact = create_contact(vorname, nachname, mail, customer, geschlecht, geburtsdatum)
	address = frappe.get_doc({
		"doctype": "Address",
		"address_title": customer,
		"address_line1": strasse + " " + nummer,
		"plz": plz,
		"pincode": plz,
		"city": ort,
		"country": "Schweiz",
		"is_primary_address": 1,
		"is_shipping_address": 1
	}).insert(ignore_permissions = True)
	
	row = address.append('links', {})
	row.link_doctype = "Customer"
	row.link_name = customer
	address.save()
	
	return "OK"


@frappe.whitelist(allow_guest=True)
def create_user(vorname, nachname, mail, pwd):
	user = frappe.get_doc({
		"doctype": "User",
		"first_name": vorname,
		"last_name": nachname,
		"email": mail,
		"user_type": "Website User",
		"send_welcome_email": 0,
		"new_password": pwd
	}).insert(ignore_permissions = True)
	
	return 'user created'
	
def create_customer(vorname, nachname, geschlecht):
	customer = frappe.get_doc({
		"doctype": "Customer",
		"first_name": vorname,
		"last_name": nachname,
		"customer_name": vorname + " " + nachname,
		"customer_type": 'Individual',
		"salutation": geschlecht
	}).insert(ignore_permissions = True)
	
	return customer.name
	
def create_contact(vorname, nachname, mail, customer, geschlecht, geburtsdatum):
	if geschlecht == "Frau":
		anrede = "Sehr geehrte Frau " + nachname
	else:
		anrede = "Sehr geehrter Herr " + nachname
	contact = frappe.get_doc({
		"doctype": "Contact",
		"first_name": vorname,
		"last_name": nachname,
		"email_id": mail,
		"user": mail,
		"salutation": geschlecht,
		"letter_salutation": anrede,
		"geburtsdatum": getdate(geburtsdatum)
	}).insert(ignore_permissions = True)
	
	row = contact.append('links', {})
	row.link_doctype = "Customer"
	row.link_name = customer
	contact.save()

	return contact.name