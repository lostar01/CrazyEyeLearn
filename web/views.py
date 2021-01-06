from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
from web.models import UserProfile
from web import dbmanger,tasks
from django.core.paginator import Paginator
from CrazyEye.settings import PER_PAGE_COUNT
from backend.utils import unique



# Create your views here.
@login_required
def index(request):
    if request.method == 'GET':
        return render(request,'index.html')


@login_required
def test(request):
    if request.method == 'GET':
        return render(request,'base.html')

@csrf_exempt
def acc_login(request):
    error = ""
    full_path = request.get_full_path().split('?')
    print(full_path)
    if len(full_path) >= 2:
        next_url = QueryDict(request.get_full_path().split('?')[1])
    else:
        next_url = ""

    if request.method == 'POST':
        _email = request.POST.get("email")
        _password = request.POST.get("password")

        user = authenticate(username=_email,password=_password)
        if user:
            login(request,user)

            if next_url != "":
                return redirect(next_url['next'])
            return redirect('/')
        else:
            error = "wrong username or password"

    return render(request,'login.html',{"error": error,"next_url": next_url})

def acc_logout(request):
    logout(request)
    return redirect("/login/")

@login_required
def display_hosts(request,current_page=1):
    user = UserProfile.objects.get(email=request.user)
    host_obj_list = user.bind_host.select_related()
    group_obj_list = user.host_groups.select_related()
    for group_obj in group_obj_list:
        host_obj_list = host_obj_list.union(group_obj.bind_hosts.select_related())


    # page paging
    page = Paginator(host_obj_list,PER_PAGE_COUNT)
    # print('page_list===',page.page(1).object_list)
    curr_page = page.page(current_page)
    curr_page_list = curr_page.object_list
    page_range = page.page_range
    page_has_nex = curr_page.has_next()
    page_has_pre = curr_page.has_previous()
    if page_has_pre:
        page_num_pre = curr_page.previous_page_number()
    if page_has_nex:
        page_num_nex = curr_page.next_page_number()



    return render(request,'hosts.html',locals())

@login_required
def connect_host(request,bind_host_id):
    token = unique()
    dbmanger.create_auditlog_obj(token=token)
    return render(request,'webssh.html',{"bindhost_id": bind_host_id,"token":token })

@login_required
def webssh(request):
    return render(request,'webssh.html')


def audit(request):
    rs = tasks.analy_audit()
    return HttpResponse(rs)
