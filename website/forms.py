from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User

from website.models import ClientLot, CompanyLot, BidCompanyLot, LotPhoto

from .models import Client, Company


# Registration
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', error_messages={'exists': 'Електронна адеса вже використовується'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        # user.groups.add(Group.objects.get_or_create(name="client"))
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']


class ClientSignForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'profile_pic', 'phone')


class CompanySignForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'profile_pic', 'phone', 'edrpou', 'location', 'website_link',)


class CreateBid(forms.ModelForm):
    class Meta:
        model = BidCompanyLot
        fields = ('price',)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        return price

    def save(self, commit=True):
        bid = super(CreateBid, self).save(commit=False)
        bid.price = self.cleaned_data['price']
        if commit:
            bid.save()
        return bid
    

# Lot add
class ClientLotCreate(forms.ModelForm):
    class Meta:
        model = ClientLot
        fields = ('name', 'description','category','price','price_gap')

    
class CompanyLotCreate(forms.ModelForm):
    class Meta:
        model = CompanyLot
        fields = ('name', 'description','category','price','price_gap',)


class LotPhotoCreate(forms.ModelForm):
    class Meta:
        model = LotPhoto
        fields = ('photo',)
