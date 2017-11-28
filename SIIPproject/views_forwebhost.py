
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login # for user login
from django.contrib.auth import authenticate, get_user_model # for user login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import View
from urllib import unquote_plus
#from SpatialReasoningTest.models import User, AnswerSet
from SIIPproject.models import UserData, TestAnswer
import time
import csv
import os
import json

# Create your views here
unit1_AnswerKey = ['X','B','A','A','D','B','C','E','E','E','D','E','E','B','D','C','E','A','A','B','B','A','D','D','C','D','C','B','E','C','E']
unit2_AnswerKey = ['X','F','B','C','G','E','A','C','B','E','A','C','G','F','E','C','A','G','C','B','A','E','G','F','E']


# Port from Illinois
@csrf_exempt
def login(request):
	# if the following
	# 1. check whether the userid has illinois postfix
	# 2. check the source of the post
	# 3. session netid exist
	# redirect index
	# else, redirect to authorsys
	# if request.POST.get('netid', False):
	# 	request.session['netid'] = request.POST['netid']
	# 	return HttpResponseRedirect('/spatialtest/index/')
	# 	if request.POST.get('test-type', False):
	# 		if request.POST['test-type'] is 'spatial':
	# 			return HttpResponseRedirect('/spatialtest/index/')
	# 		elif request.POST['test-type'] is 'temporal':
	# 			return HttpRespopnseRedirect('/temporal/index/')
	# 		else:
	# 			return ...
	# else:
	# 	return redirect('http://web.engr.illinois.edu/~authorsys')

	if request.POST.get('netid', False):
		uid = request.POST['netid']
		request.session['netid'] = uid
		#return render(request, 'siip-login.html', {'uid': uid})
		return HttpResponseRedirect('/spatialtest/index/')
	else:
		return redirect('http://web.engr.illinois.edu/~authorsys')
		#return render(reqeust, 'siip-login.html', {'uid': 'NetID not received'})


def redirect(request):
	#return HttpResponseRedirect('/index/')
	return HttpResponseRedirect('/spatialtest/index/')

def index(request):
	# check session uiuc-netid
	# if yes, do the following
	# else, redirect login
	if request.session.get('netid', False):
		tmp = request.session['netid']
		#tmp = 'fake@illinois.edu'
	# if request.method == 'POST':
	# 	tmp = request.POST['username']

        # authentication via Shiebboleth to check whether the user
        # is a vaild UIUC user



		#tmp += format(time.time(), '.0f')
		uid = tmp.split('@')[0]
		user = authenticate(username=uid)

		# new student
		if user is None:
			# new student
			student = User.objects.create_user(uid)
			student.save()
			user = authenticate(username=uid)

			student_data = UserData(user=uid)
			student_data.test1answers = json.dumps([0]*30)
			student_data.test2answers = json.dumps([0]*24)
			student_data.test1score = json.dumps(0)
			student_data.test1_attempt = json.dumps(0)
			student_data.save()

		auth_login(request, user)
		request.session['uid'] = uid


		response = HttpResponseRedirect('../intro')

		#response.set_cookie('uid', uid)
		#response.set_cookie('time', 4500)
		#addUser(tmp)
		return response
	#else:
		#return redirect('http://web.engr.illinois.edu/~authorsys')

@csrf_exempt
def upload(request):
	body = request.body
	fileContent_URLencoded = body.split('=')[1]
	fileContent = unquote_plus(fileContent_URLencoded).decode('utf8')
	#print(fileContent)
	f = open('username_log.txt', 'w')
	f.write(fileContent)
	f.close()
	return HttpResponse()

def download(request):
	f = open('username_log.txt', 'r')
	fileContent = f.read()
	f.close()
	#print(fileContent)
	return HttpResponse(fileContent)

class IntroView(View):
	template_name = "intro.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		return render(request, self.template_name, {'uid': request.user.username})

class SpatialintroView(View):
	template_name = "spatialintro.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		return render(request, self.template_name, {'uid': request.user.username})

class PSVTRView(View):
	template_name = "PSVTR.html"

	def get(self, request, *args, **kwargs):
		# if not request.user.is_authenticated():
		# 	return HttpResponseRedirect(reverse('login'))
		# return render(request, self.template_name, {'uid': request.user.username})
		return render(request, self.template_name)
# class WorkshoploginView(View):
# 	template_name = "workshoplogin.html"

# 	def get(self, request, *args, **kwargs):
# 		if not request.user.is_authenticated():
# 			return HttpResponseRedirect(reverse('login'))
# 		return render(request, self.template_name, {'uid': request.user.username})

# class WorkshopintroView(View):
# 	template_name = "workshopintro.html"

# 	def get(self, request, *args, **kwargs):
# 		if not request.user.is_authenticated():
# 			return HttpResponseRedirect(reverse('login'))
# 		return render(request, self.template_name, {'uid': request.user.username})

class SurveyView(View):
	template_name = "survey.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Survey2View(View):
	template_name = "survey2.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Test1IntroView(View):
	template_name = "test1intro.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		test1_score = UserData.objects.get(user=uid).test1score
		test1_attempt = UserData.objects.get(user=uid).test1_attempt
		# start = UserData.objects.get(user=uid).test1_start
		# notes: one attempt
		# if test1_score != '0':
		# notes: allow three attempts
		if test1_attempt == '3':
			return render(request, "error.html", {"error": "test1taken"})
		return render(request, self.template_name, {'uid': request.user.username, 'start': test1_score, 'test1_score': test1_score, 'test1_attempt': test1_attempt})

class Test1View(View):
	template_name = "test1.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		test1_score = UserData.objects.get(user=uid).test1score
		test1_attempt = UserData.objects.get(user=uid).test1_attempt
		# start = UserData.objects.get(user=uid).test1_start
		if test1_attempt == '3':
			return render(request, "error.html", {"error": "test1taken"})
		return render(request, self.template_name, {'uid': request.user.username, 'start': test1_score, 'test1_score': test1_score, 'test1_attempt': test1_attempt})

class Test2IntroView(View):
	template_name = "test2intro.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).test2_start
		if start is not None:
			return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Test2View(View):
	template_name = "test2.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).test2_start
		if start is not None:
			return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})


class BreakPageView(View):
	template_name = "break.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))

		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# test1
		test1_key = json.loads( TestAnswer.objects.get(test_id=1).answer )
		test1_ans = json.loads( user_data.test1answers)
		test1_correct = sum([test1_key[i] == test1_ans[i] for i in range(len(test1_key)) ])

		return render(request, self.template_name, {'uid': request.user.username,
			'test1_correct': test1_correct})

class ThankuView(View):

	def get(self, request, *args, **kwargs):
                if not request.user.is_authenticated():
                        return HttpResponseRedirect(reverse('login'))

		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# test1
		test1_key = json.loads( TestAnswer.objects.get(test_id=1).answer )
		test1_ans = json.loads( user_data.test1answers)
		test1_correct = sum([test1_key[i] == test1_ans[i] for i in range(len(test1_key)) ])

		# test1
		test2_key = json.loads( TestAnswer.objects.get(test_id=2).answer )
		test2_ans = json.loads( user_data.test2answers)
		test2_correct = sum([test2_key[i] == test2_ans[i] for i in range(len(test2_key)) ])

		return render(request, 'thanku.html', {'test1_correct': test1_correct, 'test2_correct': test2_correct})

