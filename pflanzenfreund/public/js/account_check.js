var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  try {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    //document.getElementById("nextBtn").innerHTML = "Submit";
	document.getElementById("nextBtn").style.display = "none";
	document.getElementById("orderBtn").style.display = "inline";
  } else {
    document.getElementById("nextBtn").innerHTML = "Weiter";
	document.getElementById("nextBtn").style.display = "inline";
	document.getElementById("orderBtn").style.display = "none";
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n)
  } catch(err) {}
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
 /*  if (currentTab >= x.length) {
    //...the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  } */
  if (currentTab == 1) {
	  //show_address("shipping");
	  //show_address("billing");
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "") {
      if (y[i].dataset.leer == "ok") {  } else {
	  // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false:
      valid = false;
	  }
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class to the current step:
  x[n].className += " active";
}



/* function show_address(trigger) {
	if (trigger == "shipping") {
		address_name = document.getElementById("user_shipping_address").value;
	}
	if (trigger == "billing") {
		address_name = document.getElementById("user_billing_address").value;
	}
	if (document.getElementById("user_shipping_address").value != '') {
		frappe.call({
		   method: "frappe.client.get",
		   args: {
				"doctype": "Address",
				"name": address_name
		   },
		   callback: function(response) {
				var address = response.message;
				if (address) {
					if (trigger == "shipping") {
						var container = document.getElementById("placeholder_shipping");
						while (container.firstChild) {
							container.removeChild(container.firstChild);
						}
					}
					if (trigger == "billing") {
						var container = document.getElementById("placeholder_billing");
						while (container.firstChild) {
							container.removeChild(container.firstChild);
						}
					}
					var sub_container = document.createElement("p");
					sub_container.style.margin = "0px";
					var content = document.createTextNode(address.address_line1);
					sub_container.appendChild(content);
					container.appendChild(sub_container);
					var sub_container = document.createElement("p");
					sub_container.style.margin = "0px";
					var content = document.createTextNode(address.address_line2);
					sub_container.appendChild(content);
					container.appendChild(sub_container);
					var sub_container = document.createElement("p");
					sub_container.style.margin = "0px";
					var content = document.createTextNode(address.pincode + " " + address.city);
					sub_container.appendChild(content);
					container.appendChild(sub_container);
					var sub_container = document.createElement("p");
					sub_container.style.margin = "0px";
					var content = document.createTextNode(address.country);
					sub_container.appendChild(content);
					container.appendChild(sub_container);
				}
		   }
		});
	}
} */

function selectaddress(div, cluster) {
	adr = document.getElementById(div);
	if (adr.classList.contains("markiert")) {
		adr.className = adr.className.replace(" markiert", "");
		if (cluster == "shipping") {
			clearShipping();
		}
		if (cluster == "billing") {
			clearBilling();
		}
	} else {
		removeAllSelectetAddresses(cluster);
		if (cluster == "shipping") {
			clearShipping();
			addShipping(div);
		}
		if (cluster == "billing") {
			clearBilling();
			addBilling(div);
		}
		adr.className += " markiert";
	}
}

function removeAllSelectetAddresses(cluster) {
	var i, x = document.getElementsByClassName(cluster+"-addresscard");
	for (i = 0; i < x.length; i++) {
		x[i].className = x[i].className.replace(" markiert", "");
	}
}

function clearShipping() {
	try {
		if (getCookie("abotype") != "Geschenk-Abo") {
			var element = document.getElementById("shipping-adresse").children[1];
		} else {
			var element = document.getElementById("shipping-adresse-Geschenk").children[1];
		}
		element.parentNode.removeChild(element);
		
		if (getCookie("abotype") != "Geschenk-Abo") {
			var placeholder = document.getElementById("keineShippingAdresse");
		} else {
			var placeholder = document.getElementById("keineShippingAdresse-Geschenk");
		}
		placeholder.className = placeholder.className.replace(" hidden", "");
	} catch {}
}

function clearBilling() {
	try {
		if (getCookie("abotype") != "Geschenk-Abo") {
			var element = document.getElementById("billing-adresse").children[1];
		} else {
			var element = document.getElementById("billing-adresse-Geschenk").children[1];
		}
		element.parentNode.removeChild(element);
		
		if (getCookie("abotype") != "Geschenk-Abo") {
			var placeholder = document.getElementById("keineBillingAdresse");
		} else {
			var placeholder = document.getElementById("keineBillingAdresse-Geschenk");
		}
		placeholder.className = placeholder.className.replace(" hidden", "");
	} catch {}
}

function addShipping(toCln) {
	var itm = document.getElementById(toCln);
	var cln = itm.cloneNode(true);
	if (getCookie("abotype") != "Geschenk-Abo") {
		document.getElementById("shipping-adresse").appendChild(cln); 
	} else {
		document.getElementById("shipping-adresse-Geschenk").appendChild(cln); 
	}
	
	if (getCookie("abotype") != "Geschenk-Abo") {
		var placeholder = document.getElementById("keineShippingAdresse");
	} else {
		var placeholder = document.getElementById("keineShippingAdresse-Geschenk");
	}
	placeholder.className += " hidden";
}

