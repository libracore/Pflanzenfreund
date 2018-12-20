// Copyright (c) 2018, libracore and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pflanzenfreund Abo', {
	refresh: function(frm) {
		if ((cur_frm.doc.abo_type == "Geschenk-Abo")&&(parseInt(cur_frm.doc.docstatus) == 0)) {
			var text = "<div><h2>Ihr Geschenk-Abonnement ‚Mein Pflanzenfreund’</h2><p>Im Auftrag von *!*Schenker*!* erhalten Sie ein Geschenk-Abonnement mit 10 Ausgaben unseres Gartenmagazins ‚Mein Pflanzenfreund’ –  bequem und rechtzeitig zur Saison.</p><br><p>‚Mein Pflanzenfreund’ ist ein zuverlässiger und praktischer Ratgeber für Leserinnen und Leser, die Garten, Terrasse und Balkon in vollen Zügen geniessen. Mit den wesentlichen Informationen zum umweltgerechten Gärtnern, mit Hintergrundberichten und vernünftigen Produktempfehlungen – seit über 100 Jahren.</p><br><p>Der «Pflanzenfreund» gibt nicht ausschliesslich Lehrmeinungen wieder. Er basiert auf handfesten Erfahrungen und dem engen Kontakt der Redaktion zur Leserschaft. Wir geben Ihnen Tipps zu exklusiven Neuzüchtungen, zu passenden Gartengeräten, Schnitt- und Pflegearbeiten, Ernte- und Überwinterungshilfen und wie Sie «Vielfrasse» nachhaltig von Ihrem Garten fernhalten können. Viele fachkundige Informationen stecken in den monatlichen Ausgaben, die Sie durchs ganze Jahr begleiten.</p><br><br><p>Wir wünschen Ihnen viel Vergnügen bei der Lektüre.</p></div>";
			cur_frm.set_value('donee_text', text);
		}
		frm.set_query('customer_address', function(doc) {
			return {
				query: 'frappe.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: 'Customer',
					link_name: doc.customer
				}
			};
		});
		frm.set_query('donee_address', function(doc) {
			return {
				query: 'frappe.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: 'Customer',
					link_name: doc.customer
				}
			};
		});
		frm.add_custom_button(__("Abo Verlängern"), function() {
			frappe.call({
			   method: "pflanzenfreund.utils.extend_abo",
			   args: {
					"abo": cur_frm.doc.name
			   },
			   callback: function(response) {
					if (response.message == "already renewed") {
						frappe.msgprint("Das Abonnement wurde bereits verlängert!", "Nicht verlängert");
					} else {
						frappe.confirm(
							'Das Abonnement wurde verlängert (neues Abo: ' + response.message +'<br>Wollen Sie zum neuen Abo wechseln?',
							function(){
								window.location.href="/desk#Form/Pflanzenfreund Abo/" + response.message;
							},
							function(){
								//nichts
							}
						)
					}
			   }
			});
		});
	},
	onload: function(frm) {
		if (frm.doc.__islocal){
			cur_frm.set_value('start_date', getStartDate());
			add_year(getStartDate());
			chooseAllEditions();
			setAllEditionsReadOnly();
			frappe["already_checked"] = false;
		}
		if ((cur_frm.doc.abo_type == "Geschenk-Abo")&&(parseInt(cur_frm.doc.docstatus) == 0)) {
			var text = "<div><h2>Ihr Geschenk-Abonnement ‚Mein Pflanzenfreund’</h2><p>Im Auftrag von *!*Schenker*!* erhalten Sie ein Geschenk-Abonnement mit 10 Ausgaben unseres Gartenmagazins ‚Mein Pflanzenfreund’ –  bequem und rechtzeitig zur Saison.</p><br><p>‚Mein Pflanzenfreund’ ist ein zuverlässiger und praktischer Ratgeber für Leserinnen und Leser, die Garten, Terrasse und Balkon in vollen Zügen geniessen. Mit den wesentlichen Informationen zum umweltgerechten Gärtnern, mit Hintergrundberichten und vernünftigen Produktempfehlungen – seit über 100 Jahren.</p><br><p>Der «Pflanzenfreund» gibt nicht ausschliesslich Lehrmeinungen wieder. Er basiert auf handfesten Erfahrungen und dem engen Kontakt der Redaktion zur Leserschaft. Wir geben Ihnen Tipps zu exklusiven Neuzüchtungen, zu passenden Gartengeräten, Schnitt- und Pflegearbeiten, Ernte- und Überwinterungshilfen und wie Sie «Vielfrasse» nachhaltig von Ihrem Garten fernhalten können. Viele fachkundige Informationen stecken in den monatlichen Ausgaben, die Sie durchs ganze Jahr begleiten.</p><br><br><p>Wir wünschen Ihnen viel Vergnügen bei der Lektüre.</p></div>";
			cur_frm.set_value('donee_text', text);
		}
	},
	abo_type: function(frm) {
		var enddate = new Date();
		var mm = getStartDate(onlyYear=false, onlyMonth=true);
		var refMM = getStartDate(onlyYear=false, onlyMonth=true);
		if ((mm == 12)||(mm == 1)||(mm == 7)||(mm == 8)) {
			mm = mm + 5;
		} else {
			mm = mm + 4; 
		}
		var yyyy = getStartDate(onlyYear=true, onlyMonth=false);
		
		if (mm > 12) {
			mm = mm - 12;
			yyyy = yyyy + 1;
		}
		
		if (mm < 10) {
			mm = '0' + mm;
		}

		enddate = yyyy + "-" + mm + "-01";
		
		if (cur_frm.doc.abo_type == "Probe-Abo") {
			cur_frm.set_value('start_date', getStartDate());
			cur_frm.set_value('end_date', enddate);
			deselectAllEditions();
			selectNextFour(parseInt(refMM));
			setAllEditionsReadOnly();
			
		} else if (cur_frm.doc.abo_type == "Kundenkarten-Abo (KK)") {
			cur_frm.set_value('start_date', getStartDate());
			cur_frm.set_value('end_date', '');
			//add_year(getStartDate());
			deselectAllEditions();
			//unsetAllEditionsReadOnly();
			selectNextThree(parseInt(refMM));
			setAllEditionsReadOnly();
		} else if (cur_frm.doc.abo_type == "Kunden-Abo (OK)") {
			cur_frm.set_value('start_date', getStartDate());
			cur_frm.set_value('end_date', '');
			//add_year(getStartDate());
			deselectAllEditions();
			selectNextTwo(parseInt(refMM));
			setAllEditionsReadOnly();
			//console.log(refMM);
		} else if (cur_frm.doc.abo_type == "Jahres-Abo") {
			cur_frm.set_value('start_date', getStartDate());
			add_year(getStartDate());
			chooseAllEditions();
			setAllEditionsReadOnly();
		} else if (cur_frm.doc.abo_type == "Geschenk-Abo") {
			//cur_frm.set_value('end_date', '');
			cur_frm.set_value('start_date', getStartDate());
			add_year(getStartDate());
			chooseAllEditions();
			setAllEditionsReadOnly();
			var start = cur_frm.doc.start_date;
			var month = start.split("-")[1];
			var day = start.split("-")[2];
			var end = (parseInt((new Date()).getFullYear()) + 1) + "-" + month + "-" + day;
			var text = "<div><h2>Ihr Geschenk-Abonnement ‚Mein Pflanzenfreund’</h2><p>Im Auftrag von *!*Schenker*!* erhalten Sie ein Geschenk-Abonnement mit 10 Ausgaben unseres Gartenmagazins ‚Mein Pflanzenfreund’ –  bequem und rechtzeitig zur Saison.</p><br><p>‚Mein Pflanzenfreund’ ist ein zuverlässiger und praktischer Ratgeber für Leserinnen und Leser, die Garten, Terrasse und Balkon in vollen Zügen geniessen. Mit den wesentlichen Informationen zum umweltgerechten Gärtnern, mit Hintergrundberichten und vernünftigen Produktempfehlungen – seit über 100 Jahren.</p><br><p>Der «Pflanzenfreund» gibt nicht ausschliesslich Lehrmeinungen wieder. Er basiert auf handfesten Erfahrungen und dem engen Kontakt der Redaktion zur Leserschaft. Wir geben Ihnen Tipps zu exklusiven Neuzüchtungen, zu passenden Gartengeräten, Schnitt- und Pflegearbeiten, Ernte- und Überwinterungshilfen und wie Sie «Vielfrasse» nachhaltig von Ihrem Garten fernhalten können. Viele fachkundige Informationen stecken in den monatlichen Ausgaben, die Sie durchs ganze Jahr begleiten.</p><br><br><p>Wir wünschen Ihnen viel Vergnügen bei der Lektüre.</p></div>";
			cur_frm.set_value('donee_text', text);
		} else {
			cur_frm.set_value('end_date', '');
			cur_frm.set_value('start_date', getStartDate());
			//add_year(getStartDate());
			chooseAllEditions();
			setAllEditionsReadOnly();
		}
	},
	validate: function(frm) {
		var count = 0;
		count = count + cur_frm.doc.winter_ed + cur_frm.doc.feb_ed + cur_frm.doc.mar_ed + cur_frm.doc.apr_ed + cur_frm.doc.may_ed + cur_frm.doc.jun_ed + cur_frm.doc.summer_ed + cur_frm.doc.sept_ed + cur_frm.doc.oct_ed + cur_frm.doc.nov_ed;
		
		if (cur_frm.doc.abo_type == "Kundenkarten-Abo (KK)") {
			if ((count != 3)) {
				frappe.msgprint("Please choose <b>3 editions</b> for Kundenkarten-Abo (KK)", "Kundenkarten-Abo (KK) Info");
				frappe.validated=false;
				console.log("Abo: Kundenkarten-Abo (KK) / count: "+count);
			} else {
				frappe.validated=true;
			}
		} else if (cur_frm.doc.abo_type == "Probe-Abo") {
			if ((count != 4)) {
				frappe.validated=false;
				console.log("Abo: Probe-Abo / count: "+count);
			} else {
				frappe.validated=true;
			}
		} else if (cur_frm.doc.abo_type == "Kunden-Abo (OK)") {
			if ((count != 2)) {
				frappe.validated=false;
				console.log("Abo: Kunden-Abo (OK) / count: "+count);
			} else {
				frappe.validated=true;
			}
		} else {
			if (!frappe["already_checked"]){
				if ((count != 10)) {
					frappe.validated=false;
					frappe.confirm(
						"You don't choose <b>all editions</b>!<br>Are you sure this is correct?",
						function(){
							//frappe.validated=true;
							frappe["already_checked"] = true;
							cur_frm.savesubmit();
						},
						function(){
							frappe.validated=false;
						}
					)
				} else {
					frappe.validated=true;
				}
			}
		}
		
	},
	set_ed_manual: function(frm) {
		if (cur_frm.doc.set_ed_manual == "1") {
			unsetAllEditionsReadOnly();
		} else {
			setAllEditionsReadOnly();
		}
	}
});

