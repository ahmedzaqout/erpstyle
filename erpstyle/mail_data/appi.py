# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe,uuid
from frappe import throw, _
import frappe.defaults
import frappe.utils, markdown2
from frappe.website.render import clear_cache
import mailchimp3
from mailchimp3 import MailChimp


@frappe.whitelist(allow_guest=True)
def add_lead(lead_name, email_id , Lead_phone,subject,description,category,priority):
    Lead_exist = frappe.get_list("Lead", fields=["lead_name","email_id"]
    , filters = {"email_id":email_id},ignore_permissions=True)

    if Lead_exist!=[] :
        issue =frappe.get_doc({'doctype': "Issue", "subject": subject,"description":description
        ,"status":"Open","raised_by":email_id,"lead":Lead_exist[0].name,"priority":priority})
        issue.flags.ignore_permissions = True
        issue.insert()
    else:
        lead =frappe.get_doc({'doctype': "Lead", "lead_name": lead_name,"email_id":email_id
        ,"status":"Open","source":"Website","phone":Lead_phone,"category":category})
        lead.flags.ignore_permissions = True
        responed =  lead.insert()
        issue =frappe.get_doc({'doctype': "Issue", "subject": subject,"description":description
        ,"status":"Open","raised_by":email_id,"lead":lead.name,"priority":priority})
        issue.flags.ignore_permissions = True
        issue.insert()

    return _("Lead added successfully")

@frappe.whitelist(allow_guest=True)
def add_Issue(user_name, raised_by_email_id , user_phone,subject,description,category,priority):
    Issue_exist = frappe.get_list("Issue", fields=["raised_by,name"]
    , filters = {"raised_by":raised_by_email_id},ignore_permissions=True)

    if category =="Sales":
        Details = "\""+subject+"\""+"\n\n"+description+"\n\n"
        lead =frappe.get_doc({'doctype': "Lead", "lead_name": user_name,"email_id":raised_by_email_id
        ,"status":"Open","source":"Website","phone":user_phone,"details":Details})
        lead.flags.ignore_permissions = True
        responed =  lead.insert()
    else :
        issue =frappe.get_doc({'doctype': "Issue", "subject": subject,"description":description +"\n"+user_phone
        ,"status":"Open","raised_by":raised_by_email_id,"user_name":user_name,"priority":priority,"category":category})
        issue.flags.ignore_permissions = True
        issue.insert()

    return _("Issue added successfully")


@frappe.whitelist(allow_guest=True)
def get_lead_category(name,key):
    client = MailChimp(name, key)
    # returns the list matching id '123456'
    # add John Doe with email john.doe@example.com to list matching id '123456'
    return client.campaign.send(campaign_id='7fc1f1efe8')



@frappe.whitelist(allow_guest=True)
def get_leads():
    records = [
    {'doctype': 'Leave Type',"modified_by":"Administrator", 'leave_type_name': _(u'Normal vacation'), 'name': _(u'Normal vacation'),
    'is_encash': 1, 'is_carry_forward': 1, 'max_days_allowed': '21', 'include_holiday': 1},
	{'doctype': 'Leave Type',"modified_by":"Administrator", 'leave_type_name': _(u'Eid vacation'), 'name': _(u'Eid vacation'),
    'is_encash': 1, 'is_carry_forward': 0, 'max_days_allowed': '8', 'include_holiday': 0},
	{'doctype': 'Leave Type',"modified_by":"Administrator", 'leave_type_name': _(u'Special leave'), 'name': _(u'Special leave'),
    'is_encash': 1, 'is_carry_forward': 0, 'max_days_allowed': '15', 'include_holiday': 1},
	{'doctype': 'Leave Type',"modified_by":"Administrator", 'leave_type_name': _(u'Of necessity leave'), 'name': _(u'Of necessity leave'),
    'is_encash': 0, 'is_carry_forward': 0, 'max_days_allowed': '60', 'include_holiday': 0}
	,
	{'doctype': 'Leave Type',"modified_by":"Administrator", 'leave_type_name': _(u'Sick leave'), 'name': _(u'Sick leave'),
    'is_encash': 1, 'is_carry_forward': 0, 'max_days_allowed': '180', 'include_holiday': 0}
	,
	{'doctype': 'Leave Type',"modified_by":"Administrator", 'leave_type_name': _(u'Haj Vacation'), 'name': _(u'Haj Vacation'),
    'is_encash': 1, 'is_carry_forward': 0, 'max_days_allowed': '15', 'include_holiday': 0}
	,
	{'doctype': 'Leave Type',"modified_by":"Administrator", 'leave_type_name': _(u'Exam study leave'), 'name': _(u'Exam study leave'),
    'is_encash': 0, 'is_carry_forward': 0, 'max_days_allowed': '15', 'include_holiday': 0}
            ]
    frappe.db.sql("""delete from `tabLeave Type`""")
    frappe.db.commit();
    from frappe.modules import scrub
    for r in records:
        doc = frappe.new_doc(r.get("doctype"))
        doc.update(r)
        # ignore mandatory for root
        parent_link_field = ("parent_" + scrub(doc.doctype))
        if doc.meta.get_field(parent_link_field) and not doc.get(parent_link_field):
            doc.flags.ignore_mandatory = True
        try:
            doc.insert(ignore_permissions=True)
        except frappe.DuplicateEntryError, e:
            # pass DuplicateEntryError and continue
            if e.args and e.args[0]==doc.doctype and e.args[1]==doc.name:
                # make sure DuplicateEntryError is for the exact same doc and not a related doc
                pass
            else:
                raise
    return "Finfished"
