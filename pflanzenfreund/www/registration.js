function toggleCheckbox() {
   if(document.getElementById("pwd").classList.contains("hidden")) {
		document.getElementById("pwd").classList.remove("hidden");
   } else {
	   document.getElementById("pwd").classList.add("hidden");
   }
}
var bestell_seite = location.search;
var ref = '1';
function anmeldung(referenz) {
	ref = referenz;
	if (ref == '1') {
		var mail = document.getElementById("login_email").value;
		var pwd = document.getElementById("login_password").value;
	} else {
		var mail = document.getElementById("login_email_2").value;
		var pwd = document.getElementById("login_password_2").value;
	}
	if (mail == '' || pwd == '') {
		login.set_indicator("{{ _("Please enter login data") }}", 'orange');
	} else {
		login(mail, pwd);
	}
}


function check_if_user_exist(mail, art) {
	frappe.call({
	   method: "pflanzenfreund.www.registration.check_if_user_exist",
	   args: {
			"mail": mail
	   },
	   callback: function(r) {
			if (r.message == "neu") {
				if (art == 'neu') {
					create_user();
				}
				if (art == 'gast') {
					create_gast();
				}
			} else {
				frappe.hide_message();
				frappe.msgprint('Sie besitzen bereits ein Kundenkonto.<br>Bitte melden Sie sich an. Sollten Sie Ihr Passwort vergessen haben, nutzen Sie die "Passwort vergessen?"-Funktion.', 'Information');
			}
	   }
	});
}

function create_address(pwd) {
	var vorname = document.getElementById("vorname").value;
	var nachname = document.getElementById("nachname").value;
	var strasse = document.getElementById("strasse").value;
	var nummer = document.getElementById("nummer").value;
	var plz = document.getElementById("plz").value;
	var ort = document.getElementById("ort").value;
	var mail = document.getElementById("email").value;
	if (document.getElementById("frau").checked == true) {
		var geschlecht = "Frau";
	} else {
		var geschlecht = "Herr";
	}
	
	frappe.call({
	   method: "pflanzenfreund.www.registration.create_address",
	   args: {
			"mail": mail,
			"vorname": vorname,
			"nachname": nachname,
			"strasse": strasse,
			"nummer": nummer,
			"plz": plz,
			"ort": ort,
			"geschlecht": geschlecht
	   },
	   callback: function(r) {
			if (r.message == "OK") {
				login(mail, pwd);
			}
	   }
	});
}

function create_gast() {
	var vorname = document.getElementById("vorname").value;
	var nachname = document.getElementById("nachname").value;
	var strasse = document.getElementById("strasse").value;
	var nummer = document.getElementById("nummer").value;
	var plz = document.getElementById("plz").value;
	var ort = document.getElementById("ort").value;
	var mail = document.getElementById("email").value;
	var pwd = makepw();
	frappe.call({
	   method: "pflanzenfreund.www.registration.create_user",
	   args: {
			"mail": mail,
			"vorname": vorname,
			"nachname": nachname,
			"pwd": pwd
	   },
	   callback: function(r) {
			if (r.message == 'user created') {
				create_address(pwd);
			}
	   }
	});
}