class PostsurveyView(View):
	template_name = "postsurvey.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Postsurvey2View(View):
	template_name = "postsurvey2.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Posttest1IntroView(View):
	template_name = "posttest1intro.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).posttest1_start
		if start is not None:
			return render(request, "error.html", {"error": "posttesttaken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Posttest1View(View):
	template_name = "posttest1.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).posttest1_start
		if start is not None:
			return render(request, "error.html", {"error": "posttesttaken"})
		return render(request, self.template_name, {'uid': request.user.username})

class PostbreakView(View):
	template_name = "postbreak.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))

		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# test1
		test1_key = json.loads( TestAnswer.objects.get(test_id=1).answer )
		posttest1_ans = json.loads( user_data.posttest1answers)
		posttest1_correct = sum([test1_key[i] == posttest1_ans[i] for i in range(len(test1_key)) ])

		return render(request, self.template_name, {'uid': request.user.username, 'posttest1_correct': posttest1_correct, 'posttest1_ans': posttest1_ans})

class Breakweek1View(View):
	template_name = "breakweek1.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))

		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# part1week1a
		week1a_key = json.loads( TestAnswer.objects.get(test_id=3).answer )
		week1a_ans = json.loads( user_data.week1aanswers)
		week1a_correct = sum([week1a_key[i] == week1a_ans[i] for i in range(len(week1a_key)) ])

		# part2week1b
		week1b_key = json.loads( TestAnswer.objects.get(test_id=4).answer )
		week1b_ans = json.loads( user_data.week1banswers)
		week1b_correct = sum([week1b_key[i] == week1b_ans[i] for i in range(len(week1b_key)) ])

		# part3week1c
		week1c_key = json.loads( TestAnswer.objects.get(test_id=5).answer )
		week1c_ans = json.loads( user_data.week1canswers)
		week1c_correct = sum([week1c_key[i] == week1c_ans[i] for i in range(len(week1c_key)) ])

		# totalscore
		week1_correct = week1a_correct + week1b_correct + week1c_correct

		# totaltime
		week1c_end = UserData.objects.get(user=uid).week1c_end
		week1a_start = UserData.objects.get(user=uid).week1a_start
		week1_totaltime = week1c_end - week1a_start


		return render(request, self.template_name, {'uid': request.user.username,
		 	'week1a_correct': week1a_correct, 'week1b_correct': week1b_correct, 'week1c_correct': week1c_correct, 'week1_correct': week1_correct, 'week1_totaltime': week1_totaltime})

class Breakweek2View(View):
	template_name = "breakweek2.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))

		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# part1week2a
		week2a_key = json.loads( TestAnswer.objects.get(test_id=6).answer )
		week2a_ans = json.loads( user_data.week2aanswers)
		week2a_correct = sum([week2a_key[i] == week2a_ans[i] for i in range(len(week2a_key)) ])

		# part2week2b
		week2b_key = json.loads( TestAnswer.objects.get(test_id=7).answer )
		week2b_ans = json.loads( user_data.week2banswers)
		week2b_correct = sum([week2b_key[i] == week2b_ans[i] for i in range(len(week2b_key)) ])

		# part3week2c
		week2c_key = json.loads( TestAnswer.objects.get(test_id=8).answer )
		week2c_ans = json.loads( user_data.week2canswers)
		week2c_correct = sum([week2c_key[i] == week2c_ans[i] for i in range(len(week2c_key)) ])

		# totalscore
		week2_correct = week2a_correct + week2b_correct + week2c_correct

		# totaltime
		week2c_end = UserData.objects.get(user=uid).week2c_end
		week2a_start = UserData.objects.get(user=uid).week2a_start
		week2_totaltime= week2c_end - week2a_start
		return render(request, self.template_name, {'uid': request.user.username,
			'week2a_correct': week2a_correct, 'week2b_correct': week2b_correct, 'week2c_correct': week2c_correct, 'week2_correct': week2_correct, 'week2_totaltime': week2_totaltime})
class Breakweek3View(View):
	template_name = "breakweek3.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))

		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# part1week3a
		week3a_key = json.loads( TestAnswer.objects.get(test_id=9).answer )
		week3a_ans = json.loads( user_data.week3aanswers)
		week3a_correct = sum([week3a_key[i] == week3a_ans[i] for i in range(len(week3a_key)) ])

		# part2week3b
		week3b_key = json.loads( TestAnswer.objects.get(test_id=10).answer )
		week3b_ans = json.loads( user_data.week3banswers)
		week3b_correct = sum([week3b_key[i] == week3b_ans[i] for i in range(len(week3b_key)) ])

		# part3week3c
		week3c_key = json.loads( TestAnswer.objects.get(test_id=11).answer )
		week3c_ans = json.loads( user_data.week3canswers)
		week3c_correct = sum([week3c_key[i] == week3c_ans[i] for i in range(len(week3c_key)) ])

		# totalscore
		week3_correct = week3a_correct + week3b_correct + week3c_correct

		# totaltime
		week3c_end = UserData.objects.get(user=uid).week3c_end
		week3a_start = UserData.objects.get(user=uid).week3a_start
		week3_totaltime = week3c_end - week3a_start

		return render(request, self.template_name, {'uid': request.user.username,
			'week3a_correct': week3a_correct, 'week3b_correct': week3b_correct, 'week3c_correct': week3c_correct, 'week3_correct': week3_correct, 'week3_totaltime': week3_totaltime})

class Breakweek4View(View):
	template_name = "breakweek4.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))

		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# part1week4a
		week4a_key = json.loads( TestAnswer.objects.get(test_id=12).answer )
		week4a_ans = json.loads( user_data.week4aanswers)
		week4a_correct = sum([week4a_key[i] == week4a_ans[i] for i in range(len(week4a_key)) ])

		# part2week4b
		week4b_key = json.loads( TestAnswer.objects.get(test_id=13).answer )
		week4b_ans = json.loads( user_data.week4banswers)
		week4b_correct = sum([week4b_key[i] == week4b_ans[i] for i in range(len(week4b_key)) ])

		# part3week4c
		week4c_key = json.loads( TestAnswer.objects.get(test_id=14).answer )
		week4c_ans = json.loads( user_data.week4canswers)
		week4c_correct = sum([week4c_key[i] == week4c_ans[i] for i in range(len(week4c_key)) ])

		# totalscore
		week4_correct = week4a_correct + week4b_correct + week4c_correct

		# totaltime
		week4c_end = UserData.objects.get(user=uid).week4c_end
		week4a_start = UserData.objects.get(user=uid).week4a_start
		week4_totaltime = week4c_end - week4a_start

		return render(request, self.template_name, {'uid': request.user.username, 'week4a_start': week4a_start, 'week4c_end': week4c_end,
			'week4a_correct': week4a_correct, 'week4b_correct': week4b_correct, 'week4c_correct': week4c_correct, 'week4_correct': week4_correct, 'week4_totaltime': week4_totaltime})



class Breakweek5View(View):
	template_name = "breakweek5.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))

		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# part1week5a
		week5a_key = json.loads( TestAnswer.objects.get(test_id=15).answer )
		week5a_ans = json.loads( user_data.week5aanswers)
		week5a_correct = sum([week5a_key[i] == week5a_ans[i] for i in range(len(week5a_key)) ])

		# part2week5b
		week5b_key = json.loads( TestAnswer.objects.get(test_id=16).answer )
		week5b_ans = json.loads( user_data.week5banswers)
		week5b_correct = sum([week5b_key[i] == week5b_ans[i] for i in range(len(week5b_key)) ])

		# part3week5c
		week5c_key = json.loads( TestAnswer.objects.get(test_id=17).answer )
		week5c_ans = json.loads( user_data.week5canswers)
		week5c_correct = sum([week5c_key[i] == week5c_ans[i] for i in range(len(week5c_key)) ])

		# part4week5d
		week5d_key = json.loads( TestAnswer.objects.get(test_id=18).answer )
		week5d_ans = json.loads( user_data.week5danswers)
		week5d_correct = sum([week5d_key[i] == week5d_ans[i] for i in range(len(week5d_key)) ])

		# totalscore
		week5_correct = week5a_correct + week5b_correct + week5c_correct + week5d_correct

		# totaltime
		week5d_end = UserData.objects.get(user=uid).week5d_end
		week5a_start = UserData.objects.get(user=uid).week5a_start
		week5_totaltime = week5d_end - week5a_start

		return render(request, self.template_name, {'uid': request.user.username,
			'week5a_correct': week5a_correct, 'week5b_correct': week5b_correct, 'week5c_correct': week5c_correct, 'week5d_correct': week5d_correct, 'week5_totaltime': week5_totaltime, 'week5_correct': week5_correct})


class Breakweek6View(View):
	template_name = "breakweek6.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))

		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# week6a
		week6a_key = json.loads( TestAnswer.objects.get(test_id=19).answer )
		week6a_ans = json.loads( user_data.week6aanswers)
		week6a_correct = sum([week6a_key[i] == week6a_ans[i] for i in range(len(week6a_key)) ])
		# week6b
		week6b_key = json.loads( TestAnswer.objects.get(test_id=20).answer )
		week6b_ans = json.loads( user_data.week6banswers)
		week6b_correct = sum([week6b_key[i] == week6b_ans[i] for i in range(len(week6b_key)) ])
		# week6c
		week6c_key = json.loads( TestAnswer.objects.get(test_id=21).answer )
		week6c_ans = json.loads( user_data.week6canswers)
		week6c_correct = sum([week6c_key[i] == week6c_ans[i] for i in range(len(week6c_key)) ])

		# totalscore
		week6_correct = week6a_correct + week6b_correct + week6c_correct

		# totaltime
		week6c_end = UserData.objects.get(user=uid).week6c_end
		week6a_start = UserData.objects.get(user=uid).week6a_start
		week6_totaltime = week6c_end - week6a_start


		return render(request, self.template_name, {'uid': request.user.username,
			'week6a_correct': week6a_correct, 'week6b_correct': week6b_correct, 'week6c_correct': week6c_correct,
			'week6_totaltime': week6_totaltime, 'week6_correct': week6_correct})

class Breakweek7View(View):
	template_name = "breakweek7.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))

		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		start = UserData.objects.get(user=uid).week7b_end
		# week7a
		week7a_key = json.loads( TestAnswer.objects.get(test_id=22).answer )
		week7a_ans = json.loads( user_data.week7aanswers)
		week7a_correct = sum([week7a_key[i] == week7a_ans[i] for i in range(len(week7a_key)) ])

		# week7b
		week7b_key = json.loads( TestAnswer.objects.get(test_id=23).answer )
		week7b_ans = json.loads( user_data.week7banswers)
		week7b_correct = sum([week7b_key[i] == week7b_ans[i] for i in range(len(week7b_key)) ])

		# totalscore
		week7_correct = week7a_correct + week7b_correct

		# totaltime
		week7b_end = UserData.objects.get(user=uid).week7b_end
		week7a_start = UserData.objects.get(user=uid).week7a_start
		week7_totaltime = week7b_end - week7a_start

		return render(request, self.template_name, {'uid': request.user.username,
			'week7a_correct': week7a_correct,'week7b_correct': week7b_correct, 'week7_totaltime': week7_totaltime, 'week7_correct': week7_correct})


class Week1aView(View):
	template_name = "week1a.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week1a_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week1bView(View):
	template_name = "week1b.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week1b_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week1cView(View):
	template_name = "week1c.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week1c_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week2aView(View):
	template_name = "week2a.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week2a_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week2bView(View):
	template_name = "week2b.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week2b_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week2cView(View):
	template_name = "week2c.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week2c_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week2retakeView(View):
	template_name = "week2retake.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
				# part1
		week2a_key = json.loads( TestAnswer.objects.get(test_id=6).answer)
		week2a_key_c=[]
		for each in week2a_key:
			if each=="A":
				week2a_key_c.append(1)
			if each=="B":
				week2a_key_c.append(2)
			if each=="C":
				week2a_key_c.append(3)
			if each=="D":
				week2a_key_c.append(4)
		week2a_ans = json.loads( user_data.week2aanswers)
		week2a_ans_c = []
		for each in week2a_ans:
			if each=="A":
				week2a_ans_c.append(1)
			if each=="B":
				week2a_ans_c.append(2)
			if each=="C":
				week2a_ans_c.append(3)
			if each=="D":
				week2a_ans_c.append(4)
			if each=="X":
				week2a_ans_c.append(999)

		week2a_correct = sum([week2a_key_c[i] == week2a_ans_c[i] for i in range(len(week2a_key_c)) ])
		week2a_wrong = []
		week2a_wrong_select = []
		week2a_wrong_key = []
		for i in range(len(week2a_key_c)):
			if week2a_key_c[i] != week2a_ans_c[i]:
				week2a_wrong.append(i+1)
				week2a_wrong_select.append(week2a_ans_c[i])
				week2a_wrong_key.append(week2a_key_c[i])
		# start = UserData.objects.get(user=uid).week2c_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username, 'week2a_wrong':week2a_wrong})

class Week2feedbackView(View):
	template_name = "week2feedback.html"
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# part1
		# answer key
		week2a_key = json.loads( TestAnswer.objects.get(test_id=6).answer)
		week2a_key_c=[]
		for each in week2a_key:
			if each=="A":
				week2a_key_c.append(1)
			if each=="B":
				week2a_key_c.append(2)
			if each=="C":
				week2a_key_c.append(3)
			if each=="D":
				week2a_key_c.append(4)
		# student answers
		week2a_ans = json.loads( user_data.week2aanswers)
		week2a_ans_c = []
		for each in week2a_ans:
			if each=="A":
				week2a_ans_c.append(1)
			if each=="B":
				week2a_ans_c.append(2)
			if each=="C":
				week2a_ans_c.append(3)
			if each=="D":
				week2a_ans_c.append(4)
			if each=="X":
				week2a_ans_c.append(999)
		# students' second attempt
		week2aa_ans = json.loads(user_data.week2aaanswers)
		week2aa_ans_c = []
		for each in week2aa_ans:
			if each=="A":
				week2aa_ans_c.append(1)
			if each=="B":
				week2aa_ans_c.append(2)
			if each=="C":
				week2aa_ans_c.append(3)
			if each=="D":
				week2aa_ans_c.append(4)
			if each=="X":
				week2aa_ans_c.append(999)

		week2a_correct = sum([week2a_key_c[i] == week2a_ans_c[i] for i in range(len(week2a_key_c)) ])
		week2a_wrong = []
		week2a_wrong_select = []
		week2a_wrong_key = []
		for i in range(len(week2a_key_c)):
			if week2a_key_c[i] != week2a_ans_c[i]:
				week2a_wrong.append(i+1)
				week2a_wrong_select.append(week2a_ans_c[i])
				week2a_wrong_key.append(week2a_key_c[i])
		# second attempt
		week2aa_correct = sum([week2a_wrong_key[i] == week2aa_ans_c[i] for i in range(len(week2a_wrong_key)) ])
		week2aa_wrong = []
		week2aa_wrong_select = []
		week2aa_wrong_key = []
		for i in range(len(week2a_wrong_key)):
			if week2a_wrong_key[i] != week2aa_ans_c[i]:
				week2aa_wrong.append(i+1)
				week2aa_wrong_select.append(week2aa_ans_c[i])
				week2aa_wrong_key.append(week2a_wrong_key[i])


		# part2
		week2b_key = json.loads( TestAnswer.objects.get(test_id=7).answer )
		week2b_key_c=[]
		for each in week2b_key:
			if each=="A":
				week2b_key_c.append(1)
			if each=="B":
				week2b_key_c.append(2)
			if each=="C":
				week2b_key_c.append(3)
			if each=="D":
				week2b_key_c.append(4)
		week2b_ans = json.loads( user_data.week2banswers)
		week2b_ans_c = []
		for each in week2b_ans:
			if each=="A":
				week2b_ans_c.append(1)
			if each=="B":
				week2b_ans_c.append(2)
			if each=="C":
				week2b_ans_c.append(3)
			if each=="D":
				week2b_ans_c.append(4)
			if each=="X":
				week2b_ans_c.append(999)


		week2b_correct = sum([week2b_key_c[i] == week2b_ans_c[i] for i in range(len(week2b_key_c)) ])
		week2b_wrong = []
		week2b_wrong_select = []
		week2b_wrong_key = []
		for i in range(len(week2b_key)):
			if week2b_key_c[i] != week2b_ans_c[i]:
				week2b_wrong.append(i+1)
				week2b_wrong_select.append(week2b_ans_c[i])
				week2b_wrong_key.append(week2b_key_c[i])



		# part3
		week2c_key = json.loads( TestAnswer.objects.get(test_id=8).answer )
		week2c_ans = json.loads( user_data.week2canswers)
		week2c_key_c =[]
		for each in week2c_key:
			if each== 0:
				week2c_key_c.append(1)
			if each== 1:
				week2c_key_c.append(2)
			if each== 2:
				week2c_key_c.append(3)
			if each== 3:
				week2c_key_c.append(4)
			if each== -1:
				week2c_key_c.append(999)

		week2c_ans_c = []
		for each in week2c_ans:
			if each== 0:
				week2c_ans_c.append(1)
			if each== 1:
				week2c_ans_c.append(2)
			if each== 2:
				week2c_ans_c.append(3)
			if each== 3:
				week2c_ans_c.append(4)
			if each== -1:
				week2c_ans_c.append(999)

		week2c_correct = 0
		week2c_correct = sum([week2c_key_c[i] == week2c_ans_c[i] for i in range(len(week2c_key_c)) ])
		week2c_wrong = []
		week2c_wrong_select = []
		week2c_wrong_key = []
		for i in range(len(week2c_key)):
			if week2c_key_c[i] != week2c_ans_c[i]:
				week2c_wrong.append(i+1)
				week2c_wrong_select.append(week2c_ans_c[i])
				week2c_wrong_key.append(week2c_key_c[i])


		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username, 'week2c_key_c': week2c_key_c, 'week2c_ans_c': week2c_ans_c, 'week2a_key': week2a_wrong_key, 'week2a_ans': week2a_wrong_select, 'week2aa_ans': week2aa_ans_c, 'week2a_correct': week2a_correct, 'week2a_wrong':week2a_wrong, 'week2aa_wrong':week2aa_wrong, 'week2b_key': week2b_wrong_key, 'week2b_ans': week2b_wrong_select, 'week2b_correct': week2b_correct, 'week2b_wrong':week2b_wrong, 'week2c_key': week2c_wrong_key, 'week2c_ans': week2c_wrong_select, 'week2c_correct': week2c_correct, 'week2c_wrong':week2c_wrong})

