from __future__ import unicode_literals
import frappe
from frappe import _
import frappe.www.list

no_cache = 1
no_sitemap = 1

def get_context(context):
	if frappe.session.user=='Guest':
		#frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
		#frappe.redirect_to_message(_('Thank you'), "<div><p>You will receive an email at test@example.com</p></div>")
		context.hide_order = True