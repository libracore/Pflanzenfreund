var bestell_seite = location.search.substring(10);
set_main_setup(bestell_seite);
set_user_data();
set_start_date();

function set_main_setup(bestell_seite) {
	if (bestell_seite == "Jahres-Abo") {
		document.getElementById("abo_typ").value = "Jahres-Abonnement";
		document.getElementById("bestellung_von_breadcrumb").innerHTML = "Bestellung Jahres-Abonnement";
		document.getElementById("jahres_abo").classList.toggle('hidden');
		document.getElementById("winter").checked = true;
		document.getElementById("feb").checked = true;
		document.getElementById("mar").checked = true;
		document.getElementById("apr").checked = true;
		document.getElementById("mai").checked = true;
		document.getElementById("jun").checked = true;
		document.getElementById("sommer").checked = true;
		document.getElementById("sept").checked = true;
		document.getElementById("okt").checked = true;
		document.getElementById("nov").checked = true;
	} else if(bestell_seite == "Probe-Abo") {
		document.getElementById("abo_typ").value = "Probe-Abonnement";
		document.getElementById("bestellung_von_breadcrumb").innerHTML = "Bestellung Probe-Abonnement";
		document.getElementById("probe_abo").classList.toggle('hidden');
	} else if(bestell_seite == "Geschenk-Abo") {
		document.getElementById("abo_typ").value = "Geschenk-Abonnement";
		document.getElementById("bestellung_von_breadcrumb").innerHTML = "Bestellung Geschenk-Abonnement";
		document.getElementById("ihre_ausgaben_label").innerHTML = "Verschenkte Ausgaben";
		document.getElementById("geschenk_abo").classList.toggle('hidden');
		document.getElementById("beschenkter").classList.toggle('hidden');
		document.getElementById("winter").checked = true;
		document.getElementById("feb").checked = true;
		document.getElementById("mar").checked = true;
		document.getElementById("apr").checked = true;
		document.getElementById("mai").checked = true;
		document.getElementById("jun").checked = true;
		document.getElementById("sommer").checked = true;
		document.getElementById("sept").checked = true;
		document.getElementById("okt").checked = true;
		document.getElementById("nov").checked = true;
	}
}

function set_user_data() {
	document.getElementById("vorname").value = "{{ user_data.first_name }}";
	document.getElementById("nachname").value = "{{ user_data.last_name }}";
	document.getElementById("strasse").value = "{{ address.address_line1 }}".replace("{{ address.address_line1 }}".split(" ")["{{ address.address_line1 }}".split(" ").length - 1], "");
	document.getElementById("nummer").value = "{{ address.address_line1 }}".split(" ")["{{ address.address_line1 }}".split(" ").length - 1];
	document.getElementById("plz").value = "{{ address.pincode }}";
	document.getElementById("ort").value = "{{ address.city }}";
	document.getElementById("email").value = "{{ user_data.email_id }}";
	if ("{{ user_data.salutation }}" == "Herr") {
		document.getElementById("herr").checked = true;
	} else if ("{{ user_data.salutation }}" == "Frau") {
		document.getElementById("frau").checked = true;
	}
}

function set_start_date() {
	var date = new Date();
	if (date.getDate() >= 15) {
		date = new Date(new Date(date.setMonth(date.getMonth() + 1))).setDate(1);
	}
	document.getElementById("start").value = new Date(date).toISOString().slice(0,10);
	set_end_date(_date=new Date(date));
}

function set_end_date(_date) {
	var date = new Date(_date);
	var year = date.getFullYear();
	var month = date.getMonth();
	var day = date.getDate();
	
	if(bestell_seite == "Probe-Abo") {
		var abo_start = month + 1;
		var shift = 0;
		var shift_list = [1, 5, 6, 7, 8, 10, 11, 12];
		
		if (shift_list.indexOf(month + 1) >= 0) {
			shift = 1;
		}
		
		if ((month + 2) > 11) {
			month = (month + 2) - 11;
			year = year + 1;
		} else {
			month = (month + 3);
		}
		
		month = month + shift;
		
		var date_in_four_months = new Date(year, month, 15, 10);
		document.getElementById("ende").value = new Date(date_in_four_months).toISOString().slice(0,10);
		
		set_probe_abo_ausgaben(abo_start=abo_start);
	} else {
		year = year + 1;
		var date_in_one_year = new Date(year, month, day, 10);
		document.getElementById("ende").value = new Date(date_in_one_year).toISOString().slice(0,10);
	}
}

