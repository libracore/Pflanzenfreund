frappe.pages['geschenkbriefe'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Erstellung Geschenkbriefe',
		single_column: true
	});
	
	frappe.geschenkbriefe.make(page);
	frappe.geschenkbriefe.run(page);
	page.job_content = $(page.body).find('#placeForWorkers');
	// add the application reference
	frappe.breadcrumbs.add("Pflanzenfreund");
}

frappe.geschenkbriefe = {
	start: 0,
	make: function(page) {
		var me = frappe.geschenkbriefe;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		var data = "";
		$(frappe.render_template('geschenkbriefe', data)).appendTo(me.body);
	},
	run: function(page) {
 
	}
}

frappe.pages['geschenkbriefe'].on_page_show = function(wrapper) {
	frappe.pages.geschenkbriefe.refresh_jobs();
}

frappe.pages.geschenkbriefe.refresh_jobs = function() {
	var page = frappe.pages.geschenkbriefe.page;

	// don't call if already waiting for a response
	if(page.called) return;
	page.called = true;
	frappe.call({
		method: 'pflanzenfreund.utils.list_all_pdfs',
		callback: function(r) {
			page.called = false;
			page.body.find('.list-jobs').remove();
			$(frappe.render_template('background_jobs', {onlyfiles:r.message || []})).appendTo(page.job_content);

			if(frappe.get_route()[0]==='geschenkbriefe') {
				frappe.background_jobs_timeout = setTimeout(frappe.pages.geschenkbriefe.refresh_jobs, 2000);
			}
		}
	});
}

function createBindPDF() {
	var bez_von = document.getElementById("start").value;
	var bez_bis = document.getElementById("end").value;
	if (!bez_von) {
		bez_von = frappe.datetime.get_today();
	}
	if (!bez_bis) {
		bez_bis = frappe.datetime.get_today();
	}
	var printformat = "Geschenk Brief";
	frappe.confirm(
		"Wollen Sie ein Sammel-PDF aller gültigen Geschenk-Abos die zwischen " + bez_von + " und " +bez_bis + " bezahlt worden sind erstellen?",
		function(){
			frappe.msgprint("Der Job wurde dem Background-Worker übergeben.<br>Sie erhalten eine Information sobald der Job erfolgreich abgeschlossen ist.<br>Alternativ können Sie den Fortschritt auch <a href='/desk#background_jobs'>hier</a> einsehen.");
			//console.log("Von " + bez_von + " bis " + bez_bis + " mit dem template " + printformat);
			startCreateBindPDF(bez_von, bez_bis, printformat);
			//startCreateBindPDF('2019-01-10', '2019-01-10', printformat);
		},
		function(){
			return false;
		}
	)
}

function startCreateBindPDF(bez_von, bez_bis, printformat) {
	frappe.call({
		method: 'pflanzenfreund.utils.createGeschenkSammelPDF',
		args: {
			'bez_von': bez_von,
			'bez_bis': bez_bis,
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