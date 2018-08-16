// Copyright (c) 2018, libracore and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pflanzenfreund Abo', {
	refresh: function(frm) {

	},
	onload: function(frm) {
		cur_frm.set_value('start_date', getStartDate());
		chooseAllEditions();
	},
	abo_type: function(frm) {
		if (cur_frm.doc.abo_type == "Probe-Abo") {
			var enddate = new Date();
			var mm = getStartDate(onlyYear=false, onlyMonth=true)
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
			cur_frm.set_value('end_date', enddate);
			
			deselectAllEditions();
			
		} else {
			cur_frm.set_value('end_date', '');
			chooseAllEditions();
		}
	},
	validate: function(frm) {
		var count = 0;
		count = count + cur_frm.doc.winter_ed + cur_frm.doc.feb_ed + cur_frm.doc.mar_ed + cur_frm.doc.apr_ed + cur_frm.doc.may_ed + cur_frm.doc.jun_ed + cur_frm.doc.summer_ed + cur_frm.doc.sept_ed + cur_frm.doc.oct_ed + cur_frm.doc.nov_ed;
		
		if (cur_frm.doc.abo_type == "Probe-Abo") {
			if ((count != 3)) {
				frappe.msgprint("Please choose <b>3 editions</b> for Probe-Abo", "Probe-Abo Info");
				frappe.validated=false;
			} else {
				frappe.validated=true;
			}
		} else {
			if ((count != 10)) {
				frappe.msgprint("Please choose <b>all editions</b>", "Abo Info");
				frappe.validated=false;
			} else {
				frappe.validated=true;
			}
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
		mm = mm + 1;
	} else {
		mm = mm + 2;
	}
	dd = '01';

	if(mm > 12) {
		mm = mm - 12;
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
	cur_frm.set_value('feb_ed', 1);
	cur_frm.set_value('mar_ed', 1);
	cur_frm.set_value('apr_ed', 1);
	cur_frm.set_value('may_ed', 1);
	cur_frm.set_value('jun_ed', 1);
	cur_frm.set_value('summer_ed', 1);
	cur_frm.set_value('sept_ed', 1);
	cur_frm.set_value('oct_ed', 1);
	cur_frm.set_value('nov_ed', 1);
}

function deselectAllEditions() {
	cur_frm.set_value('winter_ed', 0);
	cur_frm.set_value('feb_ed', 0);
	cur_frm.set_value('mar_ed', 0);
	cur_frm.set_value('apr_ed', 0);
	cur_frm.set_value('may_ed', 0);
	cur_frm.set_value('jun_ed', 0);
	cur_frm.set_value('summer_ed', 0);
	cur_frm.set_value('sept_ed', 0);
	cur_frm.set_value('oct_ed', 0);
	cur_frm.set_value('nov_ed', 0);
}