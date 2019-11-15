# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe.utils.pdf import get_pdf

@frappe.whitelist(allow_guest=True)
def vorschau(von='Kein von', fuer='Kein für', widmung='Keine Widmung', betrag=0):
	gutschein = frappe.get_doc("Gutschein Meier", 'fd5bf3155f')
	gutschein.von = von
	gutschein.fuer = fuer
	gutschein.widmung = widmung.replace("\n", "<br>")
	gutschein.betrag = betrag
	gutschein.save(ignore_permissions=True)
	
	return
	
@frappe.whitelist(allow_guest=True)
def download_vorschau_pdf():
	doctype="Gutschein Meier"
	name='fd5bf3155f'
	format='Vorschau'
	doc=None
	no_letterhead=0
	html = frappe.get_print(doctype, name, format, doc=doc, no_letterhead=no_letterhead)
	frappe.local.response.filename = "{name}.pdf".format(name=name.replace(" ", "-").replace("/", "-"))
	frappe.local.response.filecontent = get_pdf(html)
	frappe.local.response.type = "download"