
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
from SIIPproject.models import UserData, TestAnswer
import time
import csv
import os
import json

@csrf_exempt
def login(request):
	if request.POST.get('netid', False):
		uid = request.POST['netid']
		request.session['netid'] = uid
		return HttpResponseRedirect('/spatialtest/index/')
	else:
		return redirect('http://webhost.engr.illinois.edu/~authorsys')

def answerConvertNum(current_answer):
	convertedAnswer = []
	for each in current_answer:
		if each== 0:
			convertedAnswer.append(1)
		if each== 1:
			convertedAnswer.append(2)
		if each== 2:
			convertedAnswer.append(3)
		if each== 3:
			convertedAnswer.append(4)
		if each== -1:
			convertedAnswer.append(999)
	return convertedAnswer

def answerConvertLet(current_answer):
	convertedAnswer = []
	for each in current_answer:
		if each== "A":
			convertedAnswer.append(1)
		if each== "B":
			convertedAnswer.append(2)
		if each== "C":
			convertedAnswer.append(3)
		if each== "D":
			convertedAnswer.append(4)
		if each== "X":
			convertedAnswer.append(999)
	return convertedAnswer

def scoreComputation(testid,answer):
	key = json.loads(TestAnswer.objects.get(test_id=testid).answer)
	ans = json.loads(answer)
	score = 0
	for i in range(len(key)):
		if ans[i] == -1:
			continue
		correct = True
		for each in key[i]:
			if each not in ans[i]:
				correct = False
		if correct:
			score+=1
	return score

def incorrectQuestionSet(testid,answer,score,keyConvertFun,ansConvertFun):
	key = keyConvertFun(json.loads(TestAnswer.objects.get(test_id=testid).answer))
	ans = ansConvertFun(json.loads(answer))
	score = int(score)
	incorrectQueSet = []
	incorrectAnsSet = []
	incorrectKeySet = []
	for i in range(len(key)):
		if key[i] != ans[i]:
			incorrectQueSet.append(i+1)
			incorrectAnsSet.append(ans[i])
			incorrectKeySet.append(key[i])
	return [incorrectQueSet,incorrectAnsSet,incorrectKeySet]

def redirect(request):
	return HttpResponseRedirect('http://webhost.engr.illinois.edu/~authorsys')

#index for local host
def index(request):
		tmp = 'Doe112@illinois.edu'
		uid = tmp.split('@')[0]
		user = authenticate(username=uid)

		if user is None:
			newStudent = User.objects.create_user(uid)
			newStudent.save()
			user = authenticate(username=uid)
			newStudent_data = UserData(user=uid)
			newStudent_data.psvtr_score = json.dumps(0)
			newStudent_data.psvtr_attempt = json.dumps(0)
			newStudent_data.save()

		auth_login(request, user)
		request.session['uid'] = uid
		return HttpResponseRedirect('../intro')

#index for hosting online
# def index(request):
# 	# check session uiuc-netid
# 	# if yes, do the following
# 	# else, redirect login page
# 	if request.session.get('netid', False):
# 		tmp = request.session['netid']
# 		uid = tmp.split('@')[0]
# 		user = authenticate(username=uid)
#
# 		# new student
# 		if user is None:
# 			# new student
# 			newStudent = User.objects.create_user(uid)
# 			newStudent_data.psvtr_score = json.dumps(0)
# 			newStudent_data.psvtr_attempt = json.dumps(0)
# 			newStudent.save()
# 			user = authenticate(username=uid)
# 			newStudent_data = UserData(user=uid)
# 			newStudent_data.save()
#
# 		auth_login(request, user)
# 		request.session['uid'] = uid
# 		return HttpResponseRedirect('../intro')
# 	else:
# 		return redirect('http://webhost.engr.illinois.edu/~authorsys')

#upload/download for drawing app
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

@csrf_exempt
def download(request):
	f = open('username_log.txt', 'r')
	fileContent = f.read()
	f.close()
	#print(fileContent)
	return HttpResponse(fileContent)

class Announcements(View):
	template_name = "announcements.html"
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

class IntroView(View):
	template_name = "intro.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		return render(request, self.template_name, {'uid': request.user.username})

#ClassName Survey
class SurveyView(View):
	template_name = "survey.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		return render(request, self.template_name, {'uid': request.user.username})

#Gender Survey
class Survey2View(View):
	template_name = "survey2.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		return render(request, self.template_name, {'uid': request.user.username})

class Survey3View(View):
	template_name = "survey3.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		return render(request, self.template_name, {'uid': request.user.username})


class Survey4View(View):
	template_name = "survey4.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		return render(request, self.template_name, {'uid': request.user.username})
		survey3 = json.loads( user_data.survey3answers)
		if survey3 == '1':
			return HttpResponseRedirect('/testsummary/')
		# if psvtr_attempt == '3':
		# 	return render(request, "error.html", {"error": "psvtrtaken"})

class Survey5View(View):
	template_name = "survey5.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		return render(request, self.template_name, {'uid': request.user.username})