class Week3introView(View):
	template_name = "week3intro.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week3aView(View):
	template_name = "week3a.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week3a_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week3bView(View):
	template_name = "week3b.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week3b_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week3cView(View):
	template_name = "week3c.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week3c_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week3feedbackView(View):
	template_name = "week3feedback.html"
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# part1
		week3a_key = json.loads( TestAnswer.objects.get(test_id=9).answer)
		week3a_key_c=[]
		for each in week3a_key:
			if each== 0:
				week3a_key_c.append(1)
			if each== 1:
				week3a_key_c.append(2)
			if each== 2:
				week3a_key_c.append(3)
			if each== 3:
				week3a_key_c.append(4)
		week3a_ans = json.loads( user_data.week3aanswers)
		week3a_ans_c = []
		for each in week3a_ans:
			if each== 0:
				week3a_ans_c.append(1)
			if each== 1:
				week3a_ans_c.append(2)
			if each== 2:
				week3a_ans_c.append(3)
			if each== 3:
				week3a_ans_c.append(4)
			if each== -1:
				week3a_ans_c.append(999)

		week3a_correct = sum([week3a_key_c[i] == week3a_ans_c[i] for i in range(len(week3a_key_c)) ])
		week3a_wrong = []
		week3a_wrong_select = []
		week3a_wrong_key = []
		for i in range(len(week3a_key_c)):
			if week3a_key_c[i] != week3a_ans_c[i]:
				week3a_wrong.append(i+1)
				week3a_wrong_select.append(week3a_ans_c[i])
				week3a_wrong_key.append(week3a_key_c[i])


		# part2
		week3b_key = json.loads( TestAnswer.objects.get(test_id=10).answer )
		week3b_key_c=[]
		for each in week3b_key:
			if each=="A":
				week3b_key_c.append(1)
			if each=="B":
				week3b_key_c.append(2)
			if each=="C":
				week3b_key_c.append(3)
			if each=="D":
				week3b_key_c.append(4)
		week3b_ans = json.loads( user_data.week3banswers)
		week3b_ans_c = []
		for each in week3b_ans:
			if each=="A":
				week3b_ans_c.append(1)
			if each=="B":
				week3b_ans_c.append(2)
			if each=="C":
				week3b_ans_c.append(3)
			if each=="D":
				week3b_ans_c.append(4)
			if each=="X":
				week3b_ans_c.append(999)


		week3b_correct = sum([week3b_key_c[i] == week3b_ans_c[i] for i in range(len(week3b_key_c)) ])
		week3b_wrong = []
		week3b_wrong_select = []
		week3b_wrong_key = []
		for i in range(len(week3b_key)):
			if week3b_key_c[i] != week3b_ans_c[i]:
				week3b_wrong.append(i+1)
				week3b_wrong_select.append(week3b_ans_c[i])
				week3b_wrong_key.append(week3b_key_c[i])



		# part3
		week3c_key = json.loads( TestAnswer.objects.get(test_id=11).answer )
		week3c_ans = json.loads( user_data.week3canswers)
		week3c_key_c =[]
		for each in week3c_key:
			if each=="A":
				week3c_key_c.append(1)
			if each=="B":
				week3c_key_c.append(2)
			if each=="C":
				week3c_key_c.append(3)

		week3c_ans_c = []
		for each in week3c_ans:
			if each=="A":
				week3c_ans_c.append(1)
			if each=="B":
				week3c_ans_c.append(2)
			if each=="C":
				week3c_ans_c.append(3)
			if each=="X":
				week3c_ans_c.append(999)


		week3c_correct = 0
		week3c_correct = sum([week3c_key_c[i] == week3c_ans_c[i] for i in range(len(week3c_key_c)) ])
		week3c_wrong = []
		week3c_wrong_select = []
		week3c_wrong_key = []
		for i in range(len(week3c_key)):
			if week3c_key_c[i] != week3c_ans_c[i]:
				week3c_wrong.append(i+1)
				week3c_wrong_select.append(week3c_ans_c[i])
				week3c_wrong_key.append(week3c_key_c[i])


		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username, 'week3c_key_c': week3c_key_c, 'week3c_ans_c': week3c_ans_c, 'week3a_key': week3a_wrong_key, 'week3a_ans': week3a_wrong_select, 'week3a_correct': week3a_correct, 'week3a_wrong':week3a_wrong, 'week3b_key': week3b_wrong_key, 'week3b_ans': week3b_wrong_select, 'week3b_correct': week3b_correct, 'week3b_wrong':week3b_wrong, 'week3c_key': week3c_wrong_key, 'week3c_ans': week3c_wrong_select, 'week3c_correct': week3c_correct, 'week3c_wrong':week3c_wrong})