function getStartDate(onlyYear=false, onlyMonth=false) {
	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth() + 1;
	var yyyy = today.getFullYear();
	
	if (onlyYear) { return yyyy; }

	if(dd < 15) {
		mm = mm;
	} else {
		mm = mm + 1;
		dd = '01';
	}
	

	if(mm > 12) {
		mm = mm - 12;
		yyyy = yyyy + 1;
	}
	
	if (onlyMonth) { return mm; }
	
	if(mm < 10) {
		mm = '0'+mm
	} 

	startdate = yyyy + "-" + mm + "-" + dd;
	
	return startdate;
}

function chooseAllEditions() {
	cur_frm.set_value('winter_ed', 1);
	cur_frm.set_value('jan_ed', 0);
	cur_frm.set_value('feb_ed', 1);
	cur_frm.set_value('mar_ed', 1);
	cur_frm.set_value('apr_ed', 1);
	cur_frm.set_value('may_ed', 1);
	cur_frm.set_value('jun_ed', 1);
	cur_frm.set_value('summer_ed', 1);
	cur_frm.set_value('jul_ed', 0);
	cur_frm.set_value('aug_ed', 0);
	cur_frm.set_value('sept_ed', 1);
	cur_frm.set_value('oct_ed', 1);
	cur_frm.set_value('nov_ed', 1);
	cur_frm.set_value('dec_ed', 0);
}

