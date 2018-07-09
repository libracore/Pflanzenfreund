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
        cells = rows[i].split(CELL_SEPARATOR)
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