class Week4introView(View):
	template_name = "week4intro.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week4aView(View):
	template_name = "week4a.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week4a_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week4bView(View):
	template_name = "week4b.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week4b_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week4cView(View):
	template_name = "week4c.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week4c_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week4feedbackView(View):
	template_name = "week4feedback.html"
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# part1
		week4a_key = json.loads( TestAnswer.objects.get(test_id=12).answer)
		week4a_key_c=[]
		for each in week4a_key:
			if each=="A":
				week4a_key_c.append(1)
			if each=="B":
				week4a_key_c.append(2)
			if each=="C":
				week4a_key_c.append(3)
		week4a_ans = json.loads( user_data.week4aanswers)
		week4a_ans_c = []
		for each in week4a_ans:
			if each=="A":
				week4a_ans_c.append(1)
			if each=="B":
				week4a_ans_c.append(2)
			if each=="C":
				week4a_ans_c.append(3)
			if each=="X":
				week4a_ans_c.append(999)

		week4a_correct = sum([week4a_key_c[i] == week4a_ans_c[i] for i in range(len(week4a_key_c)) ])
		week4a_wrong = []
		week4a_wrong_select = []
		week4a_wrong_key = []
		for i in range(len(week4a_key_c)):
			if week4a_key_c[i] != week4a_ans_c[i]:
				week4a_wrong.append(i+1)
				week4a_wrong_select.append(week4a_ans_c[i])
				week4a_wrong_key.append(week4a_key_c[i])


		# part2
		week4b_key = json.loads( TestAnswer.objects.get(test_id=13).answer )
		week4b_key_c=[]
		for each in week4b_key:
			if each== 0:
				week4b_key_c.append(1)
			if each== 1:
				week4b_key_c.append(2)
			if each== 2:
				week4b_key_c.append(3)
			if each== 3:
				week4b_key_c.append(4)
		week4b_ans = json.loads( user_data.week4banswers)
		week4b_ans_c = []
		for each in week4b_ans:
			if each== 0:
				week4b_ans_c.append(1)
			if each== 1:
				week4b_ans_c.append(2)
			if each== 2:
				week4b_ans_c.append(3)
			if each== 3:
				week4b_ans_c.append(4)
			if each== -1:
				week4b_ans_c.append(999)


		week4b_correct = sum([week4b_key_c[i] == week4b_ans_c[i] for i in range(len(week4b_key_c)) ])
		week4b_wrong = []
		week4b_wrong_select = []
		week4b_wrong_key = []
		for i in range(len(week4b_key)):
			if week4b_key_c[i] != week4b_ans_c[i]:
				week4b_wrong.append(i+1)
				week4b_wrong_select.append(week4b_ans_c[i])
				week4b_wrong_key.append(week4b_key_c[i])



		# part3
		week4c_key = json.loads( TestAnswer.objects.get(test_id=14).answer )
		week4c_ans = json.loads( user_data.week4canswers)
		week4c_key_c =[]
		for each in week4c_key:
			if each== 0:
				week4c_key_c.append(1)
			if each== 1:
				week4c_key_c.append(2)
			if each== 2:
				week4c_key_c.append(3)
			if each== 3:
				week4c_key_c.append(4)
		week4c_ans = json.loads( user_data.week4canswers)
		week4c_ans_c = []
		for each in week4c_ans:
			if each== 0:
				week4c_ans_c.append(1)
			if each== 1:
				week4c_ans_c.append(2)
			if each== 2:
				week4c_ans_c.append(3)
			if each== 3:
				week4c_ans_c.append(4)
			if each== -1:
				week4c_ans_c.append(999)

		week4c_correct = 0
		week4c_correct = sum([week4c_key_c[i] == week4c_ans_c[i] for i in range(len(week4c_key_c)) ])
		week4c_wrong = []
		week4c_wrong_select = []
		week4c_wrong_key = []
		for i in range(len(week4c_key)):
			if week4c_key_c[i] != week4c_ans_c[i]:
				week4c_wrong.append(i+1)
				week4c_wrong_select.append(week4c_ans_c[i])
				week4c_wrong_key.append(week4c_key_c[i])


		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username, 'week4c_key_c': week4c_key_c, 'week4c_ans_c': week4c_ans_c, 'week4a_key': week4a_wrong_key, 'week4a_ans': week4a_wrong_select, 'week4a_correct': week4a_correct, 'week4a_wrong':week4a_wrong, 'week4b_key': week4b_wrong_key, 'week4b_ans': week4b_wrong_select, 'week4b_correct': week4b_correct, 'week4b_wrong':week4b_wrong, 'week4c_key': week4c_wrong_key, 'week4c_ans': week4c_wrong_select, 'week4c_correct': week4c_correct, 'week4c_wrong':week4c_wrong})



