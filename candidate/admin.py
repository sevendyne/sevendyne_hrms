from django.contrib import admin
from candidate.models import Intern, Candidate

class InternAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  

admin.site.register(Intern, InternAdmin) 


class CandidateAdmin(admin.ModelAdmin):
    exclude = ('is_deleted',)  

admin.site.register(Candidate, CandidateAdmin) 