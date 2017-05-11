# -*- coding: utf-8 -*-
import json,uuid,sys,erpstyle,os ,multiprocessing,frappe

import math

from frappe import _, _dict
from frappe.model.create_new import make_new_doc
from frappe.utils.data import cint
from recaptcha import RecaptchaClient
from recaptcha import RecaptchaUnreachableError
from recaptcha import RecaptchaException
from subprocess import Popen

from erpstyle import _subscribe_email
from erpstyle import _send_email
from erpstyle import _get_open_port
from erpstyle import site_url_without_port
from frappe.utils import getdate, nowdate, now_datetime, cstr
import json
from urllib import unquote



reload(sys)
sys.setdefaultencoding('utf-8')

@frappe.whitelist(allow_guest=True)
def get():
    # frappe.set_user_lang(frappe.session.user , "ar")
    user = frappe.get_doc('DocType',"Blog Category")
#    user = frappe.get_doc({"doctype", "Blog Category"})
    user.append_roles("Guest")
    user.save()
    return user

@frappe.whitelist(allow_guest=True)
def get_config():
    docs_config = frappe.get_module("erpstyle" + ".config.docs")
    return str(docs_config)#frappe._dict(frappe.get_site_config())


@frappe.whitelist(allow_guest=True)
def getEmployeesByDepartment(department):
	employees = frappe.get_list('Employee', fields=["name","employee_name"] , filters={'department' : department} )
	return employees

def validate_job_applicant(doc):
    return  True

@frappe.whitelist(allow_guest=False)
def save_job_applicant(doc):
    # dict = json.loads(frappe.form_dict.doc)
    userdoc = get_user_doc()
    dict  = json.loads(doc)

    dict['doctype'] = 'Job Applicant'
    is_new = True
    val = frappe.get_value('Job Applicant',{'email_id': userdoc.email}, ['name', 'modified'], as_dict=1)

    if val :
        is_new = False
        dict['name'] = val['name']
        dict['email_id']= userdoc.email
        dict['modified'] = cstr(val['modified'])

    jobApplicant = frappe.get_doc(dict)
    jobApplicant.email_id = userdoc.email
    jobApplicant.applicant_name = get_full_name(jobApplicant, 'ar');
    jobApplicant.applicant_name_english = get_full_name(jobApplicant, 'en')

    if not is_new:
        jobApplicant.application_date = jobApplicant.application_date_hijri = nowdate()
        jobApplicant.status = 'Open'

    # jobApplicant.modified = now_datetime()
    # print '================================================='
    # print jobApplicant.as_dict()
    # print '================================================='
    if not jobApplicant.applicant_name:
        jobApplicant.applicant_name='test'
    if not jobApplicant.applicant_name_english:
        jobApplicant.applicant_name_english='test'
    jobApplicant.validate()
    jobApplicant.save(ignore_permissions=True)

    return jobApplicant.as_dict(no_default_fields=1)

def get_full_name(jobApplicant, lang='ar'):
    ar = ['first_name', 'father_name', 'grandfather_name', 'last_name']
    en = ['first_name_english', 'father_name_english', 'grandfather_name_english', 'last_name_english']
    full_name = ''
    if lang == 'ar':
        if jobApplicant.first_name:
            full_name = jobApplicant.first_name + ' '
        if jobApplicant.father_name:
            full_name += jobApplicant.father_name + ' '
        if jobApplicant.grandfather_name:
            full_name += jobApplicant.grandfather_name + ' '
        if jobApplicant.last_name:
            full_name += jobApplicant.last_name + ' '


    elif lang == 'en':
        if jobApplicant.first_name_english:
            full_name = jobApplicant.first_name_english + ' '
        if jobApplicant.father_name_english:
            full_name += jobApplicant.father_name_english + ' '
        if jobApplicant.grandfather_name_english:
            full_name += jobApplicant.grandfather_name_english + ' '
        if jobApplicant.last_name_english:
            full_name += jobApplicant.last_name_english + ' '


    return full_name.strip()

def get_user_doc(user=None):
    user = frappe.session.user
    return frappe.get_doc('User', user)

def get_query_string(key, default=False, decode=0):
    query_string = frappe.request.query_string if hasattr(frappe.request, "query_string") \
        else frappe.local.flags.signed_query_string

    if query_string:
        segments = query_string.split("&" if '&' in query_string else ' ')

        for seg in segments:
            s = seg.split('=')
            if '=' in seg and s[0] == key:
                return unquote(s[1]) if decode else s[1]

    return default

