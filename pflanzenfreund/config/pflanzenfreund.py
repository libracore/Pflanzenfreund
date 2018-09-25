from __future__ import unicode_literals
from frappe import _

def get_data():
    return[
	{
		"label": _("Subscription Administration"),
		"icon": "fa fa-bookmark",
		"items": [
			{
			   "type": "doctype",
			   "name": "Pflanzenfreund Abo",
			   "label": _("Subscription"),
			   "description": _("Administration")
		   },
		   {
			   "type": "doctype",
			   "name": "Sales Invoice",
			   "label": _("Sales Invoice"),
			   "description": _("Administration")
		   },
		   {
			   "type": "doctype",
			   "name": "Payment Entry",
			   "label": _("Payment Entry"),
			   "description": _("Administration")
		   }
		]
	},
	{
		"label": _("Customer Administration"),
		"icon": "fa fa-bookmark",
		"items": [
		   {
			   "type": "doctype",
			   "name": "Customer",
			   "label": _("Customer"),
			   "description": _("Administration")
		   },
		   {
			   "type": "doctype",
			   "name": "Contact",
			   "label": _("Contact"),
			   "description": _("Administration")
		   },
		   {
			   "type": "doctype",
			   "name": "Address",
			   "label": _("Address"),
			   "description": _("Administration")
		   }
		]
	},
	{
		"label": _("Integration"),
		"icon": "fa fa-leaf",
		"items": [
		   {
			   "type": "doctype",
			   "name": "GreenInfo",
			   "label": _("GreenInfo"),
			   "description": _("GreenInfo")
		   }
		]
	},
	{
		"label": _("Tools"),
		"icon": "fa fa-wrench",
		"items": [
		   {
			   "type": "page",
			   "name": "erweiterte-kunden-su",
			   "label": _("Erweiterte Kundensuche"),
			   "description": _("Erweiterte Kunden Suche")
		   },
		   {
			   "type": "page",
			   "name": "abo_rechnungslauf",
			   "label": _("Abonnementen Rechnungslauf"),
			   "description": _("Abonnementen Rechnungslauf")
		   }
		]
	}
]
