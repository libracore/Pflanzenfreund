from __future__ import unicode_literals
from frappe import _

def get_data():
    return[
	{
		"label": _("Extranet"),
		"icon": "fa fa-bookmark",
		"items": [
		   {
			   "type": "doctype",
			   "name": "Website Settings",
			   "label": _("General Settings"),
			   "description": _("Setup Tools for the Extranet")
		   },
		   {
			   "type": "doctype",
			   "name": "Website Settings Pflanzenfreund",
			   "label": _("Navbar and Footer Settings"),
			   "description": _("Setup Tools for the Extranet")
		   }
		]
	}
]