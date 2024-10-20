from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Skill
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # messages xabarlarni yoki xatoliklarni bravzerda kursatib beradi
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.db.models import Q   # Q  or operatorini ishlarish uchun
from .utils import search_profile, paginate_profiles


def profiles(request):
    prof, search_query = search_profile(request)  # funksiya 2 ta qiymat qaytarganligi uchun 2 ta uzgaruvchi yozildi

    custom_range, prof = paginate_profiles(request, prof, 3)

    context = {
        'profiles': prof,
        'search_query': search_query,
        'custom_range': custom_range
    }
    return render(request, 'users/index.html', context)


def user_profile(request, pk):
    prof = Profile.objects.get(id=pk)

    top_skills = prof.skill_set.exclude(description__exact='')

    other_skills = prof.skill_set.filter(description='')

    context = {'profile': prof,
               'top_skills': top_skills,
               'other_skills': other_skills,
               }
    return render(request, 'users/profile.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request,
                           "Username does not exist")  # message.error() xatolik haqida xabarni brawzerga chiqarib beradi

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, 'users/login_register.html')


def logaut_user(request):
    logout(request)  # logaut foydalanuvchini uchotniy zapisdan chiqarib yuboradi
    messages.info(request, 'User was logged out!')  # user logaut qilingani haqida malumot beradi
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'An error has occurred during registration')
    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'users/login_register.html', context)


@login_required(
    login_url='login')  # foydalanuvchi ruyhatdan utmagan bulsa va accountga bossa login url orqali login sahifasiga utib ketadi
def user_account(request):
    prof = request.user.profile  # user haqida malumotni request orqali olsa ham buladi
    skills = prof.skill_set.all()  # skill clasasi profile bilan abratniy svyaz bulib boglanganu uchun shu tarrzda oldik
    projects = prof.projects_set.all()  # abratniy svyaz

    context = {
        'profile': prof,
        'skills': skills,
        'projects': projects
    }

    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile  # User Profile modeli bilan One TO One boglanganu uchun request orqali user malumotlarini qulga kiritdik
    form = ProfileForm(instance=profile)  # User malumotlari formada kurinib turadi

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # request.FILES rasmlarni yuklab olish uchun
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')  # nimaga har 1 funcsiyaga decorator berib chiqyabmiz
def create_skill(request):  # chunki urlname orqali har bir funksiyaga dostup olsa buladi
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile  # qushilmagan owner qismini qushib quydik
            skill.save()
            messages.success(request, 'Skill was added successfully')
            return redirect('account')
    context = {
        'form': form
    }

    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile  # userga tegishli profileni olib oldik
    skill = profile.skill_set.get(id=pk)  # profilega tegishli skillni olob oldik
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully')
            return redirect('account')

    context = {
        'form': form,
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully')
        return redirect('account')

    context = {'objects': skill}
    return render(request, 'users/delete.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    message_requests = profile.messages.all()  # abratniy svyaz yani Message clasidagi recipient ustunida related_name=messages yozilganu uchun abratniy svyaz qila oldik
    unread_count = message_requests.filter(is_read=False).count()  #uqilmagan habarlarni olish
    context = {
        'message_requests': message_requests,
        'unread_count': unread_count,
    }
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)  # abratniy svyaz
    if message.is_read is False:
        message.is_read = True
        message.save()  # Agar message uqilmagan bulsa uni uqilgan qilib quyamiz shunda still uqilgan qilib kursatadi
    context = {
        'message': message
    }
    return render(request, 'users/message.html', context)


def create_message(request, pk):       # bu yerda pk=sms borayotgan developer id si
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Your message was successfully sent!')
            return redirect('user_profile', pk=recipient.id)
    context = {
        'recipient': recipient,
        'form': form,
    }

    return render(request, 'users/message_form.html', context)