class Week4dView(View):
	template_name = "week4d.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week4d_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week5introView(View):
	template_name = "week5intro.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})


class Week5aView(View):
	template_name = "week5a.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week5a_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week5bView(View):
	template_name = "week5b.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week5b_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week5cView(View):
	template_name = "week5c.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week5c_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week5dView(View):
	template_name = "week5d.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week5d_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week5feedbackView(View):
	template_name = "week5feedback.html"
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# part1
		week5a_key = json.loads( TestAnswer.objects.get(test_id=15).answer)
		week5a_key_c=[]
		for each in week5a_key:
			if each== 0:
				week5a_key_c.append(1)
			if each== 1:
				week5a_key_c.append(2)
			if each== 2:
				week5a_key_c.append(3)
		week5a_ans = json.loads( user_data.week5aanswers)
		week5a_ans_c = []
		for each in week5a_ans:
			if each== 0:
				week5a_ans_c.append(1)
			if each== 1:
				week5a_ans_c.append(2)
			if each== 2:
				week5a_ans_c.append(3)
			if each== -1:
				week5a_ans_c.append(999)

		week5a_correct = sum([week5a_key_c[i] == week5a_ans_c[i] for i in range(len(week5a_key_c)) ])
		week5a_wrong = []
		week5a_wrong_select = []
		week5a_wrong_key = []
		for i in range(len(week5a_key_c)):
			if week5a_key_c[i] != week5a_ans_c[i]:
				week5a_wrong.append(i+1)
				week5a_wrong_select.append(week5a_ans_c[i])
				week5a_wrong_key.append(week5a_key_c[i])


		# part2
		week5b_key = json.loads( TestAnswer.objects.get(test_id=16).answer )
		week5b_key_c=[]
		for each in week5b_key:
			if each== 0:
				week5b_key_c.append(1)
			if each== 1:
				week5b_key_c.append(2)
			if each== 2:
				week5b_key_c.append(3)
		week5b_ans = json.loads( user_data.week5banswers)
		week5b_ans_c = []
		for each in week5b_ans:
			if each== 0:
				week5b_ans_c.append(1)
			if each== 1:
				week5b_ans_c.append(2)
			if each== 2:
				week5b_ans_c.append(3)
			if each== -1:
				week5b_ans_c.append(999)


		week5b_correct = sum([week5b_key_c[i] == week5b_ans_c[i] for i in range(len(week5b_key_c)) ])
		week5b_wrong = []
		week5b_wrong_select = []
		week5b_wrong_key = []
		for i in range(len(week5b_key)):
			if week5b_key_c[i] != week5b_ans_c[i]:
				week5b_wrong.append(i+1)
				week5b_wrong_select.append(week5b_ans_c[i])
				week5b_wrong_key.append(week5b_key_c[i])



		# part3
		week5c_key = json.loads( TestAnswer.objects.get(test_id=17).answer )
		week5c_ans = json.loads( user_data.week5canswers)
		week5c_key_c =[]
		for each in week5c_key:
			if each== 0:
				week5c_key_c.append(1)
			if each== 1:
				week5c_key_c.append(2)
			if each== 2:
				week5c_key_c.append(3)
		week5c_ans = json.loads( user_data.week5canswers)
		week5c_ans_c = []
		for each in week5c_ans:
			if each== 0:
				week5c_ans_c.append(1)
			if each== 1:
				week5c_ans_c.append(2)
			if each== 2:
				week5c_ans_c.append(3)
			if each== -1:
				week5c_ans_c.append(999)

		week5c_correct = 0
		week5c_correct = sum([week5c_key_c[i] == week5c_ans_c[i] for i in range(len(week5c_key_c)) ])
		week5c_wrong = []
		week5c_wrong_select = []
		week5c_wrong_key = []
		for i in range(len(week5c_key)):
			if week5c_key_c[i] != week5c_ans_c[i]:
				week5c_wrong.append(i+1)
				week5c_wrong_select.append(week5c_ans_c[i])
				week5c_wrong_key.append(week5c_key_c[i])
		# part4
		week5d_key = json.loads( TestAnswer.objects.get(test_id=18).answer )
		week5d_ans = json.loads( user_data.week5danswers)
		week5d_key_c =[]
		for each in week5d_key:
			if each== 0:
				week5d_key_c.append(1)
			if each== 1:
				week5d_key_c.append(2)
			if each== 2:
				week5d_key_c.append(3)
		week5d_ans = json.loads( user_data.week5danswers)
		week5d_ans_c = []
		for each in week5d_ans:
			if each== 0:
				week5d_ans_c.append(1)
			if each== 1:
				week5d_ans_c.append(2)
			if each== 2:
				week5d_ans_c.append(3)
			if each== -1:
				week5d_ans_c.append(999)

		week5d_correct = 0
		week5d_correct = sum([week5d_key_c[i] == week5d_ans_c[i] for i in range(len(week5d_key_c)) ])
		week5d_wrong = []
		week5d_wrong_select = []
		week5d_wrong_key = []
		for i in range(len(week5d_key)):
			if week5d_key_c[i] != week5d_ans_c[i]:
				week5d_wrong.append(i+1)
				week5d_wrong_select.append(week5d_ans_c[i])
				week5d_wrong_key.append(week5d_key_c[i])

		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username, 'week5c_key_c': week5c_key_c, 'week5c_ans_c': week5c_ans_c, 'week5a_key': week5a_wrong_key, 'week5a_ans': week5a_wrong_select, 'week5a_correct': week5a_correct, 'week5a_wrong':week5a_wrong, 'week5b_key': week5b_wrong_key, 'week5b_ans': week5b_wrong_select, 'week5b_correct': week5b_correct, 'week5b_wrong':week5b_wrong, 'week5c_key': week5c_wrong_key, 'week5c_ans': week5c_wrong_select, 'week5c_correct': week5c_correct, 'week5c_wrong':week5c_wrong,
			'week5d_key': week5d_wrong_key, 'week5d_ans': week5d_wrong_select, 'week5d_correct': week5d_correct, 'week5d_wrong':week5d_wrong})



