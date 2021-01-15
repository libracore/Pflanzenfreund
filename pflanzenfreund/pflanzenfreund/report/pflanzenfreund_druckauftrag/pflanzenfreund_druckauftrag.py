# Copyright (c) 2013, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import utils

def execute(filters=None):
    columns, data = [], []
    year = getYearFromString(filters.year+"-01-01")
    columns = ["Abo:Link/Pflanzenfreund Abo:150", "Abo Typ::140", "Beginn:Date:60", "End:Date:60", "Customer:Link/Customer:50", "Customer Salutation::50", "Customer Name::110", "C-Addr Line 1::50", "C-Addr Line 2::50", "C-Pincode::50", "C-City::50", "C-Country::50", "Donee:Link/Customer:50", "Donee Salutation::50", "Donee Name::110", "Address Line 1::50", "Address Line 2::50", "Pincode::50", "City::50", "Country::50"]
    if not filters.edition:
        data = frappe.db.sql("""SELECT
                t1.`name`,
                t1.`abo_type`,
                t1.`start_date`,
                t1.`end_date`,
                t1.`customer`,
                t1.`customer_letter_salutation`,
                t2.`customer_name`,
                t4.`address_line1`,
                t4.`address_line2`,
                t4.`pincode`,
                t4.`city`,
                t4.`country`,
                t1.`donee`,
                t1.`donee_letter_salutation`,
                t3.`customer_name`,
                t5.`address_line1`,
                t5.`address_line2`,
                t5.`pincode`,
                t5.`city`,
                t5.`country`
                FROM ((((`tabPflanzenfreund Abo` AS t1
                LEFT JOIN `tabCustomer` AS t2 ON t1.`customer` = t2.`name`)
                LEFT JOIN `tabCustomer` AS t3 ON t1.`donee` = t3.`name`)
                LEFT JOIN `tabAddress` AS t4 ON t1.`customer_address` = t4.`name`)
                LEFT JOIN `tabAddress` AS t5 ON t1.`donee_address` = t5.`name`)
                WHERE t1.`docstatus` = '1'
                AND (YEAR(t1.`end_date`) >= {0} OR t1.`end_date` IS NULL)
                AND YEAR(t1.`start_date`) <= {0}
                AND t1.`abo_type` = '{1}'""".format(year, filters.abo_type), as_list = True)
				
        chart_data_ = frappe.db.sql("""SELECT
                                    SUM(`winter_ed`),
                                    SUM(`feb_ed`),
                                    SUM(`mar_ed`),
                                    SUM(`apr_ed`),
                                    SUM(`may_ed`),
                                    SUM(`jun_ed`),
                                    SUM(`summer_ed`),
                                    SUM(`sept_ed`),
                                    SUM(`oct_ed`),
                                    SUM(`nov_ed`)
                                    FROM `tabPflanzenfreund Abo`
                                    WHERE (YEAR(`end_date`) >= {0} OR `end_date` IS NULL)
                                    AND YEAR(`start_date`) <= {0}
                                    AND `docstatus` = '1'""".format(year), as_list = True)
        chart=get_chart_data(data, chart_data=chart_data_)
    else:
        edition = getEDcode(filters.edition)
        #mon_in_number = get_month_in_number(edition)
        start_mon_in_number = get_start_month_in_number(edition)
        end_mon_in_number = get_end_month_in_number(edition)
        #ref_date = get_last_day(str(year)+"-"+str(mon_in_number)+"-01 12:00:00")
        ref_start_date = str(year)+"-"+str(start_mon_in_number)+"-15"
        ref_end_date = str(year)+"-"+str(end_mon_in_number)+"-01"
        data = frappe.db.sql("""SELECT
                t1.`name`,
                t1.`abo_type`,
                t1.`start_date`,
                t1.`end_date`,
                t1.`customer`,
                t1.`customer_letter_salutation`,
                t2.`customer_name`,
                t4.`address_line1`,
                t4.`address_line2`,
                t4.`pincode`,
                t4.`city`,
                t4.`country`,
                t1.`donee`,
                t1.`donee_letter_salutation`,
                t3.`customer_name`,
                t5.`address_line1`,
                t5.`address_line2`,
                t5.`pincode`,
                t5.`city`,
                t5.`country`
                FROM ((((`tabPflanzenfreund Abo` AS t1
                LEFT JOIN `tabCustomer` AS t2 ON t1.`customer` = t2.`name`)
                LEFT JOIN `tabCustomer` AS t3 ON t1.`donee` = t3.`name`)
                LEFT JOIN `tabAddress` AS t4 ON t1.`customer_address` = t4.`name`)
                LEFT JOIN `tabAddress` AS t5 ON t1.`donee_address` = t5.`name`)
                WHERE t1.`{edition}` = '1'
                AND t1.`docstatus` = '1'
                AND (t1.`end_date` >= '{ref_end_date}'
                OR t1.`end_date` IS NULL)
                AND t1.`start_date` <= '{ref_start_date}'
                AND t1.`abo_type` = '{abo_type}'""".format(edition=edition, ref_start_date=ref_start_date, ref_end_date=ref_end_date, abo_type=filters.abo_type), as_list = True)

        _chart_data = {"Jahres-Abo":"", "Probe-Abo":"", "Geschenk-Abo":"", "Gratis-Abo":"", "VIP-Abo":"", "Kundenkarten-Abo (KK)":"", "Kunden-Abo (OK)":""}
        for key in _chart_data:
            _chart_data[key] = frappe.db.sql("""SELECT
                                                COUNT(`{edition}`)
                                                FROM `tabPflanzenfreund Abo`
                                                WHERE (YEAR(`end_date`) >= {year} OR `end_date` IS NULL)
                                                AND `{edition}` = '1'
                                                AND `abo_type` = '{key}'
                                                AND `docstatus` = '1'
                                                AND (`end_date` >= '{ref_end_date}'
                                                OR `end_date` IS NULL)
                                                AND `start_date` <= '{ref_start_date}'""".format(edition=edition, key=key, year=year, ref_end_date=ref_end_date, ref_start_date=ref_start_date), as_list = True)[0]
        chart=get_chart_data(data, filtered_chart_data=_chart_data)
    return columns, data, None, chart

