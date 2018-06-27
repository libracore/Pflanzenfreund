from __future__ import print_function, unicode_literals

import frappe
from frappe.utils import update_progress_bar

def after_install():
	pf_roles = ["Administrator", "System Manager", "PF Administrator", "PF Website Manager", "PF Abo Verwalter"]
	check_if_pf_roles_exist(pf_roles)
	disable_roles_exepct_PF_roles(pf_roles)
	
	docs_for_permission = [
		'Subscription', 'Sales Invoice', 'Payment Entry',
		'Customer', 'Contact', 'Address',
		'Website Settings', 'Website Theme', 'Website Script',
		'Web Page', 'Web Form', 'Website Sidebar', 'Website Slideshow', 'Help Category',
		'Portal Settings',
		'Help Category', 'Help Article'
	]
	set_permissions(docs_for_permission, "PF Administrator")
	
	docs_for_permission = [
		'Website Settings', 'Website Theme', 'Website Script',
		'Web Page', 'Web Form', 'Website Sidebar', 'Website Slideshow', 'Help Category',
		'Portal Settings',
		'Help Category', 'Help Article'
	]
	set_permissions(docs_for_permission, "PF Website Manager")
	
	docs_for_permission = [
		'Subscription', 'Sales Invoice', 'Payment Entry',
		'Customer', 'Contact', 'Address'
	]
	set_permissions(docs_for_permission, "PF Abo Verwalter")
	
	hide_module_all_modules_exepct_pflanzenfreund()
	success_message()

def check_if_pf_roles_exist(pf_roles):
	for role in pf_roles:
		if frappe.get_doc({'doctype': "Role", "role_name": "{0}".format(role)}):
			
		else:
			frappe.get_doc({'doctype': "Role", "role_name": "{0}".format(role)}).insert()
	
def disable_roles_exepct_PF_roles(pf_roles):
	roles = get_all_roles()
	i = 0
	for role in roles:
		update_progress_bar('Deactivate Roles', i, len(roles))
		if not role[0] in pf_roles:
			disable_role(role[0])
		i = i + 1
	
def disable_role(role):
	sql_query = """UPDATE `tabRole`
		SET `disabled` = '1'
		WHERE `role_name` = '{0}'""".format(role)
	frappe.db.sql(sql_query)

def set_permissions(docs_for_permission, role):
	i = 0
	for doc in docs_for_permission:
		frappe.permissions.add_permission(doc, role)
		update_progress_bar('Define Permissions for "{0}"'.format(role), i, len(docs_for_permission))
		i = i + 1

def hide_module_all_modules_exepct_pflanzenfreund():
	modules = get_all_modules()
	i = 0
	for module in modules:
		update_progress_bar('Hide Module "Website"', i, len(modules))
		if module[0] != "Pflanzenfreund":
			sql_query = """UPDATE `tabModule Def`
				SET `restrict_to_domain` = 'Non Profit'
				WHERE `module_name` = '{0}'""".format(module[0])
			frappe.db.sql(sql_query)
		i = i + 1
		
def get_all_roles():
	sql_query = """SELECT t1.role_name
		FROM `tabRole` AS t1"""
	all_roles = frappe.db.sql(sql_query, as_list=True)
	return all_roles

def get_all_modules():
	sql_query = """SELECT t1.module_name
		FROM `tabModule Def` AS t1"""
	all_modules = frappe.db.sql(sql_query, as_list=True)
	return all_modules
		
def success_message():
	print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
	print('Installation of "Pflanzenfreund" successfull')
	print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")