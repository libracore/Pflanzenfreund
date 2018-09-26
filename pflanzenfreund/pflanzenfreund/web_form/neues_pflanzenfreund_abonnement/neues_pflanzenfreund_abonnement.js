frappe.ready(function() {
	var abo_type = $('select[data-fieldname = "abo_type"]')[0];
	var customer = $('input[name = "customer"]')[0];
	var customer_name = $('input[data-fieldname = "customer_name"]')[0];
	var customer_address = $('input[data-fieldname = "customer_address"]')[0];
	//$('input[data-fieldname = "customer_address"]').change(function() {set_customer_address_display();});
	
	
	if (frappe.doc_name) {
		frappe.msgprint("Vielen Dank für Ihr Vertrauen.<br>Die Anfrage für das Abonnement " + frappe.doc_name + " wurde erfolgreich erstellt.", "Vielen Dank");
		set_visability_of_donee(abo_type);
		set_customer_address_display($('input[data-fieldname = "customer_address"]')[0].value);
		$('input[data-label = "Start"]')[0].parentNode.classList.add("hidden");
		$('input[data-label = "Ende"]')[0].parentNode.classList.add("hidden");
		$('div[data-label = "info_html"]')[0].classList.add("hidden");
		customer_address.setAttribute("disabled", "");
		abo_type.setAttribute("disabled", "");
		$('input[data-fieldname = "donee_first_and_lastname"]')[0].setAttribute("disabled", "");
		$('input[data-fieldname = "donee_street"]')[0].setAttribute("disabled", "");
		$('input[data-fieldname = "donee_pincode"]')[0].setAttribute("disabled", "");
		$('input[data-fieldname = "donee_city"]')[0].setAttribute("disabled", "");
		$('input[data-fieldname = "donee_first_and_lastname"]')[0].removeAttribute("data-reqd");
		$('input[data-fieldname = "donee_street"]')[0].removeAttribute("data-reqd");
		$('input[data-fieldname = "donee_pincode"]')[0].removeAttribute("data-reqd");
		$('input[data-fieldname = "donee_city"]')[0].removeAttribute("data-reqd");
		if ($('input[data-fieldname = "donee_first_and_lastname"]')[0].parentNode.classList.contains("has-error")) {
			$('input[data-fieldname = "donee_first_and_lastname"]')[0].parentNode.classList.toggle('has-error');
		}
		if ($('input[data-fieldname = "donee_street"]')[0].parentNode.classList.contains("has-error")) {
			$('input[data-fieldname = "donee_street"]')[0].parentNode.classList.toggle('has-error');
		}
		if ($('input[data-fieldname = "donee_pincode"]')[0].parentNode.classList.contains("has-error")) {
			$('input[data-fieldname = "donee_pincode"]')[0].parentNode.classList.toggle('has-error');
		}
		if ($('input[data-fieldname = "donee_city"]')[0].parentNode.classList.contains("has-error")) {
			$('input[data-fieldname = "donee_city"]')[0].parentNode.classList.toggle('has-error');
		}
		$('select[data-label = "Adresse"]')[0].parentNode.classList.add("hidden");
	} else {
		$('input[data-fieldname = "start_date"]')[0].parentNode.classList.add("hidden");
		$('input[data-fieldname = "end_date"]')[0].parentNode.classList.add("hidden");
		$('input[data-fieldname = "customer_address"]')[0].parentNode.classList.add("hidden");
		
		
		$('select[data-fieldname = "abo_type"]').change(function() {set_initial_start_and_end_date(abo_type.value);set_visability_of_donee(abo_type);});
		$('input[data-label = "Start"]').change(function() {change_start(abo_type.value);});
		$('select[data-label = "Adresse"]').change(function() {copy_address_selection();set_customer_address_display("");});
		set_initial_start_and_end_date(abo_type.value);
		set_visability_of_donee(abo_type);
		
		frappe.call({
			method: "pflanzenfreund.utils.get_party",
			args: {},
			callback: function(response) {
				var customer_return = response.message;
				if (customer_return) {
					customer.value = customer_return.name;
					customer_name.value = customer_return.customer_name;
					set_adress_dropdown(customer_return.name);
				} else {
					frappe.msgprint("customer not found");
				}
			}
		});
		set_editions_based_on_abo_type_and_start_date();
	}
})

