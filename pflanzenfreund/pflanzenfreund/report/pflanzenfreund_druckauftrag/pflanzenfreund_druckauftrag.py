# Copyright (c) 2013, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	year = getYearFromString(filters.year+"-01-01")
	columns = ["Abo Typ::200", "Customer:Link/Customer:200", "Donee:Link/Customer:200", "Beginn:Date:200", "End:Date:200"]
	if not filters.edition:
		data = frappe.db.sql("""SELECT
				`abo_type`,
				`customer`,
				`donee`,
				`start_date`,
				`end_date`
				FROM `tabPflanzenfreund Abo`
				WHERE `docstatus` = '1'
				AND (YEAR(`end_date`) >= {0} OR `end_date` IS NULL)""".format(year), as_list = True)
				
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
				`abo_type`,
				`customer`,
				`donee`,
				`start_date`,
				`end_date`
				FROM `tabPflanzenfreund Abo`
				WHERE `{0}` = '1'
				AND `docstatus` = '1'
				AND (YEAR(`end_date`) >= {1} OR `end_date` IS NULL)""".format(edition, year), as_list = True)
				
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