class Week6aView(View):
	template_name = "week6a.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week6a_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})


class Week6bView(View):
	template_name = "week6b.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week6b_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week6dView(View):
	template_name = "week6d.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week6d_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week6cView(View):
	template_name = "week6c.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week6c_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week6feedbackView(View):
	template_name = "week6feedback.html"
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# part1
		week6a_key = json.loads( TestAnswer.objects.get(test_id=19).answer)
		week6a_key_c=[]
		for each in week6a_key:
			if each== 0:
				week6a_key_c.append(1)
			if each== 1:
				week6a_key_c.append(2)
			if each== 2:
				week6a_key_c.append(3)
			if each== 3:
				week6a_key_c.append(4)
		week6a_ans = json.loads( user_data.week6aanswers)
		week6a_ans_c = []
		for each in week6a_ans:
			if each== 0:
				week6a_ans_c.append(1)
			if each== 1:
				week6a_ans_c.append(2)
			if each== 2:
				week6a_ans_c.append(3)
			if each== 3:
				week6a_ans_c.append(4)
			if each== -1:
				week6a_ans_c.append(999)

		week6a_correct = sum([week6a_key_c[i] == week6a_ans_c[i] for i in range(len(week6a_key_c)) ])
		week6a_wrong = []
		week6a_wrong_select = []
		week6a_wrong_key = []
		for i in range(len(week6a_key_c)):
			if week6a_key_c[i] != week6a_ans_c[i]:
				week6a_wrong.append(i+1)
				week6a_wrong_select.append(week6a_ans_c[i])
				week6a_wrong_key.append(week6a_key_c[i])


		# part2
		week6b_key = json.loads( TestAnswer.objects.get(test_id=20).answer )
		week6b_key_c=[]
		for each in week6b_key:
			week6b_key_c=[]
		for each in week6b_key:
			if each=="A":
				week6b_key_c.append(1)
			if each=="B":
				week6b_key_c.append(2)
			if each=="C":
				week6b_key_c.append(3)
		week6b_ans = json.loads( user_data.week6banswers)
		week6b_ans_c = []
		for each in week6b_ans:
			if each=="A":
				week6b_ans_c.append(1)
			if each=="B":
				week6b_ans_c.append(2)
			if each=="C":
				week6b_ans_c.append(3)
			if each=="X":
				week6b_ans_c.append(999)

		week6b_correct = sum([week6b_key_c[i] == week6b_ans_c[i] for i in range(len(week6b_key_c)) ])
		week6b_wrong = []
		week6b_wrong_select = []
		week6b_wrong_key = []
		for i in range(len(week6b_key)):
			if week6b_key_c[i] != week6b_ans_c[i]:
				week6b_wrong.append(i+1)
				week6b_wrong_select.append(week6b_ans_c[i])
				week6b_wrong_key.append(week6b_key_c[i])



		# part3
		week6c_key = json.loads( TestAnswer.objects.get(test_id=21).answer )
		week6c_ans = json.loads( user_data.week6canswers)
		week6c_key_c =[]
		for each in week6c_key:
			if each== 0:
				week6c_key_c.append(1)
			if each== 1:
				week6c_key_c.append(2)
			if each== 2:
				week6c_key_c.append(3)
		week6c_ans = json.loads( user_data.week6canswers)
		week6c_ans_c = []
		for each in week6c_ans:
			if each== 0:
				week6c_ans_c.append(1)
			if each== 1:
				week6c_ans_c.append(2)
			if each== 2:
				week6c_ans_c.append(3)
			if each== -1:
				week6c_ans_c.append(999)

		week6c_correct = 0
		week6c_correct = sum([week6c_key_c[i] == week6c_ans_c[i] for i in range(len(week6c_key_c)) ])
		week6c_wrong = []
		week6c_wrong_select = []
		week6c_wrong_key = []
		for i in range(len(week6c_key)):
			if week6c_key_c[i] != week6c_ans_c[i]:
				week6c_wrong.append(i+1)
				week6c_wrong_select.append(week6c_ans_c[i])
				week6c_wrong_key.append(week6c_key_c[i])

		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username, 'week6c_key_c': week6c_key_c, 'week6c_ans_c': week6c_ans_c, 'week6a_key': week6a_wrong_key,
			'week6a_ans': week6a_wrong_select, 'week6a_correct': week6a_correct, 'week6a_wrong':week6a_wrong,
			'week6b_key': week6b_wrong_key, 'week6b_ans': week6b_wrong_select, 'week6b_correct': week6b_correct, 'week6b_wrong':week6b_wrong, 'week6c_key': week6c_wrong_key,
			'week6c_ans': week6c_wrong_select, 'week6c_correct': week6c_correct, 'week6c_wrong':week6c_wrong})