@frappe.whitelist(allow_guest=True)
def Blog_category_grant_perm():
    perm = frappe.get_doc({
		"doctype":"DocPerm",
		"parent": "Blog Category",
		"parenttype": "DocType",
		"parentfield": "permissions",
		"role": "Guest",
		"permlevel": 0,
		"read": 1
	})
    perm.flags.ignore_permissions = True
    perm.insert()
    validate_and_reset("Blog Category")

    return frappe.get_list("DocPerm",filters = {"parent":"Blog Category"}, fields=["*"],ignore_permissions=True)


def validate_and_reset(doctype, for_remove=False):
	from frappe.core.doctype.doctype.doctype import validate_permissions_for_doctype
	validate_permissions_for_doctype(doctype, for_remove)
	clear_doctype_cache(doctype)

def clear_doctype_cache(doctype):
	frappe.clear_cache(doctype=doctype)
	for user in frappe.db.sql_list("""select distinct tabUserRole.parent from tabUserRole, tabDocPerm
		where tabDocPerm.parent = %s
		and tabDocPerm.role = tabUserRole.role""", doctype):
		frappe.clear_cache(user=user)

@frappe.whitelist(allow_guest=True)
def add_mail(email):
    return
    mail_exist = frappe.get_list("Mail List", fields=["*"]
    , filters = {"email":email},ignore_permissions=True)

    if  mail_exist!=[]:
        for m in mail_exist:
			frappe.delete_doc("Mail List", m["name"])

    code=  uuid.uuid4().hex
    mail =frappe.get_doc({'doctype': "Mail List","email":email,"uuid":code})
    mail.flags.ignore_permissions =True
    responed =  mail.insert()

    sender = frappe.get_site_config(frappe.local.sites_path)['sender_email']
    template="templates/email/subscribe_email.html"
    args = {
      'name':email,
      'title': _('New Subscribe'),
      'code':code
      }
    frappe.sendmail(recipients=email, sender=sender, subject=_('New Subscribe'),
        message=frappe.get_template(template).render(args))


    return  _("Mail added successfully")
@frappe.whitelist(allow_guest=True)
def activate_mail(code):
    sender = 'mesa_safd@hotmail.com'
    # sender = frappe.db.get_value("User", frappe.session.user, "email")
    frappe.sendmail(recipients='mesa_safd@hotmail.com',sender=sender, subject=_('Confirmation Mail'),
                    message='HELLO')

    # mail_exist = frappe.get_list("Mail List", fields=["*"]
    # , filters = {"uuid":code},ignore_permissions=True)
    # print ("mail_exist ",mail_exist)
    # if  mail_exist==[]:
    #     print ("mail_exist empty ",mail_exist)
    #     return _("Email not exist")
    #
    # news_list_list = frappe.get_list("Newsletter List", fields=["*"]
    # , filters = {"name":"Website_Subscribers"},ignore_permissions=True)
    #
    #
    # if  len(news_list_list) ==0:
    #     Website_Subscribers =frappe.get_doc({'doctype': "Newsletter List","title":"Website_Subscribers"})
    #     Website_Subscribers.flags.ignore_permissions = True
    #     Website_Subscribers.insert()
    # else :
    #     Website_Subscribers= news_list_list[0]
    #
    # print "/////////////////////////////////"
    # print Website_Subscribers
    # print "/////////////////////////////////"
    #
    # Subscriber =frappe.get_doc({'doctype': "Newsletter List Subscriber","newsletter_list":Website_Subscribers.get("name")
    # ,"email":mail_exist[0]["email"]})
    # Subscriber.flags.ignore_permissions = True
    # Subscriber.insert()
    # for m in mail_exist:
		# frappe.delete_doc("Mail List", m["name"])

    return _("Account Activated successfully")











@frappe.whitelist(allow_guest=True)
def add_comment(args=None):
	"""
		args = {
			'comment': '',
			'comment_by': '',
			'comment_by_fullname': '',
			'reference_doctype': '',
			'reference_name': '',
			'page_name': '',
		}
	"""

	if not args:
		args = frappe.local.form_dict

	page_name = args.get("page_name")

	doc = frappe.get_doc(args["reference_doctype"], args["reference_name"])
	comment = doc.add_comment("Comment", args["comment"], comment_by=args["comment_by"])
	comment.flags.ignore_permissions = True
	comment.sender_full_name = args["comment_by_fullname"]
	comment.save()

	# since comments are embedded in the page, clear the web cache
	clear_cache(page_name)

	# notify commentors
	commentors = [d[0] for d in frappe.db.sql("""select sender from `tabCommunication`
		where
			communication_type = 'Comment' and comment_type = 'Comment'
			and reference_doctype=%s
			and reference_name=%s""", (comment.reference_doctype, comment.reference_name))]

	owner = frappe.db.get_value(doc.doctype, doc.name, "owner")
	recipients = list(set(commentors if owner=="Administrator" else (commentors + [owner])))

	message = _("{0} by {1}").format(markdown2.markdown(args.get("comment")), comment.sender_full_name)
	message += "<p><a href='{0}/{1}' style='font-size: 80%'>{2}</a></p>".format(frappe.utils.get_request_site_address(),
		page_name, _("View it in your browser"))



	template = frappe.get_template("templates/includes/comments/comment.html")

	return template.render({"comment": comment.as_dict()})



def validate_not_mobile(value):

    rule = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')

    if rule.search(value):
        return false
    else:
        return true
