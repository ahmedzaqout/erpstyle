# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import unicode_literals, absolute_import
import frappe
import json
from email.utils import formataddr, parseaddr
from frappe.utils import (get_url, get_formatted_email, cint,
	validate_email_add, split_emails, time_diff_in_seconds)
from frappe.utils.file_manager import get_file
from frappe.email.queue import check_email_limit
from frappe.utils.scheduler import log
from frappe.email.email_body import get_message_id
import frappe.email.smtp
import MySQLdb
import time
from frappe import _
from frappe.utils.background_jobs import enqueue
import sys,socket


__version__ = '0.0.1'
file_directory = 'tanants.json'
recaptcha_public = '6LebQiAUAAAAAMdCLV_Axaw9v0Uye-UjjtoL0f9D'
recaptcha_private = '6LebQiAUAAAAACKGWK5ghguDFeagDHHUeqipxsdq'


#    single_data= { "name": name ,"email":email,'telephone':telephone, "status": 0 ,'activation_code':code}


@frappe.whitelist(allow_guest=True)
def _subscribe_email(data):
    #data = {"name": "ahmed", "email": "ahmedzaqout@outlook.com", 'telephone': "0599", "status": 0, 'activation_code': "123"}

    sender = frappe.get_site_config(frappe.local.sites_path)['sender_email']
    template="templates/email/subscribe.html"
    args = {
      'name':data['name'],
      'activation_code' :data['activation_code'],
      'title': _('اشتراك جديد')
      }

    # frappe.sendmail(
    #         recipients="ahmedzaqout@outlook.com",
    #         sender="login.live.ps.ps@gmail.com",
    #         subject="subject" or "New Message from " + "ahmed",
    #         message=frappe.get_template("templates/email/new_message.html").render({
    #             "from": "ahmed",
    #             "message": "message from def add_instance(name, email, telephone,code):",
    #             "link": get_url()
    #         }))



    # frappe.sendmail(recipients=data['email'], sender=sender, subject= _('اشتراك جديد'),
    # message=frappe.get_template(template).render(args))

    from frappe.email.smtp import get_default_outgoing_email_account
    email_account = get_default_outgoing_email_account(False)

    if email_account:
        frappe.sendmail(recipients=data['email'], subject=_("اشتراك جديد"),
                        message=frappe.get_template(template).render(args))

    return template

@frappe.whitelist(allow_guest=True)
def _send_email(args,recipients, type , template = None):
    sender = frappe.get_site_config(frappe.local.sites_path)['sender_email']
   # sender="login.live.ps.ps@gmail.com"
    template="templates/email/%s"%template if template else type
    from frappe.email.smtp import get_default_outgoing_email_account

    # frappe.sendmail(recipients="ahmedzaqout@outlook.com", sender=sender, subject=_('subscription_confirmation'),
    #                 message=frappe.get_template(template).render(args))


    email_account = get_default_outgoing_email_account(False)
    if email_account:
        frappe.sendmail(recipients=recipients, subject=_(type),
            message=frappe.get_template(template).render(args))


def site_url():
    return "%s:%s"%(frappe.get_site_config(frappe.local.sites_path)['site_url'],
    frappe.get_site_config(frappe.local.sites_path)['port'])

def site_url_without_port():
    return "%s"%frappe.get_site_config(frappe.local.sites_path)['site_url']

def get_mariadb_password():
    return frappe.get_site_config(frappe.local.sites_path)['maria_db']

def _get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

def assign_user(user_id, assigned_doctype , name, description):
    frappe.desk.form.assign_to.add({
        "assign_to": user_id,
        "doctype": assigned_doctype,
        "name": name,
        "description": description
    })


def has_role(allowed_for):

    def innerfn(fn):
        user = frappe.session.user
        if allowed_for not in frappe.get_roles(user):
            frappe.local.flags.redirect_location = "/desk"
            raise frappe.Redirect

        return fn

    return innerfn


def send_sms(to):
    from twilio.rest import TwilioRestClient

    account_sid = "ACce9b7b2aec5f2cf73848f6cf431f065a" # Your Account SID from www.twilio.com/console
    auth_token  = "dd3d939ae9c0ce5e5e9cd8bbd1435808"  # Your Auth Token from www.twilio.com/console

    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(body="Hello from Python",
        to=to,    # Replace with your phone number
        from_="+1 870-493-3580") # Replace with your Twilio number

    return message #message.sid



def notify(doctype ,name, workflow_state,recipients):
    print recipients
    # Owner
    # Department Manager if Exist
    # assignee
    import re
    for r in recipients:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", r):
            frappe.throw(_("Not valid email %s"%r))

    send_notify_mail(doctype ,name, workflow_state,recipients)

def send_notify_mail(doctype ,name, workflow_state ,recipients):
    # recipients = ['oashour9@gmail.com' for i in recipients]
    subject = doctype
    print "Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is "
    print doctype
    print "Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is Doctype is "

    data = {'doctype':doctype, 'name':name, 'state':workflow_state}
#    frappe.throw(data)
#    frappe.throw(recipients)
    frappe.sendmail(recipients=recipients, subject=doctype,
        message=frappe.get_template('templates/email/docstate_update.html').render(data))

#    _send_email(data, recipients, subject, 'docstate_update.html')
