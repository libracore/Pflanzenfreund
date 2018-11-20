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
import esr
from frappe.utils.background_jobs import enqueue
from frappe.utils.data import add_days


#........................


from datetime import datetime
from PyPDF2 import PdfFileWriter

def remove_downloaded_pdf():
	path = "/home/frappe/frappe-bench/sites/assets/pflanzenfreund/sinvs_for_print/sales_invoice_print_2018-11-19.pdf"
	os.remove(path)
	
@frappe.whitelist()
def list_all_pdfs():
	from os import listdir
	from os.path import isfile, join
	path = "/home/frappe/frappe-bench/sites/assets/pflanzenfreund/sinvs_for_print/"
	onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
	return onlyfiles
	
	
def create_pdf_of_all_sinvs(print_sinv, counter, printformat):
	# sql_query = ("""SELECT `name` FROM `tabSales Invoice` WHERE `creation` > '2018-11-19 00:01:00' AND `docstatus` = 1 LIMIT 3""")
	# sinvs = frappe.db.sql(sql_query, as_dict=True)
	# print_sinv = []
	# for sinv in sinvs:
		# print_sinv.append(sinv)
		# print("found sinv")
		
	# run bind job
	if len(print_sinv) > 0:
		#print("lets binding")
		now = datetime.now()
		bind_source = "/assets/pflanzenfreund/sinvs_for_print/sales_invoice_print_{year}-{month}-{day}-{counter}.pdf".format(day=now.day, month=now.month, year=now.year, counter=counter)
		physical_path = "/home/frappe/frappe-bench/sites" + bind_source
		print_bind(print_sinv, format=printformat, dest=str(physical_path))
				
				
				
# this function will bind a pdf from all provided sales invoices (list of names)
def print_bind(sales_invoices, format=None, dest=None):
	# Concatenating pdf files
	output = PdfFileWriter()
	for sales_invoice in sales_invoices:
		output = frappe.get_print("Sales Invoice", sales_invoice, format, as_pdf = True, output = output)
		print("append to output")
	if dest != None:
		if isinstance(dest, str): # when dest is a file path
			destdir = os.path.dirname(dest)
			if destdir != '' and not os.path.isdir(destdir):
				os.makedirs(destdir)
			with open(dest, "wb") as w:
				output.write(w)
		else: # when dest is io.IOBase
			output.write(dest)
			print("first return")
		return
	else:
		print("second return")
		return output




#...............................

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