function deselectAllEditions() {
	cur_frm.set_value('winter_ed', 0);
	cur_frm.set_value('jan_ed', 0);
	cur_frm.set_value('feb_ed', 0);
	cur_frm.set_value('mar_ed', 0);
	cur_frm.set_value('apr_ed', 0);
	cur_frm.set_value('may_ed', 0);
	cur_frm.set_value('jun_ed', 0);
	cur_frm.set_value('jul_ed', 0);
	cur_frm.set_value('aug_ed', 0);
	cur_frm.set_value('summer_ed', 0);
	cur_frm.set_value('sept_ed', 0);
	cur_frm.set_value('oct_ed', 0);
	cur_frm.set_value('nov_ed', 0);
	cur_frm.set_value('dec_ed', 0);
}

function setAllEditionsReadOnly() {
	cur_frm.set_df_property('winter_ed','read_only','1');
	cur_frm.set_df_property('jan_ed','read_only','1');
	cur_frm.set_df_property('feb_ed','read_only','1');
	cur_frm.set_df_property('mar_ed','read_only','1');
	cur_frm.set_df_property('apr_ed','read_only','1');
	cur_frm.set_df_property('may_ed','read_only','1');
	cur_frm.set_df_property('jun_ed','read_only','1');
	cur_frm.set_df_property('jul_ed','read_only','1');
	cur_frm.set_df_property('aug_ed','read_only','1');
	cur_frm.set_df_property('summer_ed','read_only','1');
	cur_frm.set_df_property('sept_ed','read_only','1');
	cur_frm.set_df_property('oct_ed','read_only','1');
	cur_frm.set_df_property('nov_ed','read_only','1');
	cur_frm.set_df_property('dec_ed','read_only','1');
}

