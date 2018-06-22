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
			   "name": "Website Settings Pflanzenfreund",
			   "label": _("Settings"),
			   "description": _("Setup Tools for the Extranet")
		   }
		]
	}
]