from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import getdate

no_cache = 1
no_sitemap = 1

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	else:
		context.user_data = frappe.db.sql("""SELECT * FROM `tabContact` WHERE `email_id` = '{user}'""".format(user=frappe.session.user), as_dict=True)[0]
		context.customer = frappe.db.sql("""SELECT `link_name` FROM `tabDynamic Link` WHERE `parent` = '{contact_name}'""".format(contact_name=context.user_data["name"]), as_list=True)[0][0]
		address_name = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `parenttype` = 'Address' AND `link_doctype` = 'Customer' AND `link_name` = '{customer}' AND `idx` = '1'""".format(customer=context.customer), as_list=True)[0][0]
		context.address = frappe.db.sql("""SELECT * FROM `tabAddress` WHERE `name` = '{address_name}'""".format(address_name=address_name), as_dict=True)[0]

@frappe.whitelist(allow_guest=True)
def place_abo_order(customer, address, abo_type, start_date, end_date, winter, feb, mar, apr, may, jun, summer, sept, oct, nov, donee_name=None, street=None, pincode=None, city=None):
	if abo_type != 'Geschenk-Abo':
		abo = frappe.get_doc({
			"doctype": "Pflanzenfreund Abo",
			"customer": customer,
			"customer_address": address,
			"abo_type": abo_type,
			"start_date": getdate(start_date),
			"end_date": getdate(end_date),
			"winter_ed": winter,
			"feb_ed": feb,
			"mar_ed": mar,
			"apr_ed": apr,
			"may_ed": may,
			"jun_ed": jun,
			"summer_ed": summer,
			"sept_ed": sept,
			"oct_ed": oct,
			"nov_ed": nov
		})
		abo.insert(ignore_permissions = True)
	else:
		abo = frappe.get_doc({
			"doctype": "Pflanzenfreund Abo",
			"customer": customer,
			"customer_address": address,
			"abo_type": abo_type,
			"start_date": getdate(start_date),
			"end_date": getdate(end_date),
			"winter_ed": winter,
			"feb_ed": feb,
			"mar_ed": mar,
			"apr_ed": apr,
			"may_ed": may,
			"jun_ed": jun,
			"summer_ed": summer,
			"sept_ed": sept,
			"oct_ed": oct,
			"nov_ed": nov,
			"donee_first_and_lastname": donee_name,
			"donee_street": street,
			"donee_pincode": pincode,
			"donee_city": city
		})
		abo.insert(ignore_permissions = True)
	return abo