function unsetAllEditionsReadOnly() {
	cur_frm.set_df_property('winter_ed','read_only','0');
	cur_frm.set_df_property('jan_ed','read_only','0');
	cur_frm.set_df_property('feb_ed','read_only','0');
	cur_frm.set_df_property('mar_ed','read_only','0');
	cur_frm.set_df_property('apr_ed','read_only','0');
	cur_frm.set_df_property('may_ed','read_only','0');
	cur_frm.set_df_property('jun_ed','read_only','0');
	cur_frm.set_df_property('jul_ed','read_only','0');
	cur_frm.set_df_property('aug_ed','read_only','0');
	cur_frm.set_df_property('summer_ed','read_only','0');
	cur_frm.set_df_property('sept_ed','read_only','0');
	cur_frm.set_df_property('oct_ed','read_only','0');
	cur_frm.set_df_property('nov_ed','read_only','0');
	cur_frm.set_df_property('dec_ed','read_only','0');
}

function selectNextFour(startMonth) {
	//console.log(startMonth);
	if (startMonth == 12) {
		//cur_frm.set_value('jan_ed', 1);
		cur_frm.set_value('feb_ed', 1);
		cur_frm.set_value('mar_ed', 1);
		cur_frm.set_value('apr_ed', 1);
		cur_frm.set_value('may_ed', 1);
	} else if (startMonth == 1) {
		cur_frm.set_value('feb_ed', 1);
		cur_frm.set_value('mar_ed', 1);
		cur_frm.set_value('apr_ed', 1);
		cur_frm.set_value('may_ed', 1);
	} else if (startMonth == 2) {
		cur_frm.set_value('mar_ed', 1);
		cur_frm.set_value('apr_ed', 1);
		cur_frm.set_value('may_ed', 1);
		cur_frm.set_value('jun_ed', 1);
	} else if (startMonth == 3) {
		cur_frm.set_value('apr_ed', 1);
		cur_frm.set_value('may_ed', 1);
		cur_frm.set_value('jun_ed', 1);
		//cur_frm.set_value('jul_ed', 1);
		cur_frm.set_value('summer_ed', 1);
	} else if (startMonth == 4) {
		cur_frm.set_value('may_ed', 1);
		cur_frm.set_value('jun_ed', 1);
		//cur_frm.set_value('jul_ed', 1);
		//cur_frm.set_value('aug_ed', 1);
		cur_frm.set_value('summer_ed', 1);
		cur_frm.set_value('sept_ed', 1);
	} else if (startMonth == 5) {
		cur_frm.set_value('jun_ed', 1);
		//cur_frm.set_value('jul_ed', 1);
		//cur_frm.set_value('aug_ed', 1);
		cur_frm.set_value('summer_ed', 1);
		cur_frm.set_value('sept_ed', 1);
		cur_frm.set_value('oct_ed', 1);
	} else if (startMonth == 6) {
		//cur_frm.set_value('jul_ed', 1);
		//cur_frm.set_value('aug_ed', 1);
		cur_frm.set_value('summer_ed', 1);
		cur_frm.set_value('sept_ed', 1);
		cur_frm.set_value('oct_ed', 1);
		cur_frm.set_value('nov_ed', 1);
	} else if (startMonth == 7) {
		//cur_frm.set_value('aug_ed', 1);
		cur_frm.set_value('sept_ed', 1);
		cur_frm.set_value('oct_ed', 1);
		cur_frm.set_value('nov_ed', 1);
		cur_frm.set_value('winter_ed', 1);
	} else if (startMonth == 8) {
		cur_frm.set_value('sept_ed', 1);
		cur_frm.set_value('oct_ed', 1);
		cur_frm.set_value('nov_ed', 1);
		cur_frm.set_value('winter_ed', 1);
	} else if (startMonth == 9) {
		cur_frm.set_value('oct_ed', 1);
		cur_frm.set_value('nov_ed', 1);
		//cur_frm.set_value('dec_ed', 1);
		//cur_frm.set_value('jan_ed', 1);
		cur_frm.set_value('winter_ed', 1);
		cur_frm.set_value('feb_ed', 1);
	} else if (startMonth == 10) {
		cur_frm.set_value('nov_ed', 1);
		//cur_frm.set_value('dec_ed', 1);
		//cur_frm.set_value('jan_ed', 1);
		cur_frm.set_value('winter_ed', 1);
		cur_frm.set_value('feb_ed', 1);
		cur_frm.set_value('mar_ed', 1);
	} else if (startMonth == 11) {
		//cur_frm.set_value('dec_ed', 1);
		//cur_frm.set_value('jan_ed', 1);
		cur_frm.set_value('winter_ed', 1);
		cur_frm.set_value('feb_ed', 1);
		cur_frm.set_value('mar_ed', 1);
		cur_frm.set_value('apr_ed', 1);
	}
}

