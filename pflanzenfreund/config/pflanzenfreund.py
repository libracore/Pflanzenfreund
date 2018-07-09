from __future__ import unicode_literals
from frappe import _

def get_data():
    return[
	{
		"label": _("Subscrition Administration"),
		"icon": "fa fa-bookmark",
		"items": [
			{
			   "type": "doctype",
			   "name": "Subscription",
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
		"label": _("Website Settings"),
		"icon": "fa fa-bookmark",
		"items": [
		   {
			   "type": "doctype",
			   "name": "Website Settings",
			   "label": _("General Settings"),
			   "description": _("Setup Tools for the Website")
		   },
		   {
			   "type": "doctype",
			   "name": "Website Settings Pflanzenfreund",
			   "label": _("Navbar and Footer Settings"),
			   "description": _("Setup Tools for the Website")
		   },
		   {
			   "type": "doctype",
			   "name": "Website Theme",
			   "label": _("Website Theme"),
			   "description": _("Setup Tools for the Website")
		   },
		   {
			   "type": "doctype",
			   "name": "Website Script",
			   "label": _("Website Script"),
			   "description": _("Setup Tools for the Website")
		   }
		]
	},
	{
		"label": _("Websites and Items"),
		"icon": "fa fa-bookmark",
		"items": [
		   {
			   "type": "doctype",
			   "name": "Web Page",
			   "label": _("Web Pages"),
			   "description": _("Setup Tools for the Website")
		   },
		   {
			   "type": "doctype",
			   "name": "Web Form",
			   "label": _("Web Forms"),
			   "description": _("Setup Tools for the Website")
		   },
		   {
			   "type": "doctype",
			   "name": "Website Sidebar",
			   "label": _("Web Sidebars"),
			   "description": _("Setup Tools for the Website")
		   },
		   {
			   "type": "doctype",
			   "name": "Website Slideshow",
			   "label": _("Web Slideshows"),
			   "description": _("Setup Tools for the Website")
		   }
		]
	},
	{
		"label": _("Extranet Settings"),
		"icon": "fa fa-bookmark",
		"items": [
		   {
			   "type": "doctype",
			   "name": "Portal Settings",
			   "label": _("Portal Settings"),
			   "description": _("Setup Tools for the Extranet")
		   }
		]
	},
	{
		"label": _("Knowledge Base"),
		"icon": "fa fa-bookmark",
		"items": [
		   {
			   "type": "doctype",
			   "name": "Help Category",
			   "label": _("Help Category"),
			   "description": _("Setup Tools for KB")
		   },
		   {
			   "type": "doctype",
			   "name": "Help Article",
			   "label": _("Help Article"),
			   "description": _("Setup Tools for KB")
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
	}	
]