class Week7introView(View):
	template_name = "week7intro.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week7aView(View):
	template_name = "week7a.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week7a_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week7bView(View):
	template_name = "week7b.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week7b_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week7cView(View):
	template_name = "week7c.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		start = UserData.objects.get(user=uid).week7c_start
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username})

class Week7feedbackView(View):
	template_name = "week7feedback.html"
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		user_data = UserData.objects.get(user=uid)

		# part1

		week7a_key = json.loads( TestAnswer.objects.get(test_id=22).answer )
		week7a_key_c=[]
		for each in week7a_key:
			week7a_key_c=[]
		for each in week7a_key:
			if each=="A":
				week7a_key_c.append(1)
			if each=="B":
				week7a_key_c.append(2)
			if each=="C":
				week7a_key_c.append(3)
		week7a_ans = json.loads( user_data.week7aanswers)
		week7a_ans_c = []
		for each in week7a_ans:
			if each=="A":
				week7a_ans_c.append(1)
			if each=="B":
				week7a_ans_c.append(2)
			if each=="C":
				week7a_ans_c.append(3)
			if each=="X":
				week7a_ans_c.append(999)

		week7a_correct = sum([week7a_key_c[i] == week7a_ans_c[i] for i in range(len(week7a_key_c)) ])
		week7a_wrong = []
		week7a_wrong_select = []
		week7a_wrong_key = []
		for i in range(len(week7a_key)):
			if week7a_key_c[i] != week7a_ans_c[i]:
				week7a_wrong.append(i+1)
				week7a_wrong_select.append(week7a_ans_c[i])
				week7a_wrong_key.append(week7a_key_c[i])

		# part2
		week7b_key = json.loads( TestAnswer.objects.get(test_id=23).answer)
		week7b_key_c=[]
		for each in week7b_key:
			if each== 0:
				week7b_key_c.append(1)
			if each== 1:
				week7b_key_c.append(2)
			if each== 2:
				week7b_key_c.append(3)
			if each== 3:
				week7b_key_c.append(4)
		week7b_ans = json.loads( user_data.week7banswers)
		week7b_ans_c = []
		for each in week7b_ans:
			if each== 0:
				week7b_ans_c.append(1)
			if each== 1:
				week7b_ans_c.append(2)
			if each== 2:
				week7b_ans_c.append(3)
			if each== 3:
				week7b_ans_c.append(4)
			if each== -1:
				week7b_ans_c.append(999)

		week7b_correct = sum([week7b_key_c[i] == week7b_ans_c[i] for i in range(len(week7b_key_c)) ])
		week7b_wrong = []
		week7b_wrong_select = []
		week7b_wrong_key = []
		for i in range(len(week7b_key_c)):
			if week7b_key_c[i] != week7b_ans_c[i]:
				week7b_wrong.append(i+1)
				week7b_wrong_select.append(week7b_ans_c[i])
				week7b_wrong_key.append(week7b_key_c[i])



		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		return render(request, self.template_name, {'uid': request.user.username, 'week7a_key': week7a_wrong_key, 'week7a_ans': week7a_wrong_select, 'week7a_correct': week7a_correct, 'week7a_wrong':week7a_wrong,
			'week7b_key': week7b_wrong_key, 'week7b_ans': week7b_wrong_select, 'week7b_correct': week7b_correct, 'week7b_wrong':week7b_wrong})

class GradebookView(View):
	template_name = "gradebook.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# if start is not None:
		# 	return render(request, "error.html", {"error": "test2taken"})
		# return render(request, self.template_name, {'uid': request.user.username})

		try:
		 test1score = json.loads( user_data.test1score)
	 	except:
		 test1score = "_"
		try:
		 week1score = json.loads( user_data.week1score)
	 	except:
		 week1score = "_"
		try:
		 week2score = json.loads( user_data.week2score)
		except:
		 week2score = "_"
		try:
		 week3score = json.loads( user_data.week3score)
		except:
		 week3score = "_"
		try:
		 week4score = json.loads( user_data.week4score)
		except:
		 week4score = "_"
		try:
		 week5score = json.loads( user_data.week5score)
		except:
		 week5score = "_"
		try:
		 week6score = json.loads( user_data.week6score)
		except:
		 week6score = "_"
		try:
		 week7score = json.loads( user_data.week7score)
		except:
		 week7score = "_"
		# week4score = json.loads( user_data.week4score)
		# week5score = json.loads( user_data.week5score)
		# week6score = json.loads( user_data.week6score)
		# week7score = json.loads( user_data.week7score)
		return render(request, self.template_name, {'uid': request.user.username, 'test1score':test1score,'week1score':week1score,'week2score':week2score,'week3score':week3score,'week4score':week4score,'week5score':week5score,'week6score':week6score, 'week7score':week7score})

