from __future__ import unicode_literals
import frappe
from erpstyle.api import login_required

@login_required
def get_context(context):
    user_doc=frappe.get_doc('User',frappe.session.user)
    # print user_doc
    # print user_doc.user_type
    # print frappe.session.user
    if user_doc.user_type == u'System User' and frappe.session.user !="Guest":
        context.forms = frappe.get_list("Web Form",fields=["*"],filters={"published":1},ignore_permissions=True)
    elif user_doc.user_type == u'Website User' and frappe.session.user !="Guest":
        context.forms = frappe.get_list("Web Form",fields=["*"],filters={"published":0},ignore_permissions=True)