function addBilling(toCln) {
	var itm = document.getElementById(toCln);
	var cln = itm.cloneNode(true);
	if (getCookie("abotype") != "Geschenk-Abo") {
		document.getElementById("billing-adresse").appendChild(cln);
	} else {
		document.getElementById("billing-adresse-Geschenk").appendChild(cln);
	}
	
	if (getCookie("abotype") != "Geschenk-Abo") {
		var placeholder = document.getElementById("keineBillingAdresse");
	} else {
		var placeholder = document.getElementById("keineBillingAdresse-Geschenk");
	}
	placeholder.className += " hidden";
}


function place_order() {
	openNav();
	var item_code = getCookie("abotype");
	if (item_code != "Geschenk-Abo") {
		update_customer_details(item_code);
	} else {
		check_if_donee_exist(item_code);
	}
}

/* Open */
function openNav() {
    document.getElementById("myNav").style.display = "block";
}

/* Close */
function closeNav() {
    document.getElementById("myNav").style.display = "none";
}

function check_if_donee_exist(item_code) {
	var first_name = document.getElementById("inp_first_name_donee").value;
	var last_name = document.getElementById("inp_last_name_donee").value;
	var mobile = document.getElementById("inp_mobile_donee").value;
	var phone = document.getElementById("inp_phone_donee").value;
	var street = document.getElementById("inp_street_donee").value;
	var plz = document.getElementById("inp_plz_donee").value;
	var ort = document.getElementById("inp_ort_donee").value;
	var email = document.getElementById("inp_email_donee").value;
	frappe.call({
	   method: "pflanzenfreund.utils.check_if_donee_exist",
	   args: {
			"email": email,
			"street": street,
			"city": ort,
			"plz": plz,
			"first_name": first_name,
			"last_name": last_name,
			"phone": phone,
			"mobile": mobile
	   },
	   callback: function(response) {
			update_customer_details(item_code, response.message.name);
	   }
	});
}

function testtest() {
	
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
	
function update_customer_details(item_code, donee) {
	if (item_code != "Geschenk-Abo") {
		var first_name = document.getElementById("inp_first_name").value;
		var last_name = document.getElementById("inp_last_name").value;
		var mobile = document.getElementById("inp_mobile").value;
		var phone = document.getElementById("inp_phone").value;
	} else {
		var first_name = document.getElementById("geschenk_inp_first_name").value;
		var last_name = document.getElementById("geschenk_inp_last_name").value;
		var mobile = document.getElementById("geschenk_inp_mobile").value;
		var phone = document.getElementById("geschenk_inp_phone").value;
	}
	frappe.call({
	   method: "pflanzenfreund.utils.update_general_infos_of_existing_customer",
	   args: {
			"first_name": first_name,
			"last_name": last_name,
			"phone": phone,
			"mobile_no": mobile
	   },
	   callback: function(response) {
			var customer = response.message;
			if (item_code != "Geschenk-Abo") {
				var billing_placeholder = document.getElementById("keineBillingAdresse");
				var shipping_placeholder = document.getElementById("keineShippingAdresse");
			} else {
				var billing_placeholder = document.getElementById("keineBillingAdresse-Geschenk");
				var shipping_placeholder = document.getElementById("keineShippingAdresse-Geschenk");
			}
			if ((billing_placeholder.classList.contains("hidden")) && (shipping_placeholder.classList.contains("hidden"))) {
				if (item_code != "Geschenk-Abo") {
					shipping = document.getElementById("shipping-adresse").children[1].dataset.addressname;
					billing = document.getElementById("billing-adresse").children[1].dataset.addressname;
					place_order_abo(customer, shipping, billing, item_code, "");
				} else {
					billing = document.getElementById("billing-adresse-Geschenk").children[1].dataset.addressname;
					frappe.call({
					   method: "pflanzenfreund.utils.get_donee_address",
					   args: {
							"donee": donee
					   },
					   callback: function(r) {
							shipping = r.message[0];
							place_order_abo(customer, shipping, billing, item_code, donee);
					   }
					});
				}
			} else {
				frappe.msgprint("Bitte zuerst Liefer- und Rechnungsadresse auswählen!");
			}
			return false;
	   }
	});
}

function place_order_abo(customer, shipping, billing, abo, donee) {
	frappe.call({
	   method: "pflanzenfreund.utils.place_order_abo",
	   args: {
			"customer": customer,
			"shipping": shipping,
			"billing": billing,
			"abo": abo,
			"donee": donee
	   },
	   callback: function(response) {
			closeNav();
			frappe.msgprint("Die Bestellung des " + abo + "s wurde erfolgreich platziert.");
			if (abo != "Geschenk-Abo") {
				document.getElementById("orderModal").style.width = "0%";
			}
			setTimeout(function(){ window.location = "/abonnieren"; }, 1000);
	   }
	});
}
	
	
	
var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
        /* Toggle between adding and removing the "active" class,
        to highlight the button that controls the panel */
        var acc2 = document.getElementsByClassName("accordion");
		var i2;

		for (i2 = 0; i2 < acc2.length; i2++) {
			acc2[i2].className = acc2[i2].className.replace(" active", "");
			var panel2 = acc2[i2].nextElementSibling;
			if (panel2.style.display === "block") {
				panel2.style.display = "none";
			}
		}
		this.classList.toggle("active");

        /* Toggle between hiding and showing the active panel */
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    });
} 
