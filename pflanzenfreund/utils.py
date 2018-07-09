#
# utils.py
#
# Copyright (C) libracore, 2017
# https://www.libracore.com or https://github.com/libracore
#
# For information on ERPNext, refer to https://erpnext.org/
#
# Execute with $ bench execute pflanzenfreund.utils.<function>
#
from __future__ import unicode_literals
import frappe, os, json
from frappe import throw, _
from frappe.website.doctype.website_settings.website_settings import get_website_settings
from frappe.website.router import get_page_context
from frappe.model.document import Document
from frappe.utils import cint, flt, get_fullname, cstr
from erpnext.shopping_cart.doctype.shopping_cart_settings.shopping_cart_settings import get_shopping_cart_settings
from frappe.utils.nestedset import get_root_of

def get_navbar_items(position):
	if position == 'top':
		navbar_items = get_top_navbar_items('top_bar_items')
	
	if position == 'bottom':
		navbar_items = get_bottom_navbar_items('bottom_bar_items')
	
	return navbar_items
	
def get_top_navbar_items(parentfield):
	all_top_items = frappe.db.sql("""\
		select * from `tabTop Bar Item`
		where parent='Website Settings' and parentfield= %s
		order by idx asc""", parentfield, as_dict=1)

	top_items = [d for d in all_top_items if not d['parent_label']]

	# attach child items to top bar
	for d in all_top_items:
		if d['parent_label']:
			for t in top_items:
				if t['label']==d['parent_label']:
					if not 'child_items' in t:
						t['child_items'] = []
					t['child_items'].append(d)
					break
	return top_items

def get_bottom_navbar_items(parentfield):
	all_top_items = frappe.db.sql("""\
		select * from `tabPflanzenfreund Navbar Bottom Items`
		where parent='Website Settings' and parentfield= %s
		order by idx asc""", parentfield, as_dict=1)

	top_items = [d for d in all_top_items if not d['parent_label']]

	# attach child items to top bar
	for d in all_top_items:
		if d['parent_label']:
			for t in top_items:
				if t['label']==d['parent_label']:
					if not 'child_items' in t:
						t['child_items'] = []
					t['child_items'].append(d)
					break
	return top_items

def get_footer_items(parentfield):
	parentfield = "footer_items"
	all_footer_items = frappe.db.sql("""\
		select * from `tabTop Bar Item`
		where parent='Website Settings' and parentfield= %s
		order by idx asc""", parentfield, as_dict=1)

	footer_items = [d for d in all_footer_items if not d['parent_label']]

	# attach child items to top bar
	for d in all_footer_items:
		if d['parent_label']:
			for t in footer_items:
				if t['label']==d['parent_label']:
					if not 'child_items' in t:
						t['child_items'] = []
					t['child_items'].append(d)
					break
	return footer_items

def get_footer_social_items(parentfield):
	parentfield = "footer_social_media"
	all_footer_items = frappe.db.sql("""\
		select * from `tabPflanzenfreund Footer Social Media`
		where parent='Website Settings' and parentfield= %s
		order by idx asc""", parentfield, as_dict=1)

	footer_items = [d for d in all_footer_items if not d['parent_label']]

	# attach child items to top bar
	for d in all_footer_items:
		if d['parent_label']:
			for t in footer_items:
				if t['label']==d['parent_label']:
					if not 'child_items' in t:
						t['child_items'] = []
					t['child_items'].append(d)
					break
	return footer_items

def get_website_settings():
	pflanzenfreund_settings = frappe.get_doc("Website Settings", "Website Settings")
	return pflanzenfreund_settings

def get_footer_brand():
	return "<img src='{0}' style='max-height:84px;width:auto;'>".format(get_website_settings().footer_brand)

def get_footer_description():
	return get_website_settings().address
	
def get_all_addresses():
	party = get_party()
	address_names = frappe.db.get_all('Dynamic Link', fields=('parent'),
		filters=dict(parenttype='Address', link_doctype=party.doctype, link_name=party.name))
	
	return address_names

def get_party(user=None):
	if not user:
		user = frappe.session.user

	contact_name = frappe.db.get_value("Contact", {"email_id": user})
	party = None

	if contact_name:
		contact = frappe.get_doc('Contact', contact_name)
		if contact.links:
			party_doctype = contact.links[0].link_doctype
			party = contact.links[0].link_name

	cart_settings = frappe.get_doc("Shopping Cart Settings")

	debtors_account = ''

	if cart_settings.enable_checkout:
		debtors_account = get_debtors_account(cart_settings)

	if party:
		return frappe.get_doc(party_doctype, party)

	else:
		if not cart_settings.enabled:
			frappe.local.flags.redirect_location = "/contact"
			raise frappe.Redirect
		customer = frappe.new_doc("Customer")
		fullname = get_fullname(user)
		customer.update({
			"customer_name": fullname,
			"customer_type": "Individual",
			"customer_group": get_shopping_cart_settings().default_customer_group,
			"territory": get_root_of("Territory")
		})

		if debtors_account:
			customer.update({
				"accounts": [{
					"company": cart_settings.company,
					"account": debtors_account
				}]
			})

		customer.flags.ignore_mandatory = True
		customer.insert(ignore_permissions=True)

		contact = frappe.new_doc("Contact")
		contact.update({
			"first_name": fullname,
			"email_id": user
		})
		contact.append('links', dict(link_doctype='Customer', link_name=customer.name))
		contact.flags.ignore_mandatory = True
		contact.insert(ignore_permissions=True)

		return customer
		
def get_debtors_account(cart_settings):
	payment_gateway_account_currency = \
		frappe.get_doc("Payment Gateway Account", cart_settings.payment_gateway_account).currency

	account_name = _("Debtors ({0})".format(payment_gateway_account_currency))

	debtors_account_name = get_account_name("Receivable", "Asset", is_group=0,\
		account_currency=payment_gateway_account_currency, company=cart_settings.company)

	if not debtors_account_name:
		debtors_account = frappe.get_doc({
			"doctype": "Account",
			"account_type": "Receivable",
			"root_type": "Asset",
			"is_group": 0,
			"parent_account": get_account_name(root_type="Asset", is_group=1, company=cart_settings.company),
			"account_name": account_name,
			"currency": payment_gateway_account_currency
		}).insert(ignore_permissions=True)

		return debtors_account.name

	else:
		return debtors_account_name