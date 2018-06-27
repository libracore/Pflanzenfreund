from __future__ import print_function, unicode_literals

import frappe

def after_install():
	frappe.get_doc({'doctype': "Role", "role_name": "Pflanzenfreund Manager"}).insert()
	frappe.db.commit()