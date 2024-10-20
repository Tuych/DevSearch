""" utils.py da asosan qidiruv tizimi funksiyalari yozilafi"""
from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_profiles(request, pr, result):
    page = request.GET.get('page')
    # result = 3
    paginator = Paginator(pr, result)  # yani pr db dan keladigan malumotlar har 1 sahifada 3 ta bulib chiqsin

    try:
        pr = paginator.page(page)
    except PageNotAnInteger:  # Agar kimdir bravzerdagi urlga ?page dan kiyin text kiritishga urinsa  PageNotAnInteger xatolikni oldini oladi va 1-sahifaga otib yuboradi
        page = 1
        pr = paginator.page(page)
    except EmptyPage:  # Agar kimdir yuq sonni page ga kiritsa  EmptyPage avtanmatik ravishda ohirgi qarotga otib yuboradi va xatolikni oldi olinadi
        page = paginator.num_pages  # oxirgi raqam
        pr = paginator.page(page)

    right_index = int(page) + 5

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    left_index = int(page) - 4
    if left_index < 1:
        left_index = 1

    custom_range = range(left_index, right_index)

    return custom_range, pr


def search_profile(request):
    search_query = ''

    if request.GET.get('search_query'):  # agar inputdan qiymat kelsagina
        search_query = request.GET.get('search_query')  # search query shu qiymatga teng buladi
        # icontains katta kichik harflarga sezgir emas

    skills = Skill.objects.filter(
        name__iexact=search_query)  # iexact - suz hammasi aniq mos kelganini chiqarib beradi katta kichik harflarga sezgir emas

    prof = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |  # search query bulsa shunga mosa suzlar qidiriladi huddi LIKE operatori kabi bulmasa hamm malumotni chiqarib beradi
        Q(short_intro__icontains=search_query) |  # Q yoki degani va uni kup maratoba ishlatish mumkin
        Q(skill__in=skills))  # skill abratniy svyazga uxshab qidiriladi

    return prof, search_query

