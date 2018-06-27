from __future__ import print_function, unicode_literals

import frappe

def after_install():
	print('Deactivate Role "Website Manager"...')
	disable_website_manager()
	print('Define Permissions for "Pflanzenfreund Manager"...')
	set_permissions_for_pflanzenfreund_manager()
	print('Installation of "Pflanzenfreund" successfull')
	# frappe.get_doc({'doctype': "Role", "role_name": "Pflanzenfreund Manager"}).insert()
	# frappe.db.commit()
	
def disable_website_manager():
	sql_query = """UPDATE `tabRole`
		SET `disabled` = '1'
		WHERE `role_name` = 'Website Manager'"""
	frappe.db.sql(sql_query)
	print("...deactivated...")
	
def set_permissions_for_pflanzenfreund_manager():
	sql_query = """UPDATE `tabDocPerm`
		SET `role`='Pflanzenfreund Manager'
		WHERE `parent` IN ('Website Settings', 'Website Theme', 'Website Script', 'Web Page', 'Web Form', 'Website Sidebar', 'Website Slideshow')
		AND `role` = 'Website Manager'"""
	frappe.db.sql(sql_query)
	print("...Permissions defined...")