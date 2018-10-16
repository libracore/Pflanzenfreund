frappe.pages['abo_plausibility'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Abo Plausibilitätsprüfung',
		single_column: true
	});
	
	
	
	frappe.abo_plausibility.make(page);
	frappe.abo_plausibility.run(page);
	$(frappe.render_template('background_jobs_outer')).appendTo(page.body);
	page.job_content = $(page.body).find('.table-area');
	frappe.pages.abo_plausibility.page = page;
	
	// add the application reference
	frappe.breadcrumbs.add("Pflanzenfreund");
}

frappe.abo_plausibility = {
	start: 0,
	make: function(page) {
		var me = frappe.abo_plausibility;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		var data = "";
		$(frappe.render_template('abo_plausibility', data)).appendTo(me.body);
		

	},
	run: function(page) {
 
	}
}



frappe.pages['abo_plausibility'].on_page_show = function(wrapper) {
	frappe.pages.abo_plausibility.refresh_jobs();
}

frappe.pages.abo_plausibility.refresh_jobs = function() {
	var page = frappe.pages.abo_plausibility.page;

	// don't call if already waiting for a response
	if(page.called) return;
	page.called = true;
	frappe.call({
		method: 'frappe.core.page.background_jobs.background_jobs.get_info',
		args: {
			show_failed: page.body.find('.show-failed').prop('checked') ? 1 : 0
		},
		callback: function(r) {
			page.called = false;
			page.body.find('.list-jobs').remove();
			$(frappe.render_template('background_jobs', {jobs:r.message || []})).appendTo(page.job_content);

			if(frappe.get_route()[0]==='abo_plausibility') {
				frappe.background_jobs_timeout = setTimeout(frappe.pages.abo_plausibility.refresh_jobs, 2000);
			}
		}
	});
}


function readExistCheck() {
	var mod = document.getElementById("check-typ").value;
	frappe.call({
		method: 'pflanzenfreund.pflanzenfreund.page.abo_plausibility.utils.read_log',
		args: {
			'mod': mod
		},
		callback: function(r) {
			if (r.message) {
				closeNav();
				console.log(r.message);
				deleteTable();
				if (r.message[0][0] == "empty") {
					frappe.msgprint('Die Plausibilitätsprüfung wurde ohne Resultate abgeschlossen.', 'Keine unplausiblen Daten');
				} else if (r.message == "abort") {
					frappe.msgprint('Die vorhandenen Daten der Plausibilitätsprüfung wurden bereits ausgewertet.<br>Damit Fehler vermieden werden können, führen Sie die Aufbereitung der Daten nochmals durch.', 'Bitte Datenaufbereitung erneut durchführen');
				} else if (r.message == "not found") {
					frappe.msgprint('Die gewünschte Plausibilitätsprüfung wurde noch nicht ausgeführt.<br>Bitte führen Sie zuerst die Aufbereitung der Daten durch.', 'Bitte Datenaufbereitung durchführen');
				} else {
					for (i = 0; i < r.message.length - 1; i++) {
						crateTableContentElement(r.message[i][0], r.message[i][1], r.message[i][2], r.message[i][3], r.message[i][4]);
					}
				}
			} else {
				closeNav();
			}
		}
	});
}

function showOrHideFilters(click_element) {
	if (click_element.id == 'show') {
		if (document.getElementById("filters").classList.contains('hidden')) {
			document.getElementById("filters").classList.toggle('hidden');
		}
	}
	if (click_element.id == 'hide') {
		if (!document.getElementById("filters").classList.contains('hidden')) {
			document.getElementById("filters").classList.toggle('hidden');
		}
	}
}

function showOrHideFilterAboEnd() {
	document.getElementById("start-group").classList.toggle('hidden');
	document.getElementById("end-group").classList.toggle('hidden');
}

function showOrHideFilterCustomerMod() {
	document.getElementById("customer-start-group").classList.toggle('hidden');
	document.getElementById("customer-end-group").classList.toggle('hidden');
}

/* Open */
function openNav() {
    document.getElementById("myNav").style.display = "block";
}

/* Close */
function closeNav() {
    document.getElementById("myNav").style.display = "none";
}

function checkIfFilterSelected() {
	var main_filter = document.getElementById("show").checked;
	var mod = document.getElementById("check-typ").value;
	var abo = document.getElementById("check-abo-end").checked;
	var customer = document.getElementById("check-customer-end").checked;
	if (main_filter) {
		if (!abo && !customer) {
			frappe.msgprint("Bitte mindestens ein Filter auswählen!", "Fehlende Filter Selektion");
		} else {
			startWithFilter(mod);
		}
	} else {
		startWithoutFilter(mod);
	}
}

