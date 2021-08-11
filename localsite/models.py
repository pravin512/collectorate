'''Users Model'''
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MinLengthValidator

class AdhikariList(models.Model):
    '''User Model'''
    adhikari_id = models.AutoField(db_column='FLD_ADHIKARI_ID', primary_key=True)  
    adhikari_name = models.CharField(db_column='FLD_ADHIKARI_NAME', max_length=50, validators=[MinLengthValidator(2)])
    type = models.CharField(db_column='FLD_TYPE', max_length=50, null=True)
    mobile = models.IntegerField(db_column='FLD_MOBILE', null=True)
    designation = models.CharField(db_column='FLD_DESIGNATION', max_length=50, validators=[MinLengthValidator(2)], null=True)
    url = models.CharField(db_column='FLD_URL', max_length=256, validators=[MinLengthValidator(2)], null=True)
    created_by = models.ForeignKey(User, db_column='FLD_CREATED_BY', on_delete=models.CASCADE, null=True)
    added_date_time = models.DateTimeField(db_column='FLD_ADDED_DATE_TIME', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True,db_column='FLD_UPDATED_DATE_TIME')
    status = models.PositiveSmallIntegerField(db_column='FLD_STATUS', default=1)  
   
    class Meta:
        managed = True
        db_table = 'ADHIKARI_LIST'

    def __str__(self):
        return self.adhikari_name

class MeetingDetails(models.Model):
    '''Meeting List'''
    meeting_id = models.AutoField(db_column='FLD_MEETING_ID', primary_key=True)  
    adhikari_id = models.ForeignKey(AdhikariList, db_column='FLD_ADHIKARI_ID', on_delete=models.CASCADE)
    marking_date = models.DateTimeField(db_column='FLD_MARKING_DATE', editable=False)
    time_limit_date = models.DateTimeField(db_column='FLD_TIME_LIMIT_DATE', editable=False)
    description =models.TextField(db_column='FLD_INSTRUCTION',blank=True, null=True,verbose_name="Meeting Description")
    url = models.CharField(db_column='FLD_URL', max_length=256, validators=[MinLengthValidator(2)], null=True)
    added_date_time = models.DateTimeField(db_column='FLD_ADDED_DATE_TIME', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True,db_column='FLD_UPDATED_DATE_TIME')
    status = models.PositiveSmallIntegerField(db_column='FLD_STATUS', default=1) 

    class Meta:
        managed = True
        db_table = 'meeting_details'

    def __str__(self):
        return self.description