// Copyright (c) 2018, libracore and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pflanzenfreund Abo', {
	refresh: function(frm) {
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
	},
	onload: function(frm) {
		cur_frm.set_value('start_date', getStartDate());
		chooseAllEditions();
		setAllEditionsReadOnly();
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
			cur_frm.set_value('end_date', enddate);
			deselectAllEditions();
			selectNextFour(parseInt(refMM));
			setAllEditionsReadOnly();
			
		} else if (cur_frm.doc.abo_type == "Kundenkarten-Abo (KK)") {
			cur_frm.set_value('end_date', '');
			deselectAllEditions();
			unsetAllEditionsReadOnly();
		} else if (cur_frm.doc.abo_type == "Kunden-Abo (OK)") {
			cur_frm.set_value('end_date', '');
			deselectAllEditions();
			selectNextTwo(parseInt(refMM));
			setAllEditionsReadOnly();
		} else {
			cur_frm.set_value('end_date', '');
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
			if ((count != 10)) {
				frappe.msgprint("Please choose <b>all editions</b>", "Abo Info");
				frappe.validated=false;
				console.log("Abo: rest / count: "+count);
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

function setAllEditionsReadOnly() {
	cur_frm.set_df_property('winter_ed','read_only','1');
	cur_frm.set_df_property('feb_ed','read_only','1');
	cur_frm.set_df_property('mar_ed','read_only','1');
	cur_frm.set_df_property('apr_ed','read_only','1');
	cur_frm.set_df_property('may_ed','read_only','1');
	cur_frm.set_df_property('jun_ed','read_only','1');
	cur_frm.set_df_property('summer_ed','read_only','1');
	cur_frm.set_df_property('sept_ed','read_only','1');
	cur_frm.set_df_property('oct_ed','read_only','1');
	cur_frm.set_df_property('nov_ed','read_only','1');
}

function unsetAllEditionsReadOnly() {
	cur_frm.set_df_property('winter_ed','read_only','0');
	cur_frm.set_df_property('feb_ed','read_only','0');
	cur_frm.set_df_property('mar_ed','read_only','0');
	cur_frm.set_df_property('apr_ed','read_only','0');
	cur_frm.set_df_property('may_ed','read_only','0');
	cur_frm.set_df_property('jun_ed','read_only','0');
	cur_frm.set_df_property('summer_ed','read_only','0');
	cur_frm.set_df_property('sept_ed','read_only','0');
	cur_frm.set_df_property('oct_ed','read_only','0');
	cur_frm.set_df_property('nov_ed','read_only','0');
}

function selectNextFour(startMonth) {
	if ((startMonth == 12)||(startMonth == 1)) {
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
		cur_frm.set_value('summer_ed', 1);
	} else if (startMonth == 4) {
		cur_frm.set_value('May_ed', 1);
		cur_frm.set_value('jun_ed', 1);
		cur_frm.set_value('summer_ed', 1);
		cur_frm.set_value('sept_ed', 1);
	} else if (startMonth == 5) {
		cur_frm.set_value('jun_ed', 1);
		cur_frm.set_value('summer_ed', 1);
		cur_frm.set_value('sept_ed', 1);
		cur_frm.set_value('oct_ed', 1);
	} else if (startMonth == 6) {
		cur_frm.set_value('summer_ed', 1);
		cur_frm.set_value('sept_ed', 1);
		cur_frm.set_value('oct_ed', 1);
		cur_frm.set_value('nov_ed', 1);
	} else if ((startMonth == 7)||(startMonth == 8)) {
		cur_frm.set_value('sept_ed', 1);
		cur_frm.set_value('oct_ed', 1);
		cur_frm.set_value('nov_ed', 1);
		cur_frm.set_value('winter_ed', 1);
	} else if (startMonth == 9) {
		cur_frm.set_value('oct_ed', 1);
		cur_frm.set_value('nov_ed', 1);
		cur_frm.set_value('winter_ed', 1);
		cur_frm.set_value('feb_ed', 1);
	} else if (startMonth == 10) {
		cur_frm.set_value('nov_ed', 1);
		cur_frm.set_value('winter_ed', 1);
		cur_frm.set_value('feb_ed', 1);
		cur_frm.set_value('mar_ed', 1);
	} else if (startMonth == 11) {
		cur_frm.set_value('winter_ed', 1);
		cur_frm.set_value('feb_ed', 1);
		cur_frm.set_value('mar_ed', 1);
		cur_frm.set_value('apr_ed', 1);
	}
}

function selectNextTwo(startMonth) {
	if ((startMonth == 12)||(startMonth == 1)) {
		cur_frm.set_value('feb_ed', 1);
		cur_frm.set_value('mar_ed', 1);
	} else if (startMonth == 2) {
		cur_frm.set_value('mar_ed', 1);
		cur_frm.set_value('apr_ed', 1);
	} else if (startMonth == 3) {
		cur_frm.set_value('apr_ed', 1);
		cur_frm.set_value('may_ed', 1);
	} else if (startMonth == 4) {
		cur_frm.set_value('May_ed', 1);
		cur_frm.set_value('jun_ed', 1);
	} else if (startMonth == 5) {
		cur_frm.set_value('jun_ed', 1);
		cur_frm.set_value('summer_ed', 1);
	} else if (startMonth == 6) {
		cur_frm.set_value('summer_ed', 1);
		cur_frm.set_value('sept_ed', 1);
	} else if ((startMonth == 7)||(startMonth == 8)) {
		cur_frm.set_value('sept_ed', 1);
		cur_frm.set_value('oct_ed', 1);
	} else if (startMonth == 9) {
		cur_frm.set_value('oct_ed', 1);
		cur_frm.set_value('nov_ed', 1);
	} else if (startMonth == 10) {
		cur_frm.set_value('nov_ed', 1);
		cur_frm.set_value('winter_ed', 1);
	} else if (startMonth == 11) {
		cur_frm.set_value('winter_ed', 1);
		cur_frm.set_value('feb_ed', 1);
	}
}