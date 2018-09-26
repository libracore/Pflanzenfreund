from __future__ import unicode_literals

import frappe
from frappe.contacts.doctype.address.address import get_address_display

def get_context(context):
	# do your magic here
	pass

@frappe.whitelist()
def get_address_display(address_name):
	address_dict = frappe.get_doc("Address", address_name).as_dict()
	if not address_dict:
		return

	if not isinstance(address_dict, dict):
		address_dict = frappe.db.get_value("Address", address_dict, "*", as_dict=True) or {}

	name, template = get_address_templates(address_dict)

	try:
		return frappe.render_template(template, address_dict)
	except TemplateSyntaxError:
		frappe.throw(_("There is an error in your Address Template {0}").format(name))
		
def get_address_templates(address):
	result = frappe.db.get_value("Address Template", \
		{"country": address.get("country")}, ["name", "template"])

	if not result:
		result = frappe.db.get_value("Address Template", \
			{"is_default": 1}, ["name", "template"])

	if not result:
		frappe.throw(_("No default Address Template found. Please create a new one from Setup > Printing and Branding > Address Template."))
	else:
		return result
		
def validate(self):
	frappe.throw("okokok")
	
@frappe.whitelist()
def get_address_list(customer):
	address_list = frappe.get_list("Dynamic Link", fields=("parent"), filters={"parenttype": "Address", "link_name": customer})
	return address_list