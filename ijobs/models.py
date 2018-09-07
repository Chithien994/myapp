import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

@python_2_unicode_compatible
class IJob(models.Model):
	user 		= models.ForeignKey(get_user_model(), related_name='ijobs', on_delete=models.CASCADE)
	name		= models.CharField(max_length=80, blank=True, null=True)
	content 	= models.CharField(max_length=200, blank=True, null=True, default='')
	time 		= models.IntegerField(validators=[MaxValueValidator(999), MinValueValidator(0)], blank=True, null=True, default=0)
	begin_date 	= models.DateTimeField('Begin Date', auto_now_add=False, editable=True)
	end_date 	= models.DateTimeField('End Date', auto_now_add=False, editable=True)
		
	def __str__(self):
		return 'IJob #%s' % self.pk

	class Meta:
		db_table 			= 'ijobs'
		verbose_name_plural = 'IJobs'