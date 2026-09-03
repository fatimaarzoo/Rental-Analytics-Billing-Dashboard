from django.shortcuts import render
from main.models import Bill,Tenant
from datetime import date,datetime
import pandas as pd
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bill-v3.settings')  
django.setup()

def monthly_rent_graph(request):
    bills = Bill.objects.all().values('id','tenant','tenant__name','room','month','amount','amount2','amount3','amount4','total','bill_status' ,'date_created')

    df = pd.DataFrame(list(bills)) 
    
    #cleaned datetime   
    df['date_created'] = pd.to_datetime(df['date_created']).dt.date
    
    #added year
    df['year'] = pd.to_datetime(df['date_created']).dt.year

    
    #sorted data by month
    month_order =["January", "February", "March", "April", "May", "June", 
               "July", "August", "September", "October", "November", "December"]
    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)
    
    df.sort_values(by='month',inplace=True)
    
    tenants = Tenant.objects.all().values('id','name','room','status','joined_date','leaving_date')
    dft = pd.DataFrame(list(tenants))
    
    dft['joined_date'] = pd.to_datetime(dft['joined_date']).dt.date
    dft['joined_month'] = pd.to_datetime(df['date_created']).dt.month

    #added year
    dft['joined_year'] = pd.to_datetime(df['date_created']).dt.year

