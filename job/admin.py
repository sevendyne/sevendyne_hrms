from django.contrib import admin
from job.models import CandidateInterview, CandidateJob, Job, JobApplicant



class JobAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(Job, JobAdmin) 


class CandidateJobAdmin(admin.ModelAdmin):
    exclude = ('is_deleted')  
admin.site.register(CandidateJob, CandidateJobAdmin) 


class CandidateInterviewAdmin(admin.ModelAdmin):
    exclude = ('is_deleted')  
admin.site.register(CandidateInterview, CandidateInterviewAdmin) 


class JobApplicantAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(JobApplicant, JobApplicantAdmin) 