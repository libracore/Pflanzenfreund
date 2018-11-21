frappe.pages['abo_rechnungslauf'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Abo Verlängerung und Rechnungslauf',
		single_column: true
	});
	
	frappe.abo_rechnungslauf.make(page);
	frappe.abo_rechnungslauf.run(page);
	page.job_content = $(page.body).find('#placeForWorkers');
	// add the application reference
	frappe.breadcrumbs.add("Pflanzenfreund");
}

frappe.abo_rechnungslauf = {
	start: 0,
	make: function(page) {
		var me = frappe.abo_rechnungslauf;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		var data = "";
		$(frappe.render_template('abo_rechnungslauf', data)).appendTo(me.body);
		

	},
	run: function(page) {
 
	}
}

frappe.pages['abo_rechnungslauf'].on_page_show = function(wrapper) {
	frappe.pages.abo_rechnungslauf.refresh_jobs();
}

frappe.pages.abo_rechnungslauf.refresh_jobs = function() {
	var page = frappe.pages.abo_rechnungslauf.page;

	// don't call if already waiting for a response
	if(page.called) return;
	page.called = true;
	frappe.call({
		method: 'pflanzenfreund.utils.list_all_pdfs',
		callback: function(r) {
			page.called = false;
			page.body.find('.list-jobs').remove();
			$(frappe.render_template('background_jobs', {onlyfiles:r.message || []})).appendTo(page.job_content);

			if(frappe.get_route()[0]==='abo_rechnungslauf') {
				frappe.background_jobs_timeout = setTimeout(frappe.pages.abo_rechnungslauf.refresh_jobs, 2000);
			}
		}
	});
}


function showPromotionBullet() {
	document.getElementById("promotion-bullet").classList.toggle('hidden');
	if (!document.getElementById("geschenk-bullet").classList.contains('hidden')) {
		document.getElementById("geschenk-bullet").classList.add('hidden');
	}
	document.getElementById("bullet-text").classList.remove('hidden');
}
function showGeschenkBullet() {
	document.getElementById("geschenk-bullet").classList.toggle('hidden');
	if (!document.getElementById("promotion-bullet").classList.contains('hidden')) {
		document.getElementById("promotion-bullet").classList.add('hidden');
	}
	document.getElementById("bullet-text").classList.remove('hidden');
}
function hideBullets() {
	document.getElementById("promotion-bullet").classList.add('hidden');
	document.getElementById("geschenk-bullet").classList.add('hidden');
	document.getElementById("bullet-text").classList.add('hidden');
}

function createNewInvoices() {
	
	var periode_start = document.getElementById("start").value;
	var periode_end = document.getElementById("end").value;
	var printformat = document.getElementById("printformat").value;
	console.log(printformat);
	
	var abo_type = document.getElementById("abo-typ").value;
	var rechnungsdatum = document.getElementById("vordatierung").value;
	if (!rechnungsdatum) {
		rechnungsdatum = frappe.datetime.get_today();
	}
	
	
	
	var bullet = 'kein';
	var bullet_text = 'kein';
	/* aktuell nicht gebraucht */
	/* if (!document.getElementById("promotion-bullet").classList.contains('hidden')) {
		bullet = 'Promotion';
		bullet_text = document.getElementById("comment").value;
	} else if (!document.getElementById("geschenk-bullet").classList.contains('hidden')) {
		bullet = 'Geschenk';
		bullet_text = document.getElementById("comment").value;
	} */
	/* -------------------------------- */
	
	if (!periode_start){
		frappe.msgprint('Bitte wählen Sie mindestens <b>Abo Ablaufdatum von:</b> aus.', 'Mangelhafte Angaben');
		return false;
	}
	if (!periode_end){
		frappe.confirm(
			"Sie haben kein <b>Perioden Ende</b> ausgewählt, es wird als default 2099-01-01 ausgewählt.<br><b>Alle Abo's die zwischen "+periode_start+" und 2099-01-01 ablaufen werden verlängert!<b>",
			function(){
				//console.log(abo_type);
				//start_without_end_createNewInvoices(periode_start, abo_type, bullet, bullet_text);
				checkQTY(periode_start, '2099-01-01', abo_type, bullet, bullet_text, rechnungsdatum, printformat);
				return false;
			},
			function(){
				return false;
			}
		)
	} else {
		//start_createNewInvoices(periode_start, periode_end, abo_type, bullet, bullet_text);
		checkQTY(periode_start, periode_end, abo_type, bullet, bullet_text, rechnungsdatum, printformat);
	}
}

function checkQTY(periode_start, periode_end, abo_type, bullet, bullet_text, rechnungsdatum, printformat) {
	openNav();
	frappe.call({
		method: 'pflanzenfreund.utils.qty_abo_rechnungslauf',
		args: {
			'start': periode_start,
			'end': periode_end,
			'abo_type': abo_type
		},
		callback: function(r) {
			if (r.message) {
				closeNav();
				console.log(r.message);
				frappe.confirm(
					"Ihre Auswahl beinhaltet " + r.message + " Abonnemente. Dies kann einen Moment dauern.<br>Die Ausführung wird dem Background-Worker übergeben.<br>Möchten Sie fortfahren?",
					function(){
						frappe.msgprint("Der Job wurde dem Background-Worker übergeben.<br>Sie erhalten eine Information sobald der Job erfolgreich abgeschlossen ist.<br>Alternativ können Sie den Fortschritt auch <a href='/desk#background_jobs'>hier</a> einsehen.");
						console.log(r.message);
						start_createNewInvoices(periode_start, periode_end, abo_type, bullet, bullet_text, 'yes', rechnungsdatum, printformat);
					},
					function(){
						return false;
					}
				)
			} else {
				closeNav();
				frappe.msgprint('Es wurden keine Abos gefunden, die den Kriterien entsprechen.', 'Kein Output');
			}
		}
	});
}

