from __future__ import unicode_literals
import frappe
from frappe import _

no_cache = 1
no_sitemap = 1

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	else:
		context.user_data = frappe.db.sql("""SELECT * FROM `tabContact` WHERE `email_id` = '{user}'""".format(user=frappe.session.user), as_dict=True)[0]
		context.customer = frappe.db.sql("""SELECT `link_name` FROM `tabDynamic Link` WHERE `parent` = '{contact_name}'""".format(contact_name=context.user_data["name"]), as_list=True)[0][0]
		address_name = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `parenttype` = 'Address' AND `link_doctype` = 'Customer' AND `link_name` = '{customer}'""".format(customer=context.customer), as_list=True)[0][0]
		context.address = frappe.db.sql("""SELECT * FROM `tabAddress` WHERE `name` = '{address_name}'""".format(address_name=address_name), as_dict=True)[0]