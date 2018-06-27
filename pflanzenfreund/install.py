from __future__ import print_function, unicode_literals

import frappe

def after_install():
	print("Gratuliere, der Pflanzenfreund wurde erfolgreich installiert.")
	# frappe.get_doc({'doctype': "Role", "role_name": "Pflanzenfreund Manager"}).insert()
	# frappe.db.commit()