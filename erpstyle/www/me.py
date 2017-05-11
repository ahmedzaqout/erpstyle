# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import frappe.www.list

no_cache = 1
no_sitemap = 1

def get_context(context):
	
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)

	# m = frappe.db.sql("select email from tabUser ")
	# return context.m

	context.user_doc=frappe.get_doc('User',frappe.session.user)

    # print user_doc
    # print user_doc.user_type
    # print frappe.session.user
    # if user_doc.user_type == u'System User' and frappe.session.user !="Guest":
    #     context.forms = frappe.get_list("Web Form",fields=["*"],filters={"published":0"},ignore_permissions=True)
    # elif user_doc.user_type == u'Website User' and frappe.session.user !="Guest":
    #     context.forms = frappe.get_list("Web Form",fields=["*"],filters={"published":0},ignore_permissions=True)
