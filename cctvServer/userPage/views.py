from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from userPage.models import Document
from userPage.forms import DocumentForm 

from django.views.decorators.csrf import csrf_exempt

import logging
from datetime import datetime
# import smtplib
# from email.mime.text import MIMEText

# def sendingEmail(): 
# 	server = smtplib.SMTP('smtp.gmail.com', 587)
# 	server.starttls()
# 	server.login("postechserver@gmail.com", "wjswkghlfh")

# 	msg = "WARNING : CHECK IMG AS SOON AS POSSIBLE\n'http://52.78.37.233:8080'"

# 	# server.sendmail("postechserver@gmail.com", "yguhan@gmail.com", msg)
# 	server.sendmail("postechserver@gmail.com", "postechserver@gmail.com", msg)
# 	server.quit()

import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText

class Alarm():
	def __init__(self):
		self.initial = True
		self.timeNow = datetime.now()

	def check(self):
		if(self.initial):
			self.initial=False
			return True
		else:
			diff = (datetime.now() - self.timeNow).total_seconds()
			if diff>120:
				self.timeNow = datetime.now()
				return True
		return False

	def send_email(self):		 
	    from_addr = 'postechserver@gmail.com'
	    to_addr = 'yguhan@gmail.com'

	    server = smtplib.SMTP('smtp.gmail.com:587')
	    server.starttls()
	    server.login(from_addr, 'wjswkghlfh')

	    body = MIMEMultipart()
	    body['subject'] = "S CCTV"
	    body['From'] = from_addr
	    body['To'] = to_addr

	    html = "<div>WARNING : CHECK IMG AS SOON AS POSSIBLE\n&quot;http://52.78.37.233:8080&quot;</div>"
	    msg = MIMEText(html, 'html')
	    body.attach(msg)

	    server.sendmail(from_addr=from_addr,
	                    to_addrs=[to_addr],  
	                    msg=body.as_string())
	    server.quit()
	    print "sending time: ", self.timeNow

	def run(self):
		if self.check():
			self.send_email()
		else:
			pass
	
alarm = Alarm()
#from userPage.models import RequestLog

# Create your views here.
@csrf_exempt
def list(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)

		if form.is_valid():
			#logger = logging.getLogger(str(request))
			#logger.error(str('request: '))

			newdoc = Document(docfile = request.FILES['docfile'])
			newdoc.save()
			# sendingEmail()
			alarm.run()
		return HttpResponseRedirect("http://52.78.37.233:8080/userPage")
	else:
		form = DocumentForm()

	documents = Document.objects.all()

	return render_to_response(
		'userPage/list.html',
		{'documents': documents, 'form':form}
	)	

def index(request):
	return render_to_response('userPage/index.html')

"""
@csrf_exempt
def test(request):
	if request.method == 'POST':
		req = RequestLog(req = request.body)
		req.save()
	
		req = RequestLog(req = request.META)
		req.save()
	
	

		return HttpResponseRedirect(reverse('test'))

	else:
		requestLogs = RequestLog.objects.all()

		return render_to_response(
			'userPage/test.html',
			{'requestLogs': requestLogs}
		)
"""