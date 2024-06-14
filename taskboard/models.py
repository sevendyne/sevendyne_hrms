from django.db import models
from main.models import BaseModel
from django.utils.translation import gettext_lazy as _


PRIORITY_CHOICES = (
    ('Low', "Low"),
    ('Normal',"Normal"),
    ('High',"High")
)


class Project(BaseModel):
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
    name = models.CharField(_("Project Name"),max_length=125)
    start_date = models.DateField(_('Start Date'),help_text='start date', null=True, blank=True)
    end_date = models.DateField(_('End Date'),help_text='end date')
    priority = models.CharField(max_length=128, choices=PRIORITY_CHOICES, default='Normal', null=True, blank=True)
    project_leader = models.CharField(_("Project Leader"),max_length=125, null=True, blank=True)
    team = models.ManyToManyField("employee.Employee", verbose_name=_("Team"))
    file = models.FileField(upload_to='files/', null=True, blank=True)
    description = models.TextField(_("Description "),null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['name']
    
    def __str__(self):
        return self.name


# class Task(BaseModel):
#     company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})   
#     employee = models.ForeignKey("employee.Employee",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})  
#     project = models.ForeignKey("taskboard.Project",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
#     name = models.CharField(_("Task Name"),max_length=125)
#     priority = models.CharField(max_length=128,choices=PRIORITY_CHOICES,default='Normal',null=True,blank=True)
#     due_date = models.DateField(_('Due Date'),help_text='due_date',null=True,blank=True) 
#     description = models.TextField(_("Description "),null=True,blank=True)
#     attachment = models.FileField(upload_to='files/',null=True,blank=True)   
#     is_deleted = models.BooleanField(default=False)

#     class Meta:
#         verbose_name = _('Task')
#         verbose_name_plural = _('Tasks')
#         ordering = ['name']
    
#     def __str__(self):
#         return self.name



# class TaskComment(BaseModel):
#     company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})  
#     employee = models.ForeignKey("main.Employee",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
#     task = models.ForeignKey("main.Task",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
#     comment = models.TextField(_("Comment "),null=True, blank=True)
#     image = models.ImageField(_("Image"), upload_to='task_comment_images/', null=True, blank=True)
#     file = models.FileField(upload_to='files/', null=True, blank=True)
#     is_deleted = models.BooleanField(default=False)

#     class Meta:
#         verbose_name = _('TaskComment')
    
#     def __str__(self):
#         return self.comment