function set_probe_abo_ausgaben(abo_start) {
	document.getElementById("winter").checked = false;
	document.getElementById("feb").checked = false;
	document.getElementById("mar").checked = false;
	document.getElementById("apr").checked = false;
	document.getElementById("mai").checked = false;
	document.getElementById("jun").checked = false;
	document.getElementById("sommer").checked = false;
	document.getElementById("sept").checked = false;
	document.getElementById("okt").checked = false;
	document.getElementById("nov").checked = false;
	
	if (abo_start == 1) {
		document.getElementById("feb").checked = true;
		document.getElementById("mar").checked = true;
		document.getElementById("apr").checked = true;
		document.getElementById("mai").checked = true;
	} else if (abo_start == 2) {
		document.getElementById("feb").checked = true;
		document.getElementById("mar").checked = true;
		document.getElementById("apr").checked = true;
		document.getElementById("mai").checked = true;
	} else if (abo_start == 3) {
		document.getElementById("mar").checked = true;
		document.getElementById("apr").checked = true;
		document.getElementById("mai").checked = true;
		document.getElementById("jun").checked = true;
	} else if (abo_start == 4) {
		document.getElementById("apr").checked = true;
		document.getElementById("mai").checked = true;
		document.getElementById("jun").checked = true;
		document.getElementById("sommer").checked = true;
	} else if (abo_start == 5) {
		document.getElementById("mai").checked = true;
		document.getElementById("jun").checked = true;
		document.getElementById("sommer").checked = true;
		document.getElementById("sept").checked = true;
	} else if (abo_start == 6) {
		document.getElementById("jun").checked = true;
		document.getElementById("sommer").checked = true;
		document.getElementById("sept").checked = true;
		document.getElementById("okt").checked = true;
	} else if (abo_start == 7) {
		document.getElementById("sommer").checked = true;
		document.getElementById("sept").checked = true;
		document.getElementById("okt").checked = true;
		document.getElementById("nov").checked = true;
	} else if (abo_start == 8) {
		document.getElementById("sept").checked = true;
		document.getElementById("okt").checked = true;
		document.getElementById("nov").checked = true;
		document.getElementById("winter").checked = true;
	} else if (abo_start == 9) {
		document.getElementById("sept").checked = true;
		document.getElementById("okt").checked = true;
		document.getElementById("nov").checked = true;
		document.getElementById("winter").checked = true;
	} else if (abo_start == 10) {
		document.getElementById("okt").checked = true;
		document.getElementById("nov").checked = true;
		document.getElementById("winter").checked = true;
		document.getElementById("feb").checked = true;
	} else if (abo_start == 11) {
		document.getElementById("nov").checked = true;
		document.getElementById("winter").checked = true;
		document.getElementById("feb").checked = true;
		document.getElementById("mar").checked = true;
	} else if (abo_start == 12) {
		document.getElementById("winter").checked = true;
		document.getElementById("feb").checked = true;
		document.getElementById("mar").checked = true;
		document.getElementById("apr").checked = true;
	}
}

function change_start() {
	var start = new Date(document.getElementById("start").value);
	var now = new Date();
	if (start < now) {
		set_start_date();
		frappe.msgprint("Das Startdatum darf nicht vor heute sein.", "Zu frühes Startdatum");
	} else if (start.getDate() >= 15) {
		var _start = new Date(new Date(start).setMonth(new Date(start).getMonth() + 1));
		new_start = new Date(new Date(_start).setDate(1));
		document.getElementById("start").value = new_start.toISOString().slice(0,10);
		frappe.msgprint("Der pünktliche Versand der aktuellsten Monatsausgabe kann nur gewährleistet werden, sofern das Startdatum vor dem 15. des Monats ist.<br>Das Startdatum wurde automatisch auf das nächst mögliche gelegt.", "Automatisches Start Datum");
		set_end_date(_date=new Date(document.getElementById("start").value));
	} else {
		set_end_date(_date=new Date(document.getElementById("start").value));
	}
}

function bestellung_popup() {
	/* var confirm_txt = '<h3>Bestellübersicht</h3><br>' +
		'Abonnement: ' + bestell_seite + '<br>' +
		'Abo-Start: ' + new Date(document.getElementById("start").value).toISOString().slice(0,10) + '<br>' +
		'Abo-Ende: ' + new Date(document.getElementById("ende").value).toISOString().slice(0,10) + '<br><br>' +
		'<button class="btn btn-default" onclick="bestellung_platzieren();" style="width: 25%;">Bestellen</button><br><br>' +
		'<button class="btn btn-default" onclick="bestellung_storno();" style="width: 25%;">Bestellung ändern</button>';
	frappe.show_message(confirm_txt, 'fa fa-shopping-cart pf-icon'); */
	if (bestell_seite != "Probe-Abo") {
		var preis = 'Fr. 42.-';
	} else {
		var preis = 'Fr. 17.-';
	}
	if (bestell_seite != "Geschenk-Abo") {
		$("#bestelluebersicht_text").html('<p><b>Abo:</b><br>' + bestell_seite + '</p>' +
			'<p><b>Adresse:</b><br>' +
			'{{ user_data.salutation }}<br>' +
			document.getElementById("vorname").value + ' ' + document.getElementById("nachname").value + '<br>' +
			document.getElementById("strasse").value + ' ' + document.getElementById("nummer").value + '<br>' +
			document.getElementById("plz").value + ' ' + document.getElementById("ort").value + '<br>' +
			document.getElementById("email").value +
			'<p><b>Preis:</b><br>' + preis);
	} else {
		if (document.getElementById("frau_geschenk").checked) {
			var anrede_geschenk = 'Frau';
		} else {
			var anrede_geschenk = 'Herr';
		}
		$("#bestelluebersicht_text").html('<p><b>Abo:</b><br>' + bestell_seite + '</p>' +
			'<p><b>Geschenk-Empfänger:</b><br>' +
			anrede_geschenk + '<br>' +
			document.getElementById("vorname_geschenk").value + ' ' + document.getElementById("nachname_geschenk").value + '<br>' +
			document.getElementById("strasse_geschenk").value + ' ' + document.getElementById("nummer_geschenk").value + '<br>' +
			document.getElementById("plz_geschenk").value + ' ' + document.getElementById("ort_geschenk").value +
			'<p><b>Rechnungsadresse:</b><br>' +
			'{{ user_data.salutation }}<br>' +
			document.getElementById("vorname").value + ' ' + document.getElementById("nachname").value + '<br>' +
			document.getElementById("strasse").value + ' ' + document.getElementById("nummer").value + '<br>' +
			document.getElementById("plz").value + ' ' + document.getElementById("ort").value + '<br>' +
			document.getElementById("email").value +
			'<p><b>Preis:</b><br>' + preis);
	}
	$("#bestelluebersicht").css("display", "block");
}

