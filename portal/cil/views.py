from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import login, authenticate, logout
from .models import *
from .forms import GuestUpdateForm
from django.conf import settings
import csv

file_name = "data.csv"


# Create your views here.

class Index(View):
    template_name = 'cil/index.html'

    def get(self, request):
        return render(request, self.template_name, {})


class LogGuestView(View):
    template_name = "cil/logs.html"

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name, {})

    def post(self, request):
        data_set = request.POST
        name = data_set['name']
        department = data_set['department']
        obj = Log(name=name, department=department, user='guest')
        obj.save()
        return redirect('cil:guestauth')


class LogStudentView(View):
    template_name = "cil/logs.html"

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name, {})

    def post(self, request):
        data_set = request.POST
        name = data_set['name']
        department = data_set['department']
        obj = Log(name=name, department=department, user='student')
        obj.save()
        return redirect('cil:studentauth')


class StudentAuth(View):
    template_name = "cil/studentauth.html"

    def get(self, request):
        pro = UpcomingSeminar.objects.all()
        if request.user.is_authenticated:
            return render(request, self.template_name, {"pro": pro})
        else:
            return redirect('cil:login')


class SeminarReq(View):
    template_name = "cil/studentseminarreq.html"

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return redirect('cil:login')

    def post(self, request):
        data = request.POST['name']
        obj = SeminarRequest(topic=data)
        obj.save()
        return render(request,self.template_name,{'ms':'Request Submitted!'})



class PastSeminars(View):
    template_name = "cil/pastseminars.html"

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name, {"pro": PastSeminar.objects.all()})


class GuestUpcomingSeminars(View):
    template_name = "cil/guestupcomingseminars.html"

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.username == "guest":
                return render(request, self.template_name)
            else:
                return redirect('cil:login')


