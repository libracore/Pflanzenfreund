// Copyright (c) 2016, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pflanzenfreund Druckauftrag"] = {
	"filters": [
		{
			fieldname: "edition",
			label: __("Edition"),
			fieldtype: "Select",
			options: ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
		},
		{
			fieldname: "year",
			label: __("Year"),
			fieldtype: "Data",
			default: String((new Date()).getFullYear())
		}
	]
}