#-----------------------------------------------------------------------------------------------------    
        #profit this year 
    df['total_electricity'] =  df['total'] - df['amount4'] 
    df['profit'] = df['amount4']  - df['total_electricity']
    # print(df)
    
    # Monthly bills
    # month = request.GET.get('month')
    today_date = date.today()
    current_month = today_date.month
    current_year  = today_date.year 
    current_month_name = month_order[current_month-1]
    last_month_name = month_order[current_month-2]
    
    #current_month_and_year_data
    df_month = df[df['month']== current_month_name] #&& df['year'] == cureent_year
    df_last_month = df[df['month'] == last_month_name]
    
    # print(df_month)
    
    chart = px.pie(df_month, values='total', names='tenant__name' ,title='Monthly Bills')
    chart_html = pio.to_html(chart,full_html=False, config={"displayModeBar": False})

    #monthly profit
    chart1 = px.pie(df_month, values='amount4', names='tenant__name' ,title='Monthly Rent')
    chart_html1 = pio.to_html(chart1,full_html=False  ,config={"displayModeBar": False})
    
    fig =make_subplots(rows=2,cols=1,subplot_titles=("Rent Advance this year","Monthly profit"),x_title='Month',y_title='Profit                Rent')
    #rent this year

    fig.add_trace(go.Scatter(x=df['month'] , y =df['amount4'],fill='tozeroy',fillcolor='rgba(135, 206, 250, 0.5)'),row=1, col=1)

    
    # put the condition only if the bill_status is paid
    fig.add_trace(go.Scatter(x=df['month'],y=df['profit'],fill='tozeroy',fillcolor='rgba(180, 206, 250, 0.5)'),row=2, col=1)
    
    fig.update_layout(height=600)  
    chart2 = pio.to_html(fig,full_html=False,default_height='100%',  config={"displayModeBar": False})

    #totals of all
    
    total_electricity_bill = df['amount'].sum() + df['amount2'].sum() + df['amount3'].sum()
    total_rent_advance = df['amount4'].sum()
    total_profit = df['profit'].sum()
    
    #monthly difference in profit percentage
    month_profit = df_month['profit'].sum()
    month_diff_profit = df_month['profit'].sum() - df_last_month['profit'].sum()
    month_diff_profit_percentage = (month_diff_profit/(df_month['profit'].sum()))* 100
    month_diff_profit_percentage =month_diff_profit_percentage*100
    month_diff_profit_percentage =month_diff_profit_percentage//1
    month_diff_profit_percentage =month_diff_profit_percentage/100

    #tenants joined this month
    chart5 = px.line( y =dft['joined_month'], )
    # chart5.update_xaxes(visible=False)
    # chart5.update_yaxes(visible=False)
    chart5.update_layout(height=250 ,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    chart5= pio.to_html(chart5,full_html=False, config={"displayModeBar": False})
    
   
    
    #get the month through request too
    #monthly difference in total percentage
    
    current_month_total_electricity = df_month['total_electricity'].sum()
    last_month_total_electricity = df_last_month['total_electricity'].sum()
    month_total_electricity_diff =  df_month['total_electricity'].sum() - df_last_month['total_electricity'].sum()
    month_total_electricity_diff_percentage = (month_total_electricity_diff/(df_month['total_electricity'].sum()))*100
    month_total_electricity_diff_percentage =month_total_electricity_diff_percentage*100
    month_total_electricity_diff_percentage =month_total_electricity_diff_percentage//1
    month_total_electricity_diff_percentage =month_total_electricity_diff_percentage/100

    current_month_rent = df_month['amount4'].sum() 
    last_month_rent = df_last_month['amount4'].sum() 
    month_rent_diff =  df_month['amount4'].sum()  - df_last_month['amount4'].sum() 
    month_rent_diff_percentage = (month_rent_diff/(df_month['amount4'].sum() ))*100
    month_rent_diff_percentage =month_rent_diff_percentage*100
    month_rent_diff_percentage =month_rent_diff_percentage//1
    month_rent_diff_percentage =month_rent_diff_percentage/100
         
    current_month_rent  = df_month['amount4'].sum()
    current_month_bill_total = (df_month['total'] - df_month['amount4']).sum()
    
    #no. of active tenants
    
    active_tenants = len(dft[dft['status'] == True])
    
    chart3 = px.bar(df, y ='total', x='month',title='total_rent_each_month',color='tenant__name',category_orders={'month': month_order})
    chart3= pio.to_html(chart3,full_html=False, config={"displayModeBar": False})
    # # total length calculate from every gurl
    
    chart4 = px.histogram(df, y ='amount2', x='month',color='room' ,title='electricity_bill_each_month_room ',category_orders={'month': month_order})
    chart4= pio.to_html(chart4,full_html=False, config={"displayModeBar": False})


  
    context={'chart': chart_html,'chart1':chart_html1,'chart2':chart2,'chart3':chart3,'chart4':chart4,'chart5':chart5,
             'total_rent_advance':total_rent_advance,'total_profit':total_profit,
             'current_month_rent':current_month_rent,'month_rent_diff' :month_rent_diff ,'month_rent_diff_percentage':month_rent_diff_percentage, 
             'month_total_electricity':current_month_total_electricity,'month_total_electricity_diff':month_total_electricity_diff,'month_total_electricity_diff_percentage':month_total_electricity_diff_percentage,
             'current_month_bill_total':  current_month_bill_total,
             'month_diff_profit_percentage':month_diff_profit_percentage,'month_diff_profit':month_diff_profit ,'month_profit' : month_profit,
             'active_tenants': active_tenants}

  
    return render(request,'analysis/viz.html',context)
    
            
def load_date_from_excel():
    df = pd.read_excel(r"D:\PROGRAM CODE\python\billv3\rent_2026.xlsx")
    df.columns = df.columns.str.strip() 

    for _, row in df.iterrows():
        tename = row['Name']
        if " " in tename:
            tenames = tename.split()
            print("print the list of names",tenames)
            # tenants=[]
            
            #troubleshooting names
            #if names hare lower or upper convert all to sentence case
            # tenames = [name.capitalize() for name in tenames]
            # print("print the list of names after capitalizing",tenames)#just do this in excel
            #now now if the full name is something else then what???? what u gonna do?????????
            
            tenant = Tenant.objects.filter(name__in=tenames)
            print("through this function __in check if names exist list",tenant)
            # for name in tenames:#later check for full names how?
            #     one_tenant = Tenant.objects.filter(name__iexact=name)
            #     if one_tenant:
            #         tenant = tenants.append(one_tenant)
            #     else:
            #         print(f"Did not find{name}")
            # print("through this function [for] check if names exist list",tenant)
        else:
            tenant = Tenant.objects.filter(name=tename)
                
        if tenant:
            bill = Bill.objects.create(
                
                month       = row['Month'],
                previous    = int(row['previous']  or 0),
                previous2   = int(row['previous2'] or 0),
                current     = int(row['current']),
                current2    = int(row['current2']),
                diff        = int(row['current'])  - int(row['previous']  or 0),
                diff2       = int(row['current2']) - int(row['previous2'] or 0),
                amount      = int(row['amount']),
                amount2     = int(row['amount2']),
                amount3     = 0,
                amount4     = int(row['amount4']),
                total       = int(row['amount']) + int(row['amount2']) + int(row['amount4']),
                date_created= datetime.now()
            )
            
            bill.tenant.set(tenant)
        
            print(f"Created bill for {tenant} - {row['Month']}")
        else:
            print(f"Bill not created for {row['Name']} - {row['Month']}")

    print("Done!")
    
# load_date_from_excel()
    
def covert_to_csv():
    #SAVE THIS MONTH DB DATA TO CSV
    pass

