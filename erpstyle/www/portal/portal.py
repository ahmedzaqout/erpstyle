import frappe
from frappe.model.db_schema import type_map
from erpstyle.api import login_required

@login_required
def get_context(context , args=None):
    args = frappe.local.form_dict
#   context.form = args.get("form")
    doc = args.get("doc")
    context.arg = doc
    webform = frappe.get_doc('Web Form',{"name":doc})
    doctype = webform.as_dict()['doc_type']
    context.columns = frappe.get_meta(doctype).get_list_fields()
    context.doc = doctype
    context.table = frappe.get_list(doctype,fields=context.columns, as_list=True, filters = {"owner":frappe.session.user} )
