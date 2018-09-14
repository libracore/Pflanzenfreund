# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PflanzenfreundAbo(Document):
	def before_save(self):
		if self.abo_type == "Geschenk-Abo":
			try:
				customer_contact_link = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `link_name` = '{0}' AND `parenttype` = 'Contact'""".format(self.customer), as_list = True)
				customer_contact = frappe.get_doc("Contact", customer_contact_link[0][0])
				self.customer_letter_salutation = customer_contact.letter_salutation
				
				donee_contact_link = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `link_name` = '{0}' AND `parenttype` = 'Contact'""".format(self.donee), as_list = True)
				donee_contact = frappe.get_doc("Contact", donee_contact_link[0][0])
				self.donee_letter_salutation = donee_contact.letter_salutation
			except:
				self.customer_letter_salutation = "Sehr geehrte Damen und Herren"
				self.donee_letter_salutation = "Sehr geehrte Damen und Herren"
			
		else:
			try:
				contact_link = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `link_name` = '{0}' AND `parenttype` = 'Contact'""".format(self.customer), as_list = True)
				contact = frappe.get_doc("Contact", contact_link[0][0])
				self.customer_letter_salutation = contact.letter_salutation
			except:
				self.customer_letter_salutation = "Sehr geehrte Damen und Herren"

@frappe.whitelist()
def create_abo(customer):
	abo = frappe.new_doc("Pflanzenfreund Abo")
	abo.update({
		"customer": customer
	})
	abo.flags.ignore_mandatory = True
	abo.save(ignore_permissions=True)
	frappe.db.commit()
	return abo.name