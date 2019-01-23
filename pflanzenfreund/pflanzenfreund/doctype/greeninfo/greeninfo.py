# -*- coding: cp1252 -*-
# Copyright (c) 2018-2019, libracore and contributors
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
import csv
import codecs
from datetime import datetime

# Parser config
ROW_SEPARATOR = "\n"
CELL_SEPARATOR = "\t"
CELL_ENCAPSULATION = "\""

# CSV column allocation
ADRNR = 0                 # greeninfo_id
NNAME = 1                 # contact.last_name
VNAME = 2                 # contact.first_name
NBEZ1 = 3                 # customer.description
NBEZ2 = 4                 # customer.company
STRAS = 5                 # address.address_line1
STRASNR = 6               # address.address_line1
PLZAL = 7                 # address.pin_code
ORTBZ = 8                 # address.city
ANRED = 9                 # contact.salutation
BRANRED = 10              # contact.letter_salutation
SPRCD = 11                # customer.language
TELEF = 12                # contact.fax
TELEP = 13                # contact.phone
NATEL = 14                # contact.mobile
EMAILADR = 15             # contact.email
CODE05 = 16               # customer.code_05
CODE06 = 17               # customer.code_06 (obsoleted, ex. 17)
CODE07 = 17               # customer.code_07
CODE08 = 23               # customer.code_08 (obsoleted, ex. 19)
KARTE = 18                # customer.karte
KRSPERRE = 19             # customer.krsperre
MUTDT = 20                # last modification date (dd.mm.yyyy)
KONDI = 21                # payment terms
DLAND = 22                # country

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

def import_data(filename, force_update=False):
    if force_update == "True" or force_update == 1:
        force_update = True
    # read input file
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, dialect='excel')
        isfirst = True
        for row in reader:
            # leave out header and start to import
            if isfirst:
                isfirst = False
                continue
            # loop through all customers
            print(row)
            cells = row
            print("cells: {0}".format(len(cells)))
            if len(cells) >= 23:
                # check if customer exists by ID
                matches_by_id = frappe.get_all("Customer", filters={'greeninfo_id': get_field(cells[ADRNR])}, fields=['name'])
                print("Customer: {0}".format(get_field(cells[ADRNR])))
                if matches_by_id:
                    # found customer, update
                    print("updating...")
                    update_customer(matches_by_id[0]['name'], cells, force_update)
                else:
                    # no match found by ID, check name with 0 (ID not set)
                    matches_by_name = frappe.get_all("Customer",
                        filters={
                            'greeninfo_id': 0, 
                            'customer_name': "{0} {1}".format(get_field(cells[VNAME]), get_field(cells[NNAME]))}, fields=['name'])
                    if matches_by_name:
                        # matched customer by name and empty ID
                        print("updating by name")
                        update_customer(matches_by_name[0]['name'], cells)
                    else:
                        print("creating...")
                        create_customer(cells)
    return

def get_full_name(cells):
    return "{0} {1}".format(get_field(cells[VNAME]), get_field(cells[NNAME]))

def get_first_name(cells):
    if get_field(cells[VNAME]) == "":
        first_name = "-"
    else:
        first_name = get_field(cells[VNAME])
    return first_name

def get_address_line(cells):
    if get_field(cells[STRAS]) == "":
        address_line = "-"
    else:
        address_line = "{0} {1}".format(get_field(cells[STRAS]), get_field(cells[STRASNR]))
    return address_line

def get_country_from_dland(dland):
    if not dland or dland == "":
        return "Schweiz"
    else:
        countries = frappe.get_all('Country', filters={'code':dland.lower()}, fields=['name'])
        if countries:
            return countries[0]['name']
        else:
            return "Schweiz"

def create_customer(cells):
    # create record
    fullname = get_full_name(cells)
    try:
        code08 = get_field(cells[CODE08])
    except:
        code08 = ""
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
            "first_name": get_field(cells[VNAME]),
            "last_name": get_field(cells[NNAME]),
            "language": get_erp_language(get_field(cells[SPRCD])),
            "code_05": get_field(cells[CODE05]),
            #"code_06": get_field(cells[CODE06]),
            "code_07": get_field(cells[CODE07]),
            "code_08": code08,
            "karte": get_field(cells[KARTE]),
            "krsperre": get_field(cells[KRSPERRE]),
            "payment_terms": get_field(cells[KONDI])
        })
    try:
        new_customer = cus.insert()
    except Exception as e:
        add_log(_("Insert customer failed"), _("Insert failed for customer {0} {1} ({2}): {3}").format(
            get_field(cells[VNAME]), get_field(cells[NNAME]), get_field(cells[ADRNR]), e))
    else:
        create_contact(cells, new_customer.name)
        create_address(cells, new_customer.name)
    # write changes to db
    frappe.db.commit()
    return

