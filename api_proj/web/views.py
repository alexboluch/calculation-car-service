from django.shortcuts import render
from api.models import Calculation
from django.contrib.auth.models import User
from .logics import create_logic, create_loan_year
from .forms import CalculationCreateForm, RegistrForm, CalculationForm, CalculationDeleteForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def registration(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/main')
    data = {}
    if request.method == 'POST':
        form = RegistrForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/main')
    else:
        form = RegistrForm()
        data['form'] = form
        return render(request, 'registration/registration.html', data)


@login_required(login_url='/accounts/login/')
def create_calculation(request):
    data = {}
    if request.POST:
        print("POST")
        form = CalculationCreateForm(request.POST)
        if form.is_valid():
            calc = form.save(commit=False)
            username = request.user.username
            user = User.objects.get(username=username)
            calc.owner = user
            commission_price, swift_price, registration_price, delivery_land_price, delivery_all_price, customs_clearance_price, end_price = create_logic(form)
            calc.commission_price = commission_price
            calc.swift_price = swift_price
            calc.registration_price = registration_price
            calc.delivery_land_price = delivery_land_price
            calc.delivery_all_price = delivery_all_price
            calc.customs_clearance_price = customs_clearance_price
            calc.end_price = end_price
            calc.save()
            return HttpResponseRedirect('/main')
    else: 
        print("GET")
        form = CalculationCreateForm()
        data['form'] = form
        return render(request, 'calc/add_calc.html', data)


@login_required(login_url='/accounts/login/')
def main_view(request):
    user = User.objects.get(username=request.user.username)
    if user.is_staff:
        calculation_list = Calculation.objects.all()
    else:
        calculation_list = Calculation.objects.filter(owner=user)
    paginator = Paginator(calculation_list, 9)
    page = request.GET.get('page')  
    try:  
        posts = paginator.page(page)  
    except PageNotAnInteger:  
        # Если страница не является целым числом, поставим первую страницу  
        posts = paginator.page(1)  
    except EmptyPage:  
        # Если страница больше максимальной, доставить последнюю страницу результатов  
        posts = paginator.page(paginator.num_pages)
    context = {
        'calc_list':posts,
        'user':user,
        'page': page,
    }  
    return render(request, 'main.html', context)


@login_required(login_url='/accounts/login/')
def calc_update(request, pk):
    data = {}
    calc = get_object_or_404(Calculation, pk=pk)
    if request.POST:
        form = CalculationCreateForm(request.POST)
        if form.is_valid():
            commission_price, swift_price, registration_price, delivery_land_price, delivery_all_price, customs_clearance_price, end_price = create_logic(form)
            calc.commission_price = commission_price
            calc.swift_price = swift_price
            calc.registration_price = registration_price
            calc.delivery_land_price = delivery_land_price
            calc.delivery_all_price = delivery_all_price
            calc.customs_clearance_price = customs_clearance_price
            calc.end_price = end_price
            calc.comment = form.cleaned_data["comment"]
            calc.company_services_price = form.cleaned_data["company_services_price"]
            calc.broker_forwarding_price = form.cleaned_data["broker_forwarding_price"]
            calc.certification_price = form.cleaned_data["certification_price"]
            calc.title = form.cleaned_data["title"]
            calc.save()
            return HttpResponseRedirect("/main")
    else:
        form = CalculationCreateForm(instance=calc)
        data['form'] = form
    
    return render(request, 'calc/add_calc.html', data)


def calc_delete(request, pk):
    to_delete = get_object_or_404(Calculation, id=pk)
    if request.POST:
        form = CalculationDeleteForm(request.POST, instance=to_delete)
        if form.is_valid(): # checks CSRF
            to_delete.delete()
            return HttpResponseRedirect("/main/")
    else:
        form = CalculationDeleteForm(instance=to_delete)
    context = {'form': form}
    return render(request, 'confirm_delete.html', context)