# Copyright (c) 2013, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	year = getYearFromString(filters.year+"-01-01")
	columns = ["Abo Typ::140", "Beginn:Date:60", "End:Date:60", "Customer:Link/Customer:50", "Customer Name::110", "C-Addr Line 1::50", "C-Addr Line 2::50", "C-Pincode::50", "C-City::50", "C-Country::50", "Donee:Link/Customer:50", "Donee Name::110", "Address Line 1::50", "Address Line 2::50", "Pincode::50", "City::50", "Country::50"]
	if not filters.edition:
		data = frappe.db.sql("""SELECT
				t1.`abo_type`,
				t1.`start_date`,
				t1.`end_date`,
				t1.`customer`,
				t2.`customer_name`,
				t4.`address_line1`,
				t4.`address_line2`,
				t4.`pincode`,
				t4.`city`,
				t4.`country`,
				t1.`donee`,
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
				AND (YEAR(t1.`end_date`) >= {0} OR t1.`end_date` IS NULL)""".format(year), as_list = True)
				
		chart_data_ = frappe.db.sql("""SELECT
									SUM(`jan_ed`),
									SUM(`feb_ed`),
									SUM(`mar_ed`),
									SUM(`apr_ed`),
									SUM(`may_ed`),
									SUM(`jun_ed`),
									SUM(`jul_ed`),
									SUM(`aug_ed`),
									SUM(`sept_ed`),
									SUM(`oct_ed`),
									SUM(`nov_ed`),
									SUM(`dec_ed`)
									FROM `tabPflanzenfreund Abo`
									WHERE (YEAR(`end_date`) >= {0} OR `end_date` IS NULL)
									AND `docstatus` = '1'""".format(year), as_list = True)
		chart=get_chart_data(data, chart_data=chart_data_)
	else:
		edition = getEDcode(filters.edition)
		data = frappe.db.sql("""SELECT
				t1.`abo_type`,
				t1.`start_date`,
				t1.`end_date`,
				t1.`customer`,
				t2.`customer_name`,
				t4.`address_line1`,
				t4.`address_line2`,
				t4.`pincode`,
				t4.`city`,
				t4.`country`,
				t1.`donee`,
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
				WHERE t1.`{0}` = '1'
				AND t1.`docstatus` = '1'
				AND (YEAR(t1.`end_date`) >= {1} OR t1.`end_date` IS NULL)""".format(edition, year), as_list = True)
				
		_chart_data = {"Jahres-Abo":"", "Probe-Abo":"", "Geschenk-Abo":"", "Gratis-Abo":"", "VIP-Abo":"", "Kundenkarten-Abo (KK)":"", "Kunden-Abo (OK)":""}
		for key in _chart_data:
			_chart_data[key] = frappe.db.sql("""SELECT
										COUNT(`{0}`)
										FROM `tabPflanzenfreund Abo`
										WHERE (YEAR(`end_date`) >= {2} OR `end_date` IS NULL)
										AND `{0}` = '1'
										AND `abo_type` = '{1}'
										AND `docstatus` = '1'""".format(edition, key, year), as_list = True)[0]
		chart=get_chart_data(data, filtered_chart_data=_chart_data)
	return columns, data, None, chart

def get_chart_data(data, chart_data=False, filtered_chart_data=False):
	if not filtered_chart_data:
		labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]#[period.key for period in period_list]
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
	if edition == "January":
		edition = "jan_ed"
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
	if edition == "July":
		edition = "jul_ed"
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
