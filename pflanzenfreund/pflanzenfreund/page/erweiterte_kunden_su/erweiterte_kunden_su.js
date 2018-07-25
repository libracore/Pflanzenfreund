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
}

frappe.erweiterte_kunden_su = {
	start: 0,
	make: function(page) {
		var me = frappe.erweiterte_kunden_su;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		var data = "";
		$(frappe.render_template('erweiterte_kunden_su', data)).appendTo(me.body);
		getContentForTable();

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
	for (var i = 0; i < datas.length; i++) {
		crateTableContentElement(datas[i]["customer_name"], datas[i]["address_line1"], datas[i]["pincode"], datas[i]["city"]);
	}
}

function crateTableContentElement(name, address, pincode, city) {
	//console.log(name+" "+address+" "+pincode+" "+city);
	var tabelle = document.getElementById("myTable");
	
	var tr = document.createElement("tr");
	
	var td_first_name = document.createElement("td");
	var td_last_name = document.createElement("td");
	var td_address = document.createElement("td");
	var td_pincode = document.createElement("td");
	var td_city = document.createElement("td");
	
	var td_first_name_txt = document.createTextNode(name);
	var td_last_name_txt = document.createTextNode(name);
	var td_address_txt = document.createTextNode(address);
	var td_pincode_txt = document.createTextNode(pincode);
	var td_city_txt = document.createTextNode(city);
	
	td_first_name.appendChild(td_first_name_txt);
	td_last_name.appendChild(td_last_name_txt);
	td_address.appendChild(td_address_txt);
	td_pincode.appendChild(td_pincode_txt);
	td_city.appendChild(td_city_txt);
	
	tr.onclick = function() { 
		window.location = '/desk#Form/Customer/' + name;
	};
	
	tr.appendChild(td_first_name);
	tr.appendChild(td_last_name);
	tr.appendChild(td_address);
	tr.appendChild(td_pincode);
	tr.appendChild(td_city);
	
	tabelle.appendChild(tr);
	
}