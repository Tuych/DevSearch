from django.db.models import Q
from .models import Projects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_projects(request, pr, result):
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


def search_project(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    pr = Projects.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query)
        # owner profile bilan boglangani uchun proect egasini profile name orqali qidiradi pryamoy svyaz orqali
    )

    return pr, search_query
