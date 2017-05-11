import frappe

def get_context(context , args=None):

    args = frappe.local.form_dict
    context.args = args.get("code")