function checkLogin(abo) {
	if (frappe.get_sid()) {
		showOrderArea(abo);
		if (abo != "Geschenk-Abo") {
			openOrderModal();
		} else {
			document.getElementById("orderModalGeschenk").style.width = "100%";
		}
	} else {
		window.location = "/login";
	}
}

function showOrderArea(abo) {
	document.cookie = "abotype=" + abo;
}

/* Open */
function openOrderModal() {
    document.getElementById("orderModal").style.width = "100%";
}

/* Close */
function closeOrderModal() {
    if (getCookie("abotype") != "Geschenk-Abo") {
		document.getElementById("orderModal").style.width = "0%";
	} else {
		document.getElementById("orderModalGeschenk").style.width = "0%";
	}
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

//Geschenk Modal Funktionen (das andere modal ist im account_check!
var currenttabGeschenkGeschenk = 0; // Current tabGeschenk is set to be the first tabGeschenk (0)
showtabGeschenkGeschenk(currenttabGeschenkGeschenk); // Display the current tabGeschenk

function showtabGeschenkGeschenk(n) {
  try {
  // This function will display the specified tabGeschenk of the form ...
  var x = document.getElementsByClassName("tabGeschenk");
  x[n].style.display = "block";
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtnGeschenk").style.display = "none";
  } else {
    document.getElementById("prevBtnGeschenk").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    //document.getElementById("nextBtnGeschenk").innerHTML = "Submit";
	document.getElementById("nextBtnGeschenk").style.display = "none";
	document.getElementById("orderBtnGeschenk").style.display = "inline";
	var first_name = document.getElementById("inp_first_name_donee").value;
	var last_name = document.getElementById("inp_last_name_donee").value;
	var street = document.getElementById("inp_street_donee").value;
	var plz = document.getElementById("inp_plz_donee").value;
	var ort = document.getElementById("inp_ort_donee").value;
	
	document.getElementById("placeholder-for-geschenk-adresse").innerHTML = first_name +" "+last_name+"<br>"+street+"<br>"+ort+"<br>"+plz;
  } else {
    document.getElementById("nextBtnGeschenk").innerHTML = "Weiter";
	document.getElementById("nextBtnGeschenk").style.display = "inline";
	document.getElementById("orderBtnGeschenk").style.display = "none";
  }
  // ... and run a function that displays the correct stepGeschenk indicator:
  fixstepGeschenkIndicatorGeschenk(n)
  } catch(err) {}
}

function nextPrevGeschenk(n) {
  // This function will figure out which tabGeschenk to display
  var x = document.getElementsByClassName("tabGeschenk");
  // Exit the function if any field in the current tabGeschenk is invalid:
  if (n == 1 && !validateFormGeschenk()) return false;
  // Hide the current tabGeschenk:
  x[currenttabGeschenkGeschenk].style.display = "none";
  // Increase or decrease the current tabGeschenk by 1:
  currenttabGeschenkGeschenk = currenttabGeschenkGeschenk + n;
  // if you have reached the end of the form... :
 /*  if (currenttabGeschenkGeschenk >= x.length) {
    //...the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  } */
  if (currenttabGeschenkGeschenk == 1) {
	  //show_address("shipping");
	  //show_address("billing");
  }
  // Otherwise, display the correct tabGeschenk:
  showtabGeschenkGeschenk(currenttabGeschenkGeschenk);
}

function validateFormGeschenk() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tabGeschenk");
  y = x[currenttabGeschenkGeschenk].getElementsByTagName("input");
  // A loop that checks every input field in the current tabGeschenk:
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
  // If the valid status is true, mark the stepGeschenk as finished and valid:
  if (valid) {
    document.getElementsByClassName("stepGeschenk")[currenttabGeschenkGeschenk].className += " finish";
  }
  return valid; // return the valid status
}

function fixstepGeschenkIndicatorGeschenk(n) {
  // This function removes the "active" class of all stepGeschenks...
  var i, x = document.getElementsByClassName("stepGeschenk");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class to the current stepGeschenk:
  x[n].className += " active";
}