def create_contact(cells, customer):
    try:
        fullname = get_full_name(cells)
        if get_field(cells[VNAME]) == "":
            first_name = "-"
        else:
            first_name = get_field(cells[VNAME])
        con = frappe.get_doc(
            {
                "doctype":"Contact", 
                "name": "{0} ({1})".format(fullname, customer),
                "greeninfo_id": int(get_field(cells[ADRNR])),
                "first_name": get_first_name(cells),
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
                        "link_name": customer
                    }
                ]
            })
        new_contact = con.insert()
        return new_contact
    except Exception as e:
        add_log(_("Insert contact failed"), _("Insert failed for contact {0} {1} ({2}): {3}").format(
            get_field(cells[VNAME]), get_field(cells[NNAME]), get_field(cells[ADRNR]), e))
        return None

def create_address(cells, customer):
    try:
        fullname = get_full_name(cells)
        adr = frappe.get_doc(
            {
                "doctype":"Address", 
                "name": "{0} ({1})".format(fullname, customer),
                "address_title": "{0} ({1})".format(fullname, customer),
                "address_line1": get_address_line(cells),
                "city": get_field(cells[ORTBZ]),
                "pincode": get_field(cells[PLZAL]),
                "is_primary_address": 1,
                "is_shipping_address": 1,
                "country": get_country_from_dland(get_field(cells[DLAND])),
                "links": [
                    {
                        "link_doctype": "Customer",
                        "link_name": customer
                    }
                ]
            })
        new_adr = adr.insert()
        return new_adr
    except Exception as e:
        add_log(_("Insert address failed"), _("Insert failed for address {0} {1} ({2}): {3}").format(
            get_field(cells[VNAME]), get_field(cells[NNAME]), get_field(cells[ADRNR]), e))
        return None
    
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

def update_customer(name, cells, force=False):
    # get customer record
    cus = frappe.get_doc("Customer", name)
    # check last modification date
    update = False
    if force:
        update = True
    else:
        try:
            gi_mod_date = datetime.strptime(get_field(cells[MUTDT]), '%d.%m.%Y')
            erp_mod_date = datetime.strptime(str(cus.modified).split(' ')[0], '%Y-%m-%d')
            #print("gi: {0} erp: {1}".format(gi_mod_date, erp_mod_date))
            if gi_mod_date >= erp_mod_date:
                update = True
        except Exception as e:
            add_log(_("Invalid modification date"), _("Modification date of {0} ({1}) is invalid: {2}").format(
                get_field(cells[ADRNR]), get_field(cells[MUTDT]), get_field(cells[ADRNR]), e))
            update = True
    if update:
        #print("perform update")
        fullname = "{0} {1}".format(get_field(cells[VNAME]), get_field(cells[NNAME]))
        cus.customer_name = fullname
        cus.first_name = get_field(cells[VNAME])
        cus.last_name = get_field(cells[NNAME])
        cus.greeninfo_id = int(get_field(cells[ADRNR]))
        cus.description = get_field(cells[NBEZ1])
        cus.company = get_field(cells[NBEZ2])
        cus.language = get_erp_language(get_field(cells[SPRCD]))
        cus.code_05 = get_field(cells[CODE05])
        #cus["code_06"] = get_field(cells[CODE06])
        cus.code_07 = get_field(cells[CODE07])
        #cus["code_08"] = get_field(cells[CODE08])
        cus.karte = get_field(cells[KARTE])
        cus.krsperre = get_field(cells[KRSPERRE])
        cus.payment_terms = get_field(cells[KONDI])
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
                # update contact
                con = frappe.get_doc("Contact", con_id[0]['parent'])
                con.greeninfo_id = int(get_field(cells[ADRNR]))
                con.first_name = get_first_name(cells)
                con.last_name = get_field(cells[NNAME]) or ''
                con.email_id = get_field(cells[EMAILADR]) or ''
                con.salutation = get_field(cells[ANRED]) or ''
                con.letter_salutation = get_field(cells[BRANRED]) or ''
                con.fax = get_field(cells[TELEF]) or ''
                con.phone = get_field(cells[TELEP]) or ''
                try:
                    con.save()
                except Exception as e:
                    add_log(_("Update contact failed"), _("Update failed for contact {0} {1} ({2}): {3}").format(
                        get_field(cells[VNAME]), get_field(cells[NNAME]), get_field(cells[ADRNR]), e))
            else:
                # no contact available, create
                create_contact(cells, cus.name)
            adr_id = frappe.get_all("Dynamic Link", 
                    filters={'link_doctype': 'Customer', 'link_name': cus.name, 'parenttype': 'Address'},
                    fields=['parent'])
            if adr_id:
                if get_field(cells[STRAS]) == "":
                    address_line = "-"
                else:
                    address_line = "{0} {1}".format(get_field(cells[STRAS]), get_field(cells[STRASNR]))
                adr = frappe.get_doc("Address", adr_id[0]['parent'])
                adr.address_title = fullname
                adr.address_line1 = get_address_line(cells) or ''
                adr.city = get_field(cells[ORTBZ]) or ''
                adr.pincode = get_field(cells[PLZAL]) or ''
                adr.is_primary_address = 1
                adr.is_shipping_address = 1
                adr.country = get_country_from_dland(get_field(cells[DLAND]))
                try:
                    adr.save()
                except Exception as e:
                    add_log(_("Update address failed"), _("Update address for contact {0} {1} ({2}): {3}").format(
                        get_field(cells[VNAME]), get_field(cells[NNAME]), get_field(cells[ADRNR]), e))
            else:
                # address not found, create
                create_address(cells, cus.name)
    # write changes to db
    frappe.db.commit()
    return

