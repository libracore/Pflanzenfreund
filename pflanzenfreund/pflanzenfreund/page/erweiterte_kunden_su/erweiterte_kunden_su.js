frappe.pages['erweiterte-kunden-su'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Erweiterte Kundensuche',
		single_column: true
	});
	
	frappe.erweiterte_kunden_su.make(page);
	frappe.erweiterte_kunden_su.run(page);
	
	// add the application reference
	frappe.breadcrumbs.add("Pflanzenfreund");

	this.page.add_menu_item(__('Alle Daten Laden'), function() {
		loadAllData();
	});
	this.page.add_menu_item(__('Add to Desktop'), function() {
		frappe.add_to_desktop(this.report_name, null, this.report_name);
	});
}




frappe.erweiterte_kunden_su = {
	start: 0,
	make: function(page) {
		var me = frappe.erweiterte_kunden_su;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		var data = "";
		$(frappe.render_template('erweiterte_kunden_su', data)).appendTo(me.body);
		

	},
	run: function(page) {
 
	}
}


function searchByFirstName(searchID="FirstNameInput", searchIn="0") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("filteredFirstName");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("filteredFirstName");
	  }
    }
  }
}
function searchByLastName(searchID="LastNameInput", searchIn="1") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("filteredLastName");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("filteredLastName");
	  }
    }
  }
}
function searchByStreet(searchID="streetInput", searchIn="2") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("filteredStreet");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("filteredStreet");
	  }
    }
  }
}
function searchByPincodes(searchID="plzInput", searchIn="3") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("filteredPLZ");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("filteredPLZ");
	  }
    }
  }
}
function searchBycity(searchID="cityInput", searchIn="4") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("filteredCity");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("filteredCity");
	  }
    }
  }
}





function getContentForTable() {
	frappe.call({
		method: 'pflanzenfreund.pflanzenfreund.page.erweiterte_kunden_su.erweiterte_kunden_su.get_all_infos',
		callback: function(r) {
			if (r.message) {
				//console.log(r.message);
				createTableWithContent(r.message);
				
			} 
		}
	});
}

function createTableWithContent(datas) {
	var tabelle = document.getElementById("myTable");

	var rowCount = tabelle.rows.length;
	for (var i = rowCount - 1; i > 0; i--) {
		tabelle.deleteRow(i);
	}
	for (var i = 0; i < datas.length; i++) {
		crateTableContentElement(datas[i]["first_name"], datas[i]["last_name"], datas[i]["address_line1"], datas[i]["pincode"], datas[i]["city"], datas[i]["name"]);
	}
	closeNav();
}

function crateTableContentElement(first_name, last_name, address, pincode, city, referenz) {
	//console.log(name+" "+address+" "+pincode+" "+city);
	var tabelle = document.getElementById("myTable");
	
	var tr = document.createElement("tr");
	
	var td_first_name = document.createElement("td");
	var td_last_name = document.createElement("td");
	var td_address = document.createElement("td");
	var td_pincode = document.createElement("td");
	var td_city = document.createElement("td");
	
	var td_first_name_txt = document.createTextNode(first_name);
	var td_last_name_txt = document.createTextNode(last_name);
	var td_address_txt = document.createTextNode(address);
	var td_pincode_txt = document.createTextNode(pincode);
	var td_city_txt = document.createTextNode(city);
	
	td_first_name.appendChild(td_first_name_txt);
	td_last_name.appendChild(td_last_name_txt);
	td_address.appendChild(td_address_txt);
	td_pincode.appendChild(td_pincode_txt);
	td_city.appendChild(td_city_txt);
	
	tr.onclick = function() { 
		window.location = '/desk#Form/Customer/' + referenz;
	};
	
	tr.appendChild(td_first_name);
	tr.appendChild(td_last_name);
	tr.appendChild(td_address);
	tr.appendChild(td_pincode);
	tr.appendChild(td_city);
	
	tabelle.appendChild(tr);
	
}


function loadAllData() {
	frappe.confirm(
		'Wollen Sie wirklich alle Daten laden?<br>Dies kann einige Zeit in Anspruch nehmen!',
		function(){
			openNav();
			getContentForTable();
		},
		function(){
			window.close();
		}
	);	
}

function loadPreFilterData() {
	var name = document.getElementById("vorselektionierungNachnamen").value;
	var plz = document.getElementById("vorselektionierungPostleitzahl").value;
	if ((name == "") && (plz == "")) {
		frappe.msgprint("Bitte treffen Sie zuerst eine Vorselektionierung", "Vorselektionierung fehlt");
	} else {	
		openNav();
		frappe.call({
			method: 'pflanzenfreund.pflanzenfreund.page.erweiterte_kunden_su.erweiterte_kunden_su.get_filtered_infos',
			args: {
				'name': name,
				'plz': plz
			},
			callback: function(r) {
				if (r.message) {
					//console.log(r.message);
					createTableWithContent(r.message);
					
				} else {
					closeNav();
					var tabelle = document.getElementById("myTable");

					var rowCount = tabelle.rows.length;
					for (var i = rowCount - 1; i > 0; i--) {
						tabelle.deleteRow(i);
					}
					frappe.msgprint("Keine Suchresultate gefunden!", "Suche ergebnislos");
				}
			}
		});
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
