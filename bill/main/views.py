from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Bill,Tenant
from .forms import Makebill,Addtenant
from datetime import date
# Create your views here.


def home(request):
    context= { "bills" : Bill.objects.all(),
      "tenants" : Tenant.objects.all()
      }
    return render(request,'main/home.html',context)

def alltenants(request):
    tenants  = Tenant.objects.all()
    category = request.GET.get('category')
    if category == 'ACTIVE':
        tenants = Tenant.objects.all().filter(status=True)
    elif category == 'NOTACTIVE':
        tenants = Tenant.objects.all().filter(status=False)
    elif category == 'ALL':
        tenants  = Tenant.objects.all()
        
    return render(request, 'main/tenants.html',{'tenants' : tenants})

def detail(request, id):
    tenant= Tenant.objects.get(id=id)
    bills = Bill.objects.filter(tenant=tenant.id)
    # print(bills)
    return render(request, 'main/detail.html', {'tenant' : tenant,'bills':bills})

def delete_tenant(request,id):
    tenant =Tenant.objects.get(id=id)
    tenant.delete()
    return redirect('alltenants')


def addtenant(request):
    form = Addtenant(request.POST)
    if request.method == 'POST':
            if form.is_valid():
                form.save()
                print("yay tenant addeddd")
                return redirect('alltenants')
    else:
        form= Addtenant()
    # context={'form' : form}
    return render(request,'main/addtenant.html',{'form' : form})

def update_tenant(request,id):
    tenant = Tenant.objects.get(id=id)
    # if request.method == 'POST':
    form = Addtenant(request.POST or None,instance=tenant)
    if form.is_valid():
        form.save()
        print("yay tenant addeddd")
        return redirect('alltenants')
    # context={'form' : form}
    return render(request,'main/update_tenant.html',{'form' : form})


def all_bills(request):
    bill = Bill.objects.all()
    if request.method == "GET":
        value = request.GET.get('button')
        if value == "paid":
            result = Bill.objects.filter(bill_status="paid").all()
        if value == "due":
            result = Bill.objects.filter(bill_status="due").all()
        if value == "active":
            result = Tenant.objects.filter(status=True).all()
        if value == "inactive":
            result = Tenant.objects.filter(status=False).all()
        value2 = request.GET.get('room')
        if value2:
            result = Bill.objects.filter(room=value2).all()

    return render(request,'main/bills.html',{'bill' : bill})
    


def create_bill(request):
    if request.method == 'POST':
        names = request.POST.getlist('name')          # list of tenant ids/names from checkboxes
        tenants = Tenant.objects.filter(name__in=names)  # or filter(id__in=names) if using ids
                
        room    = request.POST.get('room')
        month   = request.POST.get('month')
        pre     = int(request.POST.get('pre'))
        pre2    = int(request.POST.get('pre2'))
        pre3    = int(request.POST.get('pre3'))
        cur     = int(request.POST.get('cur'))
        cur2    = int(request.POST.get('cur2'))
        cur3    = int(request.POST.get('cur3'))
        am4     = int(request.POST.get('am4'))
        remark1 = request.POST.get('rem')
        remark2 = request.POST.get('rem2')
        remark3 = request.POST.get('rem3')

        diff  = cur  - pre
        diff2 = cur2 - pre2
        diff3 = cur3 - pre3
        am    = diff  * 10
        am2   = diff2 * 10
        am3   = diff3 * 10
        total = am + am2 + am3 + am4

        bill = Bill.objects.create(
            month=month, room=room,
            previous=pre,   previous2=pre2,   previous3=pre3,
            current=cur,    current2=cur2,    current3=cur3,
            diff=diff, diff2=diff2, diff3=diff3,
            amount=am,     amount2=am2,     amount3=am3,     amount4=am4,
            total=total,
            remark1=remark1, remark2=remark2, remark3=remark3,
            bill_status="due"
        )
        bill.tenant.set(tenants)   # M2M — set after save, not in create()

    context = {
        'tenants': Tenant.objects.all(),
    }
    return render(request, 'main/createbill.html', context)

def view_bill(request,id):
    bill = Bill.objects.get(id=id)
    
    if request.method == "POST":
        status = request.POST.get('status')
        print(status)
        if status == 'paid':
            bill.bill_status = status
            # bill.paid_date = datetime.now()
            bill.save()
        elif status == 'due':
            bill.bill_status = status
            bill.save()
        else:
            print('outofbounds')
    print(bill.bill_status)
    return render(request, 'main/view-bill.html' , {'bill' : bill})

def delete_bill(request,id):
    bill = Bill.objects.get(id=id)
    bill.delete()
    return redirect('alltenants')


        
def bill_room_update():
    tenants = Tenant.objects.all()
    bills = Bill.objects.all()
    for bill in bills:
        if bill.room is None:
            for t in bill.tenant.all():
                print(t.room)
                if t.room: 
                    bill.room = t.room
                    bill.save()
                else:
                    print("tenant does not have designated room")
        else:
            print("bill with id",bill.id,"already exists")



    
    
    
    
