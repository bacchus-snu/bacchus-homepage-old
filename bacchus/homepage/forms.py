from django import forms


class ArticleWriteForm(forms.Form):
    name = forms.CharField(max_length=32, label="Name")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    email = forms.CharField(max_length=256, label="E-Mail")
    homepage = forms.CharField(max_length=256, required=False, label="Homepage")
    is_secret = forms.BooleanField(required=False, label="Secret?")
    title = forms.CharField(max_length=256, label="Title")
    content = forms.CharField(widget=forms.Textarea(), label="Content")

class ArticleRemoveForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class CommentWriteForm(forms.Form):
    name = forms.CharField(max_length=32, label="Name*")
    email = forms.CharField(max_length=256, label="E-Mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Password*")
    content = forms.CharField(widget=forms.Textarea(), label="Message*")

