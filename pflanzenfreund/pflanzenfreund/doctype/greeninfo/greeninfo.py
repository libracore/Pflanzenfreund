# -*- coding: cp1252 -*-
# Copyright (c) 2018, libracore and contributors
# For license information, please see license.txt
#
# Test with
#   bench execute pflanzenfreund.pflanzenfreund.doctype.greeninfo.greeninfo.import_data --kwargs "{'filename': '/mnt/share/testin.csv'}"
#   bench execute pflanzenfreund.pflanzenfreund.doctype.greeninfo.greeninfo.export_data --kwargs "{'filename': '/mnt/share/testout.csv'}"

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
TELEP = 13				# contact.phone
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
    f = open(filename, "rU")
    # use 'ansi'/'cp1252' encoding, not 'utf-8'
    data = f.read()  # .decode('cp1252')
    f.close()
    rows = data.split(ROW_SEPARATOR)
    # leave out header and start to import
    for i in range(1, len(rows)):
        # loop through all customers 
        cells = rows[i].split(CELL_SEPARATOR)
        if len(cells) >= 23:
            # check if customer exists by ID
            matches_by_id = frappe.get_all("Customer", filters={'greeninfo_id': get_field(cells[ADRNR])}, fields=['name'])
            if matches_by_id:
                # found customer, update
                update_customer(matches_by_id[0]['name'], cells)
            else:
                # no match found by ID, check name with 0 (ID not set)
                matches_by_name = frappe.get_all("Customer", 
                    filters={
                        'greeninfo_id': 0, 
                        'customer_name': "{0} {1}".format(get_field(cells[ADRNR]), get_field(cells[ADRNR]))}, fields=['name'])
                if matches_by_name:    
                    # matched customer by name and empty ID
                    update_customer(matches_by_name[0]['name'], cells)
                else:
                    create_customer(cells)

    return

def create_customer(cells):
    # create record
    fullname = "{0} {1}".format(get_field(cells[VNAME]), get_field(cells[NNAME]))
    cus = frappe.get_doc(
        {
            "doctype":"Customer", 
            "customer_name": fullname,
            "customer_type": "Individual",
            "customer_group": "All Customer Groups",
            "territory": "All Territories",
            "greeninfo_id": int(get_field(cells[ADRNR])),
            "description": get_field(cells[NBEZ1]),
            "company": get_field(cells[NBEZ2]),
            "language": get_erp_language(get_field(cells[SPRCD])),
			"code_05": get_field(cells[CODE05]),
			"code_06": get_field(cells[CODE06]),
			"code_07": get_field(cells[CODE07]),
			"code_08": get_field(cells[CODE08]),
			"karte": get_field(cells[KARTE]),
			"krsperre": get_field(cells[KRSPERRE]),
        })
    try:
        new_customer = cus.insert()
    except Exception as e:
        add_log(_("Insert customer failed"), _("Insert failed for customer {0} {1} ({2}): {3}").format(
            get_field(cells[VNAME]), get_field(cells[NNAME]), get_field(cells[ADRNR]), e))
    else:
        if get_field(cells[VNAME]) == "":
            first_name = "-"
        else:
            first_name = get_field(cells[VNAME])
        con = frappe.get_doc(
            {
                "doctype":"Contact", 
                "name": "{0} ({1})".format(fullname, new_customer.name),
                "greeninfo_id": int(get_field(cells[ADRNR])),
                "first_name": first_name,
                "last_name": get_field(cells[NNAME]),
                "email_id": get_field(cells[EMAILADR]),
                "salutation": get_field(cells[ANRED]),
                "letter_salutation": get_field(cells[BRANRED]),
                "fax": get_field(cells[TELEF]),
                "phone": get_field(cells[TELEP]),
                "mobile_no": get_field(cells[NATEL]),
                "links": [
                    {
                        "link_doctype": "Customer",
                        "link_name": new_customer.name
                    }
                ]
            })
        try:
            con.insert()
        except Exception as e:
            add_log(_("Insert contact failed"), _("Insert failed for contact {0} {1} ({2}): {3}").format(
                get_field(cells[VNAME]), get_field(cells[NNAME]), get_field(cells[ADRNR]), e))
        else:
            adr = frappe.get_doc(
                {
                    "doctype":"Address", 
                    "name": "{0} ({1})".format(fullname, new_customer.name),
                    "address_title": "{0} ({1})".format(fullname, new_customer.name),
                    "address_line1": "{0} {1}".format(get_field(cells[STRAS]), get_field(cells[STRASNR])),
                    "city": get_field(cells[ORTBZ]),
                    "pincode": get_field(cells[PLZAL]),
                    "is_primary_address": 1,
                    "is_shipping_address": 1,
                    "links": [
                        {
                            "link_doctype": "Customer",
                            "link_name": new_customer.name
                        }
                    ]
                })
            try:
                adr.insert()
            except Exception as e:
                add_log(_("Insert address failed"), _("Insert failed for address {0} {1} ({2}): {3}").format(
                    get_field(cells[VNAME]), get_field(cells[NNAME]), get_field(cells[ADRNR]), e))
    return