def get_chart_data(data, chart_data=False, filtered_chart_data=False):
    if not filtered_chart_data:
        labels = ["Dec / Jan", "February", "March", "April", "May", "June", "Jul / Aug", "September", "October", "November"]#[period.key for period in period_list]
    else:
        labels = ["Jahres-Abo", "Probe-Abo", "Geschenk-Abo", "Gratis-Abo", "VIP-Abo", "Kundenkarten-Abo (KK)", "Kunden-Abo (OK)"]
    datasets = []
    if not filtered_chart_data:
        datasets.append({
            'title': 'Abo Quantity',
            'values': chart_data[0]
        })
    else:
        datasets.append({
            'title': 'Abo Quantity',
            'values': [filtered_chart_data["Jahres-Abo"][0], filtered_chart_data["Probe-Abo"][0], filtered_chart_data["Geschenk-Abo"][0], filtered_chart_data["Gratis-Abo"][0], filtered_chart_data["VIP-Abo"][0], filtered_chart_data["Kundenkarten-Abo (KK)"][0], filtered_chart_data["Kunden-Abo (OK)"][0]]
        })
    chart = {
        "data": {
            'labels': labels,
            'datasets': datasets
        }
    }
    chart["type"] = "line"
    return chart

def getEDcode(edition):
    if edition == "Dec / Jan":
        edition = "winter_ed"
    if edition == "February":
        edition = "feb_ed"
    if edition == "March":
        edition = "mar_ed"
    if edition == "April":
        edition = "apr_ed"
    if edition == "May":
        edition = "may_ed"
    if edition == "June":
        edition = "jun_ed"
    if edition == "Jul / Aug":
        edition = "summer_ed"
    if edition == "August":
        edition = "aug_ed"
    if edition == "September":
        edition = "sept_ed"
    if edition == "October":
        edition = "oct_ed"
    if edition == "November":
        edition = "nov_ed"
    if edition == "December":
        edition = "dec_ed"
    return edition
	
def getYearFromString(raw_year):
    from datetime import datetime
    dt = datetime.strptime(raw_year, '%Y-%m-%d')
    return dt.year

def get_start_month_in_number(edition):
    if edition == "feb_ed":
        edition = "01"
    if edition == "mar_ed":
        edition = "02"
    if edition == "apr_ed":
        edition = "03"
    if edition == "may_ed":
        edition = "04"
    if edition == "jun_ed":
        edition = "05"
    if edition == "sept_ed":
        edition = "08"
    if edition == "oct_ed":
        edition = "09"
    if edition == "nov_ed":
        edition = "10"
    if edition == "winter_ed":
        edition = "11"
    if edition == "summer_ed":
        edition = "06"
    return edition

def get_end_month_in_number(edition):
    if edition == "feb_ed":
        edition = "02"
    if edition == "mar_ed":
        edition = "03"
    if edition == "apr_ed":
        edition = "04"
    if edition == "may_ed":
        edition = "05"
    if edition == "jun_ed":
        edition = "06"
    if edition == "sept_ed":
        edition = "09"
    if edition == "oct_ed":
        edition = "10"
    if edition == "nov_ed":
        edition = "11"
    if edition == "winter_ed":
        edition = "12"
    if edition == "summer_ed":
        edition = "07"
    return edition

def get_last_day(dt):
    return utils.get_last_day(dt)