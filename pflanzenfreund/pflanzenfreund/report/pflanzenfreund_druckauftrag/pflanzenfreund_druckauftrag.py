# Copyright (c) 2013, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	
	columns = ["Abo Typ::200", "Customer:Link/Customer:200", "Donee:Link/Customer:200", "Beginn:Date:200", "End:Date:200"]
	
	if not filters:
		data = frappe.db.sql("""SELECT
				`abo_type`,
				`customer`,
				`donee`,
				`start_date`,
				`end_date`
				FROM `tabPflanzenfreund Abo`""", as_list = True)
				
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
									WHERE YEAR(`end_date`) >= YEAR(CURDATE()) OR `end_date` IS NULL""", as_list = True)
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
				WHERE `{0}` = '1'""".format(edition), as_list = True)
				
		_chart_data = {"Jahres-Abo":"", "Probe-Abo":"", "Geschenk-Abo":""}
		for key in _chart_data:
			_chart_data[key] = frappe.db.sql("""SELECT
										COUNT(`{0}`)
										FROM `tabPflanzenfreund Abo`
										WHERE (YEAR(`end_date`) >= YEAR(CURDATE()) OR `end_date` IS NULL)
										AND `{0}` = '1'
										AND `abo_type` = '{1}'""".format(edition, key), as_list = True)[0]
		chart=get_chart_data(data, filtered_chart_data=_chart_data)
	return columns, data, None, chart

def get_chart_data(data, chart_data=False, filtered_chart_data=False):
	# fuel_exp_data,service_exp_data,fueldata,servicedata = [],[],[],[]
	# service_exp_data = []
	# fueldata = []
	# for period in period_list:
		# total_fuel_exp=0
		# total_ser_exp=0
		# for row in data:
			# if row["Date"] <= period.to_date and row["Date"] >= period.from_date:
				# total_fuel_exp+=flt(row["Fuel Price"])
				# total_ser_exp+=flt(row["Service Expense"])
		# fueldata.append([period.key,total_fuel_exp])
		# servicedata.append([period.key,total_ser_exp])
	if not filtered_chart_data:
		labels = ["Winter", "February", "March", "April", "May", "June", "Summer", "September", "October", "November"]#[period.key for period in period_list]
	else:
		labels = ["Jahres-Abo", "Probe-Abo", "Geschenk-Abo"]
	# fuel_exp_data= [row[1] for row in fueldata]
	# service_exp_data= [row[1] for row in servicedata]
	datasets = []
	#if fuel_exp_data:
	if not filtered_chart_data:
		datasets.append({
			'title': 'Abo Quantity',
			'values': chart_data[0]
		})
	else:
		datasets.append({
			'title': 'Abo Quantity',
			'values': [filtered_chart_data["Jahres-Abo"][0], filtered_chart_data["Probe-Abo"][0], filtered_chart_data["Geschenk-Abo"][0]]
		})
	# if service_exp_data:
		# datasets.append({
			# 'title': 'Service Expenses',
			# 'values': service_exp_data
		# })
	chart = {
		"data": {
			'labels': labels,
			'datasets': datasets
		}
	}
	chart["type"] = "line"
	return chart
	
def getEDcode(edition):
	if edition == "Winter":
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
	if edition == "Summer":
		edition = "summer_ed"
	if edition == "September":
		edition = "sept_ed"
	if edition == "October":
		edition = "oct_ed"
	if edition == "November":
		edition = "nov_ed"
	return edition