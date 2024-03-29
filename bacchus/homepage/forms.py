from django import forms

class AccountArticleWriteForm(forms.Form):
    name = forms.CharField(max_length=64, label="Name*")
    year = forms.IntegerField(label="Student I.D. Year(eg. 2015)*")
    password = forms.CharField(widget=forms.PasswordInput, label="Password*")
    email = forms.CharField(max_length=256, label="E-Mail*")
    homepage = forms.CharField(max_length=256, required=False, label="Homepage")
    title = forms.CharField(max_length=256, label="Title*")
    content = forms.CharField(widget=forms.Textarea(), label="Content*")

class ArticleWriteForm(forms.Form):
    email = forms.CharField(max_length=256, label="E-Mail*")
    homepage = forms.CharField(max_length=256, required=False, label="Homepage")
    is_secret = forms.BooleanField(required=False, label="Secret?")
    title = forms.CharField(max_length=256, label="Title*")
    content = forms.CharField(widget=forms.Textarea(), label="Content*")

class ArticleRemoveForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Password*")

class CommentWriteForm(forms.Form):
    email = forms.CharField(max_length=256, label="E-Mail*")
    content = forms.CharField(widget=forms.Textarea(), label="Message*")
