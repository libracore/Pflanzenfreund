// Copyright (c) 2016, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pflanzenfreund Druckauftrag"] = {
	"filters": [
		{
			fieldname: "edition",
			label: __("Edition"),
			fieldtype: "Select",
			options: ["", "Dec / Jan", "February", "March", "April", "May", "June", "Jul / Aug", "September", "October", "November"]
		},
		{
			fieldname: "year",
			label: __("Year"),
			fieldtype: "Data",
			default: String((new Date()).getFullYear())
		},
		{
			fieldname: "abo_type",
			label: __("Abo Typ"),
			fieldtype: "Select",
			options: ["Jahres-Abo", "Probe-Abo", "Geschenk-Abo", "Gratis-Abo", "VIP-Abo", "Kundenkarten-Abo (KK)", "Kunden-Abo (OK)"]
		}
	]
}
