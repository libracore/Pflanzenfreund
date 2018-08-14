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
from frappe import utils

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
	#query = """SELECT `name` FROM `tabDynamic Link` WHERE `parenttype` = 'Address' AND `link_name` = '{0}'""".format(party.name)
	#address_names = frappe.db.sql(query)
	address_names = frappe.db.get_all('Dynamic Link', fields=('parent'),
		filters=dict(parenttype='Address', link_doctype=party.doctype, link_name=party.name))
	return address_names
	
def get_address_details(address_name):
	return frappe.get_doc("Address", address_name)

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
		update_customer = update_existing_customer(contact.links[0].link_name)
		return frappe.get_doc(party_doctype, party)

	else:
		if not cart_settings.enabled:
			frappe.local.flags.redirect_location = "/contact"
			raise frappe.Redirect
		customer = frappe.new_doc("Customer")
		fullname = get_fullname(user)
		first_name = frappe.db.get_value("User", user, "first_name")
		last_name = frappe.db.get_value("User", user, "last_name")
		customer.update({
			"customer_name": fullname,
			"first_name": first_name,
			"last_name": last_name,
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
		
	
def update_existing_customer(link):
	user = frappe.session.user
	first_name = frappe.db.get_value("User", user, "first_name")
	last_name = frappe.db.get_value("User", user, "last_name")
	customer = frappe.get_doc("Customer", link)
	customer.update({
			"first_name": first_name,
			"last_name": last_name,
			"customer_name": first_name +" "+ last_name
		})
	customer.flags.ignore_mandatory = True
	customer.save(ignore_permissions=True)
	frappe.db.commit()

@frappe.whitelist()
def update_general_infos_of_existing_customer(first_name, last_name, phone, mobile_no):
	user = frappe.session.user
	query = """UPDATE `tabUser`
		SET `first_name` = '{0}', `last_name` = '{1}', `full_name` = '{0} {1}', `phone` = '{2}', `mobile_no` = '{3}'
		WHERE `name` = '{4}'""".format(first_name, last_name, phone, mobile_no, user)
	frappe.db.sql(query)
	contact_name = frappe.db.get_value("Contact", {"email_id": user})
	contact = frappe.get_doc('Contact', contact_name)
	party = contact.links[0].link_name
	update_existing_customer(party)
	return party
		
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

@frappe.whitelist()
def place_order_probe(customer="CUST-00007", shipping="Zuhause-Billing", billing="Zuhause-Billing"):
	sales_order = frappe.new_doc("Sales Order")
	sales_order.update({
		"customer": customer,
		"customer_address": billing,
		"shipping_address_name": shipping,
		"delivery_date": utils.today(),
		"items": [{
			"item_code": "Probe-Abo",
			"qty": "1"
		}]
	})
	sales_order.flags.ignore_mandatory = True
	sales_order.save(ignore_permissions=True)
	sales_order.submit()
	frappe.db.commit()
	create_invoice(customer, billing, shipping, sales_order)
	
def create_invoice(customer, billing, shipping, sales_order):
	sales_invoice = frappe.new_doc("Sales Invoice")
	sales_invoice.update({
		"customer": customer,
		"customer_address": billing,
		"shipping_address_name": shipping,
		"delivery_date": utils.today(),
		"items": [{
			"item_code": "Probe-Abo",
			"qty": "1",
			"sales_order": sales_order.name
		}]
	})
	sales_invoice.flags.ignore_mandatory = True
	sales_invoice.save(ignore_permissions=True)
	sales_invoice.submit()
	frappe.db.commit()
	create_subscription(sales_invoice)
	
def create_subscription(sales_invoice):
	subscription = frappe.new_doc("Subscription")
	subscription.update({
		"reference_doctype": "Sales Invoice",
		"reference_document": sales_invoice.name,
		"start_date": utils.today(),
		"submit_on_creation": 1,
		"frequency": "Yearly",
		"repeat_on_day": "0"
	})
	subscription.flags.ignore_mandatory = True
	subscription.save(ignore_permissions=True)
	subscription.submit()
	frappe.db.commit()