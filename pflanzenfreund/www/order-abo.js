var bestell_seite = location.search.substring(10);
console.log(bestell_seite);
set_abo_data(bestell_seite);

function set_abo_data(bestell_seite) {
	if (bestell_seite == "Jahres-Abo") {
		document.getElementById("abo_typ").value = "Jahres-Abonnement";
		document.getElementById("bestellung_von_breadcrumb").innerHTML = "Bestellung Jahres-Abonnement";
		document.getElementById("jahres_abo").classList.toggle('hidden');
		var date = new Date();
		var currentDate = date.toISOString().slice(0,10);
		var in_a_year = new Date(new Date().setFullYear(new Date().getFullYear() + 1));
		var in_a_year_date = in_a_year.toISOString().slice(0,10);
		document.getElementById("start").value = currentDate;
		document.getElementById("ende").value = in_a_year_date;
	} else if(bestell_seite == "Probe-Abo") {
		document.getElementById("abo_typ").value = "Probe-Abonnement";
		document.getElementById("bestellung_von_breadcrumb").innerHTML = "Bestellung Probe-Abonnement";
		document.getElementById("probe_abo").classList.toggle('hidden');
		var date = new Date();
		var currentDate = date.toISOString().slice(0,10);
		var in_four_months = new Date(new Date().setMonth(new Date().getMonth() + 4));
		var in_four_months_date = in_four_months.toISOString().slice(0,10);
		document.getElementById("start").value = currentDate;
		document.getElementById("ende").value = in_four_months_date;
	} else if(bestell_seite == "Geschenk-Abo") {
		document.getElementById("abo_typ").value = "Geschenk-Abonnement";
		document.getElementById("bestellung_von_breadcrumb").innerHTML = "Bestellung Geschenk-Abonnement";
		document.getElementById("ihre_ausgaben_label").innerHTML = "Verschenkte Ausgaben";
		document.getElementById("geschenk_abo").classList.toggle('hidden');
		document.getElementById("beschenkter").classList.toggle('hidden');
		var date = new Date();
		var currentDate = date.toISOString().slice(0,10);
		var in_a_year = new Date(new Date().setFullYear(new Date().getFullYear() + 1));
		var in_a_year_date = in_a_year.toISOString().slice(0,10);
		document.getElementById("start").value = currentDate;
		document.getElementById("ende").value = in_a_year_date;
	}
}

function change_start() {
	var start = new Date(document.getElementById("start").value);
	var now = new Date();
	if(bestell_seite != "Probe-Abo") {
		if (start < now) {
			var currentDate = now.toISOString().slice(0,10);
			document.getElementById("start").value = currentDate;
			var in_a_year = new Date(new Date().setFullYear(new Date().getFullYear() + 1));
			var in_a_year_date = in_a_year.toISOString().slice(0,10);
			document.getElementById("ende").value = in_a_year_date;
			frappe.msgprint("Das Datum darf nicht in der vergangenheit liegen.");
		} else {
			var in_a_year = new Date(new Date(start).setFullYear(start.getFullYear() + 1));
			var in_a_year_date = in_a_year.toISOString().slice(0,10);
			document.getElementById("ende").value = in_a_year_date;
		}
	} else {
		if (start < now) {
			var date = new Date();
			var currentDate = date.toISOString().slice(0,10);
			var in_four_months = new Date(new Date().setMonth(new Date().getMonth() + 4));
			var in_four_months_date = in_four_months.toISOString().slice(0,10);
			document.getElementById("start").value = currentDate;
			document.getElementById("ende").value = in_four_months_date;
			frappe.msgprint("Das Datum darf nicht in der vergangenheit liegen.");
		} else {
			var in_four_months = new Date(new Date(start).setMonth(new Date().getMonth() + 4));
			var in_four_months_date = in_four_months.toISOString().slice(0,10);
			document.getElementById("ende").value = in_four_months_date;
		}
	}
}

function bestellung_platzieren() {
	
}