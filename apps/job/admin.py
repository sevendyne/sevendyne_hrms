from django.contrib import admin
from apps.job.models import CandidateInterview, CandidateJob, Job, JobApplicant



class JobAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(Job, JobAdmin) 


admin.site.register(CandidateJob)

admin.site.register(CandidateInterview)

class JobApplicantAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(JobApplicant, JobApplicantAdmin) 