/* function start_without_end_createNewInvoices(periode_start, abo, bullet, bullet_text) {
	openNav();
	frappe.call({
		method: 'pflanzenfreund.utils.createNewInvoices_abo_rechnungslauf',
		args: {
			'start': periode_start,
			'end': '2099-01-01',
			'abo_type': abo,
			'bullet_type': bullet,
			'bullet_text': bullet_text
		},
		callback: function(r) {
			if (r.message) {
				closeNav();
				//console.log(r.message);
				if (document.getElementById("myTable").classList.contains('hidden')) {
					document.getElementById("myTable").classList.toggle('hidden');
				}
				var tabelle = document.getElementById("myTable");
				var rowCount = tabelle.rows.length;
				for (var i = rowCount - 1; i > 0; i--) {
					tabelle.deleteRow(i);
				}
				for (i=0;i<r.message.length;i++) {
					crateTableContentElement(r.message[i][0], r.message[i][1]);
				}
			} else {
				closeNav();
				frappe.msgprint('Es wurden keine Abos gefunden, die den Kriterien entsprechen.', 'Kein Output');
			}
		}
	});
} */

function start_createNewInvoices(periode_start, periode_end, abo, bullet, bullet_text, background, rechnungsdatum, printformat) {
	openNav();
	frappe.call({
		method: 'pflanzenfreund.utils.createNewInvoices_abo_rechnungslauf',
		args: {
			'start': periode_start,
			'end': periode_end,
			'abo_type': abo,
			'bullet_type': bullet,
			'bullet_text': bullet_text,
			'background': background,
			'rechnungsdatum': rechnungsdatum,
			'printformat': printformat
		},
		callback: function(r) {
			if (r.message) {
				closeNav();
				//console.log(r.message);
				if (document.getElementById("myTable").classList.contains('hidden')) {
					document.getElementById("myTable").classList.toggle('hidden');
				}
				var tabelle = document.getElementById("myTable");
				var rowCount = tabelle.rows.length;
				for (var i = rowCount - 1; i > 0; i--) {
					tabelle.deleteRow(i);
				}
				for (i=0;i<r.message.length;i++) {
					crateTableContentElement(r.message[i][0], r.message[i][1]);
				}
			} else {
				closeNav();
				frappe.msgprint('Es wurden keine Abos gefunden, die den Kriterien entsprechen.', 'Kein Output');
			}
		}
	});
}



/* Open */
function openNav() {
    document.getElementById("myNav").style.display = "block";
}

/* Close */
function closeNav() {
    document.getElementById("myNav").style.display = "none";
}

function crateTableContentElement(abo, invoice) {
	//console.log(name+" "+address+" "+pincode+" "+city);
	var tabelle = document.getElementById("myTable");
	
	var tr = document.createElement("tr");
	
	var td_abo = document.createElement("td");
	td_abo.setAttribute("style", "cursor:alias;");
	var td_invoice = document.createElement("td");
	td_invoice.setAttribute("style", "cursor:alias;");
	
	var td_abo_txt = document.createTextNode(abo);
	var td_invoice_txt = document.createTextNode(invoice);
	
	td_abo.appendChild(td_abo_txt);
	td_invoice.appendChild(td_invoice_txt);
	
	td_abo.onclick = function() { 
		window.location = '/desk#Form/Pflanzenfreund Abo/' + abo;
	};
	td_invoice.onclick = function() { 
		window.location = '/desk#Form/Sales Invoice/' + invoice;
	};
	
	tr.appendChild(td_abo);
	tr.appendChild(td_invoice);
	
	tabelle.appendChild(tr);
	
}


function createBindPDF() {
	var rechnungsdatum = document.getElementById("vordatierung").value;
	if (!rechnungsdatum) {
		rechnungsdatum = frappe.datetime.get_today();
	}
	var printformat = document.getElementById("printformat").value;
	frappe.confirm(
		"Wollen Sie ein Sammel-PDF aller gültigen Rechnungen mit dem Valuta-Datum " + rechnungsdatum + " erstellen?",
		function(){
			frappe.msgprint("Der Job wurde dem Background-Worker übergeben.<br>Sie erhalten eine Information sobald der Job erfolgreich abgeschlossen ist.<br>Alternativ können Sie den Fortschritt auch <a href='/desk#background_jobs'>hier</a> einsehen.");
			startCreateBindPDF(rechnungsdatum, printformat);
		},
		function(){
			return false;
		}
	)
}




function startCreateBindPDF(rechnungsdatum, printformat) {
	frappe.call({
		method: 'pflanzenfreund.utils.createSammelPDF',
		args: {
			'valuta': rechnungsdatum,
			'printformat': printformat
		},
		callback: function(r) {
			
		}
	});
}

function deleteAllPDF() {
	frappe.confirm(
		"Wollen Sie alle oben aufgeführten PDF's vom Server entfernen?<br>Sie können diese nachträglich auch wieder erstellen.",
		function(){
			frappe.call({
				method: 'pflanzenfreund.utils.remove_downloaded_pdf',
				callback: function(r) {
					frappe.msgprint("Die PDF's wurden entfernt");
				}
			});
		},
		function(){
			return false;
		}
	)
}