# Exports the contacts
#
# Parameters
#  filename: target file name
#  mod_date: only load data with modified date equal or larger than this (reduce file size and increase speed)
def export_data(filename, mod_date="2000-01-01"):
    print("prepare file...")
    # write output file
    f = codecs.open(filename, "w", 'cp1252')
    # write header line
    output = "adrnr,nname,vname,nbez1,nbez2,stras,strasnr,plzal,ortbz,anred,branred,sprcd,telef,telep,natel,emailadr,code05,code07,karte,krsperre,mutdt,kondi,dland\n"
    f.write(output)
    f.close()
    print("starting query...")
    sql_query = """SELECT `tabCustomer`.`name`
                   FROM `tabCustomer` 
                   WHERE `tabCustomer`.`modified` >= '{date}'
                   UNION SELECT `tblDL2`.`link_name`
                   FROM `tabAddress` 
                   LEFT JOIN `tabDynamic Link` As `tblDL2` ON `tblDL2`.`parent` = `tabAddress`.`name` AND `tblDL2`.`parenttype` = 'Address' AND `tblDL2`.`link_doctype` = 'Customer'
                   WHERE `tabAddress`.`modified` >= '{date}'
                   UNION SELECT `tblDL1`.`link_name`
                   FROM `tabContact` 
                   LEFT JOIN `tabDynamic Link` As `tblDL1` ON `tblDL1`.`parent` = `tabContact`.`name` AND `tblDL1`.`parenttype` = 'Contact' AND `tblDL1`.`link_doctype` = 'Customer'
                   WHERE `tabContact`.`modified` >= '{date}';""".format(date=mod_date)

    contacts = frappe.db.sql(sql_query, as_dict=True)
    print("Contacts: {0}".format(len(contacts)))
    # append to output file
    f = codecs.open(filename, "a", 'cp1252')
    # write content
    for contact_name in contacts:
        print("Looking for {0}...".format(contact_name['name']))
        customer = frappe.get_doc("Customer", contact_name['name'])
        adr_link = frappe.get_all("Dynamic Link", filters={'link_name': contact_name['name'], 'parenttype': 'Address', 'idx': 1}, fields=['parent'])
        if adr_link:
            address = frappe.get_doc("Address", adr_link[0]['parent'])
        else:
            # skip when there is no address
            continue
        cnt_link = frappe.get_all("Dynamic Link", filters={'link_name': contact_name['name'], 'parenttype': 'Contact'}, fields=['parent'])
        if cnt_link:
            contact = frappe.get_doc("Contact", cnt_link[0]['parent'])
        else:
            # skip when there is no contact
            continue
        try:
            street_parts = address.address_line1.split(" ")
            if len(street_parts) == 1:
                 stras = address.address_line1
                 strasnr = ""
            else:
                 stras = " ".join(street_parts[0:-1])
                 strasnr = street_parts[-1]
        except:
            stras = ""
            strasnr = ""
        mod = customer.modified
        first_name = contact.first_name
        if not first_name:
            first_name = ""
        elif first_name == "-":
            first_name = ""
        country = frappe.get_value("Country", address.country, "code")
        if country:
            country = country.upper()
        else:
            country = "CH"
        modification = "{0}.{1}.{2}".format(mod.day, mod.month, mod.year)
        line = "{0},\"{1}\",\"{2}\",\"{3}\",\"{4}\",\"{5}\",\"{6}\",\"{7}\",\"{8}\",\"{9}\",\"{10}\",\"{11}\",\"{12}\",\"{13}\",\"{14}\",\"{15}\",\"{16}\",\"{17}\",\"{18}\",\"{19}\",\"{20}\",\"{21}\",\"{22}\"".format(
                customer.greeninfo_id or '',
                contact.last_name or '',
                first_name,
                customer.description or '',
                customer.company or '',
                stras or '',
                strasnr or '',
                address.pincode or '',
                address.city or '',
                contact.salutation or '',
                contact.letter_salutation or '',
                get_greeninfo_lanugage(customer.language),
                contact.fax or '',
                contact.phone or '',
                contact.mobile_no or '',
                contact.email_id or '',
                customer.code_05 or '',
                customer.code_07 or '',
                customer.karte or '',
                customer.krsperre or '',
                modification,
                customer.payment_terms,
                country
              )

        #print(line) # do not print strings that may encode unicode characters, will crash cron
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
    c = None
    try:
        c = content.decode('utf8')
    except UnicodeDecodeError:
        c = content.decode('latin1')
    except:
        c = content.decode('cp1252')
    return c.replace("\"", "")

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
