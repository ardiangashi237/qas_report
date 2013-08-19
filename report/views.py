from django.shortcuts import render_to_response, redirect
from django.template import Context, loader
from django.template.context import RequestContext
from django.http import HttpResponse
from httplib2 import Http
from urllib import urlencode
import json,ast
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import requires_csrf_token
from django.utils import simplejson
from operator import itemgetter
from django import template
import csv
from django.http import HttpResponse
from django import forms
import cgi
from datetime import datetime, timedelta
from datetime import date

register = template.Library()

import datetime

def call_api(parameter, login=False):
    if login is True:
        url = "http://%s/resource/qaslogin.cgi" % settings.SERVER_HOSTNAME
    else:
        url = "http://%s/resource/apireporting.cgi" % settings.SERVER_HOSTNAME
    response, content = Http().request(url, "POST", urlencode(parameter))
    if response['status'] == '200':
        return content
    return None

def logout(request):
    if 'profile_id' in request.session:
        del request.session['profile_id']
        del request.session['username']
    return redirect('/')

def login(request, template_name='index.html'):
    error = ""
    if request.method == 'POST':
        param = dict(username=request.POST.get("username", ""), license=request.POST.get("license", ""))
        result = call_api(param, login=True)
        if result is not None:
            result = ast.literal_eval(result)
            if result['status_code'] == 10:
                request.session['profile_id'] = result['profile_id']
                request.session['username'] = request.POST.get('username')
                request.session['date_format'] = "d/m/Y"
                return redirect(reverse('daily_usage_report'))
            else:
                error = "Username or password was incorrect, please try again"
        else:
            error = "Server returned error"
    template_context = {}
    template_context['user_authenticated'] = False
    template_context['user_name'] = ""
    template_context['error'] = error
    return render_to_response(template_name, template_context, RequestContext(request))

def my_key(dict_key):
    try:
        return int(dict_key)
    except ValueError:
        return dict_key

