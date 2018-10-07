from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect,JsonResponse

def login_required(view_func):
	def login_check(request):
		if 'user' in request.session:
			return view_func(request)
		else :
			return JsonResponse({'msg':'User not logged in'})
	return login_check

def isLoggedInCh(conn_func):
	def new_conn_func(message):
		if message.http_session.get('logged_in',False):
			return conn_func(message)
		else:
			message.reply_channel.send({
				'text' : json.dumps({ "close" : True })
			})
	return new_conn_func