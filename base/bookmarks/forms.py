from django.forms import ModelForm
from .models import BookmarkCategory, BookmarkSubCategory, Bookmark


class BookmarkCategoryForm(ModelForm):

    class Meta:
        model = BookmarkCategory
        fields = '__all__'
        exclude = ['user']


class BookmarkSubCategoryForm(ModelForm):

    class Meta:
        model = BookmarkSubCategory
        fields = '__all__'


class BookmarkForm(ModelForm):

    class Meta:
        model = Bookmark
        fields = '__all__'
