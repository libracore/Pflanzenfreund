# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore and contributors
# For license information, please see license.txt

# imports
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils.background_jobs import enqueue

# Parser config
ROW_SEPARATOR = "\n"
CELL_SEPARATOR = ","

# CSV column allocation
ADRNR = 0				# greeninfo_id
NNAME = 1				# contact.last_name
VNAME = 2				# contact.first_name
NBEZ1 = 3				# customer.description
NBEZ2 = 4				# customer.company
STRAS = 5				# address.address_line1
STRASNR = 6				# address.address_line1
PLZAL = 7				# address.pin_code
ORTBZ = 8				# address.city
ANRED = 9				# contact.salutation
BRANRED = 10			# contact.letter_salutation
SPRCD = 11				# customer.language
TELEF = 12				# contact.fax
TELEPH = 13				# contact.phone
NATEL = 14				# contact.mobile
EMAILADR = 15			# contact.email
CODE05 = 16				# customer.code_05
CODE06 = 17				# customer.code_06
CODE07 = 18				# customer.code_07
CODE08 = 19				# customer.code_08
KARTE = 20				# customer.karte
KRSPERRE = 21			# customer.krsperre
MUTDT = 22				# last modification date (dd.mm.yyyy)

class GreenInfo(Document):
    def sync(self):
        # enque sync
        add_log(_("Sync started"), _("Sync process started"))
        kwargs={
            'config': self
        }
        enqueue("pflanzenfreund.pflanzenfreund.doctype.greeninfo.greeninfo.sync",
            queue='long',
            timeout=15000,
            **kwargs)
        return _("Sync started. See log for details.")

# sync data with GreenInfo
def sync_greeninfo(config):
    # get configuration
    input_file = config.input_file
    output_file = config.output_file
    # first, import contacts from GreenInfo
    import_data(input_file)
    return

def import_data(filename):
    # read input file
    file = open(filename, "rU")
    # use 'ansi' encoding, not 'utf-8'
    data = file.read().decode('ansi')
    rows = data.split(ROW_SEPARATOR)
    print("Rows: {0}".format(len(rows)))
    # leave out header and start to import
    for i in range(1, len(rows)):
        # loop through all customers 
        cells = rows[i].split(CELL_SEPARATOR)
        # check if customer exists by ID
        matches_by_id = frappe.get_all("Customer", filters={'greeninfo_id': getfield(cells[ADRNR])}, fields=['name'])
        if matches_by_id:
            # found customer, update
            update_customer(matches_by_id[0]['name'], cells)
        else:
            # no match found by ID, check name with 0 (ID not set)
            matches_by_name = frappe.get_all("Customer", 
                filters={
                    'greeninfo_id': 0, 
                    'name': "{0} {1}".format(getfield(cells[ADRNR]), getfield(cells[ADRNR]))}, fields=['name'])
            if matches_by_name:    
                # matched customer by name and empty ID
                update_customer(matches_by_name[0]['name'], cells)
    		else:
                create_customer(cells)

    return

def create_customer(cells):
    # create record
    fullname = "{0} {1}".format(getfield(cells[FNAME]), getfield(cells[NNAME]))
    cus = frappe.get_doc(
        {
            "doctype":"Customer", 
            "name": fullname,
            "greeninfo_id": int(getfield(cells[ADRNR])),
            "description": getfield(cells[NBEZ1]),
            "company": getfield(cells[NBEZ2]),
            "lanugage": get_erp_language(getfield(cells[SPRCD])),
			"code_05": getfield(cells[CODE05]),
			"code_06": getfield(cells[CODE06]),
			"code_07": getfield(cells[CODE07]),
			"code_08": getfield(cells[CODE08]),
			"karte": getfield(cells[KARTE]),
			"krsperre": getfield(cells[KRSPERRE]),
        }
    try:
        cus.insert()
    except:
        add_log(_("Insert customer failed"), _("Insert failed for customer {0} {1} ({2})").format(
            getfield(cells[FNAME]), getfield(cells[NNAME]), getfield(cells[ADRNR])))
    else:
        con = frappe.get_doc(
            {
                "doctype":"Contact", 
                "greeninfo_id": int(getfield(cells[ADRNR])),
                "first_name": getfield(cells[FNAME]),
                "last_name": getfield(cells[NNAME]),
                "email_id": getfield(cells[EMAILADR]),
                "salutation": getfield(cells[ANRED]),
                "letter_salutation": getfield(cells[BRANRED]),
                "fax": getfield(cells[TELEF]),
                "phone": getfield(cells[TELEP]),
                "mobile_no": getfield(cells[NATEL]),
                "links": [
                    {
                        "link_doctype": "Customer",
                        "link_name": fullname
                    }
                ]
            }
        try:
            con.insert()
        except:
            add_log(_("Insert contact failed"), _("Insert failed for contact {0} {1} ({2})").format(
                getfield(cells[FNAME]), getfield(cells[NNAME]), getfield(cells[ADRNR])))
        else:
            adr = frappe.get_doc(
                {
                    "doctype":"Address", 
                    "address_title": fullname,
                    "address_line1": "{0} {1}".format(getfield(cells[STRAS]), getfield(cells[STRASNR])),
                    "city": getfield(cells[ORTBZ]),
                    "pincode": getfield(cells[PLZAL]),
                    "is_primary_address": 1,
                    "is_shipping_address": 1,
                    "links": [
                        {
                            "link_doctype": "Customer",
                            "link_name": fullname
                        }
                    ]
                }
            try:
                adr.insert()
            except:
                add_log(_("Insert address failed"), _("Insert failed for address {0} {1} ({2})").format(
                    getfield(cells[FNAME]), getfield(cells[NNAME]), getfield(cells[ADRNR])))
    return

def get_erp_language(lang_code):
    l = lang_code.lower()
    if l == "d":
        return "de"
    elif l = "e":
        return "en"
    elif l = "f":
        return "fr"
    elif l = "i":
        return "it"
    else:
        return "de"
        
def get_greeninfo_lanugage(language):
    if lanugage = "en":
        return "E"
    elif lanugage = "fr":
        return "F"
    elif lanugage = "it":
        return "I"
    else
        return "D"
        
def update_customer(name, cells):
	
	return
		
def export_data(filename):
    pass

# create a new log entry
def add_log(title, message):
    new_log = frappe.get_doc({'doctype': 'GreenInfo Sync Log'})
    new_log.title = title
    new_log.message = message
    new_log.insert()
    return

# removes the quotation marks from a cell
def get_field(content):
	return content.replace("\"", "")