function startWithoutFilter(mod) {
	frappe.confirm(
		'Wollen Sie die Prüfung ohne Filter ausführen?<br>Dies kann einige Augenblicke in Anspruch nehmen.',
		function(){
			openNav();
			goAhead(mod=mod);
		},
		function(){
			
		}
	)
}

function goAhead(mod='Deaktivierte Kunden', withFilter=false) {
	var start = "";
	var end = "";
	if (withFilter) {
		if (document.getElementById("check-customer-end").checked) {
			start = document.getElementById("customer-start").value;
			if (start) {
				start = start + " 00:00:00";
			}
			end = document.getElementById("customer-end").value;
			if (end) {
				end = end + " 23:59:59";
			}
		}
	}
	frappe.call({
		method: 'pflanzenfreund.pflanzenfreund.page.abo_plausibility.utils.start_background_jop',
		args: {
			'mod': mod,
			'start': start,
			'end': end
		},
		callback: function(r) {
			if (r.message) {
				// wenn code hierhin kommt, stimmt etwas nicht!
			} else {
				closeNav();
				deleteTable();
				frappe.msgprint('Die Plausibilitätsprüfung wurde erfolgreich dem Background-Worker übergeben.', 'Erfolg');
			}
		}
	});
}

function startWithFilter(mod) {
	openNav();
	goAhead(mod=mod, withFilter=true);
}

function deleteTable() {
	if (document.getElementById("myTable").classList.contains('hidden')) {
		document.getElementById("myTable").classList.toggle('hidden');
	}
	var tabelle = document.getElementById("myTable");
	var rowCount = tabelle.rows.length;
	for (var i = rowCount - 1; i > 0; i--) {
		tabelle.deleteRow(i);
	}
	resetToSelectAll();
}

function crateTableContentElement(zustand, bereinigung, action, customer, abo) {
	var tabelle = document.getElementById("myTable");
	
	var tr = document.createElement("tr");
	
	var td_check = document.createElement("td");
	var td_zustand = document.createElement("td");
	var td_bereinigung = document.createElement("td");
	var td_btn = document.createElement("td");
	var td_btn_btn_span = document.createElement("span");
	var input_checkbox = document.createElement("input");
	var td_btn_btn = document.createElement("button");
	
	var td_zustand_txt = document.createTextNode(zustand);
	var td_bereinigung_txt = document.createTextNode(bereinigung);
	var td_btn_btn_span_txt = document.createTextNode('Diese Position bereinigen');
	
	
	
	td_btn_btn.setAttribute("class", "btn btn-primary btn-sm primary-action");
	td_btn_btn.onclick = function() { 
		einzelZeileBereinigen(this);
	};
	
	input_checkbox.setAttribute("type", "checkbox");
	input_checkbox.setAttribute("class", "form-check-input");
	
	td_btn.setAttribute("data-todo", action);
	td_btn.setAttribute("data-refcustomer", customer);
	td_btn.setAttribute("data-refabo", abo);
	
	td_check.appendChild(input_checkbox);
	td_zustand.appendChild(td_zustand_txt);
	td_bereinigung.appendChild(td_bereinigung_txt);
	td_btn_btn_span.appendChild(td_btn_btn_span_txt);
	td_btn_btn.appendChild(td_btn_btn_span);
	td_btn.appendChild(td_btn_btn);
	
	tr.appendChild(td_check);
	tr.appendChild(td_zustand);
	tr.appendChild(td_bereinigung);
	tr.appendChild(td_btn);
	
	tabelle.appendChild(tr);
}

function selectAll(btn) {
	var tabelle = document.getElementById("myTable");
	var rowCount = tabelle.rows.length;
	if (btn.childNodes[0].innerHTML == "Alle auswählen") {
		for (var i = rowCount - 1; i > 0; i--) {
			tr = tabelle.getElementsByTagName("tr")[i],
			td = tr.getElementsByTagName("td")[0];
			td.childNodes[0].checked = true;
		}
		btn.childNodes[0].innerHTML = "Alle abwählen";
	} else if (btn.childNodes[0].innerHTML == "Alle abwählen") {
		for (var i = rowCount - 1; i > 0; i--) {
			tr = tabelle.getElementsByTagName("tr")[i],
			td = tr.getElementsByTagName("td")[0];
			td.childNodes[0].checked = false;
		}
		btn.childNodes[0].innerHTML = "Alle auswählen";
	}
}

function resetToSelectAll() {
	var tabelle = document.getElementById("myTable");
	tabelle.childNodes[1].childNodes[0].childNodes[1].childNodes[0].childNodes[0].innerHTML = "Alle auswählen";
}

