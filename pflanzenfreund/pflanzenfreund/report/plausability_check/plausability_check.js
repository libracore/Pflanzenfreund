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
			fieldtype: "Int"
		},
		{
			fieldname: "bis",
			label: __("Max. Daten"),
			fieldtype: "Int",
			default: "250"
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
	},
	onload: function(report) {
		report.page.add_inner_button(__('Bereinigen'), function () {
		   if (report.data && report.data.length > 0) {
			   if (report.filters[0].value == "Deaktivierte Kunden") {
				   frappe.confirm(
						'Wollen Sie alle unten ersichtlichen, überflüssigen Abos stornieren?',
						function(){
							frappe.msgprint("Bitte warten");
							var kunden = [];
							for (i=0;i<report.data.length;i++) {
								if (report.data[i]["Geschenk-Abos"] > 0 || report.data[i]["Gratis-Abos"] > 0 || report.data[i]["Jahres-Abos"] > 0 || report.data[i]["KK-Abos"] > 0 || report.data[i]["OK-Abos"] > 0 || report.data[i]["Probe-Abos"] > 0 || report.data[i]["VIP-Abos"] > 0) {
									kunden.push(report.data[i].Kunde);
								}
							}
							//console.log(kunden);
							if (kunden.length > 0) {
								report.data = [];
								frappe.call({
									"method": "pflanzenfreund.pflanzenfreund.report.plausability_check.plausability_check.remove_all_abos",
									"args": {
										"kunden": kunden
									},
									"callback": function(r) {
										if (r.message == "OK") {
											frappe.msgprint("Die überflüssigen Abos wurden storniert.<br>Der Bericht wird neu geladen.", "Bereinigung abgeschlossen");
											frappe.show_alert("Bereinigung vollständig");
											report.refresh();
										}
									}
								});
							} else {
								frappe.msgprint("Es existieren keine überflüssigen Abos.", "Bereinigung abgeschlossen");
								frappe.show_alert("Bereinigung abgebrochen");
							}
						},
						function(){}
					)
			   }
			   if (report.filters[0].value == "Kunden mit WS") {
				   frappe.confirm(
						'Wollen Sie alle unten ersichtlichen, überflüssigen Abos stornieren?',
						function(){
							frappe.msgprint("Bitte warten");
							var kunden = [];
							for (i=0;i<report.data.length;i++) {
								if (report.data[i]["Gratis-Abos"] > 0 || report.data[i]["KK-Abos"] > 0 || report.data[i]["OK-Abos"] > 0 || report.data[i]["VIP-Abos"] > 0) {
									kunden.push(report.data[i].Kunde);
								}
							}
							//console.log(kunden);
							if (kunden.length > 0) {
								report.data = [];
								frappe.call({
									"method": "pflanzenfreund.pflanzenfreund.report.plausability_check.plausability_check.remove_all_abos_ws_affected",
									"args": {
										"kunden": kunden
									},
									"callback": function(r) {
										if (r.message == "OK") {
											frappe.msgprint("Die überflüssigen Abos wurden storniert.<br>Der Bericht wird neu geladen.", "Bereinigung abgeschlossen");
											frappe.show_alert("Bereinigung vollständig");
											report.refresh();
										}
									}
								});
							} else {
								frappe.msgprint("Es existieren keine überflüssigen Abos.", "Bereinigung abgeschlossen");
								frappe.show_alert("Bereinigung abgebrochen");
							}
						},
						function(){}
					)
			   }
			   if (report.filters[0].value == "Kunden mit Kundenkarte") {
				   frappe.confirm(
						'Wollen Sie alle unten ersichtlichen, überflüssigen Abos stornieren?',
						function(){
							/*
							Case 1: hat bezahlte abos und sonstige
							Case 2: keine bezahlten Abos aber Gratis/VIP Abos UND KK-Abos
							case 3: hat gar kein abo (ausser allenfalls ok)
							case 4: hat ok abo
							*/
							var case1 = [];
							var case2 = [];
							var case3 = [];
							var case4 = [];
							for (i=0;i<report.data.length;i++) {
								//case 1
								if ((report.data[i]["Jahres-Abos"] > 0 || report.data[i]["Probe-Abos"] > 0 || report.data[i]["Geschenk-Abos"] > 0) && (report.data[i]["Gratis-Abos"] > 0 || report.data[i]["KK-Abos"] > 0 || report.data[i]["VIP-Abos"] > 0)) {
									case1.push(report.data[i].Kunde);
								}
								
								//case 2
								if ((report.data[i]["Jahres-Abos"] == 0 && report.data[i]["Probe-Abos"] == 0 && report.data[i]["Geschenk-Abos"] == 0) && (report.data[i]["Gratis-Abos"] > 0 || report.data[i]["VIP-Abos"] > 0) && (report.data[i]["KK-Abos"] > 0)) {
									case2.push(report.data[i].Kunde);
								}
								
								//case 3
								if (report.data[i]["Jahres-Abos"] == 0 && report.data[i]["Probe-Abos"] == 0 && report.data[i]["Geschenk-Abos"] == 0 && report.data[i]["Gratis-Abos"] == 0 && report.data[i]["VIP-Abos"] == 0 && report.data[i]["KK-Abos"] == 0) {
									case3.push(report.data[i].Kunde);
								}
								
								//case 4
								if (report.data[i]["OK-Abos"] > 0) {
									case4.push(report.data[i].Kunde);
								}
							}
							/* console.log("case 1");
							console.log(case1);
							console.log("case 2");
							console.log(case2);
							console.log("case 3");
							console.log(case3);
							console.log("case 4");
							console.log(case4); */
							if ((case1.length > 0) || (case2.length > 0) || (case3.length > 0) || (case4.length > 0)) {
								report.data = [];
								
								if ((case3.length > 0)) {
									var d = new frappe.ui.Dialog({
										'title': __('Bitte selektieren Sie die gewünschten Ausgaben'),
										'fields': [
											{'fieldname': 'ht', 'fieldtype': 'HTML'},
											{'fieldname': 'ht_xx', 'fieldtype': 'Section Break', 'label': 'Ausgaben'},
											{'fieldname': 'winter_ed', 'fieldtype': 'Check', 'label': 'Winter'},
											{'fieldname': 'feb_ed', 'fieldtype': 'Check', 'label': 'Februar'},
											{'fieldname': 'mar_ed', 'fieldtype': 'Check', 'label': 'März'},
											{'fieldname': 'apr_ed', 'fieldtype': 'Check', 'label': 'April'},
											{'fieldname': 'may_ed', 'fieldtype': 'Check', 'label': 'Mai'},
											{'fieldname': 'break', 'fieldtype': 'Column Break'},
											//{'fieldname': 'ht_xx', 'fieldtype': 'HTML'},
											{'fieldname': 'jun_ed', 'fieldtype': 'Check', 'label': 'Juni'},
											{'fieldname': 'summer_ed', 'fieldtype': 'Check', 'label': 'Summer'},
											{'fieldname': 'sept_ed', 'fieldtype': 'Check', 'label': 'September'},
											{'fieldname': 'okt_ed', 'fieldtype': 'Check', 'label': 'Oktober'},
											{'fieldname': 'nov_ed', 'fieldtype': 'Check', 'label': 'November'}
										],
										primary_action: function(){
											d.hide();
											frappe.msgprint("Bitte warten");
											frappe.call({
												"method": "pflanzenfreund.pflanzenfreund.report.plausability_check.plausability_check.remove_abos_on_case_kk",
												"args": {
													"case1": case1,
													"case2": case2,
													"case3": case3,
													"case4": case4,
													"winter_ed": d.get_values().winter_ed,
													"feb_ed": d.get_values().feb_ed,
													"mar_ed": d.get_values().mar_ed,
													"apr_ed": d.get_values().apr_ed,
													"may_ed": d.get_values().may_ed,
													"jun_ed": d.get_values().jun_ed,
													"summer_ed": d.get_values().summer_ed,
													"sept_ed": d.get_values().sept_ed,
													"okt_ed": d.get_values().okt_ed,
													"nov_ed": d.get_values().nov_ed
												},
												"callback": function(r) {
													if (r.message == "OK") {
														frappe.msgprint("Die überflüssigen Abos wurden storniert/ergänzt.<br>Der Bericht wird neu geladen.", "Bereinigung abgeschlossen");
														frappe.show_alert("Bereinigung vollständig");
														report.refresh();
													}
												}
											});
										},
										primary_action_label: __('Start Bereinigung/Anlage')
									});
									d.fields_dict.ht.$wrapper.html('Wählen Sie <b>3 Ausgaben</b>');
									//d.fields_dict.ht_xx.$wrapper.html('<br><br>');
									d.show();
								} else {
									frappe.msgprint("Bitte warten");
									frappe.call({
										"method": "pflanzenfreund.pflanzenfreund.report.plausability_check.plausability_check.remove_abos_on_case_kk",
										"args": {
											"case1": case1,
											"case2": case2,
											"case3": case3,
											"case4": case4
										},
										"callback": function(r) {
											if (r.message == "OK") {
												frappe.msgprint("Die überflüssigen Abos wurden storniert.<br>Der Bericht wird neu geladen.", "Bereinigung abgeschlossen");
												frappe.show_alert("Bereinigung vollständig");
												report.refresh();
											}
										}
									});
								}
							} else {
								frappe.msgprint("Es existieren keine überflüssigen Abos.", "Bereinigung abgeschlossen");
								frappe.show_alert("Bereinigung abgebrochen");
							}
						},
						function(){}
					)
			   }
			   if (report.filters[0].value == "Kunden ohne Kundenkarte") {
				   frappe.confirm(
						'Wollen Sie alle unten ersichtlichen, überflüssigen Abos stornieren?',
						function(){
							/*
							Case 1: hat bezahlte abos und sonstige
							Case 2: keine bezahlten Abos aber Gratis/VIP Abos UND OK-Abos
							case 3: hat gar kein abo (ausser allenfalls kk)
							case 4: hat kk abo
							*/
							var case1 = [];
							var case2 = [];
							var case3 = [];
							var case4 = [];
							for (i=0;i<report.data.length;i++) {
								//case 1
								if ((report.data[i]["Jahres-Abos"] > 0 || report.data[i]["Probe-Abos"] > 0 || report.data[i]["Geschenk-Abos"] > 0) && (report.data[i]["Gratis-Abos"] > 0 || report.data[i]["OK-Abos"] > 0 || report.data[i]["VIP-Abos"] > 0)) {
									case1.push(report.data[i].Kunde);
								}
								
								//case 2
								if ((report.data[i]["Jahres-Abos"] == 0 && report.data[i]["Probe-Abos"] == 0 && report.data[i]["Geschenk-Abos"] == 0) && (report.data[i]["Gratis-Abos"] > 0 || report.data[i]["VIP-Abos"] > 0) && (report.data[i]["OK-Abos"] > 0)) {
									case2.push(report.data[i].Kunde);
								}
								
								//case 3
								if (report.data[i]["Jahres-Abos"] == 0 && report.data[i]["Probe-Abos"] == 0 && report.data[i]["Geschenk-Abos"] == 0 && report.data[i]["Gratis-Abos"] == 0 && report.data[i]["VIP-Abos"] == 0 && report.data[i]["OK-Abos"] == 0) {
									case3.push(report.data[i].Kunde);
								}
								
								//case 4
								if (report.data[i]["KK-Abos"] > 0) {
									case4.push(report.data[i].Kunde);
								}
							}
							/* console.log("case 1");
							console.log(case1);
							console.log("case 2");
							console.log(case2);
							console.log("case 3");
							console.log(case3);
							console.log("case 4");
							console.log(case4); */
							if ((case1.length > 0) || (case2.length > 0) || (case3.length > 0) || (case4.length > 0)) {
								report.data = [];
								if ((case3.length > 0)) {
									var d = new frappe.ui.Dialog({
										'title': __('Bitte selektieren Sie die gewünschten Ausgaben'),
										'fields': [
											{'fieldname': 'ht', 'fieldtype': 'HTML'},
											{'fieldname': 'ht_xx', 'fieldtype': 'Section Break', 'label': 'Ausgaben'},
											{'fieldname': 'winter_ed', 'fieldtype': 'Check', 'label': 'Winter'},
											{'fieldname': 'feb_ed', 'fieldtype': 'Check', 'label': 'Februar'},
											{'fieldname': 'mar_ed', 'fieldtype': 'Check', 'label': 'März'},
											{'fieldname': 'apr_ed', 'fieldtype': 'Check', 'label': 'April'},
											{'fieldname': 'may_ed', 'fieldtype': 'Check', 'label': 'Mai'},
											{'fieldname': 'break', 'fieldtype': 'Column Break'},
											//{'fieldname': 'ht_xx', 'fieldtype': 'HTML'},
											{'fieldname': 'jun_ed', 'fieldtype': 'Check', 'label': 'Juni'},
											{'fieldname': 'summer_ed', 'fieldtype': 'Check', 'label': 'Summer'},
											{'fieldname': 'sept_ed', 'fieldtype': 'Check', 'label': 'September'},
											{'fieldname': 'okt_ed', 'fieldtype': 'Check', 'label': 'Oktober'},
											{'fieldname': 'nov_ed', 'fieldtype': 'Check', 'label': 'November'}
										],
										primary_action: function(){
											d.hide();
											frappe.msgprint("Bitte warten");
											frappe.call({
												"method": "pflanzenfreund.pflanzenfreund.report.plausability_check.plausability_check.remove_abos_on_case_ok",
												"args": {
													"case1": case1,
													"case2": case2,
													"case3": case3,
													"case4": case4,
													"winter_ed": d.get_values().winter_ed,
													"feb_ed": d.get_values().feb_ed,
													"mar_ed": d.get_values().mar_ed,
													"apr_ed": d.get_values().apr_ed,
													"may_ed": d.get_values().may_ed,
													"jun_ed": d.get_values().jun_ed,
													"summer_ed": d.get_values().summer_ed,
													"sept_ed": d.get_values().sept_ed,
													"okt_ed": d.get_values().okt_ed,
													"nov_ed": d.get_values().nov_ed
												},
												"callback": function(r) {
													if (r.message == "OK") {
														frappe.msgprint("Die überflüssigen Abos wurden storniert/ergänzt.<br>Der Bericht wird neu geladen.", "Bereinigung abgeschlossen");
														frappe.show_alert("Bereinigung vollständig");
														report.refresh();
													}
												}
											});
										},
										primary_action_label: __('Start Bereinigung/Anlage')
									});
									d.fields_dict.ht.$wrapper.html('Wählen Sie <b>2 Ausgaben</b>');
									//d.fields_dict.ht_xx.$wrapper.html('<br><br>');
									d.show();
								} else {
									frappe.msgprint("Bitte warten");
									frappe.call({
										"method": "pflanzenfreund.pflanzenfreund.report.plausability_check.plausability_check.remove_abos_on_case_ok",
										"args": {
											"case1": case1,
											"case2": case2,
											"case3": case3,
											"case4": case4
										},
										"callback": function(r) {
											if (r.message == "OK") {
												frappe.msgprint("Die überflüssigen Abos wurden storniert.<br>Der Bericht wird neu geladen.", "Bereinigung abgeschlossen");
												frappe.show_alert("Bereinigung vollständig");
												report.refresh();
											}
										}
									});
								}
							} else {
								frappe.msgprint("Es existieren keine überflüssigen Abos.", "Bereinigung abgeschlossen");
								frappe.show_alert("Bereinigung abgebrochen");
							}
						},
						function(){}
					)
			   }
		   } else {
			   frappe.msgprint("Bitte warten bis der Report geladen ist...", "Bitte warten");
		   }
		   //console.log(report);
		});
	}
}
