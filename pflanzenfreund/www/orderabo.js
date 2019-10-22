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
	document.getElementById("strasse").value = "{{ address.address_line1 }}".split(" ")["{{ address.address_line1 }}".split.length - 2];
	document.getElementById("nummer").value = "{{ address.address_line1 }}".split(" ")["{{ address.address_line1 }}".split.length - 1];
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

function bestellung_platzieren() {
	
}