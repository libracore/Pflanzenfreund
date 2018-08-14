var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
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
		var element = document.getElementById("shipping-adresse").children[1];
		element.parentNode.removeChild(element);
		
		var placeholder = document.getElementById("keineShippingAdresse");
		placeholder.className = placeholder.className.replace(" hidden", "");
	} catch {}
}

function clearBilling() {
	try {
		var element = document.getElementById("billing-adresse").children[1];
		element.parentNode.removeChild(element);
		
		var placeholder = document.getElementById("keineBillingAdresse");
		placeholder.className = placeholder.className.replace(" hidden", "");
	} catch {}
}

function addShipping(toCln) {
	var itm = document.getElementById(toCln);
	var cln = itm.cloneNode(true);
	document.getElementById("shipping-adresse").appendChild(cln); 
	
	var placeholder = document.getElementById("keineShippingAdresse");
	placeholder.className += " hidden";
}

function addBilling(toCln) {
	var itm = document.getElementById(toCln);
	var cln = itm.cloneNode(true);
	document.getElementById("billing-adresse").appendChild(cln); 
	
	var placeholder = document.getElementById("keineBillingAdresse");
	placeholder.className += " hidden";
}


function place_order(item_code) {
	update_customer_details(item_code);
}
	
	
function update_customer_details(item_code) {
	var first_name = document.getElementById("inp_first_name").value;
	var last_name = document.getElementById("inp_last_name").value;
	var mobile = document.getElementById("inp_mobile").value;
	var phone = document.getElementById("inp_phone").value;
	frappe.call({
	   method: "pflanzenfreund.utils.update_general_infos_of_existing_customer",
	   args: {
			"first_name": first_name,
			"last_name": last_name,
			"phone": phone,
			"mobile_no": mobile
	   },
	   callback: function(response) {
			var billing_placeholder = document.getElementById("keineBillingAdresse");
			var shipping_placeholder = document.getElementById("keineShippingAdresse");
			if ((billing_placeholder.classList.contains("hidden")) && (shipping_placeholder.classList.contains("hidden"))) {
				shipping = document.getElementById("shipping-adresse").children[1].dataset.addressname;
				billing = document.getElementById("billing-adresse").children[1].dataset.addressname;
				customer = response.message;
				if (item_code == "Probe-Abo") {
					place_order_probe(customer, shipping, billing);
				}
			} else {
				frappe.msgprint("Bitte zuerst Liefer- und Rechnungsadresse auswählen!");
			}
			return false;
	   }
	});
}

function place_order_probe(customer, shipping, billing) {
	frappe.call({
	   method: "pflanzenfreund.utils.place_order_probe",
	   args: {
			"customer": customer,
			"shipping": shipping,
			"billing": billing
	   },
	   callback: function(response) {
			frappe.msgprint("Die Bestellung des Probe-Abos wurde erfolgreich platziert.");
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