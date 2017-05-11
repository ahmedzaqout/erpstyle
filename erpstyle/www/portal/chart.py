#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, date

from erpnext.hr.doctype.leave_application.leave_application import get_number_of_leave_days, \
    get_approved_leaves_for_period
from erpstyle.api import get_user_doc, login_required
import frappe
from frappe.utils import nowdate, date_diff, getdate, get_last_day, cint
from frappe import _

@login_required
def get_context(context):
    args = frappe.local.form_dict
    chart_type = args.get("type")
    context.chart_type = chart_type
    filters = []

    employee = get_employee()
    print '-------------------------------------------------------------'
    if not employee:
        frappe.throw("The user {} is not has Employee Doc".format(frappe.session.user))
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


    if chart_type == "leave":
        filters = [
            {'key':'fiscal_year_name', 'name' : _('Select Fiscal Year') ,'values': get_company_fiscal_years(employee.company)},
            {'key':'leave_type', 'name' : _('Leave Type') , 'values':get_leave_types()},
            {'key':'month' , 'name':_('Month') , 'values':months},
            {'key':'day' , 'name':_('day') , 'values':days}
        ]
    elif chart_type == "permission":
        filters = [
            {'key':'month' , 'name':_('Month') , 'values':months},
            {'key':'day' , 'name':_('Day') , 'values':days}
        ]
    elif chart_type == "persistence":
        filters = [
            {'key':'fiscal_year_name', 'name' : _('Select Fiscal Year') ,'values': get_company_fiscal_years(employee.company)},
            {'key':'month' , 'name':_('Month') , 'values':months},
            {'key':'day' , 'name':_('Day') , 'values':days}

        ]

    context.filters = filters
    if u'System Manager' in frappe.get_roles():
        context.employees = frappe.get_list('Employee',fields={'name','employee_name'})
        context.is_system_manager = 1


@frappe.whitelist()
def get_data(employee_name=None):
    args = frappe.local.form_dict
    if args.chart_type == "leave":
        return get_leaves_data(args.fiscal_year_name, args.leave_type, employee_name,args.month,args.day)
    elif args.chart_type == "permission":
        return get_permission_data(employee_name)
    elif args.chart_type == "persistence":
        return get_persistence_data(args.fiscal_year_name, employee_name, args.month,args.day)

#    chart_type = args.get("type")

def get_leaves_data(fiscal_year_name, leave_type, employee_name=None, month = None , day = None):
    fiscal_year = get_fiscal_year(fiscal_year_name)

    start_date = fiscal_year.year_start_date
    end_date = getdate("2016-12-31")

    result = {}
    if month:
        _day = int(day) if day else 01

        start_date = date(cint(fiscal_year.year), cint(month),  _day)
        if day:
            end_date = start_date
        else:
            end_date = get_last_day(start_date)

    days_ago = date_diff(end_date, start_date)
    if 'Department Manager' in frappe.get_roles(frappe.session.user) and not employee_name:
        department = frappe.get_doc('Employee', {'user_id': frappe.session.user}).department

        generals = get_leave_days_by_department(department, end_date, start_date, leave_type)
        result['total'] = get_leave_days_by_department_total(department, end_date, start_date, leave_type)
        approved_leaves = generals['Leave']
        leave_days_number = generals['All']
    else:
        employee = get_employee(employee_name)
        leave_days_number = get_leave_allocation_number(leave_type, fiscal_year.year_start_date, fiscal_year.year_end_date,employee.name)
        approved_leaves = get_approved_leaves_for_period(employee.name, leave_type, fiscal_year.year_start_date, fiscal_year.year_end_date)

    if leave_days_number == None:
        leave_days_number = 0
    if approved_leaves == None:
        approved_leaves = 0

    result['stats'] = [
        {'name': 'الرصيد', 'value': leave_days_number-approved_leaves},
        {'name': 'ايام الاجازات', 'value': approved_leaves}
    ]
    return frappe.as_json(result)

def get_permission_data(employee_name=None):
    fiscal_year = get_fiscal_year()
    result = {}
    if 'Department Manager' in frappe.get_roles(frappe.session.user) and not employee_name:
        department = frappe.get_doc('Employee', {'user_id': frappe.session.user}).department
        perms_number = get_permission_number_department(department, fiscal_year.year_start_date, fiscal_year.year_end_date)
    else:
        employee = get_employee(employee_name)
        perms_number = get_permission_number(employee.name, fiscal_year.year_start_date, fiscal_year.year_end_date)
