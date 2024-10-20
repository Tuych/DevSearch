from django.db import models
from users.models import Profile


class Projects(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    featured_image = models.ImageField(default="default.jpg", upload_to="projects/%Y/%m/%d")
    demo_link = models.CharField(max_length=200, blank=True)
    source_link = models.CharField(max_length=200, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, blank=True)
    vote_ratio = models.IntegerField(default=0, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']   # proectlar teskari tartibda chiqadi, agar ulat teng bulsa title tartibida chiqadi

    def reviewers(self):  # Review tableadn hamma ownerlarning idsini list kurinishida oldik
        queryset = self.review_set.all().values_list('owner__id', flat=True) # bu bilan biz user coment yozgan bulsa uni tekshiramiz va comentga shu orqali shart beramiz
        return queryset

    def get_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value='up').count()
        total_votes = reviews.count()

        ratio = up_votes / total_votes * 100
        self.vote_total = total_votes
        self.vote_ratio = ratio

        self.save()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    value = models.CharField(max_length=20, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value

    class Meta:
        unique_together = [['owner', 'project']]    # 1 ta owner 1 ta ptojectga comment yoza oladi


"""
 classlar haqida qisqacha
 
 1.     featured_image = models.ImageField(default="default.jpg", upload_to="projects/%Y/%m/%d")
    rasm kursatilgan dek projects/%Y/%m/%d - papkaning ichiga sanalat bilan saqlanadi
    agar rasm bulmasa default tanlangan rasm joylashadi

2. Agar ulamoqchi bulgan classimiz pasta bulsa uni ' ' ichiga qozib quysak buladi
    tags = models.ManyToManyField('Tag', blank=True)

"""