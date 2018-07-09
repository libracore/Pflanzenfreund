# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils.background_jobs import enqueue

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
    return

def import_data(filename):
    pass
	
def export_data(filename):
    pass

# create a new log entry
def add_log(title, message):
    new_log = frappe.get_doc({'doctype': 'GreenInfo Sync Log'})
    new_log.title = title
    new_log.message = message
    new_log.insert()
    return