function bestellung_storno() {
	//frappe.hide_message();
	$("#bestelluebersicht").css("display", "none");
}

function bestellung_platzieren() {
	//frappe.hide_message();
	$("#bestelluebersicht").css("display", "none");
	var start = new Date(document.getElementById("start").value);
	var ende = new Date(document.getElementById("ende").value);
	if (bestell_seite != 'Geschenk-Abo') {
		frappe.call({
			method: 'pflanzenfreund.www.orderabo.place_abo_order',
			args: {
				"customer": "{{ customer }}",
				"address": "{{ address.name }}",
				"abo_type": bestell_seite,
				"start_date": start.getFullYear() + "-" + (start.getMonth() + 1) + "-" + start.getDate(),
				"end_date": ende.getFullYear() + "-" + (ende.getMonth() + 1) + "-" + ende.getDate(),
				"winter": document.getElementById("winter").checked? 1 : 0,
				"feb": document.getElementById("feb").checked? 1 : 0,
				"mar": document.getElementById("mar").checked? 1 : 0,
				"apr": document.getElementById("apr").checked? 1 : 0,
				"may": document.getElementById("mai").checked? 1 : 0,
				"jun": document.getElementById("jun").checked? 1 : 0,
				"summer": document.getElementById("sommer").checked? 1 : 0,
				"sept": document.getElementById("sept").checked? 1 : 0,
				"oct": document.getElementById("okt").checked? 1 : 0,
				"nov": document.getElementById("nov").checked? 1 : 0
			},
			freeze: true,
			freeze_message: "Bitte warten bis die Abo-Bestellung abgeschlossen ist.",
			callback: function(r) {
				//console.log(r.message);
				window.open("/bestaetigung","_self")
			}
		});
	} else {
		var control_inputs = document.getElementsByClassName("pf-alert");
		if (control_inputs.length > 0) {
			frappe.msgprint("Bitte zuerst alle Pflichtfelder ausfüllen.", "Leere Pflichtfelder");
		} else {
			frappe.call({
				method: 'pflanzenfreund.www.orderabo.place_abo_order',
				args: {
					"customer": "{{ customer }}",
					"address": "{{ address.name }}",
					"abo_type": bestell_seite,
					"start_date": start.getFullYear() + "-" + (start.getMonth() + 1) + "-" + start.getDate(),
					"end_date": ende.getFullYear() + "-" + (ende.getMonth() + 1) + "-" + ende.getDate(),
					"winter": document.getElementById("winter").checked? 1 : 0,
					"feb": document.getElementById("feb").checked? 1 : 0,
					"mar": document.getElementById("mar").checked? 1 : 0,
					"apr": document.getElementById("apr").checked? 1 : 0,
					"may": document.getElementById("mai").checked? 1 : 0,
					"jun": document.getElementById("jun").checked? 1 : 0,
					"summer": document.getElementById("sommer").checked? 1 : 0,
					"sept": document.getElementById("sept").checked? 1 : 0,
					"oct": document.getElementById("okt").checked? 1 : 0,
					"nov": document.getElementById("nov").checked? 1 : 0,
					"donee_name": document.getElementById("vorname_geschenk").value + " " + document.getElementById("nachname_geschenk").value,
					"street": document.getElementById("strasse_geschenk").value + " " + document.getElementById("nummer_geschenk").value,
					"pincode": document.getElementById("plz_geschenk").value,
					"city": document.getElementById("ort_geschenk").value
				},
				freeze: true,
				freeze_message: "Bitte warten bis die Abo-Bestellung abgeschlossen ist.",
				callback: function(r) {
					//console.log(r.message);
					window.open("/bestaetigung","_self")
				}
			});
		}
	}
}

function check_value(input) {
	if (input.value != '') {
		if (input.classList.contains('pf-alert')) {
			input.classList.toggle('pf-alert');
		}
	} else if (input.value == '') {
		if (!input.classList.contains('pf-alert')) {
			input.classList.toggle('pf-alert');
		}
	}
}