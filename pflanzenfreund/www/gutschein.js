function betrag() {
	var auswahl = document.getElementById("sel1");
	var betragfeld = document.getElementById("betrag_gruppe");
	if (auswahl.value == 'Eigener Betrag') {
		betragfeld.classList.remove("hidden");
	} else {
		if (betragfeld.classList.contains("hidden")) {} else {
			betragfeld.classList.add("hidden");
		}
	}
}

function count() {
	var feld = document.getElementById("comment");
	var rest = 160 - feld.value.length;
	var anzahl_zeichen = document.getElementById("anzahlzeichen");
	anzahl_zeichen.innerHTML = rest.toString() + " Zeichen übrig";
}

function vorschau() {
	var url = 'http://localhost/api/method/frappe.utils.print_format.download_pdf?doctype=Pflanzenfreund%20Abo&name=ABO-0139397&format=Geschenk%20Brief&no_letterhead=0';
	var win = window.open(url, '_blank');
	win.focus();
}