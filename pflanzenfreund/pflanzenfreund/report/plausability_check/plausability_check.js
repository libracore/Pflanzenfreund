// Copyright (c) 2016, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Plausability Check"] = {
	"filters": [
		{
			fieldname: "abfrage",
			label: __("Abfrage"),
			fieldtype: "Select",
			options: ["Deaktivierte Kunden", "Kunden mit WS", "Kunden mit Kundenkarte", "Kunden ohne Kundenkarte"],
			default: "Deaktivierte Kunden"
		},
		{
			fieldname: "von",
			label: __("Daten von"),
			fieldtype: "Int",
			default: "0"
		},
		{
			fieldname: "bis",
			label: __("Max. Daten"),
			fieldtype: "Int",
			default: "100"
		}
	],
	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
		value = default_formatter(row, cell, value, columnDef, dataContext);
		if (dataContext["Status"] == 'Deaktiviert' || dataContext["Status"] == 'Mit WS') {
			if (columnDef.id == __("Kunde") && (dataContext["Jahres-Abos"] > 0 || dataContext["Probe-Abos"] > 0 || dataContext["Geschenk-Abos"] > 0 || dataContext["KK-Abos"] > 0 || dataContext["OK-Abos"] > 0 || dataContext["Gratis-Abos"] > 0 || dataContext["VIP-Abos"] > 0)) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
			}
			if (columnDef.id == __("Kundennamen") && (dataContext["Jahres-Abos"] > 0 || dataContext["Probe-Abos"] > 0 || dataContext["Geschenk-Abos"] > 0 || dataContext["KK-Abos"] > 0 || dataContext["OK-Abos"] > 0 || dataContext["Gratis-Abos"] > 0 || dataContext["VIP-Abos"] > 0)) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
			}
			if (columnDef.id == __("Jahres-Abos") && (dataContext["Jahres-Abos"] > 0)) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
			}
			if (columnDef.id == __("Probe-Abos") && dataContext["Probe-Abos"] > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
			}
			if (columnDef.id == __("Geschenk-Abos") && dataContext["Geschenk-Abos"] > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
			}
			if (columnDef.id == __("KK-Abos") && dataContext["KK-Abos"] > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
			}
			if (columnDef.id == __("OK-Abos") && dataContext["OK-Abos"] > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
			}
			if (columnDef.id == __("Gratis-Abos") && dataContext["Gratis-Abos"] > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
			}
			if (columnDef.id == __("VIP-Abos") && dataContext["VIP-Abos"] > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
			}
			return value;
		} else if (dataContext["Status"] == 'Mit Kundenkarte') {
			var kontrolle = (parseInt(dataContext["Jahres-Abos"]) + parseInt(dataContext["Probe-Abos"]) + parseInt(dataContext["Geschenk-Abos"]) + parseInt(dataContext["Gratis-Abos"]) + parseInt(dataContext["VIP-Abos"]));
			var kontrolle_2 = (parseInt(dataContext["Jahres-Abos"]) + parseInt(dataContext["Probe-Abos"]) + parseInt(dataContext["Geschenk-Abos"]));
			var kk = parseInt(dataContext["KK-Abos"]);
			var ok = parseInt(dataContext["OK-Abos"]);
			var gratis = parseInt(dataContext["Gratis-Abos"]);
			var vip = parseInt(dataContext["VIP-Abos"]);
			if (columnDef.id == __("Kunde") || columnDef.id == __("Kundennamen")) {
				if ( kontrolle > 0) {
					if (kk > 0) {
						value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
					}
				} else {
					if (kk == 0 || kk > 1) {
						value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
					}
				}
				
				if (ok > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
				}
				
				if (kontrolle_2 > 0 && gratis > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
				}
				
				if (kontrolle_2 > 0 && vip > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
				}
			}
			
			if (columnDef.id == __("KK-Abos")) {
				if ( kontrolle > 0) {
					if (kk > 0) {
						value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
					}
				} else {
					if (kk == 0 || kk > 1) {
						value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
					}
				}
			}
			
			if (columnDef.id == __("OK-Abos")) {
				if (ok > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
				}
			}
			
			if (columnDef.id == __("Gratis-Abos")) {
				if (kontrolle_2 > 0 && gratis > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
				}
			}
			
			if (columnDef.id == __("VIP-Abos")) {
				if (kontrolle_2 > 0 && vip > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
				}
			}
			
			return value;
		} else if (dataContext["Status"] == 'Ohne Kundenkarte') {
			var kontrolle = (parseInt(dataContext["Jahres-Abos"]) + parseInt(dataContext["Probe-Abos"]) + parseInt(dataContext["Geschenk-Abos"]) + parseInt(dataContext["Gratis-Abos"]) + parseInt(dataContext["VIP-Abos"]));
			var kontrolle_2 = (parseInt(dataContext["Jahres-Abos"]) + parseInt(dataContext["Probe-Abos"]) + parseInt(dataContext["Geschenk-Abos"]));
			var kk = parseInt(dataContext["KK-Abos"]);
			var ok = parseInt(dataContext["OK-Abos"]);
			var gratis = parseInt(dataContext["Gratis-Abos"]);
			var vip = parseInt(dataContext["VIP-Abos"]);
			if (columnDef.id == __("Kunde") || columnDef.id == __("Kundennamen")) {
				if ( kontrolle > 0) {
					if (ok > 0) {
						value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
					}
				} else {
					if (ok == 0 || ok > 1) {
						value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
					}
				}
				
				if (kk > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
				}
				
				if (kontrolle_2 > 0 && gratis > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
				}
				
				if (kontrolle_2 > 0 && vip > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
				}
			}
			
			if (columnDef.id == __("OK-Abos")) {
				if ( kontrolle > 0) {
					if (ok > 0) {
						value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
					}
				} else {
					if (ok == 0 || ok > 1) {
						value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
					}
				}
			}
			
			if (columnDef.id == __("KK-Abos")) {
				if (kk > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
				}
			}
			
			if (columnDef.id == __("Gratis-Abos")) {
				if (kontrolle_2 > 0 && gratis > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
				}
			}
			
			if (columnDef.id == __("VIP-Abos")) {
				if (kontrolle_2 > 0 && vip > 0) {
					value = "<div style='text-align: right; background-color:red!important;'>" + value + "</div>";
				}
			}
			
			return value;
		} else {
			return value;
		}
	}
}





/* Kunde & name

Wenn
(dataContext["Jahres-Abos"] > 0 || dataContext["Probe-Abos"] > 0 || dataContext["Geschenk-Abos"] > 0)
&&
(dataContext["KK-Abos"] > 0 || dataContext["OK-Abos"] > 0 || dataContext["Gratis-Abos"] > 0 || dataContext["VIP-Abos"] > 0)

oder wenn
(dataContext["Jahres-Abos"] = 0 || dataContext["Probe-Abos"] = 0 || dataContext["Geschenk-Abos"] = 0)
&&
(dataContext["KK-Abos"] != 1 || dataContext["OK-Abos"] > 0 || dataContext["Gratis-Abos"] > 0 || dataContext["VIP-Abos"] > 0)

------------------------------

Jahres-Abos
Wenn */
