from django.urls import path, re_path
from taskboard import views

urlpatterns = [    
    path('project/create/', views.create_project, name='create_project'),
    path("projects/", views.projects, name="projects"),
    path("projects-list/", views.projects_list, name="projects_list"),
    re_path(r'^project/edit/(?P<pk>.*)/$', views.edit_project, name='edit_project'),
    re_path(r'^delete-project/(?P<pk>.*)/$', views.delete_project, name='delete_project'),    
    re_path(r'^project/(?P<pk>.*)/$', views.project, name='project')

    path('task-board/create/', views.create_task_board, name='create_task_board'),
    path("task-boards/", views.task_boards, name="task_boards"),
    re_path(r'^task-board/edit/(?P<pk>.*)/$', views.edit_task_board, name='edit_task_board'),
    re_path(r'^delete-task-board/(?P<pk>.*)/$', views.delete_task_board, name='delete_task_board'),    
    re_path(r'^task-board/(?P<pk>.*)/$', views.task_board, name='task_board')
    

    # path('task/create/', views.create_task, name='create_task'),
    # path("tasks/", views.tasks, name="tasks"),
    # re_path(r'^task/edit/(?P<pk>.*)/$', views.edit_task, name='edit_task'),
    # re_path(r'^delete-task/(?P<pk>.*)/$', views.delete_task, name='delete_task'),    
    # re_path(r'^task/(?P<pk>.*)/$', views.task, name='task'),
    
    
    # path('tasklist/create/', views.create_tasklist, name='create_tasklist'),
    # path("tasklists/", views.tasklists, name="tasklists"),
    # re_path(r'^tasklist/edit/(?P<pk>.*)/$', views.edit_tasklist, name='edit_tasklist'),
    # re_path(r'^delete-tasklist/(?P<pk>.*)/$', views.delete_tasklist, name='delete_tasklist'),    
    # re_path(r'^tasklist/(?P<pk>.*)/$', views.tasklist, name='tasklist'),

    # path('taskcomment/create/', views.create_taskcomment, name='create_taskcomment'),
    # path("taskcomments/", views.taskcomments, name="taskcomments"),
    # re_path(r'^taskcomment/edit/(?P<pk>.*)/$', views.edit_taskcomment, name='edit_taskcomment'),
    # re_path(r'^delete-taskcomment/(?P<pk>.*)/$', views.delete_taskcomment, name='delete_taskcomment'),    
    # re_path(r'^taskcomment/(?P<pk>.*)/$', views.taskcomment, name='taskcomment')

]
