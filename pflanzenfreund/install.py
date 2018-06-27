from __future__ import print_function, unicode_literals

import frappe

def after_install():
	print('Deactivate Role "Website Manager"...')
	disable_website_manager()
	print('Define Permissions for "Pflanzenfreund Manager"...')
	set_permissions_for_pflanzenfreund_manager()
	print('Change Module definition from "Website" to "Pflanzenfreund"...')
	change_module_def()
	print('Installation of "Pflanzenfreund" successfull')
	
def disable_website_manager():
	sql_query = """UPDATE `tabRole`
		SET `disabled` = '1'
		WHERE `role_name` = 'Website Manager'"""
	frappe.db.sql(sql_query)
	print("...deactivated...")
	
def set_permissions_for_pflanzenfreund_manager():
	docs_for_permission = [
		'Subscription', 'Sales Invoice', 'Payment Entry',
		'Customer', 'Contact', 'Address',
		'Website Settings', 'Website Theme', 'Website Script',
		'Web Page', 'Web Form', 'Website Sidebar', 'Website Slideshow', 'Help Category',
		'Portal Settings',
		'Help Category', 'Help Article'
	]
	for doc in docs_for_permission:
		frappe.permissions.add_permission(doc, "Pflanzenfreund Manager")
	print("...Permissions defined...")
	
def change_module_def():
	sql_query = """UPDATE `tabDocType`
		SET `module` = 'Pflanzenfreund'
		WHERE `module` = 'Website'"""
	frappe.db.sql(sql_query)
	print("...Module changed...")