function selectNextTwo(startMonth) {
	if (startMonth == 12) {
		//cur_frm.set_value('jan_ed', 1);
		cur_frm.set_value('mar_ed', 1);
		cur_frm.set_value('sept_ed', 1);
	} else if (startMonth == 1) {
		cur_frm.set_value('feb_ed', 1);
		cur_frm.set_value('summer_ed', 1);
	} else if (startMonth == 2) {
		cur_frm.set_value('mar_ed', 1);
		cur_frm.set_value('sept_ed', 1);
	} else if (startMonth == 3) {
		cur_frm.set_value('apr_ed', 1);
		cur_frm.set_value('oct_ed', 1);
	} else if (startMonth == 4) {
		cur_frm.set_value('May_ed', 1);
		cur_frm.set_value('nov_ed', 1);
	} else if (startMonth == 5) {
		cur_frm.set_value('jun_ed', 1);
		//cur_frm.set_value('jul_ed', 1);
		cur_frm.set_value('winter_ed', 1);
	} else if (startMonth == 6) {
		//cur_frm.set_value('jul_ed', 1);
		//cur_frm.set_value('aug_ed', 1);
		cur_frm.set_value('summer_ed', 1);
		cur_frm.set_value('feb_ed', 1);
	} else if (startMonth == 7) {
		//cur_frm.set_value('aug_ed', 1);
		cur_frm.set_value('sept_ed', 1);
		cur_frm.set_value('mar_ed', 1);
	} else if (startMonth == 8) {
		cur_frm.set_value('apr_ed', 1);
		cur_frm.set_value('oct_ed', 1);
	} else if (startMonth == 9) {
		cur_frm.set_value('may_ed', 1);
		cur_frm.set_value('nov_ed', 1);
	} else if (startMonth == 10) {
		cur_frm.set_value('jun_ed', 1);
		//cur_frm.set_value('dec_ed', 1);
		cur_frm.set_value('winter_ed', 1);
	} else if (startMonth == 11) {
		//cur_frm.set_value('dec_ed', 1);
		//cur_frm.set_value('jan_ed', 1);
		cur_frm.set_value('summer_ed', 1);
		cur_frm.set_value('feb_ed', 1);
	}
}

