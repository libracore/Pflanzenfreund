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