class LogIn(View):
    template_name = 'cil/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('cil:adminauth')
            elif request.user.username == "guest":
                return redirect("cil:guestauth")
            elif request.user.username == "student":
                return redirect("cil:studentauth")
        return render(request, self.template_name, {})

    def post(self, request):
        data_set = request.POST
        username = data_set["username"]
        password = data_set["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if request.user.is_superuser:
                    return redirect('cil:adminauth')
                elif request.user.username == 'guest':
                    return redirect('cil:logsguest')
                else:
                    return redirect('cil:logsstudent')
        else:
            return render(request, self.template_name, {'err_ms': "Invalid Username or Password!"})


class AdminAuth(View):
    template_name = 'cil/adminauth.html'

    def get(self, request):
        dom = Profile.objects.all().values('domain').distinct().order_by('domain')
        pro = Profile.objects.all()
        file = open(settings.MEDIA_ROOT + "/" + file_name, "w")
        writer = csv.writer(file)

        if request.user.is_superuser:
            # t = PrettyTable(["Sr.No.", "Name", "Experience", "Designation", "Domain", "Email", "Phone"])
            t = ["Sr.No.", "Name", "Experience", "Designation", "Domain", "Email", "Phone"]
            writer.writerow(t)
            for i, d in enumerate(pro):
                writer.writerow([str(i + 1), d.name, str(d.exp), d.designation, d.domain, d.email, d.phone])
            # file.write(str(t))
            return render(request, self.template_name, {'pro': pro, 'dom': dom})

    def post(self, request):
        domain = request.POST['domain']
        if domain == "all":
            pro = Profile.objects.all()
        else:
            pro = Profile.objects.filter(domain=domain)
        dom = Profile.objects.all().values('domain').distinct().order_by('domain')

        file = open(settings.MEDIA_ROOT + "/" + file_name, "w")
        writer = csv.writer(file)

        t = ["Sr.No.", "Name", "Experience", "Designation", "Domain", "Email", "Phone"]
        writer.writerow(t)
        for i, d in enumerate(pro):
            writer.writerow([str(i + 1), d.name, str(d.exp), d.designation, d.domain, d.email, d.phone])
        return render(request, self.template_name, {'pro': pro, 'dom': dom, 'current': domain})


class GuestAuth(View):
    template_name = 'cil/guestauth.html'

    def get(self, request):
        dom = Profile.objects.all().values('domain').distinct().order_by('domain')
        pro = Profile.objects.all()

        file = open(settings.MEDIA_ROOT + "/" + file_name, "w")
        writer = csv.writer(file)
        if not request.user.is_superuser:
            t = ["Sr.No.", "Name", "Experience", "Designation", "Domain", "Email", "Phone"]
            writer.writerow(t)
            for i, d in enumerate(pro):
                writer.writerow([str(i + 1), d.name, str(d.exp), d.designation, d.domain, d.email, d.phone])
            return render(request, self.template_name, {'pro': pro, 'dom': dom})

    def post(self, request):
        domain = request.POST['domain']
        if domain == "all":
            pro = Profile.objects.all()
        else:
            pro = Profile.objects.filter(domain=domain)

        dom = Profile.objects.all().values('domain').distinct().order_by('domain')

        file = open(settings.MEDIA_ROOT + "/" + file_name, "w")
        writer = csv.writer(file)
        t = ["Sr.No.", "Name", "Experience", "Designation", "Domain", "Email", "Phone"]
        writer.writerow(t)
        for i, d in enumerate(pro):
            writer.writerow([str(i + 1), d.name, str(d.exp), d.designation, d.domain, d.email, d.phone])

        return render(request, self.template_name, {'pro': pro, 'dom': dom, 'current': domain})


class GuestAdd(View):
    template_name = 'cil/guestadd.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        data_set = request.POST
        if request.FILES:
            bio_file = request.FILES['biodata']
            if (not (bio_file.name.endswith('pdf')) and not (bio_file.name.endswith('doc')) and not (
                    bio_file.name.endswith('docx'))):
                return render(request, self.template_name,
                              {'ms': 'Please add your biodata in doc or docx or pdf format'})

        domains = data_set['domain']
        if ',' in domains:
            domain_ls = domains.split(',')
            for i in range(len(domain_ls)):
                domain_add = domain_ls[i].strip()
                domain_add = domain_add.upper()
                print(i)
                obj = TempProfileAdd()
                obj.create(name=data_set['name'], exp=data_set['exp'], domain=domain_add,
                           designation=data_set['designation'], email=data_set['email'],
                           phone=data_set['phone'])
                if request.FILES:
                    obj.biodata = bio_file
                obj.save()
        else:
            obj = TempProfileAdd()
            obj.create(name=data_set['name'], exp=data_set['exp'], domain=data_set['domain'].upper(),
                       designation=data_set['designation'], email=data_set['email'], phone=data_set['phone'])
            if request.FILES:
                obj.biodata = bio_file
            obj.save()
        return render(request, self.template_name, {'ms': 'Added!'})


class GuestEdit(View):
    template_name = 'cil/guestedit.html'

    def get(self, request):
        obj = Profile.objects.all()
        return render(request, self.template_name, {'items': obj})

    def post(self, request):
        try:
            obj = Profile.objects.get(pk=request.POST.get('id'))
        except Profile.DoesNotExist:
            return render(request, self.template_name, {'ms': 'Name not found in Database', 'items': obj})
        base_url = reverse_lazy('cil:guestupdate', kwargs={'profile': obj.id})
        return redirect(base_url)


class GuestUpdate(View):
    template_name = 'cil/guestupdate.html'
    template_name_2 = 'cil/guestedit.html'

    def get(self, request, profile):
        obj = Profile.objects.get(id=profile)
        form = GuestUpdateForm(instance=obj)
        return render(request, self.template_name, {'form': form})

    def post(self, request, profile):
        pro = Profile.objects.all()
        data_set = request.POST
        profile_obj = Profile.objects.get(id=profile)
        form = GuestUpdateForm(instance=profile_obj)
        if request.FILES:
            bio_file = request.FILES['biodata']
            if (not (bio_file.name.endswith('pdf')) and not (bio_file.name.endswith('doc')) and not (
                    bio_file.name.endswith('docx'))):
                return render(request, self.template_name,
                              {'ms': 'Please add your biodata in doc or docx or pdf format', 'form': form})

        obj = TempProfileEdit(name=data_set['name'], exp=data_set['exp'], domain=data_set['domain'],
                              designation=data_set['designation'],
                              email=data_set['email'], phone=data_set['phone'],
                              profile=profile_obj)
        if request.FILES:
            obj.biodata = bio_file
        obj.save()
        return redirect('cil:guestedit')


class GuestDelete(View):
    template_name = 'cil/guestdelete.html'

    def get(self, request):
        pro = Profile.objects.all()
        return render(request, self.template_name, {'pro': pro})

    def post(self, request):
        pro = Profile.objects.all()
        obj = Profile.objects.get(pk=request.POST['profid'])
        try:
            TempProfileDelete.objects.get(profile=obj)
        except TempProfileDelete.DoesNotExist:
            temp_obj = TempProfileDelete()
            temp_obj.create(obj)
            temp_obj.save()
            return render(request, self.template_name, {'ms': 'Delete request submitted!', 'pro': pro})
        return render(request, self.template_name, {'ms': 'Delete request has already been submitted!', 'pro': pro})


def logoff(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('cil:login')