function set_customer_address_display(selected_address) {
	if (selected_address == "") {
		selected_address = $('select[data-label = "Adresse"]')[0].value;
	}
	if (selected_address) {
		frappe.call({
			method: "pflanzenfreund.pflanzenfreund.web_form.neues_pflanzenfreund_abonnement.neues_pflanzenfreund_abonnement.get_address_display",
			args: {
				"address_name": selected_address
			},
			callback: function(response) {
				if (response.message) {
					$('div[data-label = "Address Display"]')[0].innerHTML = response.message; //.appendChild(address_text);
				}
			}
		});
	}
}

function set_initial_start_and_end_date(abo_type) {
	var user_start = $('input[data-label = "Start"]')[0];
	var user_end = $('input[data-label = "Ende"]')[0];
	var start_date = $('input[data-fieldname = "start_date"]')[0];
	var end_date = $('input[data-fieldname = "end_date"]')[0];
	
	var raw_today = new Date();
	start_date.value = formatDate_as_dd_mm_yyyy(raw_today);
	user_start.value = formatDate_as_dd_mm_yyyy(raw_today);
	if (abo_type != 'Probe-Abo') {
		end_date.value = formatDate_as_yyyy_mm_dd(add_one_year_to_date(raw_today));
		user_end.value = formatDate_as_dd_mm_yyyy(add_one_year_to_date(raw_today));
	} else {
		end_date.value = formatDate_as_yyyy_mm_dd(add_four_months_to_date(raw_today));
		user_end.value = formatDate_as_dd_mm_yyyy(add_four_months_to_date(raw_today));
	}
	if (user_start.parentNode.classList.contains("has-error")) {
		user_start.parentNode.classList.toggle('has-error');
	}
	set_editions_based_on_abo_type_and_start_date();
}

function change_start(abo_type) {
	var _user_start = $('input[data-label = "Start"]')[0].value.split("-");
	var user_start = new Date(_user_start[2], _user_start[1] - 1, _user_start[0]);
	
	$('input[data-fieldname = "start_date"]')[0].value = formatDate_as_dd_mm_yyyy(user_start);
	if (abo_type != 'Probe-Abo') {
		$('input[data-fieldname = "end_date"]')[0].value = formatDate_as_yyyy_mm_dd(add_one_year_to_date(user_start));
		$('input[data-label = "Ende"]')[0].value = formatDate_as_dd_mm_yyyy(add_one_year_to_date(user_start));
	} else {
		$('input[data-fieldname = "end_date"]')[0].value = formatDate_as_yyyy_mm_dd(add_four_months_to_date(user_start));
		$('input[data-label = "Ende"]')[0].value = formatDate_as_dd_mm_yyyy(add_four_months_to_date(user_start));
	}
	set_editions_based_on_abo_type_and_start_date();
}

function formatDate_as_yyyy_mm_dd(value) {
   var month = value.getMonth() + 1;
   if (month < 10) {
	   month = "0" + month;
   }
   return value.getFullYear() + "-" + month + "-" + value.getDate();
}

function formatDate_as_dd_mm_yyyy(value) {
   var month = value.getMonth() + 1;
   if (month < 10) {
	   month = "0" + month;
   }
   return value.getDate() + "-" + month + "-" + value.getFullYear();
}

function add_one_year_to_date(d) {
	var year = d.getFullYear();
	var month = d.getMonth();
	var day = d.getDate();
	return new Date(year + 1, month, day)
}

function add_four_months_to_date(d) {
	var year = d.getFullYear();
	var month = d.getMonth();
	var day = d.getDate();
	return new Date(year, month + 4, day)
}

