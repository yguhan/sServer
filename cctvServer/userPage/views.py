from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from userPage.models import Document
from userPage.forms import DocumentForm 

from django.views.decorators.csrf import csrf_exempt

import logging

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

			return HttpResponseRedirect(reverse('list'))
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