def redirect_invalid_users(fn):
    def innerfn(context):
        user_doc = get_user_doc()
        print user_doc.user_type
        if user_doc.user_type == u'Website User':

            has_supplier = frappe.db.exists("Supplier", {"user": user_doc.name})
            if has_supplier:
                if not frappe.request.path.startswith("/c-portal/supplier_form"):
                    frappe.local.flags.redirect_location = "/c-portal/supplier_form"
                    raise frappe.Redirect




            else:
                job_applicant = get_job_applicant_doc()
                if not job_applicant and not frappe.request.path.startswith("/c-portal/edit_personal_data"):
                    frappe.local.flags.redirect_location = "/c-portal/edit_personal_data"
                    raise frappe.Redirect

                if job_applicant:
                    frappe.local.job_applicant = job_applicant

        else:
           frappe.local.flags.redirect_location = "/services"
           raise frappe.Redirect

        return fn(context)

    return innerfn

def login_required(fn):
    def innerfn(context):
        user_doc = get_user_doc()
        if user_doc.user_type != u'System User' or frappe.session.user == "Guest":
            frappe.local.flags.redirect_location = "/"
            raise frappe.Redirect

        return fn(context)


    return innerfn

def get_job_applicant_doc():
    job_applicant_name = get_job_applicant()
    if job_applicant_name:
        return frappe.get_doc('Job Applicant', job_applicant_name)

    return False

def get_job_applicant():
    userdoc = get_user_doc()
    return frappe.get_value('Job Applicant', {'email_id': userdoc.email}, 'name')

def website_user_home_page(user):
    return ''
    if frappe.session.user != 'Guest':
        user_doc = get_user_doc(user)
        if user_doc and user_doc.user_type == u'Website User':
            return '/home'
        return '/e-portal'
    else:
        return '/index'

def dict_to_html(dict):
    for key, value in dict.items():
        dict[key] = cstr(dict[key])

    return dict

def get_page_number():
    page = cint(get_query_string('page', 1))
    if page == 0:
        page = 1

    return page

class Pagination:
    def __init__(self, total_items_count, items_per_page=10):
        self.total_items_count = total_items_count
        self.items_per_page = items_per_page

        self.total_page_count = self.get_total_page_count()


    def get_total_page_count(self):
        return int(math.ceil(float(self.total_items_count) / self.items_per_page))


    def get_offset(self, page_number):
        return (page_number - 1) * self.items_per_page


    def html(self):
        if self.total_page_count:
            html = '<ul class="pagination">'
            for i in range(self.total_page_count):
                html += '<li><a href="?page={page}">{page}</a></li>'.format(page=i + 1)
            html += '</ul>'

            return html

        return ''

@frappe.whitelist()
def get_guardianship_type(category):
    doc = frappe.get_list("Guardianship Type", fields=["*"],filters={"guardianship_category": category})
    return doc

@frappe.whitelist()
def get_guardianship(type):
    doc = frappe.get_list('Guardianship', fields=["*"],filters={'guardianship_type':type})
    return doc

def dump(obj):
  for attr in dir(obj):
    print "obj.%s = %s" % (attr, getattr(obj, attr))

@frappe.whitelist(allow_guest=True)
def sign_up(email, full_name, user_type, redirect_to):
    # print 'r' * 50
    if not user_type or user_type not in ['Website User', 'Supplier User']:
        frappe.throw('Invalid user type')


    user = frappe.db.get("User", {"email": email})
    if user:
        if user.disabled:
            return _("Registered but disabled.")
        else:
            return _("Already Registered")
    else:
        if frappe.db.sql("""select count(*) from tabUser where
			HOUR(TIMEDIFF(CURRENT_TIMESTAMP, TIMESTAMP(modified)))=1""")[0][0] > 300:
            frappe.respond_as_web_page(_('Temperorily Disabled'),
                                       _(
                                           'Too many users signed up recently, so the registration is disabled. Please try back in an hour'),
                                       http_status_code=429)

        from frappe.utils import random_string
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": full_name,
            "enabled": 1,
            "new_password": random_string(10),
            "user_type": user_type
        })
        user.flags.ignore_permissions = True
        user.insert()

        if user_type == u"Supplier User":
            supplier = frappe.new_doc("Supplier");
            supplier.user = user.name
            supplier.flags.ignore_permissions = True
            supplier.insert()

        if redirect_to:
            frappe.cache().hset('redirect_after_login', user.name, redirect_to)

        if user.flags.email_sent:
            return _("Please check your email for verification")
        else:
            return _("Please ask your administrator to verify your sign-up")

