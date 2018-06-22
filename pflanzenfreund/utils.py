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
from frappe.website.doctype.website_settings.website_settings import get_website_settings
from frappe.website.router import get_page_context
from frappe.model.document import Document


def get_navbar_items(position):
	if position == 'top':
		navbar_items = get_top_items('top_bar_items')
	
	if position == 'bottom':
		navbar_items = get_bottom_items('bottom_bar_items')
	
	return navbar_items
	
def get_top_items(parentfield):
	all_top_items = frappe.db.sql("""\
		select * from `tabPflanzenfreund Navbar Top items`
		where parent='Website Settings Pflanzenfreund' and parentfield= %s
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
	
def get_bottom_items(parentfield):
	all_bottom_items = frappe.db.sql("""\
		select * from `tabPflanzenfreund Navbar Bottom Items`
		where parent='Website Settings Pflanzenfreund' and parentfield= %s
		order by idx asc""", parentfield, as_dict=1)

	bottom_items = [d for d in all_bottom_items if not d['parent_label']]

	# attach child items to top bar
	for d in all_bottom_items:
		if d['parent_label']:
			for t in bottom_items:
				if t['label']==d['parent_label']:
					if not 'child_items' in t:
						t['child_items'] = []
					t['child_items'].append(d)
					break
	return bottom_items
	
def get_pflanzenfreund_settings():
	pflanzenfreund_settings = frappe.get_doc("Website Settings Pflanzenfreund", "Website Settings Pflanzenfreund")
	return pflanzenfreund_settings
	
def get_brand():
	return "<img src='{0}' style='max-height:84px;width:auto;'>".format(get_pflanzenfreund_settings().brand)