#        company_work_days= days_ago - holidays

    data = [
       {'name': 'ايام الحضور', 'value': perms_number[0]},
       {'name': 'الاستئذانات', 'value': perms_number[1]}
    ]
    result['stats'] = data

    return frappe.as_json(result)

def get_persistence_data(fiscal_year_name, employee_name=None, month=None , day=None):
    fiscal_year = get_fiscal_year(frappe.db.escape(fiscal_year_name))
    start_date = fiscal_year.year_start_date
    end_date = nowdate()
    result = {}
    if month:
        _day = int(day) if day else 01

        start_date = date(cint(fiscal_year.year), cint(month),  _day)
        if day:
            end_date = start_date
        else:
            end_date = get_last_day(start_date)

    if 'Department Manager' in frappe.get_roles(frappe.session.user) and not employee_name:
        department = frappe.get_doc('Employee', {'user_id': frappe.session.user}).department
        print end_date, start_date
        attendance_days = get_attendance_days_by_department(department, end_date, start_date)

    else:
        employee = get_employee(employee_name)
        holidays = get_holidays(employee.holiday_list, end_date, start_date)
        attendance_days = get_attendance_days(employee.name, end_date, start_date)
#        company_work_days= days_ago - holidays

    result['stats'] = []
    for d in attendance_days:
        result['stats'].append({'name': _(d[1]) , 'value':d[0]})
    return frappe.as_json(result)



def get_leave_types():
    return frappe.get_list('Leave Type', fields=["leave_type_name","name"])

def get_employee(employee_name=None):
    if not employee_name:
        user_doc = get_user_doc()
        employee_name = frappe.get_value('Employee', {'user_id': user_doc.name}, 'name')
    return frappe.get_doc('Employee', employee_name) if employee_name else None


def get_fiscal_year(fiscal_year_name=None):
    if not fiscal_year_name:
        fiscal_year_name = frappe.db.get_single_value("Global Defaults", "current_fiscal_year")
    return frappe.get_doc('Fiscal Year', fiscal_year_name)

def get_company_fiscal_years(company):
    # query = """SELECT fis.name FROM `tabFiscal Year` fis INNER JOIN `tabFiscal Year Company` cmp
    #            ON fis.name=cmp.parent WHERE cmp.company='%s' ORDER BY fis.year DESC"""

    query = """SELECT fis.name FROM `tabFiscal Year` fis ORDER BY fis.year DESC"""
    # print query%(holiday_name, start_period_date, end_period_date)
    fiscal_years = frappe.db.sql(query, as_dict=1)
    return fiscal_years

def get_leave_allocation_number(leave_type, from_date, to_date ,employee=None):

    query = """select sum(total_leaves_allocated)
                from `tabLeave Allocation`
                where
                leave_type ='{leave_type}' and
                ( ( from_date >= '{from_date}' AND to_date <= '{to_date}' ) OR ( to_date >= '{to_date}' AND from_date <= '{from_date}') )
                and docstatus=1
              """.format(leave_type=leave_type, from_date=from_date, to_date=to_date)

    if employee:
        query += " and employee= '%s' " % employee

    print query

    leave_allocation_record = frappe.db.sql(query)

    return leave_allocation_record[0][0]

def get_permission_number(employee, start_date, end_date):
    q = """
    select * from
    (select count(*) as present from `tabAttendance`
    where
    employee='{employee}' and
    status = 'Present' and
    att_date >='{from_date}' and
    att_date<='{to_date}' and
    docstatus = 1) as att,
    (select count(*) as permession from `tabPermission Application`
    where
    employee='{employee}' and
    permission_date >='{from_date}' and
    permission_date<='{to_date}' and
    docstatus = 1) as perm
    """.format(employee=employee , from_date = start_date , to_date = end_date)

    print q
    perms_number = frappe.db.sql(q)

    return perms_number[0]


def get_permission_number_department(department, start_date, end_date):
    q = """
    select * from
    (select count(*) as present from `tabAttendance` , `tabEmployee`
    where
    `tabAttendance`.employee = `tabEmployee`.name and
    `tabEmployee`.department = '{department}' and
    `tabAttendance`.status = 'Present' and
    att_date >='{from_date}' and
    att_date<='{to_date}' and
    `tabAttendance`.docstatus = 1) as att,
    (select count(*) as permession from `tabPermission Application`, `tabEmployee`
    where
    `tabEmployee`.name = `tabPermission Application`.employee and
    `tabEmployee`.department = '{department}' and
    permission_date >='{from_date}' and
    permission_date<='{to_date}' and
    `tabPermission Application`.docstatus = 1) as perm
    """.format(department=department, from_date = start_date , to_date = end_date)

    print q
    perms_number = frappe.db.sql(q)

    return perms_number[0]

