# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.controllers.sales_and_purchase_return import make_return_doc

class PflanzenfreundAbo(Document):
	def before_save(self):
		if self.abo_type == "Geschenk-Abo":
			try:
				customer_contact_link = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `link_name` = '{0}' AND `parenttype` = 'Contact'""".format(self.customer), as_list = True)
				customer_contact = frappe.get_doc("Contact", customer_contact_link[0][0])
				self.customer_letter_salutation = customer_contact.salutation
				
				donee_contact_link = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `link_name` = '{0}' AND `parenttype` = 'Contact'""".format(self.donee), as_list = True)
				donee_contact = frappe.get_doc("Contact", donee_contact_link[0][0])
				self.donee_letter_salutation = donee_contact.salutation
			except:
				self.customer_letter_salutation = "Sehr geehrte Damen und Herren"
				self.donee_letter_salutation = "Sehr geehrte Damen und Herren"
			
		else:
			try:
				contact_link = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `link_name` = '{0}' AND `parenttype` = 'Contact'""".format(self.customer), as_list = True)
				contact = frappe.get_doc("Contact", contact_link[0][0])
				self.customer_letter_salutation = contact.salutation
			except:
				self.customer_letter_salutation = "Sehr geehrte Damen und Herren"

	def before_cancel(self):
		customer = frappe.get_doc("Customer", self.customer)
		disable_status = False
		if customer.disabled == 1:
			disable_status = True
			enable_customer = frappe.db.sql("""UPDATE `tabCustomer` SET `disabled` = '0' WHERE `name` = '{0}'""".format(self.customer), as_list=True)
		
		linked_sales_invoices = frappe.db.sql("""SELECT `name` FROM `tabSales Invoice` WHERE `pflanzenfreund_abo` = '{0}'""".format(self.name), as_list=True)
		remove_links_in_sales_invoice = frappe.db.sql("""UPDATE `tabSales Invoice` SET `pflanzenfreund_abo` = null WHERE `pflanzenfreund_abo` = '{0}'""".format(self.name), as_list=True)
		for _sales_invoice in linked_sales_invoices:
			sales_invoice = frappe.get_doc("Sales Invoice", _sales_invoice[0])
			sales_invoice.add_comment('Comment', 'Diese Rechnung wurde automatisiert storniert/gutgeschrieben')
			reurn_invoice = make_return_doc("Sales Invoice", sales_invoice.name)
			reurn_invoice.insert()
			reurn_invoice.add_comment('Comment', 'Diese Gutschrift wurde automatisiert erstellt')
			reurn_invoice.submit()
			frappe.db.commit()
		frappe.db.commit()
		
		if disable_status:
			disable_customer = frappe.db.sql("""UPDATE `tabCustomer` SET `disabled` = '1' WHERE `name` = '{0}'""".format(self.customer), as_list=True)
		
		for linked_abo in frappe.get_all("Pflanzenfreund Abo", filters={"new_abo": self.name}, fields=["name"]):
			remove_link = frappe.db.sql("""UPDATE `tabPflanzenfreund Abo` SET `new_abo` = '' WHERE `name` = '{0}'""".format(linked_abo.name), as_list = True)
		frappe.msgprint("Alle existierenden Abo Verknüpfungen wurden entfernt und für alle verknüpften Rechnungen eine Gutschrift erstellt.", "Entfernung Abo-Verknüpfungen & Erstellung Gutschrift")
		
@frappe.whitelist()
def create_abo(customer):
	abo = frappe.new_doc("Pflanzenfreund Abo")
	abo.update({
		"customer": customer,
		"start_date": frappe.utils.data.today(),
		"end_date": frappe.utils.data.add_years(None, 1),
		"jan_ed": 0,
		"feb_ed": 1,
		"mar_ed": 1,
		"apr_ed": 1,
		"may_ed": 1,
		"jun_ed": 1,
		"jul_ed": 0,
		"aug_ed": 0,
		"sept_ed": 1,
		"oct_ed": 1,
		"nov_ed": 1,
		"dec_ed": 0,
		"set_ed_manual": 1,
		"winter_ed": 1,
		"summer_ed": 1
	})
	abo.flags.ignore_mandatory = True
	abo.save(ignore_permissions=True)
	frappe.db.commit()
	return abo.name