def get_file(doctype, docname):
    import mimetypes
    from frappe.utils.file_manager import save_uploaded, get_uploaded_content, get_content_hash, \
        get_file_data_from_hash, \
        check_max_file_size
    fname, content = get_uploaded_content()
    content_hash = get_content_hash(content)
    file_data = get_file_data_from_hash(content_hash, is_private=1)
    content_type = mimetypes.guess_type(fname)[0]

    if not file_data:
        return False

    file_size = check_max_file_size(content)

    file_data.update({
        "doctype": "File",
        "attached_to_doctype": doctype,
        "attached_to_name": docname,
        "folder": '',
        "file_size": file_size,
        "content_hash": content_hash,
        "is_private": 1
    })

    f = frappe.get_doc(file_data)
    f.set_new_name()

    n_records = frappe.db.sql("""select file_url from `tabFile`
    	where content_hash=%s
    	and name!=%s
    	and attached_to_doctype=%s
    	and attached_to_name=%s""", (frappe.db.escape(f.content_hash), f.name, doctype,
                                     docname), as_dict=1)



    if len(n_records) > 0:
        return n_records[0]

@frappe.whitelist(allow_guest=True)
def get_logged_employee():
    user = get_user_doc()
    if user:
        return frappe.get_doc('Employee', {'user_id':user.name})

def extend_bootinfo(bootinfo):  
    employee = get_logged_employee()        
    bootinfo.employee = employee
    bootinfo.user.employee = employee

    if employee:
        frappe.local.employee = employee;

def get_department_manager(department):
    query = """select user.name as user_name, employee.name as employee_name from tabEmployee employee
                        Inner Join tabUserRole role on employee.user_id = role.parent
                        Inner Join tabUser user on employee.user_id = user.name
                        where role.role = 'Department Manager' and employee.department='{department}' LIMIT 1"""

    manager = frappe.db.sql(query.format(department=frappe.db.escape(department)), as_dict=1)
    print manager
    def has_manager():
        return True if manager and manager[0] else False

    def select(doctype):
        if has_manager():
            if doctype == 'User':
                return frappe.get_doc("User", manager[0].user_name)
            elif doctype == 'Employee':
                return frappe.get_doc("Employee", manager[0].employee_name)            


    return select

def get_head_of_department(department):
    dep_doc = frappe.get_doc("Department", department)

    def role_to_field(role):
        return role.lower().replace (" ", "_")

    def get_linked(doctype, role):                
        if dep_doc:
            role_field = role_to_field( role )
            if doctype == 'User':
                return frappe.get_doc("User", dep_doc.get(role_field) )
            elif doctype == 'Employee':
                return frappe.get_doc("Employee", {'user_id': dep_doc.get(role_field)})            


    return get_linked

def link_user_with_employee():
    print 'w'*50
    print 'w'*50
    print 'w'*50
    print session.user
    print 'w'*50

@frappe.whitelist(allow_guest=True)
def get_employee_roles(employee_name):
    from frappe import get_roles
    user_id = frappe.get_value("Employee", employee_name, "user_id")
    return get_roles(user_id)