def get_erp_language(lang_code):
    l = lang_code.lower()
    if l == "d":
        return "de"
    elif l == "e":
        return "en"
    elif l == "f":
        return "fr"
    elif l == "i":
        return "it"
    else:
        return "de"
        
def get_greeninfo_lanugage(language):
    if language == "en":
        return "E"
    elif language == "fr":
        return "F"
    elif language == "it":
        return "I"
    else:
        return "D"
        
def update_customer(name, cells):
    # get customer record
    cus = frappe.get_doc("Customer", name)
	# check last modification date
    gi_last_modified_fields = get_field(cells[MUTDT]).split(".")
    mod = str(cus.modified)
    update = False
    if int(gi_last_modified_fields[2]) >= int(mod[0:4]):
        if int(gi_last_modified_fields[1]) >= int(mod[5:7]):
            if int(gi_last_modified_fields[0]) > int(mod[8:10]):
                update = True
    if update:
        fullname = "{0} {1}".format(get_field(cells[VNAME]), get_field(cells[NNAME]))
        cus["customer_name"] = fullname
        cus["greeninfo_id"] = int(get_field(cells[ADRNR]))
        cus["description"] = get_field(cells[NBEZ1])
        cus["company"] = get_field(cells[NBEZ2])
        cus["language"] = get_erp_language(get_field(cells[SPRCD]))
        cus["code_05"] = get_field(cells[CODE05])
        cus["code_06"] = get_field(cells[CODE06])
        cus["code_07"] = get_field(cells[CODE07])
        cus["code_08"] = get_field(cells[CODE08])
        cus["karte"] = get_field(cells[KARTE])
        cus["krsperre"] = get_field(cells[KRSPERRE])
        try:
            cus.save()
        except Exception as e:
            add_log(_("Update customer failed"), _("Update failed for customer {0} {1} ({2}): {3}").format(
                get_field(cells[VNAME]), get_field(cells[NNAME]), get_field(cells[ADRNR]), e))
        else:
            con_id = frappe.get_all("Dynamic Link", 
                filters={'link_doctype': 'Customer', 'link_name': cus.name, 'parenttype': 'Contact'},
                fields=['parent'])
            if con_id:
                if get_field(cells[VNAME]) == "":
                    first_name = "-"
                else:
                    first_name = get_field(cells[VNAME])
                con = frappe.get_doc("Contact", con_id[0]['parent'])
                con["greeninfo_id"] = int(get_field(cells[ADRNR])),
                con["first_name"] = first_name,
                con["last_name"] = get_field(cells[NNAME]),
                con["email_id"] = get_field(cells[EMAILADR]),
                con["salutation"] = get_field(cells[ANRED]),
                con["letter_salutation"] = get_field(cells[BRANRED]),
                con["fax"] = get_field(cells[TELEF]),
                con["phone"] = get_field(cells[TELEP]),
                try:
                    con.save()
                except Exception as e:
                    add_log(_("Update contact failed"), _("Update failed for contact {0} {1} ({2}): {3}").format(
                        get_field(cells[VNAME]), get_field(cells[NNAME]), get_field(cells[ADRNR]), e))
                else:
                    adr_id = frappe.get_all("Dynamic Link", 
                        filters={'link_doctype': 'Customer', 'link_name': cus.name, 'parenttype': 'Address'},
                        fields=['parent'])
                    if adr_id:
                        adr = frappe.get_doc("Address", adr_id[0]['parent'])
                        adr["address_title"] = fullname,
                        adr["address_line1"] = "{0} {1}".format(get_field(cells[STRAS]), get_field(cells[STRASNR])),
                        adr["city"] = get_field(cells[ORTBZ]),
                        adr["pincode"] = get_field(cells[PLZAL]),
                        adr["is_primary_address"] = 1,
                        adr["is_shipping_address"] = 1,
                        try:
                            adr.save()
                        except Exception as e:
                            add_log(_("Update address failed"), _("Update address for contact {0} {1} ({2}): {3}").format(
                                get_field(cells[VNAME]), get_field(cells[NNAME]), get_field(cells[ADRNR]), e))
    return
		
