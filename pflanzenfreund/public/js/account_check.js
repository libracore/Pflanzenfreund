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
    document.getElementById("nextBtn").innerHTML = "Next";
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
	  show_address("shipping");
	  show_address("billing");
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



function show_address(trigger) {
	address_name = document.getElementById("user_shipping_address").value;
	
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
				}
				if (trigger == "billing") {
					var container = document.getElementById("placeholder_billing");
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




function place_order(item_code, customer, shipping, billing) {
		shipping = document.getElementById("user_shipping_address").value;
		billing = document.getElementById("user_billing_address").value;
		frappe.msgprint("Es wird eine Bestellung von "+item_code+", für den Kunden "+customer+" angelegt. Rechnungsadresse: "+billing+" / Lieferadresse: "+shipping);
		return false;
	}