from django.shortcuts import render, redirect
from .models import Projects
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import search_project, paginate_projects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages


def projects(request):
    pr, search_query = search_project(request)
    custom_range, pr = paginate_projects(request, pr, 3)

    context = {
        'projects': pr,
        'search_query': search_query,
        'custom_range': custom_range,
        }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project_obj = Projects.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()

        project_obj.get_vote_count()

        messages.success(request, 'Your review was succesfully submited')
        return redirect('project', pk=project_obj.id)  # redirectga dinamik url name berilsa pk ham berilishi shart

    context = {
        'project': project_obj,
        'form': form
    }
    return render(request, 'projects/single-project.html', context)


@login_required(login_url='login')     # foydalanubchi shu sahifaga kirishga urinsa name=login bo'lgan url sahivasiga utib ketadi
def create_project(request):
    profile = request.user.profile # Profile PRoject bilan owner columni orqali boglangan
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)  # request.FILES = rasm yoki fayllarni tugri yuklash uchun
        if form.is_valid():                              #  form.is_valid() formadagi malumotlar tugri kiritilganini tekshirib beradi
            project = form.save(commit=False)
            project.owner = profile    # ownerni avtamatik ravishda qushish
            project.save()
            return redirect('account')
    context = {
        'form': form
    }

    return render(request, 'projects/form-template.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.projects_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {
        'project': project,
        'form': form
    }
    return render(request, 'projects/form-template.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.projects_set.get(id=pk)  # yani profile clasi Projects clasiga abratniy svyaz bulib boglangan

    if request.method == 'POST':
        project.delete()
        return redirect('account')

    context = {
        'object': project
    }

    return render(request, 'projects/delete.html', context)