def get_holidays(holiday_name, end_period_date, start_period_date):
    query = """SELECT count(*) FROM tabHoliday WHERE parent='%s' AND holiday_date>='%s' AND holiday_date<='%s'"""
    # print query%(holiday_name, start_period_date, end_period_date)
    holidays = frappe.db.sql(query%(holiday_name, start_period_date, end_period_date))

    return holidays[0][0]
    # cnt = frappe.db.count('Holiday', filters=[['Holiday','parent', '=', holiday_name],
    #                             ['Holiday', 'holiday_date', '>=', start_period_date],
    #                             ['Holiday', 'holiday_date', '<=', end_period_date]])
    #
    #
    # return cnt

def get_attendance_days(employee, end_period_date, start_period_date):
    query = """
SELECT count(*) , status
FROM `tabAttendance`
WHERE
employee='{employee}'
and docstatus =1
and att_date>='{from_date}' AND att_date<='{to_date}'
group by status
"""
    # print query%(holiday_name, start_period_date, end_period_date)
    q = query.format(employee=employee ,from_date = start_period_date , to_date = end_period_date )
    print q
    att_days = frappe.db.sql(q)
    return att_days

def get_attendance_days_by_department(department, end_period_date, start_period_date):
    query = """
    select count(*) , `tabAttendance`.status from
    `tabAttendance` , `tabEmployee`
    where
    `tabAttendance`.docstatus = 1 and
    `tabEmployee`.name =`tabAttendance`.employee and
    `tabEmployee`.department = '{department}' and
    `tabAttendance`.att_date >= '{from_date}' AND `tabAttendance`.att_date <= '{to_date}'
    group by `tabAttendance`.status
    """
    q = query.format(department=department , from_date=start_period_date , to_date=end_period_date)

    att_days = frappe.db.sql(q)
    return att_days
#    print query%(department,department, start_period_date, end_period_date)
#    return result#query%(department, start_period_date, end_period_date)

def get_leave_days_by_department_total(department, end_period_date, start_period_date , type = None ):

    query = """
        SELECT count(*) , `leave_type` FROM `tabLeave Application` join `tabEmployee` on
        `tabLeave Application`.employee = `tabEmployee`.name
        where
        `tabEmployee`.department = '%s'
        and `tabLeave Application`.`docstatus` = 1
        and `tabLeave Application`.`status` = 'Approved'
        and ( ( from_date >= '%s' AND to_date <= '%s' ) OR ( to_date >= '%s' AND from_date <= '%s') )
        group by `leave_type`
    """

    att_days = frappe.db.sql(query%(department , start_period_date,end_period_date,start_period_date,end_period_date))

    print query%(department , start_period_date,end_period_date,start_period_date,end_period_date)

    return att_days #query%(department, start_period_date, end_period_date)

def get_leave_days_by_department(department, end_period_date, start_period_date , type = None ):

    query = """
select * from (select IFNULL(sum(total_leave_days),0) as leaves
from `tabLeave Application` ,  tabEmployee
where
`tabEmployee`.name = `tabLeave Application`.employee
and `tabEmployee`.department ='{department}'
and`tabLeave Application`.docstatus =1
and `tabLeave Application`.status = 'Approved'
and ( ( `tabLeave Application`.from_date >= '{from_date}' AND `tabLeave Application`.to_date <= '{to_date}' ) OR ( `tabLeave Application`.to_date >= '{to_date}' AND `tabLeave Application`.from_date <= '{from_date}') )
and `tabLeave Application`.leave_type = '{type}') as total_leavs ,

(SELECT IFNULL(sum( `total_leaves_allocated`),0) as allocated

FROM `tabLeave Allocation`,`tabEmployee`

WHERE
`tabLeave Allocation`.employee = `tabEmployee`.name and
`tabLeave Allocation`.leave_type = '{type}' and
`tabEmployee`.department = '{department}' and
`tabLeave Allocation`.docstatus = 1
) as leaves_allocated
"""

    sql_query = query.format(department=department,from_date=start_period_date , to_date=end_period_date , type=type)

    att_days = frappe.db.sql(sql_query)

    result = {
        'Leave':att_days[0][0],
        'All':att_days[0][1]
    }
    return result#query%(department, start_period_date, end_period_date)