def daily_report(request):
    if not 'profile_id' in request.session:
        return redirect("/")
    template_context = {}
    template_context['results'] = None

    today = date.today()
    template_context['startdate'] = date(today.year, today.month, 1).strftime("%d/%m/%Y")
    if today.day > 1:
        template_context['enddate'] = date(today.year, today.month, today.day - 1).strftime("%d/%m/%Y")
    else:
        template_context['enddate'] = date(today.year, today.month, 1).strftime("%d/%m/%Y")

    if not request.is_ajax() and request.method == 'POST':
        if request.POST.get("report_type") == 'daily':
            if request.session['date_format'] == 'm/d/Y':
                startdate = datetime.datetime.strptime(request.POST.get("startDate"), '%m/%d/%Y').strftime('%Y-%m-%d')
                enddate = datetime.datetime.strptime(request.POST.get("endDate"), '%m/%d/%Y').strftime('%Y-%m-%d')
            else:
                startdate = datetime.datetime.strptime(request.POST.get("startDate"), '%d/%m/%Y').strftime('%Y-%m-%d')
                enddate = datetime.datetime.strptime(request.POST.get("endDate"), '%d/%m/%Y').strftime('%Y-%m-%d')
            param = dict(profile_id=request.session['profile_id'], type="daily", start_date=startdate, end_date=enddate)
            #param = dict(profile_id=request.session['profile_id'], type="license")
            result = call_api(param, login=False)
            import json
            if result is not None:
                result = json.loads(result)
                template_context['status_code'] = result['status_code']
                if result is not None:
                    #result = ast.literal_eval(result)
                    if result["status_code"] == 10:
                        template_context['results'] = result['results']
                        template_context['report_type'] = request.POST.get("report_type")
                        template_context['startdate'] = request.POST.get("startDate")
                        template_context['enddate'] = request.POST.get("endDate")
                        template_context['date_format'] = request.session['date_format']
                        for eachobject in template_context['results']:
                            if not eachobject['valid']:
                                eachobject['valid'] = 0;
                            if not eachobject['invalid']:
                                eachobject['invalid'] = 0;
                            if not eachobject['corrections']:
                                eachobject['corrections'] = 0;
            else:
                template_context['startdate'] = request.POST.get("startDate")
                template_context['enddate'] = request.POST.get("endDate")
                template_context['report_type'] = request.POST.get("report_type")
                template_context['date_format'] = request.session['date_format']
                template_context['status_code'] = '15'
        if request.POST.get("report_type") == 'total':
            if request.session['date_format'] == 'm/d/Y':
                startdate = datetime.datetime.strptime(request.POST.get("startDate"), '%m/%d/%Y').strftime('%Y-%m-%d')
                enddate = datetime.datetime.strptime(request.POST.get("endDate"), '%m/%d/%Y').strftime('%Y-%m-%d')
            else:
                startdate = datetime.datetime.strptime(request.POST.get("startDate"), '%d/%m/%Y').strftime('%Y-%m-%d')
                enddate = datetime.datetime.strptime(request.POST.get("endDate"), '%d/%m/%Y').strftime('%Y-%m-%d')
                #param = dict(profile_id=request.session['profile_id'], type="summary", start_date=startdate, end_date=enddate)
            param = dict(profile_id=request.session['profile_id'], type="summary", start_date=startdate, end_date=enddate)
            if request.session['date_format'] == 'm/d/Y':
                startdate = datetime.datetime.strptime(request.POST.get("startDate"), '%m/%d/%Y').strftime('%d-%b-%Y')
                enddate = datetime.datetime.strptime(request.POST.get("endDate"), '%m/%d/%Y').strftime('%d-%b-%Y')
            else:
                startdate = datetime.datetime.strptime(request.POST.get("startDate"), '%d/%m/%Y').strftime('%d-%b-%Y')
                enddate = datetime.datetime.strptime(request.POST.get("endDate"), '%d/%m/%Y').strftime('%d-%b-%Y')
            result = call_api(param, login=False)
            import json
            if result is not None:
                result = json.loads(result)
                template_context['status_code'] = result['status_code']
                if result is not None:
                    if result["status_code"] == 10:
                        template_context['date_format'] = request.session['date_format']
                        template_context['report_type'] = request.POST.get("report_type")
                        template_context['summary'] = result['results']
                        if 'corrections' in template_context['summary']:
                            template_context['summary']['55555'] = template_context['summary'].pop('corrections')
                        template_context['summary'] = [(int(k), template_context['summary'][k]) for k in sorted(template_context['summary'], key=my_key)]
                        template_context['codes'] = dict({5:'Timeout', 10:'Syntax OK', 20:'Syntax OK and domain valid according to database', 30:'Syntax OK and domain exists', 40:'Syntax OK, domain exists and can receive email', 45:'Domain does not support validation (accepts all mailboxes)', 50:'Syntax OK, domain exists, and mailbox not rejected',
                                                          100:'General syntax error', 110:'Invalid character in address', 115:'Invalid domain syntax', 120:'Invalid username syntax', 125:'Invalid username syntax for a common domain', 130:'Address is too long', 135:'Unbalanced delimiters in address', 140:'Email does not have a username', 145:'Email does not have a domain', 150:'Email does not have an @ sign', 155:'Email has multiple @ signs', 200:'Invalid top level domain (I.e., not .com, .edu, etc.)', 205:'IP address not allowed as a domain', 210: 'Address contains comment or extra text', 215:'Unquoted spaces not allowed',
                                                          310:'Domain does not exist', 315:'Domain does not have a valid IP address', 325:'Domain can not receive email',
                                                          400:'Mailbox is invalid or does not exist', 410:'Mailbox is full or soft bounces', 420:'Mail is not accepted for this domain',
                                                          500:'Addresses with that username are not allowed', 505:'Addresses with that domain are not allowed', 510:'Address is a bot or other suppression', 520:'Address is a known bouncer', 525:'Address is a spamtrap or known complainer', 530:'Address has opted out from commercial email'})
                        template_context['startdate'] = request.POST.get("startDate")
                        template_context['enddate'] = request.POST.get("endDate")
                        #template_context['summary'] = sorted(dict(template_context['summary']).iteritems(), key=my_key)
                        template_context['report_type'] = request.POST.get("report_type")
            else:
                template_context['date_format'] = request.session['date_format']
                template_context['startdate'] = request.POST.get("startDate")
                template_context['enddate'] = request.POST.get("endDate")
                template_context['report_type'] = request.POST.get("report_type")
                template_context['status_code'] = '15'

    template_context['user_authenticated'] = False
    template_context['user_name'] = ""
    if 'profile_id' in request.session:
        template_context['user_authenticated'] = True
        template_context['user_name'] = request.session['username']
        param = dict(profile_id=request.session['profile_id'], type="license")
        result = call_api(param, login=False)
        #template_context['culicense'] = {'allowed_usage': '1000000000','end_date': '2013-11-29','remaining_usage': 999994958,'start_date': '2010-11-29','usage': 5042}
        if result is not None:
            result = ast.literal_eval(result)
            error = "Not Found"
            if result['status_code'] == 10:
                template_context['date_format'] = request.session['date_format']
                template_context['license'] = result['results']
                if request.is_ajax():
                    template_context['date_format'] = request.POST['date_format']
                    request.session['date_format']= template_context['date_format']
                    if template_context['date_format'] == 'd/m/Y':
                        template_context['license']['start_date'] = datetime.datetime.strptime(template_context['license']['start_date'], '%Y-%m-%d').strftime("%d/%m/%Y")
                        template_context['license']['end_date'] = datetime.datetime.strptime(template_context['license']['end_date'], '%Y-%m-%d').strftime("%d/%m/%Y")
                    if template_context['date_format'] == 'm/d/Y':
                        template_context['license']['start_date'] = datetime.datetime.strptime(template_context['license']['start_date'], '%Y-%m-%d').strftime("%m/%d/%Y")
                        template_context['license']['end_date'] = datetime.datetime.strptime(template_context['license']['end_date'], '%Y-%m-%d').strftime("%m/%d/%Y")
                    return HttpResponse(simplejson.dumps(template_context['license']))
                template_context['license']['start_date'] = datetime.datetime.strptime(template_context['license']['start_date'], '%Y-%m-%d')
                template_context['license']['end_date'] = datetime.datetime.strptime(template_context['license']['end_date'], '%Y-%m-%d')
                error = "Successfully"
        else:
            error = "Server returned error"
        template_context['error'] = error
    if request.is_ajax():
        template_context['date_format'] = request.POST['date_format']
        request.session['date_format'] = template_context['date_format']
        return HttpResponse(simplejson.dumps(template_context['license']))
    return render_to_response("daily_report.html", template_context, RequestContext(request))

def download_csv(request):

    # Create the HttpResponse object with the appropriate CSV header.
    if request.method == 'POST':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Report.csv"'

        writer = csv.writer(response)

        #writer.writerow(request.POST['csvdata[0][]']);
        #writer.writerow(request.POST['csvdata[1][]']);
        writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
        #writer.writerow([form])
        return response

def download_pdf(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['Report', 'A1', 'A2', 'A3'])
    writer.writerow(['Result', 'Username', 'Email', 'Phone', 'Address', "ZipCode"])

    return response