function set_editions_based_on_abo_type_and_start_date() {
	var abo_type = $('select[data-fieldname = "abo_type"]')[0];
	var start_date = $('input[data-fieldname = "start_date"]')[0];
	var jan = $('input[data-fieldname = "jan_ed"]')[0];
	var feb = $('input[data-fieldname = "feb_ed"]')[0];
	var mar = $('input[data-fieldname = "mar_ed"]')[0];
	var apr = $('input[data-fieldname = "apr_ed"]')[0];
	var may = $('input[data-fieldname = "may_ed"]')[0];
	var jun = $('input[data-fieldname = "jun_ed"]')[0];
	var jul = $('input[data-fieldname = "jul_ed"]')[0];
	var aug = $('input[data-fieldname = "aug_ed"]')[0];
	var sept = $('input[data-fieldname = "sept_ed"]')[0];
	var oct = $('input[data-fieldname = "oct_ed"]')[0];
	var nov = $('input[data-fieldname = "nov_ed"]')[0];
	var dec = $('input[data-fieldname = "dec_ed"]')[0];
	if (abo_type.value != "Probe-Abo") {
		jan.checked = true;
		feb.checked = true;
		mar.checked = true;
		apr.checked = true;
		may.checked = true;
		jun.checked = true;
		jul.checked = true;
		aug.checked = true;
		sept.checked = true;
		oct.checked = true;
		nov.checked = true;
		dec.checked = true;
	} else {
		jan.checked = false;
		feb.checked = false;
		mar.checked = false;
		apr.checked = false;
		may.checked = false;
		jun.checked = false;
		jul.checked = false;
		aug.checked = false;
		sept.checked = false;
		oct.checked = false;
		nov.checked = false;
		dec.checked = false;
		var start_day = parseInt(start_date.value.split("-")[0]);
		var start_month = parseInt(start_date.value.split("-")[1]);
		if (start_day >= 15) {
			start_month = start_month + 1;
		}
		
		if (start_month == 1) {
			jan.checked = true;
			feb.checked = true;
			mar.checked = true;
			apr.checked = true;
		}
		if (start_month == 2) {
			feb.checked = true;
			mar.checked = true;
			apr.checked = true;
			may.checked = true;
		}
		if (start_month == 3) {
			mar.checked = true;
			apr.checked = true;
			may.checked = true;
			jun.checked = true;
		}
		if (start_month == 4) {
			apr.checked = true;
			may.checked = true;
			jun.checked = true;
			jul.checked = true;
		}
		if (start_month == 5) {
			may.checked = true;
			jun.checked = true;
			jul.checked = true;
			aug.checked = true;
		}
		if (start_month == 6) {
			jun.checked = true;
			jul.checked = true;
			aug.checked = true;
			sept.checked = true;
		}
		if (start_month == 7) {
			jul.checked = true;
			aug.checked = true;
			sept.checked = true;
			oct.checked = true;
		}
		if (start_month == 8) {
			aug.checked = true;
			sept.checked = true;
			oct.checked = true;
			nov.checked = true;
		}
		if (start_month == 9) {
			sept.checked = true;
			oct.checked = true;
			nov.checked = true;
			dec.checked = true;
		}
		if (start_month == 10) {
			oct.checked = true;
			nov.checked = true;
			dec.checked = true;
			jan.checked = true;
		}
		if (start_month == 11) {
			nov.checked = true;
			dec.checked = true;
			jan.checked = true;
			feb.checked = true;
		}
		if (start_month == 12) {
			dec.checked = true;
			jan.checked = true;
			feb.checked = true;
			mar.checked = true;
		}
	}
}

