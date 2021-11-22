from django.shortcuts import render, redirect

from django.contrib.auth import login, logout
from django.contrib import messages

from .models import *
from .forms import *
from datetime import datetime
from .excel_month import  get_attachment_month
from .excel_quarter import get_attachment_quater
from .excel_year import get_attachment_year



# Create your views here.
def user_logout(request):
    logout(request)
    return redirect('start_page')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        staff_form = StaffForm(request.POST)
        if form.is_valid() and staff_form.is_valid():
            user = form.save()
            login(request, user)
            staff = staff_form.save(commit=False)
            staff.user = user
            staff.save()

            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('start_page')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
        staff_form = StaffForm()
    return render(request, 'accounting/register.html', {'form': form, 'staff_form': staff_form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('start_page')
    else:
        form = UserLoginForm()
    return render(request, 'accounting/login.html', {'form': form})





def start_page(request):
    waste = Waste.objects.all()

    return render(request, 'accounting/start_page.html',
                  {'waste': waste,  'title': 'Перечень видов отходов'})

def view_branch(request):
    branch = NameOfBranch.objects.all()

    return render(request, 'accounting/view_branch.html',
                  {'branch': branch,  'title': 'Перечень филиалов'})



def view_objects(request):


    user = Staff.objects.get(user=request.user)

    try:
        objects = NameOfObjects.objects.filter(branch=user.branch)
    except:
        objects = NameOfObjects.objects.all()
    return render(request, 'accounting/view_objects.html',
                  {'objects': objects,  'title': 'Перечень объектов'})


def add_educated_waste(request):

    branch = request.user.staff.branch

    if request.method == 'GET':

        form = AddEducatedWaste1(branch, request.POST or None)
        return render(request, 'accounting/add_educated_waste.html', {'form': form})

def add_educated_waste1(request):


    if request.method == 'POST':

        form = AddEducatedWaste(request.POST)
        if form.is_valid():

            z = form.save(commit=False)  # сохраняем форму без записи в БД
            branch = NameOfObjects.objects.get(name=z.object_name).branch
            z.branch = branch
            z.user_name = request.user

            z.save()  # сохраняем форму в БД
            return redirect('view_waste_motion')



def add_reclaimed_waste(request):

    branch = request.user.staff.branch

    if request.method == 'GET':

        form = AddReclaimedWaste1(branch, request.POST or None)
        return render(request, 'accounting/add_reclaimed_waste.html', {'form': form})

def add_reclaimed_waste1(request):


    if request.method == 'POST':

        form = AddReclaimedWaste(request.POST)
        if form.is_valid():

            z = form.save(commit=False)  # сохраняем форму без записи в БД
            branch = NameOfObjects.objects.get(name=z.object_name).branch
            z.branch = branch
            z.user_name = request.user

            name_waste = z.name
            object_name = z.object_name
            educated = EducatedWaste.objects.filter(object_name=object_name, name=name_waste)
            reclimed = ReclaimedWaste.objects.filter(object_name=object_name, name=name_waste)
            transfered = TransferredWaste.objects.filter(object_name=object_name, name=name_waste)

            sum_educated = 0
            for i in educated:
                sum_educated += i.quantity

            sum_reclimed = 0
            for i in reclimed:
                sum_reclimed += i.quantity

            sum_transfered = 0
            for i in transfered:
                sum_transfered += i.quantity


            if round((sum_educated - sum_reclimed - sum_transfered - z.quantity),5) < 0:
                messages.error(request, 'Количество переданного превышает хранящиеся')
                return render(request, 'accounting/add_reclaimed_waste.html', {'form': form})
            else:
                z.save()  # сохраняем форму в БД
                return redirect('view_waste_motion')


def add_transferred_waste(request):

    branch = request.user.staff.branch

    if request.method == 'GET':

        form = AddTransferredWaste1(branch, request.POST or None)
        return render(request, 'accounting/add_transferred_waste.html', {'form': form})

def add_transferred_waste1(request):


    if request.method == 'POST':

        form = AddTransferredWaste(request.POST)
        if form.is_valid():

            z = form.save(commit=False)  # сохраняем форму без записи в БД
            branch = NameOfObjects.objects.get(name=z.object_name).branch
            z.branch = branch
            z.user_name = request.user
            name_waste = z.name
            object_name = z.object_name
            educated = EducatedWaste.objects.filter(object_name=object_name, name=name_waste)
            reclimed = ReclaimedWaste.objects.filter(object_name=object_name, name=name_waste)
            transfered = TransferredWaste.objects.filter(object_name=object_name, name=name_waste)

            sum_educated = 0
            for i in educated:
                sum_educated += i.quantity

            sum_reclimed = 0
            for i in reclimed:
                sum_reclimed += i.quantity

            sum_transfered = 0
            for i in transfered:
                sum_transfered += i.quantity


            if round((sum_educated - sum_reclimed - sum_transfered - z.quantity), 5) < 0:
                messages.error(request, 'Количество утилизированного превышает хранящиеся')
                return render(request, 'accounting/add_transferred_waste.html', {'form': form})
            else:
                z.save()  # сохраняем форму в БД
                return redirect('view_waste_motion')

def view_waste_motion(request):
    today = datetime.today()
    branch = request.user.staff.branch
    objects = NameOfObjects.objects.filter(branch=branch)
    wastes = Waste.objects.all()

    educated = EducatedWaste.objects.filter(branch=branch)
    reclaimed = ReclaimedWaste.objects.filter(branch=branch)
    transferred = TransferredWaste.objects.filter(branch=branch)
    result = []
    for item in educated:
        result.append(['образовано', item.name, item.object_name, item. quantity, item.date_of_educated, item.pk])

    for item in reclaimed:
        result.append(['утилизировано', item.name, item.object_name, item. quantity, item.date_of_reclaimed, item.pk])

    for item in transferred:
        result.append(['передано', item.name, item.object_name, item. quantity, item.date_of_transferred, item.pk])

    sort_by_5_attribute = sorted(result, key=lambda k: k[4], reverse=True)

    return render(request, 'accounting/view_waste_motion.html', {'motion': sort_by_5_attribute, 'objects':objects, 'wastes':wastes})

def create_report(request):
    if request.method == 'POST':
        form = ChoseReportDate(request.POST)
        if form.is_valid():
            type_report = form.cleaned_data['type_report']
            if type_report == 'month':

                return redirect('month_report')
            elif type_report == 'quater':


                return redirect('quater_report')
            else:

                return redirect('year_report')
    else:
        form = ChoseReportDate()
    return render(request, 'accounting/chose_report.html', {'form': form})

def month_report(request):
    branch = request.user.staff.branch
    user = request.user
    if request.method == 'POST':

        form = ReportMonth(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            data = [branch, user, month, year]
            get_attachment_month(data)




            return redirect('reports')
    else:
        form = ReportMonth()
    return render(request, 'accounting/month_report.html', {'form': form})


def quater_report(request):
    branch = request.user.staff.branch
    user = request.user
    if request.method == 'POST':

        form = ReportQuater(request.POST)
        if form.is_valid():
            if request.method == 'POST':

                form = ReportQuater(request.POST)
                if form.is_valid():
                    quater = form.cleaned_data['quater']
                    year = form.cleaned_data['year']
                    data = [branch, user, quater, year]
                    get_attachment_quater(data)




            return redirect('reports')
    else:
        form = ReportQuater()
    return render(request, 'accounting/quater_report.html', {'form': form})


def year_report(request):
    branch = request.user.staff.branch
    user = request.user
    if request.method == 'POST':

        form = ReportYear(request.POST)
        if form.is_valid():
            if form.is_valid():

                year = form.cleaned_data['year']
                data = [branch, user, year]
                get_attachment_year(data)




            return redirect('reports')
    else:
        form = ReportYear()
    return render(request, 'accounting/year_report.html', {'form': form})


def remove_motion(request, atribute):
    atribute = atribute.split('_')
    pk = atribute[0]
    type_motion = atribute[1]
    if type_motion == 'образовано':
        EducatedWaste.objects.filter(pk=pk).delete()
    elif type_motion == 'утилизировано':
        ReclaimedWaste.objects.filter(pk=pk).delete()
    elif type_motion == 'передано':
        TransferredWaste.objects.filter(pk=pk).delete()

    return redirect('view_waste_motion')

def report(request):
    user_name = request.user.username

    reports = Report.objects.filter(user=user_name)
    return render(request, "accounting/reports.html", {'reports':reports})

def remove_report(request, pk):
    reports = Report.objects.filter(pk=pk)
    for report in reports:
        report.delete()
    return redirect('reports')


def sort_waste_motion (request):
    branch = request.user.staff.branch
    objects = NameOfObjects.objects.filter(branch=branch)
    wastes = Waste.objects.all()
    data = request.POST
    name_obj = ''
    name_waste = ''
    for key in data:
        if key == 'name_object':
            if data[key] != 'Сортировка по объекту':
                name_obj = data[key]
        elif key == 'name_waste':
            if data[key] != 'Сортировка по наменованию отходов':
                name_waste = data[key]

    if name_obj != '' and  name_waste != '':
        educated = EducatedWaste.objects.filter(object_name=name_obj, name=name_waste)
        reclaimed = ReclaimedWaste.objects.filter(object_name=name_obj, name=name_waste)
        transferred = TransferredWaste.objects.filter(object_name=name_obj, name=name_waste)
        result = []
        for item in educated:
            result.append(['образовано', item.name, item.object_name, item.quantity, item.date_of_educated, item.pk])

        for item in reclaimed:
            result.append(
                ['утилизировано', item.name, item.object_name, item.quantity, item.date_of_reclaimed, item.pk])

        for item in transferred:
            result.append(['передано', item.name, item.object_name, item.quantity, item.date_of_transferred, item.pk])

        sort_by_5_attribute = sorted(result, key=lambda k: k[4], reverse=True)

        return render(request, 'accounting/view_waste_motion.html',
                      {'motion': sort_by_5_attribute, 'objects': objects, 'wastes': wastes})
    elif name_obj != '' and name_waste == '':
        educated = EducatedWaste.objects.filter(object_name=name_obj)
        reclaimed = ReclaimedWaste.objects.filter(object_name=name_obj)
        transferred = TransferredWaste.objects.filter(object_name=name_obj)
        result = []
        for item in educated:
            result.append(['образовано', item.name, item.object_name, item.quantity, item.date_of_educated, item.pk])

        for item in reclaimed:
            result.append(
                ['утилизировано', item.name, item.object_name, item.quantity, item.date_of_reclaimed, item.pk])

        for item in transferred:
            result.append(['передано', item.name, item.object_name, item.quantity, item.date_of_transferred, item.pk])

        sort_by_5_attribute = sorted(result, key=lambda k: k[4], reverse=True)

        return render(request, 'accounting/view_waste_motion.html',
                      {'motion': sort_by_5_attribute, 'objects': objects, 'wastes': wastes})

    elif name_obj == '' and name_waste != '':
        educated = EducatedWaste.objects.filter( name=name_waste)
        reclaimed = ReclaimedWaste.objects.filter(name=name_waste)
        transferred = TransferredWaste.objects.filter(name=name_waste)
        result = []
        for item in educated:
            result.append(['образовано', item.name, item.object_name, item.quantity, item.date_of_educated, item.pk])

        for item in reclaimed:
            result.append(
                ['утилизировано', item.name, item.object_name, item.quantity, item.date_of_reclaimed, item.pk])

        for item in transferred:
            result.append(['передано', item.name, item.object_name, item.quantity, item.date_of_transferred, item.pk])

        sort_by_5_attribute = sorted(result, key=lambda k: k[4], reverse=True)

        return render(request, 'accounting/view_waste_motion.html',
                      {'motion': sort_by_5_attribute, 'objects': objects, 'wastes': wastes})

    elif name_obj == '' and name_waste == '':
        educated = EducatedWaste.objects.filter(branch=branch)
        reclaimed = ReclaimedWaste.objects.filter(branch=branch)
        transferred = TransferredWaste.objects.filter(branch=branch)
        result = []
        for item in educated:
            result.append(['образовано', item.name, item.object_name, item.quantity, item.date_of_educated, item.pk])

        for item in reclaimed:
            result.append(
                ['утилизировано', item.name, item.object_name, item.quantity, item.date_of_reclaimed, item.pk])

        for item in transferred:
            result.append(['передано', item.name, item.object_name, item.quantity, item.date_of_transferred, item.pk])

        sort_by_5_attribute = sorted(result, key=lambda k: k[4], reverse=True)

        return render(request, 'accounting/view_waste_motion.html',
                      {'motion': sort_by_5_attribute, 'objects': objects, 'wastes': wastes})