def export_data(filename):
    sql_query = """SELECT 
        `tCus`.`greeninfo_id` AS `adrnr`,
        `tCon`.`last_name` AS `nname`,
        `tCon`.`first_name` AS `vname`,
        `tCus`.`description` AS `nbez1`,
        `tCus`.`company` AS `nbez2`,
        `tAdr`.`address_line1` AS `str`,
        `tAdr`.`pincode` AS `plzal`,
        `tAdr`.`city` AS `ortbz`,
        `tCon`.`salutation` AS `anred`,
        `tCon`.`letter_salutation` AS `branred`,
        `tCus`.`language` AS `language`,
        `tCon`.`fax` AS `telef`,
        `tCon`.`phone` AS `telep`,
        `tCon`.`mobile_no` AS `natel`,
        `tCon`.`email_id` AS `emailadr`,
        `tCus`.`code_05` AS `code05`,
        `tCus`.`code_06` AS `code06`,
        `tCus`.`code_07` AS `code07`,
        `tCus`.`code_08` AS `code08`,
        `tCus`.`karte` AS `karte`,
        `tCus`.`krsperre` AS `krsperre`,
        `tCus`.`modified` AS `modified`        
      FROM `tabCustomer` AS `tCus`
      LEFT JOIN `tabDynamic Link` AS `tDL1` ON (`tCus`.`name` = `tDL1`.`link_name` AND `tDL1`.`parenttype` = "Contact")
      LEFT JOIN `tabContact` AS `tCon` ON (`tDL1`.`parent` = `tCon`.`name`)
      LEFT JOIN `tabDynamic Link` AS `tDL2` ON (`tCus`.`name` = `tDL2`.`link_name` AND `tDL2`.`parenttype` = "Address")
      LEFT JOIN `tabAddress` AS `tAdr` ON (`tDL2`.`parent` = `tAdr`.`name`)"""
    contacts = frappe.db.sql(sql_query, as_dict=True)
    
    # write output file
    f = open(filename, "w")
    # write header line 
    f.write("adrnr,nname,vname,nbez1,nbez2,stras,strasnr,plzal,ortbz,anred,branred,sprcd,telef,telep,natel,emailadr,code05,code06,code07,code08,karte,krsperre,mutdt\n")
    # write content
    for contact in contacts:
        try:
            street_parts = contact['str'].split(" ")
            if len(street_parts) == 1:
                stras = contact['str']
                strasnr = ""
            else:
                stras = " ".join(street_parts[0:-1])
                strasnr = street_parts[-1]
        except:
            stras = ""
            strasnr = ""
        mod = str(contact['modified'])
        line = "{0},\"{1}\",\"{2}\",\"{3}\",\"{4}\",\"{5}\",\"{6}\",\"{7}\",\"{8}\",\"{9}\",\"{10}\",\"{11}\",\"{12}\",\"{13}\",\"{14}\",\"{15}\",\"{16}\",\"{17}\",\"{18}\",\"{19}\",\"{20}\",\"{21}\",{22}".format(
            contact['adrnr'],
            contact['nname'],
            contact['vname'],
            contact['nbez1'],
            contact['nbez2'],
            stras,
            strasnr,
            contact['plzal'],
            contact['ortbz'],
            contact['anred'],
            contact['branred'],
            get_greeninfo_lanugage(contact['language']),
            contact['telef'],
            contact['telep'],
            contact['natel'],
            contact['emailadr'],
            contact['code05'],
            contact['code06'],
            contact['code07'],
            contact['code08'],
            contact['karte'],
            contact['krsperre'],
            "{0}.{1}.{2}".format(mod[8:10], mod[5:7], mod[0:4])
          )
        f.write(line + "\n")
            
    f.close()  
    return

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

def test():
    con = frappe.get_doc(
        {
            "doctype":"Contact", 
            "name": "Lars",
            "greeninfo_id": 123,
            "first_name": "Lars",
            "last_name": "M",
            "email_id": "lars.mueller@libracore.com",
            "salutation": "Herr",
            "letter_salutation": "BlaBla",
            "fax": "",
            "phone": "052",
            "mobile_no": "079",
            "links": [
                {
                    "link_doctype": "Customer",
                    "link_name": "Guest"
                }
            ]
        })
    con.insert()
