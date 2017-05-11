from __future__ import unicode_literals
import frappe
from erpstyle.api import login_required



@login_required
def get_context(context):
    user_doc = frappe.get_doc('User', frappe.session.user)
    if user_doc.user_type == u'System User' and frappe.session.user != "Guest":
       forms = frappe.get_list("Web Form", fields=["*"], filters={"published": 1}, ignore_permissions=True)
       context.forms=forms;
    elif user_doc.user_type == u'Website User' and frappe.session.user != "Guest":
        forms = frappe.get_list("Web Form", fields=["*"], filters={"published": 1}, ignore_permissions=True)
        context.forms = forms;

    context.forms_number = len(forms)