def is_english(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def _generate_temp_password(length):
    if not isinstance(length, int) or length < 8:
        raise _("temp password must have positive length")


    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    from os import urandom
    return "".join([chars[ord(c) % len(chars)] for c in urandom(length)])

def _validate_instance(name, email, telephone):
    with open(erpstyle.file_directory) as json_file:
        json_data = json.load(json_file)
        data = json_data if not None else []

    needs = {'name':name , 'email':email ,'telephone':telephone}

    for key in needs.keys():
        try:
            needs[key].isalpha()
        except ValueError as e:
            #raise ("Not English" , key)
            raise ("اللغة ليست انجليزية", key)

        if needs[key] is None or not needs[key]:
            #raise ValueError(_("Field missing.."), key)
            raise ValueError(_("الحقول مفقودة..."), key)

        if needs[key].find(' ') != -1:
            #raise ValueError(_("{0} Must not has white space"), needs[key])
            raise ValueError(_("{0} لا يجب ان يحتوي علي فراغات"), needs[key])
    for key in needs.keys():
        if any(d[key] == needs[key] for d in data):
            #raise ValueError(_("{0} already in use."), needs[key])
            raise ValueError(_("{0} فعلا مستخدم ."), needs[key])

def _update_json_file(file , old ,new):
    with open(file) as f:
        data = json.load(f)
        for i in range(len(data)):
            if data[i]['name'] == old['name']:
                data[i] = new
                with open(erpstyle.file_directory, 'w') as outfile:
                    json.dump(data, outfile)
                    return "Done"
    return "Fail"

def _read_json_file(file_directory):
    with open(file_directory) as json_file:
        json_data = json.load(json_file)
        data = json_data if not None else []
    return data

@frappe.whitelist(allow_guest=True)
def add_instance(name, email, telephone):
    # , recaptcha_challenge_field = None, recaptcha_response_field = None
    # recaptcha_client = RecaptchaClient(public_key=erpstyle.recaptcha_public, private_key=erpstyle.recaptcha_private)
    # code = uuid.uuid4().hex
    #
    # try:
    #     is_solution_correct = recaptcha_client.is_solution_correct(
    #         recaptcha_response_field,
    #         recaptcha_challenge_field,
    #         erpstyle.site_url()
    #         )
    # except RecaptchaUnreachableError as exc:
    #     return _("Captcha Error")
    # except RecaptchaException as exc:
    #     return _("Captcha Error")
    # else:
    #     if not is_solution_correct:
    #         return _("Captcha Error")
    single_data= { "name": name ,"email":email,'telephone':telephone, "status": 0 ,'activation_code':uuid.uuid4().hex}
    try:
        _validate_instance(name,email,telephone)
    except ValueError as e:
        return str(e[0]).format(e[1])
    except Exception as e:
        return str("Error")

    with open(erpstyle.file_directory) as json_file:
        json_data = json.load(json_file)
        data = json_data if not None else []

        data.append(single_data)
        with open(erpstyle.file_directory, 'w') as outfile:
            json.dump(data, outfile)
    _subscribe_email(single_data)
    #return  { 'status' :1 , 'message': _("Please check your email and follow the activation process.") }
    return  { 'status' :1 , 'message': _("يرجى فتح بريدك الإلكتروني ومتابعة عملية التنشيط.") }
@frappe.whitelist(allow_guest=True)
def install_instance(code):

    data = _read_json_file(erpstyle.file_directory)

    target = None
    # return data
    for elem in data:
        if 'activation_code' in elem:
            print "%s %s"%(code,elem['activation_code'])

            if elem['activation_code'] == code:

                target = elem


                if 'port' in target or target['status'] == 1:
               #     return _("Installed before, please review your email.")
                    return _("مثبت من قبل , يرجى مراجعة البريد الإلكتروني الخاص بك.")



    if target:
        admin_password = _generate_temp_password(15)
        port = _get_open_port()
        new_target = target
        new_target['port'] = port
        new_target['activation_code'] = code
        new_target['admin_password'] = admin_password
        new_target['site_url']= erpstyle.site_url_without_port()
        _update_json_file(file=erpstyle.file_directory , new=new_target , old=target)


        # from frappe.email.smtp import get_default_outgoing_email_account
        # email_account = get_default_outgoing_email_account(False)
        # return  email_account
        #
        # _send_email(new_target,target['email'], 'Subscription Confirmation' ,'subscription_confirmation.html')
        #_send_email(new_target,target['email'], 'Subscription Confirmation' ,'subscription_confirmation.html')

        def r():
            import subprocess
            Process = Popen('../bashbosh.sh %s %s %s %s' % (target['name'] ,erpstyle.get_mariadb_password(), admin_password ,str(port),), shell=True)

            #os.system("../bashbosh.sh %s %s %s %s"%(target['name'] ,erpstyle.get_mariadb_password(), admin_password ,str(port)))
            new_target['status'] = 1
            _update_json_file(file=erpstyle.file_directory , new=new_target , old=target)
            print "%s Must be run"%target['name']

        p = multiprocessing.Process(target= r , args=())
        p.start()
        p.join()



        #_send_email(new_target,target['email'], 'Subscription Confirmation' ,'subscription_confirmation.html')
        _send_email(new_target,target['email'], 'تأكيد الاشتراك' ,'subscription_confirmation.html')

    else:
        #return _('Unkown request, If you want to own your system click <a href="/login_erp" > here </a>.')
        return _('طلب غير معروف , اذا كنت تمتلك هذا الحساب اضغط هنا  <a href="/login_erp" > here </a>.')

    return _("سوف تتلقى رسالة بريد إلكتروني مع تفاصيل تسجيل الدخول.")
    #return _("You will receive an email with login details.")

@frappe.whitelist(allow_guest=True)
def test():
    return frappe.get_site_config(frappe.local.sites_path)['maria_db']

@frappe.whitelist(allow_guest=True)
def test2():
    from frappe.email.smtp import get_default_outgoing_email_account


    email_account = get_default_outgoing_email_account(False)

    frappe.sendmail(
        recipients="ahmedzaqout@outlook.com",
        sender="login.live.ps.ps@gmail.com",
        subject="subject" or "New Message from " + "ahmed",
        message=frappe.get_template("templates/emails/new_message.html").render({
            "from": "ahmed",
            "message": "message from ahmed 11:07 AM",
            "link": "http://namegithub.com"
        }))
    return  email_account