class LogView(View):
	template_name = "base.html" # dummy

	def post(self, request, *args, **kwargs):

		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))

		path = request.POST.get('path', '')
		action = request.POST.get('action', '')
		msg = request.POST.get('msg', '')
		time = timezone.now()
		record = {"timestamp": time.isoformat(), "path": path, "action": action, "msg": msg}
		# print json.dumps(record)

		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# save the time when they start the tests
		if action == "LOAD" and path == "/spatialtest/test1/":
			user_data.test1_start = time
		elif action == "LOAD" and path == "/spatialtest/test2/":
			user_data.test2_start = time
		elif action == "LOAD" and path == "/spatialtest/posttest1/":
			user_data.posttest1_start = time
		elif action == "LOAD" and path == "/spatialtest/week1a/":
			user_data.week1a_start = time
		elif action == "LOAD" and path == "/spatialtest/week1b/":
			user_data.week1b_start = time
		elif action == "LOAD" and path == "/spatialtest/week1c/":
			user_data.week1c_start = time
		elif action == "WEEK1CTIME":
			user_data.week1c_end = time
		elif action == "LOAD" and path == "/spatialtest/week2a/":
			user_data.week2a_start = time
		elif action == "LOAD" and path == "/spatialtest/week2b/":
			user_data.week2b_start = time
		elif action == "LOAD" and path == "/spatialtest/week2c/":
			user_data.week2c_start = time
		elif action == "WEEK2CTIME":
			user_data.week2c_end = time
		elif action == "LOAD" and path == "/spatialtest/week3a/":
			user_data.week3a_start = time
		elif action == "LOAD" and path == "/spatialtest/week3b/":
			user_data.week3b_start = time
		elif action == "LOAD" and path == "/spatialtest/week3c/":
			user_data.week3c_start = time
		elif action == "WEEK3CTIME":
			user_data.week3c_end = time
		elif action == "LOAD" and path == "/spatialtest/week4a/":
			user_data.week4a_start = time
		elif action == "LOAD" and path == "/spatialtest/week4b/":
			user_data.week4b_start = time
		elif action == "LOAD" and path == "/spatialtest/week4c/":
			user_data.week4c_start = time
		elif action == "WEEK4CTIME":
			user_data.week4c_end = time
		elif action == "LOAD" and path == "/spatialtest/week4d/":
			user_data.week4d_start = time
		elif action == "LOAD" and path == "/spatialtest/week5a/":
			user_data.week5a_start = time
		elif action == "LOAD" and path == "/spatialtest/week5b/":
			user_data.week5b_start = time
		elif action == "LOAD" and path == "/spatialtest/week5c/":
			user_data.week5c_start = time
		elif action == "LOAD" and path == "/spatialtest/week5d/":
			user_data.week5d_start = time
		elif action == "WEEK5DTIME":
			user_data.week5d_end = time
		elif action == "LOAD" and path == "/spatialtest/week6a/":
			user_data.week6a_start = time
		elif action == "LOAD" and path == "/spatialtest/week6b/":
			user_data.week6b_start = time
		elif action == "LOAD" and path == "/spatialtest/week6c/":
			user_data.week6c_start = time
		elif action == "WEEK6CTIME":
			user_data.week6c_end = time
		elif action == "LOAD" and path == "/spatialtest/week6d/":
			user_data.week6d_start = time
		elif action == "LOAD" and path == "/spatialtest/week7a/":
			user_data.week7a_start = time
		elif action == "LOAD" and path == "/spatialtest/week7b/":
			user_data.week7b_start = time
		elif action == "WEEK7BTIME":
			user_data.week7b_end = time
		elif action == "LOAD" and path == "/spatialtest/week7c/":
			user_data.week7c_start = time
		# store answers
		if action == "ATTEMPT1":
			user_data.test1_attempt = msg
		if action == "ANSWER1":
			user_data.test1answers = msg
		elif action == "ANSWER2":
			user_data.test2answers = msg
		elif action == "SURVEY1":
			user_data.survey1answers = msg
		elif action == "SURVEY2":
			user_data.survey2answers = msg
		elif action == "POSTANSWER1":
			user_data.posttest1answers = msg
		elif action == "POSTSURVEY1":
			user_data.postsurvey1answers = msg
		elif action == "POSTSURVEY2":
			user_data.postsurvey2answers = msg
		elif action == "POSTTEST1":
			user_data.posttest1score = msg
		elif action == "TEST1":
			user_data.test1score = msg
		elif action == "TEST2":
			user_data.test2score = msg
		elif action == "WEEK1A":
			user_data.week1aanswers = msg
		elif action == "WEEK1B":
			user_data.week1banswers = msg
		elif action == "WEEK1C":
			user_data.week1canswers = msg
		elif action == "WEEK1SCORE":
			user_data.week1score = msg
		elif action == "WEEK1TIME":
			user_data.week1_totaltime = time
		elif action == "WEEK2A":
			user_data.week2aanswers = msg
		elif action == "WEEK2AA":
			user_data.week2aaanswers = msg
		elif action == "WEEK2B":
			user_data.week2banswers = msg
		elif action == "WEEK2C":
			user_data.week2canswers = msg
		elif action == "WEEK2SCORE":
			user_data.week2score = msg
		elif action == "WEEK2TIME":
			user_data.week2_totaltime = time
		elif action == "WEEK3A":
			user_data.week3aanswers = msg
		elif action == "WEEK3B":
			user_data.week3banswers = msg
		elif action == "WEEK3C":
			user_data.week3canswers = msg
		elif action == "WEEK3SCORE":
			user_data.week3score = msg
		elif action == "WEEK3TIME":
			user_data.week3_totaltime = time
		elif action == "WEEK4A":
			user_data.week4aanswers = msg
		elif action == "WEEK4B":
			user_data.week4banswers = msg
		elif action == "WEEK4C":
			user_data.week4canswers = msg
		elif action == "WEEK4SCORE":
			user_data.week4score = msg
		elif action == "WEEK4TIME":
			user_data.week4_totaltime = msg
		elif action == "WEEK5A":
			user_data.week5aanswers = msg
		elif action == "WEEK5B":
			user_data.week5banswers = msg
		elif action == "WEEK5C":
			user_data.week5canswers = msg
		elif action == "WEEK5D":
			user_data.week5danswers = msg
		elif action == "WEEK5SCORE":
			user_data.week5score = msg
		elif action == "WEEK5TIME":
			user_data.week5_totaltime = msg
		elif action == "WEEK6A":
			user_data.week6aanswers = msg
		elif action == "WEEK6B":
			user_data.week6banswers = msg
		elif action == "WEEK6C":
			user_data.week6canswers = msg
		elif action == "WEEK6SCORE":
			user_data.week6score = msg
		elif action == "WEEK6TIME":
			user_data.week6_totaltime = msg
		elif action == "WEEK7A":
			user_data.week7aanswers = msg
		elif action == "WEEK7B":
			user_data.week7banswers = msg
		elif action == "WEEK7SCORE":
			user_data.week7score = msg
		elif action == "WEEK7TIME":
			user_data.week7_totaltime = msg
		logs = json.loads(user_data.log)
		logs.append(record)
		user_data.log = json.dumps(logs)
		user_data.save()
		return render(request, self.template_name)
