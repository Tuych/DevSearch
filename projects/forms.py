from django.forms import ModelForm
from .models import Projects, Review
from django import forms


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place you vote',
            'body': 'Add a comments with your vote'
        }

    def __init__(self, *args,
                 **kwargs):  # tepadagi classga ulandik super() orqali va init funksiya hamma joyga kirishga dostup buladi
        super().__init__(*args, **kwargs)

        for field in self.fields.values():  # bu yerdagi self.fields.values() Meta classning ichidagi fildlarni siklag uzatdik
            field.widget.attrs.update({'class': 'input'})  # va har bir fieldga input clss berib chiqdik


class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        widgets = {'tags': forms.CheckboxSelectMultiple()}  # tags ustunini checbox qilib tanlaydigan qildik

    def __init__(self, *args, **kwargs):  # tepadagi classga ulandik super() orqali va init funksiya hamma joyga kirishga dostup buladi
        super().__init__(*args, **kwargs)

        for field in self.fields.values():    # bu erdagi self.fields.values() Meta classning ichidagi fildlarni siklag uzatdik
            field.widget.attrs.update({'class': 'input'})  # va har bir fieldga input clss berib chiqdik