function selectNextThree(startMonth) {
	if (startMonth == 12) {
		cur_frm.set_value('feb_ed', 1);
		cur_frm.set_value('may_ed', 1);
		cur_frm.set_value('oct_ed', 1);
	} else if (startMonth == 1) {
		cur_frm.set_value('feb_ed', 1);
		cur_frm.set_value('may_ed', 1);
		cur_frm.set_value('sept_ed', 1);
	} else if (startMonth == 2) {
		cur_frm.set_value('mar_ed', 1);
		cur_frm.set_value('jun_ed', 1);
		cur_frm.set_value('oct_ed', 1);
	} else if (startMonth == 3) {
		cur_frm.set_value('apr_ed', 1);
		cur_frm.set_value('nov_ed', 1);
		cur_frm.set_value('summer_ed', 1);
	} else if (startMonth == 4) {
		cur_frm.set_value('May_ed', 1);
		cur_frm.set_value('sept_ed', 1);
		cur_frm.set_value('winter_ed', 1);
	} else if (startMonth == 5) {
		cur_frm.set_value('jun_ed', 1);
		cur_frm.set_value('feb_ed', 1);
		cur_frm.set_value('oct_ed', 1);
	} else if (startMonth == 6) {
		//cur_frm.set_value('jul_ed', 1);
		cur_frm.set_value('mar_ed', 1);
		cur_frm.set_value('summer_ed', 1);
		cur_frm.set_value('nov_ed', 1);
	} else if (startMonth == 7) {
		cur_frm.set_value('apr_d', 1);
		cur_frm.set_value('sept_ed', 1);
		cur_frm.set_value('winter_ed', 1);
	} else if (startMonth == 8) {
		cur_frm.set_value('mar_ed', 1);
		cur_frm.set_value('sept_ed', 1);
		cur_frm.set_value('nov_ed', 1);
	} else if (startMonth == 9) {
		cur_frm.set_value('may_ed', 1);
		cur_frm.set_value('feb_ed', 1);
		cur_frm.set_value('oct_ed', 1);
	} else if (startMonth == 10) {
		cur_frm.set_value('jun_ed', 1);
		cur_frm.set_value('mar_ed', 1);
		cur_frm.set_value('nov_ed', 1);
	} else if (startMonth == 11) {
		//cur_frm.set_value('dec_ed', 1);
		cur_frm.set_value('winter_ed', 1);
		cur_frm.set_value('summer_ed', 1);
		cur_frm.set_value('apr_ed', 1);
	}
}

function add_year(date) {
	frappe.call({
	   method: "pflanzenfreund.utils.add_year",
	   args: {
			"date": date
	   },
	   callback: function(response) {
			cur_frm.set_value('end_date', response.message);
	   }
	});
}
