# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "pflanzenfreund"
app_title = "Pflanzenfreund"
app_publisher = "libracore"
app_description = "Alles rund um die Zeitschrift Pflanzenfreund"
app_icon = "octicon octicon-book"
app_color = "green"
app_email = "info@libracore.com"
app_license = "AGPL"

after_install = "pflanzenfreund.install.after_install"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/pflanzenfreund/css/pflanzenfreund.css"
# app_include_js = "/assets/pflanzenfreund/js/pflanzenfreund.js"

# include js, css files in header of web template
web_include_css = "/assets/pflanzenfreund/css/pflanzenfreund.css"
# web_include_js = "/assets/pflanzenfreund/js/pflanzenfreund.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

jenv = {
	"methods": [
		"navbar_items:pflanzenfreund.utils.get_navbar_items",
		"get_footer_items:pflanzenfreund.utils.get_footer_items",
		"get_footer_social_items:pflanzenfreund.utils.get_footer_social_items",
		"footer_brand:pflanzenfreund.utils.get_footer_brand",
		"footer_description:pflanzenfreund.utils.get_footer_description",
		"get_all_addresses:pflanzenfreund.utils.get_all_addresses",
		"get_address_details:pflanzenfreund.utils.get_address_details"
		]
}

website_context = {
	"base_template_path": "templates/pflanzenfreund_base.html"
}

# website_route_rules = [
	# {"from_route": "/desk#modules/Website", "to_route": "/desk#modules/Pflanzenfreund"}
# ]

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "pflanzenfreund.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "pflanzenfreund.install.before_install"
# after_install = "pflanzenfreund.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "pflanzenfreund.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"pflanzenfreund.tasks.all"
# 	],
# 	"daily": [
# 		"pflanzenfreund.tasks.daily"
# 	],
# 	"hourly": [
# 		"pflanzenfreund.tasks.hourly"
# 	],
# 	"weekly": [
# 		"pflanzenfreund.tasks.weekly"
# 	]
# 	"monthly": [
# 		"pflanzenfreund.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "pflanzenfreund.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "pflanzenfreund.event.get_events"
# }

fixtures = ["Custom Field", "Custom Script"]