function set_visability_of_donee(abo_type) {
	if (abo_type.value != "Geschenk-Abo") {
		$('input[data-fieldname = "donee_first_and_lastname"]')[0].value = "";
		$('input[data-fieldname = "donee_street"]')[0].value = "";
		$('input[data-fieldname = "donee_pincode"]')[0].value = "";
		$('input[data-fieldname = "donee_city"]')[0].value = "";
		$('input[data-fieldname = "donee_first_and_lastname"]')[0].parentNode.classList.add("hidden");
		$('input[data-fieldname = "donee_street"]')[0].parentNode.classList.add("hidden");
		$('input[data-fieldname = "donee_pincode"]')[0].parentNode.classList.add("hidden");
		$('input[data-fieldname = "donee_city"]')[0].parentNode.classList.add("hidden");
		$('input[data-fieldname = "donee_first_and_lastname"]')[0].removeAttribute("data-reqd");
		$('input[data-fieldname = "donee_street"]')[0].removeAttribute("data-reqd");
		$('input[data-fieldname = "donee_pincode"]')[0].removeAttribute("data-reqd");
		$('input[data-fieldname = "donee_city"]')[0].removeAttribute("data-reqd");
		if ($('input[data-fieldname = "donee_first_and_lastname"]')[0].parentNode.classList.contains("has-error")) {
			$('input[data-fieldname = "donee_first_and_lastname"]')[0].parentNode.classList.toggle('has-error');
		}
		if ($('input[data-fieldname = "donee_street"]')[0].parentNode.classList.contains("has-error")) {
			$('input[data-fieldname = "donee_street"]')[0].parentNode.classList.toggle('has-error');
		}
		if ($('input[data-fieldname = "donee_pincode"]')[0].parentNode.classList.contains("has-error")) {
			$('input[data-fieldname = "donee_pincode"]')[0].parentNode.classList.toggle('has-error');
		}
		if ($('input[data-fieldname = "donee_city"]')[0].parentNode.classList.contains("has-error")) {
			$('input[data-fieldname = "donee_city"]')[0].parentNode.classList.toggle('has-error');
		}
	} else {
		$('input[data-fieldname = "donee_first_and_lastname"]')[0].parentNode.classList.remove("hidden");
		$('input[data-fieldname = "donee_street"]')[0].parentNode.classList.remove("hidden");
		$('input[data-fieldname = "donee_pincode"]')[0].parentNode.classList.remove("hidden");
		$('input[data-fieldname = "donee_city"]')[0].parentNode.classList.remove("hidden");
		$('input[data-fieldname = "donee_first_and_lastname"]')[0].setAttribute("data-reqd", "1");
		$('input[data-fieldname = "donee_street"]')[0].setAttribute("data-reqd", "1");
		$('input[data-fieldname = "donee_pincode"]')[0].setAttribute("data-reqd", "1");
		$('input[data-fieldname = "donee_city"]')[0].setAttribute("data-reqd", "1");
		if (!$('input[data-fieldname = "donee_first_and_lastname"]')[0].parentNode.classList.contains("has-error")) {
			$('input[data-fieldname = "donee_first_and_lastname"]')[0].parentNode.classList.toggle('has-error');
		}
		if (!$('input[data-fieldname = "donee_street"]')[0].parentNode.classList.contains("has-error")) {
			$('input[data-fieldname = "donee_street"]')[0].parentNode.classList.toggle('has-error');
		}
		if (!$('input[data-fieldname = "donee_pincode"]')[0].parentNode.classList.contains("has-error")) {
			$('input[data-fieldname = "donee_pincode"]')[0].parentNode.classList.toggle('has-error');
		}
		if (!$('input[data-fieldname = "donee_city"]')[0].parentNode.classList.contains("has-error")) {
			$('input[data-fieldname = "donee_city"]')[0].parentNode.classList.toggle('has-error');
		}
	}
}

function set_adress_dropdown(customer) {
	frappe.call({
		method: "pflanzenfreund.pflanzenfreund.web_form.neues_pflanzenfreund_abonnement.neues_pflanzenfreund_abonnement.get_address_list",
		args: {
			"customer": customer
		},
		callback: function(response) {
			var address_return = response.message;
			if (address_return) {
				var selector = $('select[data-label = "Adresse"]')[0];
				while (selector.hasChildNodes()) {  
					selector.removeChild(selector.firstChild);
				}
				for (i = 0; i < address_return.length; i++) {
					if (i == 0) {
						$('input[data-fieldname = "customer_address"]')[0].value = address_return[i]["parent"];
					}
					var option = document.createElement("option");
					option.setAttribute("value", address_return[i]["parent"]);
					var txt_option = document.createTextNode(address_return[i]["parent"]);
					option.appendChild(txt_option);
					selector.appendChild(option);
				}
				set_customer_address_display("");
			} else {
				frappe.msgprint("address not found");
			}
		}
	});
}

function copy_address_selection() {
	selected_address = $('select[data-label = "Adresse"]')[0].value;
	$('input[data-fieldname = "customer_address"]')[0].value = selected_address;
}