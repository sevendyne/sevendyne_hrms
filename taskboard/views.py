import datetime
import json
from os import name
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from main.decorators import company_required
from taskboard.forms import ProjectForm
from taskboard.models import Project
from main.functions import generate_form_errors, get_a_id, get_auto_id, get_current_company, has_hrms_permission
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.core.paginator import Paginator


# Project crud starts here
@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def create_project(request):
    current_company = get_current_company(request)   
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            priority = form.cleaned_data['priority']
            project_leader = form.cleaned_data['project_leader']
            team = form.cleaned_data['team']
            file = form.cleaned_data['file']
            description = form.cleaned_data['description']
            auto_id = get_auto_id(Project)
            a_id = get_a_id(Project,request)
            creator = request.user
            updator = request.user

            if not Project.objects.filter(name = name,company=current_company,is_deleted=False).exists():
                Project(
                    name = name,
                    start_date = start_date,
                    end_date = end_date,
                    company = current_company,
                    priority = priority,
                    project_leader = project_leader,
                    team = team,
                    file = file,
                    description = description,
                    auto_id = auto_id,
                    a_id = a_id,
                    creator = creator,
                    updator = updator                    
                ).save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Project created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('taskboard:projects')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Project already exists",                        
                }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "form_error",
                "title": "Form validation error",
                "message": str(message),               
            }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = ProjectForm()
        context = {
            "title": "Create Project",
            "form": form,
            "redirect": "true",
            "create":True
        }        
        return render(request, "project/projects.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def projects(request):
    current_company = get_current_company(request)
    projects = Project.objects.filter(company=current_company,is_deleted=False)
    paginator = Paginator(projects,1000000000000)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    context = {
        'projects': projects,
        "title": 'Projects' 
    }
    return render(request, "project/projects.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
def edit_project(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Project.objects.filter(pk=pk,ompany=current_company,is_deleted=False))    
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Project updated successfully.",                
                "redirect_url": reverse('taskboard:projects')
            }

        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "false",
                "message": str(message),
                "title": "Form validation error"  
            }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = ProjectForm(instance=instance)       
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Project :" + instance.name,            
            "redirect": "true",
            "url": reverse('taskboard:edit_project', kwargs={'pk': instance.pk})
        }
        return render(request, 'project/projects.html', context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
def project(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Project.objects.filter(pk=pk,company=current_company,is_deleted=False))
    context = {
        'instance': instance,
        'title': 'Project'
    }
    return render(request, "project/projects.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
def delete_project(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Project.objects.filter(pk=pk,company=current_company,is_deleted=False))    
    Project.objects.filter(pk=pk).update(is_deleted=True,name=instance.name + "_deleted_" + str(instance.auto_id))
    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Project Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('taskboard:projects')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')


# Task crud starts here
# @login_required
# @user_passes_test(has_hrms_permission, redirect_field_name=None)
# @company_required
# def create_task(request): 
#     current_company = get_current_company(request)  
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             priority = form.cleaned_data['priority']
#             due_date = form.cleaned_data['due_date']
#             description = form.cleaned_data['description']
#             employee = form.cleaned_data['employee']
#             project = form.cleaned_data['project']
#             attachment = form.cleaned_data['attachment']
#             auto_id = get_auto_id(Task)
#             a_id = get_a_id(Task,request)
#             creator = request.user
#             updator = request.user

#             if not Task.objects.filter(name = name,is_deleted=False).exists():
#                 Task(
#                     company = current_company,
#                     name = name,
#                     priority = priority,
#                     due_date = due_date,
#                     description = description,
#                     employee = employee,
#                     project = project,
#                     attachment = attachment,
#                     auto_id = auto_id,
#                     a_id = a_id,
#                     creator = creator,
#                     updator = updator
#                 ).save()
#                 response_data = {
#                     "status": "true",
#                     "title": "Successfully Created",
#                     "message": "Task created successfully.",
#                     "redirect": "true",
#                     "redirect_url": reverse('task:tasks')
#                 }
#             else:               
#                 response_data = {
#                     "status": "false",
#                     "stable": "true",
#                     "title": "Already exists",
#                     "message": "Task already exists",                        
#                 }
#         else:
#             message = generate_form_errors(form, formset=False)
#             response_data = {
#                 "stable": "true",
#                 "status": "form_error",
#                 "title": "Form validation error",
#                 "message": str(message),               
#             }
#         return HttpResponse(json.dumps(response_data), content_type='application/json')
#     else:
#         form = TaskForm()
#         context = {
#             "title": "Create Task",
#             "form": form,
#             "redirect": "true",
#             "create":True
#         }        
#         return render(request, "task/tasks.html", context)
    

# @login_required
# @user_passes_test(has_hrms_permission, redirect_field_name=None)
# @company_required
# def tasks(request):
#     current_company = get_current_company(request)
#     tasks = Task.objects.filter(company=current_company,is_deleted=False)
#     paginator = Paginator(tasks,1000000000000)
#     page_number = request.GET.get('page')
#     tasks = paginator.get_page(page_number)
#     context = {
#         'tasks': tasks,
#         "title": 'Tasks' 
#     }
#     return render(request, "task/tasks.html", context)


# @login_required
# @user_passes_test(has_hrms_permission, redirect_field_name=None)
# @company_required
# def edit_task(request, pk):
#     current_company = get_current_company(request)
#     instance = get_object_or_404(Task.objects.filter(pk=pk,company=current_company, is_deleted=False))    
#     if request.method == "POST":
#         form = TaskForm(request.POST, instance=instance)
#         if form.is_valid():
#             data = form.save(commit=False)
#             data.updator = request.user
#             data.date_updated = datetime.datetime.now()
#             data.save()
#             response_data = {
#                 "status": "true",
#                 "redirect" : "true",
#                 "title": "Successfully Updated",
#                 "message": "Task updated successfully.",                
#                 "redirect_url": reverse('task:tasks')
#             }
#         else:
#             message = generate_form_errors(form, formset=False)
#             response_data = {
#                 "stable": "true",
#                 "status": "false",
#                 "message": str(message),
#                 "title": "Form validation error"  
#             }
#         return HttpResponse(json.dumps(response_data), content_type='application/json')
#     else:
#         form = TaskForm(instance=instance)       
#         context = {
#             "form": form,
#             "instance": instance,
#             "title": "Edit Task :" + instance.name,            
#             "redirect": "true",
#             "url": reverse('task:edit_task', kwargs={'pk': instance.pk})
#         }
#         return render(request, "task/tasks.html", context)
    

# @login_required
# @user_passes_test(has_hrms_permission, redirect_field_name=None)
# @company_required
# def task(request,pk):
#     current_company = get_current_company(request)
#     instance = get_object_or_404(Task.objects.filter(pk=pk,company=current_company,is_deleted=False))
#     context = {
#         'instance': instance,
#         'title': 'Task'
#     }
#     return render(request, "task/tasks.html", context)


# @login_required
# @user_passes_test(has_hrms_permission, redirect_field_name=None)
# @company_required
# def delete_task(request,pk):
#     current_company = get_current_company(request)
#     instance = get_object_or_404(Task.objects.filter(pk=pk,company=current_company,is_deleted=False))    
#     Task.objects.filter(pk=pk).update(is_deleted=True,name=instance.name + "_deleted_" + str(instance.auto_id))
#     response_data = {
#         "status" : "true",        
#         "title" : "Successfully Deleted",
#         "message" : "Task Successfully Deleted.", 
#         "redirect" : "true",       
#         "redirect_url" : reverse('task:tasks')
#     }
#     return HttpResponse(json.dumps(response_data), content_type='application/json')
   


#tasklist views



# def create_tasklist(request):
   
#     if request.method == 'POST':
#         form = TasklistForm(request.POST)
#         if form.is_valid():
#             company = form.cleaned_data['company']
#             name = form.cleaned_data['name']
            
#             auto_id = get_auto_id(TasklistForm)
#             creator = request.user
#             updator = request.user

#             if not Tasklist.objects.filter(name = name,is_deleted=False).exists():
#                 Tasklist(
#                     company = company,
#                     name=name,
#                     auto_id = auto_id,
#                     creator = creator,
#                     updator = updator

#                 ).save()
#                 response_data = {
#                     "status": "true",
#                     "title": "Successfully Created",
#                     "message": "Task List created successfully.",
#                     "redirect": "true",
#                     "redirect_url": reverse('tasklist:tasklists')
#                 }
#             else:               
#                 response_data = {
#                     "status": "false",
#                     "stable": "true",
#                     "title": "Already exists",
#                     "message": "Task List already exists",                        
#                 }
#         else:
#             message = generate_form_errors(form, formset=False)
#             response_data = {
#                 "stable": "true",
#                 "status": "form_error",
#                 "title": "Form validation error",
#                 "message": str(message),               
#             }
#         return HttpResponse(json.dumps(response_data), content_type='application/json')
#     else:
#         form = TasklistForm()
#         context = {
#             "title": "Create Tasklist",
#             "form": form,
#             "redirect": "true",
#             "create":True
#         }
        
#         return render(request, 'task-board.html', context)


# def tasklists(request):
#     tasklists = TasklistForm.objects.filter(is_deleted=False)
#     paginator = Paginator(tasklists,1000000000000)
#     page_number = request.GET.get('page')
#     tasklists = paginator.get_page(page_number)
#     context = {
#         'tasklists': tasklists,
#         "title": 'Tasklists' 
#     }
#     return render(request, "task-board.html", context)



# def edit_tasklist(request, pk):
#     instance = get_object_or_404(Tasklist.objects.filter(pk=pk, is_deleted=False))    
#     if request.method == "POST":
#         form = TasklistForm(request.POST, instance=instance)

#         if form.is_valid():
#             data = form.save(commit=False)
#             data.updator = request.user
#             data.date_updated = datetime.datetime.now()
#             data.save()

#             response_data = {
#                 "status": "true",
#                 "redirect" : "true",
#                 "title": "Successfully Updated",
#                 "message": "TaskList updated successfully.",                
#                 "redirect_url": reverse('tasklist:tasklists')
#             }

#         else:
#             message = generate_form_errors(form, formset=False)

#             response_data = {
#                 "stable": "true",
#                 "status": "false",
#                 "message": str(message),
#                 "title": "Form validation error"  
#             }

#         return HttpResponse(json.dumps(response_data), content_type='application/json')
#     else:
#         form = TasklistForm(instance=instance)
       
#         context = {
#             "form": form,
#             "instance": instance,
#             "title": "Edit Task List :" + instance.da,
            
#             "redirect": "true",
#             "url": reverse('tasklist:edit_tasklist', kwargs={'pk': instance.pk}),

#         }
#         return render(request, 'task-board.html', context)


# def tasklist(request,pk):
#     instance = get_object_or_404(Tasklist.objects.filter(pk=pk,is_deleted=False))

#     context = {
#         'instance': instance,
#         'title': 'Tasklist',

#     }
#     return render(request, "task-board.html", context)




# def delete_tasklist(request,pk):
#     instance = get_object_or_404(Tasklist.objects.filter(pk=pk,is_deleted=False))
    
#     Tasklist.objects.filter(pk=pk).update(is_deleted=True,da=instance.da + "_deleted_" + str(instance.auto_id))

#     response_data = {
#         "status" : "true",        
#         "title" : "Successfully Deleted",
#         "message" : "Task List Successfully Deleted.", 
#         "redirect" : "true",       
#         "redirect_url" : reverse('tasklist:tasklists')
#     }
#     return HttpResponse(json.dumps(response_data), content_type='application/json')
   

#taskcomment views



# def create_taskcomment(request):
   
#     if request.method == 'POST':
#         form = TaskcommentForm(request.POST)
#         if form.is_valid():
#             company = form.cleaned_data['company']
#             employee = form.cleaned_data['employee']
#             task = form.cleaned_data['task']
#             comment = form.cleaned_data['comment']
#             image = form.cleaned_data['image']
#             file = form.cleaned_data['file']

#             auto_id = get_auto_id(TaskcommentForm)
#             creator = request.user
#             updator = request.user

#             if not Taskcomment.objects.filter(name = name,is_deleted=False).exists():
#                 Taskcomment(
#                     company = company,
#                     employee = employee,
#                     task = task,
#                     comment = comment,
#                     image = image,
#                     file = file,
                    
#                     auto_id = auto_id,
#                     creator = creator,
#                     updator = updator

#                 ).save()
#                 response_data = {
#                     "status": "true",
#                     "title": "Successfully Created",
#                     "message": "Task Comment created successfully.",
#                     "redirect": "true",
#                     "redirect_url": reverse('taskcomment:taskcomments')
#                 }
#             else:               
#                 response_data = {
#                     "status": "false",
#                     "stable": "true",
#                     "title": "Already exists",
#                     "message": "Task Comment already exists",                        
#                 }
#         else:
#             message = generate_form_errors(form, formset=False)
#             response_data = {
#                 "stable": "true",
#                 "status": "form_error",
#                 "title": "Form validation error",
#                 "message": str(message),               
#             }
#         return HttpResponse(json.dumps(response_data), content_type='application/json')
#     else:
#         form = TaskcommentForm()
#         context = {
#             "title": "Create Taskcomment",
#             "form": form,
#             "redirect": "true",
#             "create":True
#         }
        
#         return render(request, 'task-board.html', context)


# def taskcomments(request):
#     taskcomments = TaskcommentForm.objects.filter(is_deleted=False)
#     paginator = Paginator(taskcomments,1000000000000)
#     page_number = request.GET.get('page')
#     taskcomments = paginator.get_page(page_number)
#     context = {
#         'taskcomments': taskcomments,
#         "title": 'Taskcomments' 
#     }
#     return render(request, "task-board.html", context)



# def edit_taskcomment(request, pk):
#     instance = get_object_or_404(Taskcomment.objects.filter(pk=pk, is_deleted=False))    
#     if request.method == "POST":
#         form = TaskcommentForm(request.POST, instance=instance)

#         if form.is_valid():
#             data = form.save(commit=False)
#             data.updator = request.user
#             data.date_updated = datetime.datetime.now()
#             data.save()

#             response_data = {
#                 "status": "true",
#                 "redirect" : "true",
#                 "title": "Successfully Updated",
#                 "message": "Taskcomment updated successfully.",                
#                 "redirect_url": reverse('taskcomment:taskcomments')
#             }

#         else:
#             message = generate_form_errors(form, formset=False)

#             response_data = {
#                 "stable": "true",
#                 "status": "false",
#                 "message": str(message),
#                 "title": "Form validation error"  
#             }

#         return HttpResponse(json.dumps(response_data), content_type='application/json')
#     else:
#         form = TaskcommentForm(instance=instance)
       
#         context = {
#             "form": form,
#             "instance": instance,
#             "title": "Edit Task Comment :" + instance.da,
            
#             "redirect": "true",
#             "url": reverse('taskcomment:edit_taskcomment', kwargs={'pk': instance.pk}),

#         }
#         return render(request, 'task-board.html', context)


# def taskcomment(request,pk):
#     instance = get_object_or_404(Taskcomment.objects.filter(pk=pk,is_deleted=False))

#     context = {
#         'instance': instance,
#         'title': 'Taskcomment',

#     }
#     return render(request, "task-board.html", context)




# def delete_taskcomment(request,pk):
#     instance = get_object_or_404(Taskcomment.objects.filter(pk=pk,is_deleted=False))
    
#     Taskcomment.objects.filter(pk=pk).update(is_deleted=True,da=instance.da + "_deleted_" + str(instance.auto_id))

#     response_data = {
#         "status" : "true",        
#         "title" : "Successfully Deleted",
#         "message" : "Task Comment Successfully Deleted.", 
#         "redirect" : "true",       
#         "redirect_url" : reverse('taskcomment:taskcomments')
#     }
#     return HttpResponse(json.dumps(response_data), content_type='application/json')
   
