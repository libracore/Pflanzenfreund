from __future__ import print_function, unicode_literals

import frappe
from frappe.utils import update_progress_bar

def after_install():
	disable_website_manager()
	set_permissions_for_pflanzenfreund_manager()
	print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
	print('Installation of "Pflanzenfreund" successfull')
	print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
	
def disable_website_manager():
	update_progress_bar('Deactivate Role "Website Manager"', 0, 1)
	sql_query = """UPDATE `tabRole`
		SET `disabled` = '1'
		WHERE `role_name` = 'Website Manager'"""
	frappe.db.sql(sql_query)
	
def set_permissions_for_pflanzenfreund_manager():
	docs_for_permission = [
		'Subscription', 'Sales Invoice', 'Payment Entry',
		'Customer', 'Contact', 'Address',
		'Website Settings', 'Website Theme', 'Website Script',
		'Web Page', 'Web Form', 'Website Sidebar', 'Website Slideshow', 'Help Category',
		'Portal Settings',
		'Help Category', 'Help Article'
	]
	i = 0
	for doc in docs_for_permission:
		frappe.permissions.add_permission(doc, "Pflanzenfreund Manager")
		update_progress_bar('Define Permissions for "Pflanzenfreund Manager"', i, len(docs_for_permission))
		i = i + 1
