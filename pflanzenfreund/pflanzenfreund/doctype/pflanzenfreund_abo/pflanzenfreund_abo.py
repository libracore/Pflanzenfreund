# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PflanzenfreundAbo(Document):
	pass

@frappe.whitelist()
def create_abo(customer):
	abo = frappe.new_doc("Pflanzenfreund Abo")
	abo.update({
		"customer": customer
	})
	abo.flags.ignore_mandatory = True
	abo.save(ignore_permissions=True)
	frappe.db.commit()
	return abo.name