function makepw() {
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  for (var i = 0; i < 5; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}

function create_user() {
	var vorname = document.getElementById("vorname").value;
	var nachname = document.getElementById("nachname").value;
	var strasse = document.getElementById("strasse").value;
	var nummer = document.getElementById("nummer").value;
	var plz = document.getElementById("plz").value;
	var ort = document.getElementById("ort").value;
	var mail = document.getElementById("email").value;
	var pwd = document.getElementById("password").value;
	
	frappe.call({
	   method: "pflanzenfreund.www.registration.create_user",
	   args: {
			"mail": mail,
			"vorname": vorname,
			"nachname": nachname,
			"pwd": pwd
	   },
	   callback: function(r) {
			if (r.message == 'user created') {
				create_address(pwd);
			}
	   }
	});
}


function registrieren() {
	var vorname = document.getElementById("vorname");
	var nachname = document.getElementById("nachname");
	var strasse = document.getElementById("strasse");
	var nummer = document.getElementById("nummer");
	var plz = document.getElementById("plz");
	var ort = document.getElementById("ort");
	var mail = document.getElementById("email");
	var pwd = document.getElementById("password");
	if(document.getElementById("check").checked) {
		if (check_all_field_reg(true, vorname, nachname, strasse, nummer, plz, ort, mail, pwd)) {
		   frappe.show_message("Bitte warten, ein neues Gastkonto wird erstellt.");
		   check_if_user_exist(mail.value, 'gast');
		}
	} else {
	   if (check_all_field_reg(false, vorname, nachname, strasse, nummer, plz, ort, mail, pwd)) {
		   frappe.show_message("Bitte warten, ein neues Benutzerkonto wird erstellt.");
		   check_if_user_exist(mail.value, 'neu');
	   }
	}
}

function check_all_field_reg(gast, vorname, nachname, strasse, nummer, plz, ort, mail, pwd) {
	
	if ((vorname.value != "")&&(nachname.value != "")) {
		vorname.parentNode.classList.remove("has-error");
		vorname = true;
		
	} else {
		vorname.parentNode.classList.add("has-error");
		vorname = false;
	}
	
	
	if ((strasse.value != "")&&(nummer.value != "")&&(plz.value != "")&&(ort.value != "")) {
		strasse.parentNode.classList.remove("has-error");
		strasse = true;
		
	} else {
		strasse.parentNode.classList.add("has-error");
		strasse = false;
	}
	
	
	if (mail.value != "") {
		mail.parentNode.classList.remove("has-error");
		mail = true;
		
	} else {
		mail.parentNode.classList.add("has-error");
		mail = false;
	}
	
	if (gast) {
		pwd = true;
	} else {
		if (pwd.value) {
			pwd.parentNode.classList.remove("has-error");
			pwd = true;
			
		} else {
			pwd.parentNode.classList.add("has-error");
			pwd = false;
		}
	}
	
	if (mail && vorname && nachname && strasse && nummer && plz && ort && mail && pwd) {
		return true
	} else {
		return false
	}
}


function login(user, psw) {
	var args = {};
		args.cmd = "login";
		args.usr = user;
		args.pwd = psw;
		args.device = "desktop";
	frappe.call({
		type: "POST",
		args: args,
		statusCode: login.login_handlers
	});
}

login.login_handlers = (function() {
	var get_error_handler = function(default_message) {
		return function(xhr, data) {
			if(xhr.responseJSON) {
				data = xhr.responseJSON;
			}

			var message = default_message;
			if (data._server_messages) {
				message = ($.map(JSON.parse(data._server_messages || '[]'), function(v) {
					// temp fix for messages sent as dict
					try {
						return JSON.parse(v).message;
					} catch (e) {
						return v;
					}
				}) || []).join('<br>') || default_message;
			}

			if(message===default_message) {
				login.set_indicator(message, 'red');
				frappe.hide_message();
			} else {
				login.reset_sections(false);
			}

		};
	}

	var login_handlers = {
		200: function(data) {
			login.set_indicator("{{ _("Success") }}", 'green');
			window.location.href = "orderabo" + bestell_seite;
		},
		401: get_error_handler("{{ _("Invalid Login. Try again.") }}"),
		417: get_error_handler("{{ _("Oops! Something went wrong") }}")
	};

	return login_handlers;
} )();

login.set_indicator = function(message, color) {
	if (ref == '1') {
		document.getElementById("ampel").classList = '';
		document.getElementById("ampel").classList.add('indicator');
		document.getElementById("ampel").classList.add(color);
		document.getElementById("ampel").innerText = message;
	} else {
		document.getElementById("ampel_2").classList = '';
		document.getElementById("ampel_2").classList.add('indicator');
		document.getElementById("ampel_2").classList.add(color);
		document.getElementById("ampel_2").innerText = message;
	}
}

function prepare_pw_reset(btn_ref) {
	if (btn_ref == '1') {
		document.getElementById("btn_anmeldung_1").classList.add("hidden");
		document.getElementById("btn_reset_1").classList.remove("hidden");
		document.getElementById("login_password").disabled = true;
	} else {
		document.getElementById("btn_anmeldung_2").classList.add("hidden");
		document.getElementById("btn_reset_2").classList.remove("hidden");
		document.getElementById("login_password_2").disabled = true;
	}
}

function reset_passwort(btn_ref) {
	if (btn_ref == '1') {
		var mail = document.getElementById("login_email").value;
	} else {
		ref = '2';
		var mail = document.getElementById("login_email_2").value;
	}
	if (mail != '') {
		frappe.call({
		   method: "frappe.core.doctype.user.user.reset_password",
		   args: {
				"user": mail
		   },
		   callback: function(r) {
				
		   }
		});
	} else {
		frappe.msgprint("Bitte tragen Sie eine E-Mail Adresse ein.", "Information");
	}
}