// Copyright (c) 2016, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pflanzenfreund Druckauftrag"] = {
	"filters": [
		{
			fieldname: "edition",
			label: __("Edition"),
			fieldtype: "Select",
			options: ["", "Winter", "February", "March", "April", "May", "June", "Summer", "September", "October", "November"]
		}
	]
}