class TestsummaryView(View):
	template_name = "survey3.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		return render(request, self.template_name, {'uid': request.user.username})


class PSVTRIntroView(View):
	template_name = "psvtrintro.html"
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		psvtr_score = UserData.objects.get(user=uid).psvtr_score
		psvtr_attempt = UserData.objects.get(user=uid).psvtr_attempt
		# start = UserData.objects.get(user=uid).test1_start
		# notes: one attempt
		# if test1_score != '0':
		# notes: allow three attempts
		if psvtr_attempt == '3':
			return render(request, "error.html", {"error": "psvtrtaken"})
		return render(request, self.template_name, {'uid': request.user.username, 'psvtr_score': psvtr_score, 'psvtr_attempt': psvtr_attempt})

class PSVTRTestView(View):
	template_name = "psvtrtest.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		psvtr_attempt = UserData.objects.get(user=uid).psvtr_attempt
		if psvtr_attempt == '3':
			return render(request, "error.html", {"error": "psvtrtaken"})
		return render(request, self.template_name, {'uid': request.user.username, 'psvtr_attempt': psvtr_attempt})

class PSVTRSummaryView(View):
	template_name = "psvtrsummary.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))

		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# psvtr
		psvtr_key = json.loads(TestAnswer.objects.get(test_id=1).answer)
		psvtr_ans = json.loads(user_data.psvtr_answers_last_attempt)
		psvtr_attempt = json.loads( user_data.psvtr_attempt)
		highest_score = json.loads(user_data.psvtr_score)
		psvtr_score = sum([psvtr_key[i] == psvtr_ans[i] for i in range(len(psvtr_key)) ])
		return render(request, self.template_name, {'uid': request.user.username,
			'psvtr_score': psvtr_score, 'highest_score': highest_score})

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


class TestView(View):
	template_name = "test.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		return render(request, self.template_name, {'uid': request.user.username})

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

		# test2
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


		return render(request, self.template_name, {'uid': request.user.username, 'week1c_ans': week1c_ans, 'week1a_correct': week1a_correct, 'week1b_correct': week1b_correct, 'week1c_correct': week1c_correct, 'week1_correct': week1_correct, 'week1_totaltime': week1_totaltime})

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


class GradebookView(View):
	template_name = "gradebook.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		uid = request.user.username
		user_data = UserData.objects.get(user=uid)

		try:
		 mrttestscore = json.loads( user_data.mrttestscore)
	 	except:
		 mrttestscore = "_"


		return render(request, self.template_name, {'uid': request.user.username, 'mrttestscore':mrttestscore})

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

		uid = request.user.username
		user_data = UserData.objects.get(user=uid)
		# save the time when they start the tests
		print("1111111")
		print(action)
		print(path)
		# if action == "LOAD" and path == "/psvtrtest/":
		# 	user_data.psvtr_start = time
		# elif action == "LOAD" and path == "/spatialtest/test2/":
		# 	user_data.test2_start = time
		# elif action == "LOAD" and path == "/spatialtest/posttest1/":
		# 	user_data.posttest1_start = time
		if action == "LOAD" and path == "/spatialtest/test/":
			user_data.mrt_start = time
		elif action == "MRTTIME":
			start=user_data.mrt_start
			end = time
			interval = end-start
			user_data.mrttime= str(interval)
		# store answers
		# if action == "PSVTR_ATTEMPT":
		# 	user_data.psvtr_attempt = msg
		# if action == "PSVTR_ANSWER":
		# 	highest_score = user_data.psvtr_score
		# 	psvtr_score = scoreComputation(1,msg)
		# 	if psvtr_score >= int(highest_score):
		# 		user_data.psvtr_answers = msg
		# 		user_data.psvtr_score = psvtr_score
		# 		user_data.psvtr_totaltime=time-user_data.psvtr_start
		# 	user_data.psvtr_answers_last_attempt = msg
		# elif action == "ANSWER2":
		# 	user_data.test2answers = msg
		if action == "SURVEY1":
			user_data.survey1answers = msg
		elif action == "SURVEY2":
			user_data.survey2answers = msg
		elif action == "SURVEY3":
			user_data.survey3answers = msg
		elif action == "SURVEY4":
			user_data.survey4answers = msg
		# elif action == "POSTANSWER1":
		# 	user_data.posttest1answers = msg
		# elif action == "POSTSURVEY1":
		# 	user_data.postsurvey1answers = msg
		# elif action == "POSTSURVEY2":
		# 	user_data.postsurvey2answers = msg
		# elif action == "POSTTEST1":
		# 	user_data.posttest1score = msg
		elif action == "MRTTEST":
			user_data.mrttestanswers = msg
			user_data.mrttestscore = str(scoreComputation(1,msg))
			# user_data.mrttesttime = time - user_data.week3a_start

		logs = json.loads(user_data.log)
		logs.append(record)
		user_data.log = json.dumps(logs)
		user_data.save()
		return render(request, self.template_name)
