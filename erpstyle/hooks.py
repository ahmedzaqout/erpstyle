# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "erpstyle"
app_title = "style"
app_publisher = "style"
app_description = "style"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "style"
app_license = "MIT"

# Includes in <head>
# ------------------

website_context = {
	"favicon": 	"/assets/erpstyle/images/erpstyle.png",
	"splash_image": "/assets/erpstyle/images/erpstyle.png"
}

# Includes in <head>
# ------------------
app_include_css = ['/assets/erpstyle/css/desk.css',"/assets/erpstyle/css/nilighttheme.css"]
# include js, css files in header of desk.html
# app_include_css = "/assets/erpstyle/css/erpstyle.css"
# app_include_js = "/assets/erpstyle/js/erpstyle.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpstyle/css/erpstyle.css"
# web_include_js = "/assets/erpstyle/js/erpstyle.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "erpstyle.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "erpstyle.install.before_install"
# after_install = "erpstyle.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpstyle.notifications.get_notification_config"

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
# 		"erpstyle.tasks.all"
# 	],
# 	"daily": [
# 		"erpstyle.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpstyle.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpstyle.tasks.weekly"
# 	]
# 	"monthly": [
# 		"erpstyle.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "erpstyle.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpstyle.event.get_events"
# }

