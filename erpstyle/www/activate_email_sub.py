import frappe
import json,socket
from erpstyle import _send_email

def get_context(context , args=None):
    args = frappe.local.form_dict
    context.args = args.get("code")
