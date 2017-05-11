# -*- coding: utf-8 -*-
import frappe
from erpstyle.api import get_user_doc, login_required
from frappe import _
from frappe.utils import get_last_day, cint
from datetime import date

@login_required
def get_context(context):

    employee = get_employee()
    if employee and 'Department Manager' in frappe.get_roles(frappe.session.user):
        days = [{'name':'' , 'title':'اختر يوم'}]
        for i in range(1 ,31):
            days.append({'name':i, 'title': i})

        months = [
                {'name':'', 'title': 'اختر الشهر'},
                {'name':'1', 'title': 'Jan'},
                {'name':'2', 'title': 'Feb'},
                {'name':'3', 'title': 'Mar'},
                {'name':'4', 'title': 'Apr'},
                {'name':'5', 'title': 'May'},
                {'name':'6', 'title': 'Jun'},
                {'name':'7', 'title': 'Jul'},
                {'name':'8', 'title': 'Aug'},
                {'name':'9', 'title': 'Sep'},
                {'name':'10', 'title': 'Oct'},
                {'name':'11', 'title': 'Nov'},
                {'name':'12', 'title': 'Dec'}
            ]
        filters = [
            {'key':'day' , 'name':_('Day') , 'values':days},
            {'key':'month' , 'name':_('Month') , 'values':months},
            {'key':'fiscal_year_name', 'name' : _('Select Fiscal Year') ,'values': get_company_fiscal_years(employee.company)}
        ]
        context.filters = filters


@frappe.whitelist()
def get_data(employee_name=None):
    args = frappe.local.form_dict

    fiscal_year = get_fiscal_year(args.fiscal_year_name)

    start_date = fiscal_year.year_start_date
    end_date = get_last_day(date(cint(fiscal_year.year), cint(12),  01))
    result = {}
    if args.month:
        _day = int(args.day) if args.day else 01

        start_date = date(cint(fiscal_year.year), cint(args.month),  _day)
        if args.day:
            end_date = start_date
        else:
            end_date = get_last_day(start_date)
    result = {}
    if 'Department Manager' in frappe.get_roles(frappe.session.user) and not employee_name:
        department = frappe.get_doc('Employee', {'user_id': frappe.session.user}).department

        result['الإجازات'] = get_doctype_total_by_department('tabLeave Application' , 'leave_type', department,'from_date','to_date' ,end_date, start_date ,"and `tabLeave Application`.`status` = 'Approved'")
        result['الحضور'] = get_doctype_total_by_department('tabAttendance','status',department,'att_date','att_date', end_date, start_date)
        result['الاستئذانات'] = get_doctype_total_by_department('tabPermission Application','permission_type',department,'permission_date','permission_date', end_date, start_date)
        result['الانتداب'] = get_doctype_requests_by_workflow_department_total('tabJob Assignment','assignment_type',department,'from_date','to_date', end_date, start_date)
        result['المقابلات'] = get_interview_by_department_total(department, end_date, start_date)
    return result


def get_doctype_requests_by_workflow_department_total(doctype, status , department,from_date , to_date , end_period_date, start_period_date , extra_where = ""):

    query = """
        SELECT count(*) , `%s` FROM `%s` join (select name from `tabEmployee` where department = '%s') as employees on
        `%s`.employee = employees.name
        WHERE
         ( ( %s >= '%s' AND %s <= '%s' ) OR ( %s >= '%s' AND %s <= '%s') )
        group by `%s`
      """

    q = query%(status,
                doctype,
                department,
                doctype,
                from_date,
                start_period_date,
                to_date,
                end_period_date,
                to_date,
                end_period_date,
                from_date,
                start_period_date,
                status,
                )
    print q
    att_days = frappe.db.sql(q)
#    print query%(query%(status,doctype,department,doctype,doctype,status, start_period_date,end_period_date,start_period_date,end_period_date))
    return att_days #query%(department, start_period_date, end_period_date)

def get_interview_by_department_total(department, end_period_date, start_period_date):

    query = """
        SELECT count(*) , 'Count' FROM `tabInterview`
        WHERE
        department = '%s' AND
         ( (start_date>= '%s' AND end_date<= '%s' ) OR ( end_date >= '%s' AND start_date <= '%s') )

      """

    q = query%(department,
                start_period_date,
                end_period_date,
                end_period_date,
                start_period_date,
                )
    print q
    att_days = frappe.db.sql(q)
#    print query%(query%(status,doctype,department,doctype,doctype,status, start_period_date,end_period_date,start_period_date,end_period_date))
    return att_days #query%(department, start_period_date, end_period_date)


def get_doctype_total_by_department(doctype, status , department,from_date , to_date , end_period_date, start_period_date , extra_where = ""):

    query = """
        SELECT count(*) , `%s`.`%s` FROM `%s` join `tabEmployee` on
        `%s`.employee = `tabEmployee`.name
        where
        `tabEmployee`.department = '%s'
        and `%s`.`docstatus` = 1
        %s
        and ( ( %s >= '%s' AND %s <= '%s' ) OR ( %s >= '%s' AND %s <= '%s') )
        group by `%s`.`%s`
    """
    print query%(doctype,
                                    status,
                                    doctype,
                                    doctype,
                                    department,
                                    doctype,
                                    extra_where,
                                    from_date,
                                    start_period_date,
                                    to_date,
                                    end_period_date,
                                    to_date,
                                    end_period_date,
                                    from_date,
                                    start_period_date,
                                    doctype,
                                    status)
    att_days = frappe.db.sql(query%(doctype,
                                    status,
                                    doctype,
                                    doctype,
                                    department,
                                    doctype,
                                    extra_where,
                                    from_date,
                                    start_period_date,
                                    to_date,
                                    end_period_date,
                                    to_date,
                                    end_period_date,
                                    from_date,
                                    start_period_date,
                                    doctype,
                                    status))
#    print query%(query%(status,doctype,department,doctype,doctype,status, start_period_date,end_period_date,start_period_date,end_period_date))
    return att_days #query%(department, start_period_date, end_period_date)



def get_company_fiscal_years(company):
    # query = """SELECT fis.name FROM `tabFiscal Year` fis INNER JOIN `tabFiscal Year Company` cmp
    #            ON fis.name=cmp.parent WHERE cmp.company='%s' ORDER BY fis.year DESC"""

    query = """SELECT fis.name FROM `tabFiscal Year` fis ORDER BY fis.year DESC"""
    # print query%(holiday_name, start_period_date, end_period_date)
    fiscal_years = frappe.db.sql(query, as_dict=1)

    return fiscal_years

def get_employee(employee_name=None):
    if not employee_name:
        user_doc = get_user_doc()
        employee_name = frappe.get_value('Employee', {'user_id': user_doc.name}, 'name')
    return frappe.get_doc('Employee', employee_name) if employee_name else None

def get_fiscal_year(fiscal_year_name=None):
    if not fiscal_year_name:
        fiscal_year_name = frappe.db.get_single_value("Global Defaults", "current_fiscal_year")
    return frappe.get_doc('Fiscal Year', fiscal_year_name)