function einzelZeileBereinigen(btn) {
	var action = btn.parentNode.dataset.todo;
	var customer = btn.parentNode.dataset.refcustomer;
	var abo = btn.parentNode.dataset.refabo;
	if (action == "storno") {
		einzel_storno(customer, abo);
	} else if (action == "geschenk_gratis") {
		einzel_geschenk_gratis(customer, abo);
	} else if (action == "anlage_kk") {
		einzel_anlage_kk(customer);
	} else if (action == "anlage_ok") {
		einzel_anlage_ok(customer);
	} else if (action == "none") {
		frappe.msgprint("Diese Aktion kann nicht automatisch ausgeführt werden.", "Bitte um manuelle Ausführung");
	} else {
		frappe.msgprint("Bitte wenden Sie sich an libracore.", "ERROR");
	}
}

function einzel_storno(customer, abo) {
	openNav();
	frappe.call({
		method: 'pflanzenfreund.pflanzenfreund.page.abo_plausibility.utils.storno_bereinigung',
		args: {
			'customer': customer,
			'abo': abo
		},
		callback: function(r) {
			if (r.message) {
				closeNav();
				console.log(r.message);
			} else {
				closeNav();
				frappe.msgprint("Bitte wenden Sie sich an libracore.", "ERROR");
			}
		}
	});
}

function einzel_geschenk_gratis(customer, abo) {
	openNav();
	frappe.call({
		method: 'pflanzenfreund.pflanzenfreund.page.abo_plausibility.utils.umwandlungen_bereinigung',
		args: {
			'customer': customer,
			'abo': abo
		},
		callback: function(r) {
			if (r.message) {
				closeNav();
				console.log(r.message);
			} else {
				closeNav();
				frappe.msgprint("Bitte wenden Sie sich an libracore.", "ERROR");
			}
		}
	});
}

function einzel_anlage_kk(customer) {
	openNav();
	frappe.call({
		method: 'pflanzenfreund.pflanzenfreund.page.abo_plausibility.utils.anlagen_kk_bereinigung',
		args: {
			'customer': customer
		},
		callback: function(r) {
			if (r.message) {
				closeNav();
				console.log(r.message);
			} else {
				closeNav();
				frappe.msgprint("Bitte wenden Sie sich an libracore.", "ERROR");
			}
		}
	});
}

function einzel_anlage_ok(customer) {
	openNav();
	frappe.call({
		method: 'pflanzenfreund.pflanzenfreund.page.abo_plausibility.utils.anlagen_ok_bereinigung',
		args: {
			'customer': customer
		},
		callback: function(r) {
			if (r.message) {
				closeNav();
				console.log(r.message);
			} else {
				closeNav();
				frappe.msgprint("Bitte wenden Sie sich an libracore.", "ERROR");
			}
		}
	});
}

function allSelectedBereinigen() {
	openNav();
	var tabelle = document.getElementById("myTable");
	var rowCount = tabelle.rows.length;
	var control_qty = 0;
	var stornos = [];
	var umwandlungen = [];
	var anlagen_kk = [];
	var anlagen_ok = [];
	for (var i = rowCount - 1; i > 0; i--) {
		tr = tabelle.getElementsByTagName("tr")[i],
		td = tr.getElementsByTagName("td")[0];
		if (td.childNodes[0].checked == true) {
			var ref_td = tr.getElementsByTagName("td")[3];
			var action = ref_td.dataset.todo;
			var customer = ref_td.dataset.refcustomer;
			var abo = ref_td.dataset.refabo;
			if (action == "storno") {
				stornos.push([customer, abo]);
			} else if (action == "geschenk_gratis") {
				umwandlungen.push([customer, abo]);
			} else if (action == "anlage_kk") {
				anlagen_kk.push(customer);
			} else if (action == "anlage_ok") {
				anlagen_ok.push(customer);
			}
			control_qty += 1;
		}
	}
	if (control_qty == 0) {
		closeNav();
		frappe.msgprint("Es wurde keine Zeile ausgewählt", "Keine Aktion getroffen");
	} else {
		frappe.call({
			method: 'pflanzenfreund.pflanzenfreund.page.abo_plausibility.utils.sammel_bereinigung',
			args: {
				'stornos': stornos,
				'umwandlungen': umwandlungen,
				'anlagen_kk': anlagen_kk,
				'anlagen_ok': anlagen_ok
			},
			callback: function(r) {
				if (r.message) {
					closeNav();
					console.log(r.message);
				} else {
					closeNav();
					frappe.msgprint("Bitte wenden Sie sich an libracore.", "ERROR");
				}
			}
		});
	}
}