@frappe.whitelist()
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
def place_order_abo(customer, shipping, billing, abo, donee):
	customer_letter_salutation = ""
	donee_letter_salutation = ""
	if abo == "Geschenk-Abo":
		try:
			customer_contact_link = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `link_name` = '{0}' AND `parenttype` = 'Contact'""".format(customer), as_list = True)
			customer_contact = frappe.get_doc("Contact", customer_contact_link[0][0])
			customer_letter_salutation = customer_contact.letter_salutation
			
			donee_contact_link = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `link_name` = '{0}' AND `parenttype` = 'Contact'""".format(donee), as_list = True)
			donee_contact = frappe.get_doc("Contact", donee_contact_link[0][0])
			donee_letter_salutation = donee_contact.letter_salutation
		except:
			customer_letter_salutation = "Sehr geehrte Damen und Herren"
			donee_letter_salutation = "Sehr geehrte Damen und Herren"
	else:
		try:
			contact_link = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `link_name` = '{0}' AND `parenttype` = 'Contact'""".format(customer), as_list = True)
			contact = frappe.get_doc("Contact", contact_link[0][0])
			customer_letter_salutation = contact.letter_salutation
		except:
			customer_letter_salutation = "Sehr geehrte Damen und Herren"
	
	pflanzenfreund_abo = frappe.new_doc("Pflanzenfreund Abo")
	if abo == "Jahres-Abo":
		pflanzenfreund_abo.update({
			"customer": customer,
			"customer_address": billing,
			"customer_letter_salutation": customer_letter_salutation,
			"abo_type": abo,
			"start_date": utils.today(),
			"end_date": add_year(utils.today()),
			"jan_ed": 1,
			"feb_ed": 1,
			"mar_ed": 1,
			"apr_ed": 1,
			"may_ed": 1,
			"jun_ed": 1,
			"jul_ed": 1,
			"aug_ed": 1,
			"sept_ed": 1,
			"oct_ed": 1,
			"nov_ed": 1,
			"dec_ed": 1
		})
	if abo == "Probe-Abo":
		pflanzenfreund_abo.update({
			"customer": customer,
			"customer_address": billing,
			"customer_letter_salutation": customer_letter_salutation,
			"abo_type": abo,
			"start_date": utils.today(),
			"end_date": get_abo_end_date(),
			"jan_ed": 0,
			"feb_ed": 0,
			"mar_ed": 0,
			"apr_ed": 0,
			"may_ed": 0,
			"jun_ed": 0,
			"jul_ed": 0,
			"aug_ed": 0,
			"sept_ed": 0,
			"oct_ed": 0,
			"nov_ed": 0,
			"dec_ed": 0
		})
		add_editions_to_abo_based_on_act_month(pflanzenfreund_abo)
	if abo == "Geschenk-Abo":
		pflanzenfreund_abo.update({
			"customer": customer,
			"customer_address": billing,
			"customer_letter_salutation": customer_letter_salutation,
			"donee": donee,
			"donee_address": shipping,
			"donee_letter_salutation": donee_letter_salutation,
			"abo_type": abo,
			"start_date": utils.today(),
			"end_date": add_year(utils.today()),
			"jan_ed": 1,
			"feb_ed": 1,
			"mar_ed": 1,
			"apr_ed": 1,
			"may_ed": 1,
			"jun_ed": 1,
			"jul_ed": 1,
			"aug_ed": 1,
			"sept_ed": 1,
			"oct_ed": 1,
			"nov_ed": 1,
			"dec_ed": 1
		})
	pflanzenfreund_abo.flags.ignore_mandatory = True
	pflanzenfreund_abo.save(ignore_permissions=True)
	pflanzenfreund_abo.submit()
	frappe.db.commit()
	create_invoice(customer, billing, shipping, pflanzenfreund_abo, abo)
	
def get_abo_end_date():
	start = utils.today()
	end = utils.add_months(start, 4)
	return (end)
	
def add_editions_to_abo_based_on_act_month(pflanzenfreund_abo):
	start_date = utils.now_datetime()
	start_day = start_date.day
	start_month = start_date.month
	if start_day > 14:
		start_month = start_month + 1
	if start_month == 1:
		pflanzenfreund_abo.update({
			"jan_ed": 1,
			"feb_ed": 1,
			"mar_ed": 1,
			"apr_ed": 1
		})
	if start_month == 2:
		pflanzenfreund_abo.update({
			"feb_ed": 1,
			"mar_ed": 1,
			"apr_ed": 1,
			"may_ed": 1
		})
	if start_month == 3:
		pflanzenfreund_abo.update({
			"mar_ed": 1,
			"apr_ed": 1,
			"may_ed": 1,
			"jun_ed": 1
		})
	if start_month == 4:
		pflanzenfreund_abo.update({
			"apr_ed": 1,
			"may_ed": 1,
			"jun_ed": 1,
			"jul_ed": 1
		})
	if start_month == 5:
		pflanzenfreund_abo.update({
			"may_ed": 1,
			"jun_ed": 1,
			"jul_ed": 1,
			"aug_ed": 1
		})
	if start_month == 6:
		pflanzenfreund_abo.update({
			"jun_ed": 1,
			"jul_ed": 1,
			"aug_ed": 1,
			"sept_ed": 1
		})
	if start_month == 7:
		pflanzenfreund_abo.update({
			"jul_ed": 1,
			"aug_ed": 1,
			"sept_ed": 1,
			"oct_ed": 1
		})
	if start_month == 8:
		pflanzenfreund_abo.update({
			"aug_ed": 1,
			"sept_ed": 1,
			"oct_ed": 1,
			"nov_ed": 1
		})
	if start_month == 9:
		pflanzenfreund_abo.update({
			"sept_ed": 1,
			"oct_ed": 1,
			"nov_ed": 1,
			"dec_ed": 1
		})
	if start_month == 10:
		pflanzenfreund_abo.update({
			"jan_ed": 1,
			"oct_ed": 1,
			"nov_ed": 1,
			"dec_ed": 1
		})
	if start_month == 11:
		pflanzenfreund_abo.update({
			"jan_ed": 1,
			"feb_ed": 1,
			"nov_ed": 1,
			"dec_ed": 1
		})
	if start_month == 12:
		pflanzenfreund_abo.update({
			"jan_ed": 1,
			"feb_ed": 1,
			"mar_ed": 1,
			"dec_ed": 1
		})
	return(pflanzenfreund_abo)
	
def create_invoice(customer, billing, shipping, pflanzenfreund_abo, abo):
	sales_invoice = frappe.new_doc("Sales Invoice")
	sales_invoice.update({
		"customer": customer,
		"customer_address": billing,
		"shipping_address_name": shipping,
		"delivery_date": utils.today(),
		"pflanzenfreund_abo": pflanzenfreund_abo.name,
		"taxes_and_charges": "Schweiz normal (302) - GCM",
		"items": [{
			"item_code": abo,
			"qty": "1"
		}],
		"taxes": [{
			"charge_type": "On Net Total",
			"account_head": "2200 - Umsatzsteuer - GCM",
			"cost_center": "Haupt - GCM",
			"rate": "7.7",
			"description": "Inkl. 7.7% MwSt"
		}]
	})
	sales_invoice.flags.ignore_mandatory = True
	sales_invoice.save(ignore_permissions=True)
	referencenumber = sales_invoice.name.split("-")[1]
	sales_invoice.update({
		"esr_reference": esr.get_reference_number(referencenumber),
		"esr_code": esr.generateCodeline(sales_invoice.grand_total, esr.get_reference_number(referencenumber), "013100113")
	})
	sales_invoice.save(ignore_permissions=True)
	sales_invoice.submit()
	frappe.db.commit()
	#create_subscription(sales_invoice)
	
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
	
def get_logged_in_user():
	return frappe.session.user
	
	


def get_address(customer):
	query = """SELECT `parent` FROM `tabDynamic Link` WHERE `parenttype` = 'Address' AND `link_doctype` = 'Customer' AND `link_name` = '{0}'""".format(customer)
	do_query = frappe.db.sql(query, as_list = True)
	return do_query[0]

@frappe.whitelist()
def check_if_donee_exist(email, first_name, last_name, street, city, plz, phone, mobile):
	if email:
		user = frappe.db.get("User", {"email": email})
		if user:
			contact_name = frappe.db.get_value("Contact", {"email_id": email})
			party = None

			if contact_name:
				contact = frappe.get_doc('Contact', contact_name)
				if contact.links:
					party_doctype = contact.links[0].link_doctype
					party = contact.links[0].link_name

			if party:
				return party

			else:
				customer = frappe.new_doc("Customer")
				first_name = frappe.db.get_value("User", email, "first_name")
				last_name = frappe.db.get_value("User", email, "last_name")
				fullname = get_fullname(email)
				customer.update({
					"customer_name": fullname,
					"first_name": first_name,
					"last_name": last_name,
					"customer_type": "Individual",
					"customer_group": "Pflanzenfreund",
					"territory": get_root_of("Territory")
				})

				customer.flags.ignore_mandatory = True
				customer.insert(ignore_permissions=True)

				contact = frappe.new_doc("Contact")
				contact.update({
					"first_name": fullname,
					"email_id": email
				})
				contact.append('links', dict(link_doctype='Customer', link_name=customer.name))
				contact.flags.ignore_mandatory = True
				contact.insert(ignore_permissions=True)
				
				address = frappe.new_doc("Address")
				address.update({
					"address_type": "Geschenk",
					"address_line1": street,
					"city": city,
					"country": "Schweiz",
					"pincode": plz
				})
				address.append('links', dict(link_doctype='Customer', link_name=customer.name))
				logged_in_user = frappe.session.user
				contact_name = frappe.db.get_value("Contact", {"email_id": logged_in_user})
				party = None
				contact = frappe.get_doc('Contact', contact_name)
				party_doctype = contact.links[0].link_doctype
				party = contact.links[0].link_name
				address.append('links', dict(link_doctype='Customer', link_name=party))
				address.flags.ignore_mandatory = True
				address.insert(ignore_permissions=True)
				return customer
				
	customer = frappe.new_doc("Customer")
	fullname = first_name + " " + last_name
	customer.update({
		"customer_name": fullname,
		"first_name": first_name,
		"last_name": last_name,
		"customer_type": "Individual",
		"customer_group": "Pflanzenfreund",
		"territory": get_root_of("Territory")
	})

	customer.flags.ignore_mandatory = True
	customer.insert(ignore_permissions=True)

	contact = frappe.new_doc("Contact")
	contact.update({
		"first_name": fullname
	})
	contact.append('links', dict(link_doctype='Customer', link_name=customer.name))
	contact.flags.ignore_mandatory = True
	contact.insert(ignore_permissions=True)
	
	address = frappe.new_doc("Address")
	address.update({
		"address_type": "Geschenk",
		"address_line1": street,
		"city": city,
		"country": "Schweiz",
		"pincode": plz
	})
	address.append('links', dict(link_doctype='Customer', link_name=customer.name))
	logged_in_user = frappe.session.user
	contact_name = frappe.db.get_value("Contact", {"email_id": logged_in_user})
	party = None
	contact = frappe.get_doc('Contact', contact_name)
	party_doctype = contact.links[0].link_doctype
	party = contact.links[0].link_name
	address.append('links', dict(link_doctype='Customer', link_name=party))
	address.flags.ignore_mandatory = True
	address.insert(ignore_permissions=True)
	return customer

@frappe.whitelist()
def get_donee_address(donee):
	query = """SELECT `parent` FROM `tabDynamic Link` WHERE `parenttype` = 'Address' AND `link_doctype` = 'Customer' AND `link_name` = '{0}' ORDER BY `creation` DESC LIMIT 1""".format(donee)
	do_query = frappe.db.sql(query, as_list = True)
	return do_query[0]
	


@frappe.whitelist()
def add_year(date):
	return utils.add_years(date, 1)
	
@frappe.whitelist()
def qty_abo_rechnungslauf(start, end, abo_type):
	return len(frappe.get_all('Pflanzenfreund Abo', filters=[['docstatus', '=', '1'], ['end_date', '>=', start], ['end_date', '<=', end], ['abo_type', '=', abo_type], ['abo_renewed', '=', '0']], fields=['name']))
	
@frappe.whitelist()
def createNewInvoices_abo_rechnungslauf(start, end, abo_type, bullet_type, bullet_text, background, rechnungsdatum, printformat):
	# if background == "no":
		# return _createNewInvoices_abo_rechnungslauf(start, end, abo_type, bullet_type, bullet_text, background, rechnungsdatum)
	# else:
	max_time = (qty_abo_rechnungslauf(start, end, abo_type) / 10) * 120
	args = {
		'start': start,
		'end': end,
		'abo_type': abo_type,
		'bullet_type': bullet_type,
		'bullet_text': bullet_text,
		'background': background,
		'rechnungsdatum': rechnungsdatum,
		'printformat': printformat
	}
	enqueue("pflanzenfreund.utils._createNewInvoices_abo_rechnungslauf", queue='long', job_name='Automatisierter Abonnementenlauf in 10er Batches', timeout=max_time, **args)
	
def _createNewInvoices_abo_rechnungslauf(start, end, abo_type, bullet_type, bullet_text, background, rechnungsdatum, printformat):
	results = []
	abo_counter = 0
	loop_control = 1
	print_sinv = []
	_abos = frappe.get_all('Pflanzenfreund Abo', filters=[['docstatus', '=', '1'], ['end_date', '>=', start], ['end_date', '<=', end], ['abo_type', '=', abo_type], ['abo_renewed', '=', '0']], fields=['name'])
	abos = []

	for abo in _abos:
		abos.append(abo.name)
	
	

	for abo in abos:
		#get old abo
		old_abo = frappe.get_doc('Pflanzenfreund Abo', abo)
		#create new abo
		new_abo = frappe.new_doc("Pflanzenfreund Abo")
		new_abo.update({
			"abo_ist_verlaengerung": 1,
			"customer": old_abo.customer,
			"customer_address": old_abo.customer_address,
			"customer_letter_salutation": old_abo.customer_letter_salutation,
			"donee": old_abo.donee,
			"donee_address": old_abo.donee_address,
			"donee_letter_salutation": old_abo.donee_letter_salutation,
			"donee_text": old_abo.donee_text,
			"abo_type": old_abo.abo_type,
			"start_date": add_year(old_abo.start_date),
			"end_date": add_year(old_abo.end_date),
			"jan_ed": 1,
			"feb_ed": 1,
			"mar_ed": 1,
			"apr_ed": 1,
			"may_ed": 1,
			"jun_ed": 1,
			"jul_ed": 1,
			"aug_ed": 1,
			"sept_ed": 1,
			"oct_ed": 1,
			"nov_ed": 1,
			"dec_ed": 1
		})
		new_abo.flags.ignore_mandatory = True
		new_abo.save(ignore_permissions=True)
		new_abo.submit()
		frappe.db.commit()
		set_renewd = frappe.db.sql("""UPDATE `tabPflanzenfreund Abo` SET `abo_renewed` = 1, `new_abo` = '{1}' WHERE `name` = '{0}'""".format(old_abo.name, new_abo.name), as_list = True)
		#create new invoice for abo
		sales_invoice = frappe.new_doc("Sales Invoice")
		sales_invoice.update({
			"customer": old_abo.customer,
			"customer_address": old_abo.customer_address,
			"shipping_address_name": old_abo.donee_address,
			"set_posting_time": 1,
			"posting_date": add_days(rechnungsdatum, 0),
			"pflanzenfreund_abo": new_abo.name,
			"taxes_and_charges": "Schweiz normal (302) - GCM",
			"items": [{
				"item_code": abo_type,
				"qty": "1"
			}],
			"taxes": [{
				"charge_type": "On Net Total",
				"account_head": "2200 - Umsatzsteuer - GCM",
				"cost_center": "Haupt - GCM",
				"rate": "7.7",
				"description": "Inkl. 7.7% MwSt"
			}],
			"due_date": add_days(rechnungsdatum, 30),
			"payment_schedule": [{
				"payment_term": "30 Tage netto",
				"description": "30 Tage netto",
				"due_date": add_days(rechnungsdatum, 30),
				"invoice_portion": "100",
				"payment_amount": sales_invoice.rounded_total
			}]
		})
		# sales_invoice.update({
			# "due_date": add_days(rechnungsdatum, 30),
			# "payment_terms_template": "30 Tage netto",
			# "payment_schedule": [{
				# "payment_term": "30 Tage netto",
				# "description": "30 Tage netto",
				# "due_date": add_days(rechnungsdatum, 30),
				# "invoice_portion": "100",
				# "payment_amount": sales_invoice.rounded_total
			# }]
		# })
		if bullet_type != 'kein':
			sales_invoice.update({
				"bullet_selection": bullet_type,
				"bullet_text": bullet_text
			})
		sales_invoice.flags.ignore_mandatory = True
		sales_invoice.save(ignore_permissions=True)
		
		referencenumber = sales_invoice.name.split("-")[1]
		sales_invoice.update({
			"esr_reference": esr.get_reference_number(referencenumber),
			"esr_code": esr.generateCodeline(sales_invoice.grand_total, esr.get_reference_number(referencenumber), "013100113")
		})
		sales_invoice.save(ignore_permissions=True)
		
		
		
		sales_invoice.submit()
		frappe.db.commit()
		#appened new invoice to new_invoices
		results.append([new_abo.name, sales_invoice.name])
		
		print_sinv.append(sales_invoice.name)
		abo_counter += 1
		if abo_counter == batch:
			create_pdf_of_all_sinvs(print_sinv, "(" + str(abo_counter) + ")Invoices_Loop(" + str(loop_control) + ")", printformat)
			abo_counter = 0
			loop_control += 1
			print_sinv = []
	# if background == "no":
		# return results
	# else:
	if abo_counter > 0:
		create_pdf_of_all_sinvs(print_sinv, "(" + str(abo_counter) + ")Invoices_Loop(" + str(loop_control) + ")", printformat)
	message = 'Der Background-Job Automatisierter Abonnementenlauf wurde erfolgreich abgeschlossen.'
	frappe.publish_realtime(event='msgprint',message=message,user=frappe.session.user)
	
@frappe.whitelist()
def get_abos_for_customer_view(customer):
	query = """SELECT `name`, `abo_type`, `start_date`, `end_date`
		FROM `tabPflanzenfreund Abo`
		WHERE `docstatus` = '1'
		AND `customer` = '{0}' OR `donee` = '{0}'""".format(customer)
	return frappe.db.sql(query, as_list = True)
	
@frappe.whitelist()
def extend_abo(abo):
	old_abo = frappe.get_doc('Pflanzenfreund Abo', abo)
	if old_abo.abo_renewed == 1:
		return "already renewed"
	#create new abo
	new_abo = frappe.new_doc("Pflanzenfreund Abo")
	new_abo.update({
		"abo_ist_verlaengerung": 1,
		"customer": old_abo.customer,
		"customer_address": old_abo.customer_address,
		"donee": old_abo.donee,
		"donee_address": old_abo.donee_address,
		"donee_text": old_abo.donee_text,
		"abo_type": old_abo.abo_type,
		"start_date": add_year(old_abo.start_date),
		"end_date": add_year(old_abo.end_date),
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
		"dec_ed": old_abo.dec_ed
	})
	new_abo.flags.ignore_mandatory = True
	new_abo.save(ignore_permissions=True)
	new_abo.submit()
	frappe.db.commit()
	set_renewd = frappe.db.sql("""UPDATE `tabPflanzenfreund Abo` SET `abo_renewed` = 1, `new_abo` = '{1}' WHERE `name` = '{0}'""".format(old_abo.name, new_abo.name), as_list = True)
	return new_abo.name
	
def get_customernumber(greenid):
	query = """SELECT `name` FROM `tabCustomer` WHERE `greeninfo_id` = '{0}'""".format(greenid)
	do_query = frappe.db.sql(query, as_list = True)
	return do_query[0]
	
	
def update_existing_abo_with_salutations():
	abos = frappe.get_all("Pflanzenfreund Abo")
	count = 0
	for abo in abos:
		a = frappe.get_doc("Pflanzenfreund Abo", abo.name)
		if a.abo_type == "Geschenk-Abo":
			try:
				customer_contact_link = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `link_name` = '{0}' AND `parenttype` = 'Contact'""".format(a.customer), as_list = True)
				customer_contact = frappe.get_doc("Contact", customer_contact_link[0][0])
				
				donee_contact_link = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `link_name` = '{0}' AND `parenttype` = 'Contact'""".format(a.donee), as_list = True)
				donee_contact = frappe.get_doc("Contact", donee_contact_link[0][0])
				
				do_update = frappe.db.sql("""UPDATE `tabPflanzenfreund Abo` SET `customer_letter_salutation` = '{0}', `donee_letter_salutation` = '{1}' WHERE `name` = '{2}'""".format(customer_contact.letter_salutation, donee_contact.letter_salutation, a.name), as_list = True)
			except:
				do_update = frappe.db.sql("""UPDATE `tabPflanzenfreund Abo` SET `customer_letter_salutation` = 'Sehr geehrte Damen und Herren', `donee_letter_salutation` = 'Sehr geehrte Damen und Herren' WHERE `name` = '{0}'""".format(a.name), as_list = True)
			count += 1
		else:
			try:
				customer_contact_link = frappe.db.sql("""SELECT `parent` FROM `tabDynamic Link` WHERE `link_name` = '{0}' AND `parenttype` = 'Contact'""".format(a.customer), as_list = True)
				customer_contact = frappe.get_doc("Contact", customer_contact_link[0][0])
				
				do_update = frappe.db.sql("""UPDATE `tabPflanzenfreund Abo` SET `customer_letter_salutation` = '{0}' WHERE `name` = '{1}'""".format(customer_contact.letter_salutation, a.name), as_list = True)
			except:
				do_update = frappe.db.sql("""UPDATE `tabPflanzenfreund Abo` SET `customer_letter_salutation` = 'Sehr geehrte Damen und Herren' WHERE `name` = '{0}'""".format(a.name), as_list = True)
			count += 1
			
		print("updatet {0} of {1}".format(count, len(abos)))
		
def create_user_based_on_contact():
	contacts = frappe.get_list("Contact", fields=["name"])
	for _contact in contacts:
		contact = frappe.get_doc("Contact", _contact["name"])
		if contact.email_id:
			if contact.has_permission("write"):
				try:
					user = frappe.get_doc({
						"doctype": "User",
						"first_name": contact.first_name,
						"last_name": contact.last_name,
						"email": contact.email_id,
						"user_type": "Website User",
						"send_welcome_email": 0,
						"language": "de"
					}).insert(ignore_permissions = True)
					print("New User {0} created!".format(user.name))
				except:
					print("Contact {0} already exist as user!".format(contact.email_id))
