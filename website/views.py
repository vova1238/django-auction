from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView

from website.forms import ClientLotCreate, CompanyLotCreate, LotPhotoCreate
from website.models import ClientLot, CompanyLot

from .forms import ClientSignForm, CompanySignForm, UserCreateForm

User = get_user_model()

class CompanyLotsListView(ListView):
    model = CompanyLot
    template_name = 'website/lot_list.html'
    context_object_name = 'lots'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Here i can add some additional context
        # context['now'] = timezone.now()
        context['get_params'] = [

        ]
        return context

    def get_queryset(self):
        category = self.request.GET.get('category')
        category_valid = category.isdecimal() if not category is None else False
        sorting = self.request.GET.get('sort')
        
        allowed_sorting = {
            'date-created', '-date-created',
            'date_end', '-date_end',
            'price', '-price',
            }
        
        if category_valid:
            print("Understandable category, have a nice day")
            qs = self.model.objects.filter(category_id=category)
        else:
            qs = self.model.objects.all()

        if sorting in allowed_sorting:
            qs = qs.order_by(sorting)
        else:
            qs = qs.order_by('-date_created')

        return qs
        


class CompanyLotDetailView(DetailView):
    model = CompanyLot
    template_name = 'website/lot_detail.html'
    context_object_name = 'lot'
    slug_field = 'url'
    


def home(request):
    return render(request, 'website/index.html', context = {'page_name': 'Home page'})


def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to = reverse('login'))

    # Client profile 
    if request.user.groups.filter(name='client').exists():
        user_profile = request.user.client
        lots = user_profile.clientlot_set.all()

        if request.method == 'POST':
            client_lot_form = ClientLotCreate(request.POST)
            if client_lot_form.is_valid():
                client_lot = client_lot_form.save(commit=False)
                client_lot.owner = request.user.client
                client_lot.save()
        else:
            client_lot_form = ClientLotCreate(request.POST)
        
        context = {
            "user_profile" : user_profile,
            "lots" : lots,
            "client_lot_form" : client_lot_form
        }
        return render(request, 'website/profile.html', context=context)

    # Company profile 
    if request.user.groups.filter(name='company').exists():
        user_profile = request.user.company
        lots = user_profile.companylot_set.all()

        if request.method == 'POST':
            company_lot_form = CompanyLotCreate(request.POST)

            if company_lot_form.is_valid():
                company_lot = company_lot_form.save(commit=False)
                company_lot.owner = request.user.company
                company_lot.save()
                print(company_lot)
                
                lot_photo_form = LotPhotoCreate(request.POST, request.FILES)
                print(lot_photo_form)
                if lot_photo_form.is_valid():
                    print('form is valid')
                    lot_photo = lot_photo_form.save(commit=False)
                    lot_photo.lot = company_lot
                    lot_photo.save()
                    print('saved image')

        else:
            company_lot_form = ClientLotCreate(request.POST)
            lot_photo_form = LotPhotoCreate(request.POST, request.FILES)
        
        context = {
            "user_profile" : user_profile,
            "lots" : lots,
            "company_lot_form" : company_lot_form,
            "lot_photo_form" : lot_photo_form,
        }
        return render(request, 'website/profile.html', context=context)
    
    
    return HttpResponse("User profile")



# Authentification
class signup(TemplateView):
    template_name = 'registration/signup.html'


def signup_client(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        client_profile_form = ClientSignForm(request.POST, request.FILES)
        if client_profile_form.is_valid() and user_form.is_valid():
            new_user = user_form.save(commit=False)
            client_profile = client_profile_form.save(commit=False)
            new_user.save()
            new_user.groups.add(Group.objects.get(name="client"))
            client_profile.user = new_user
            client_profile.save()
            new_user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('home')
    else:
        user_form = UserCreateForm()
        client_profile_form = ClientSignForm(request.POST, request.FILES)
    context = {'user_form': user_form, 'client_profile_form': client_profile_form}
    return render(request, 'registration/signup_client.html', context)


def signup_company(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        company_profile_form = CompanySignForm(request.POST, request.FILES)
        if company_profile_form.is_valid() and user_form.is_valid():
            new_user = user_form.save(commit=False)
            company_profile = company_profile_form.save(commit=False)
            new_user.save()
            new_user.groups.add(Group.objects.get(name="company"))
            company_profile.user = new_user
            company_profile.save()
            new_user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('home')
    else:
        user_form = UserCreateForm()
        company_profile_form = CompanySignForm(request.POST, request.FILES)
    context = {'user_form': user_form, 'company_profile_form': company_profile_form}
    return render(request, 'registration/signup_company.html', context)
