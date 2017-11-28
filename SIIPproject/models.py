from django.db import models
from django.contrib.auth.models import User


# Create your models here.
#class User(models.Model):
#	name = models.CharField(max_length=200)
#	def __unicode__(self):
#		return self.name


class UserData(models.Model):
	user = models.CharField(max_length=200)
	# psvtr_attempt = models.TextField()
	# psvtr_answers = models.TextField()
	# psvtr_start = models.DateTimeField(null=True)
	# psvtr_answers_last_attempt = models.TextField()
	# psvtr_totaltime = models.TextField(null=True)
	# psvtr_score = models.TextField()
	survey1answers = models.TextField()
	survey2answers = models.TextField()
	survey3answers = models.TextField()
	survey4answers = models.TextField()

# test(MRT) Data
	mrt_start = models.DateTimeField(null=True)
	mrttesttime = models.TextField()
	mrttestanswers = models.TextField()
	mrttestscore = models.TextField()

	test1_start = models.DateTimeField(null=True)
	log = models.TextField(default="[]")
	# totaltime should be Text
	# start/end time should be DateTime


class TestAnswer(models.Model):
	test_id = models.IntegerField()
	answer = models.TextField()
