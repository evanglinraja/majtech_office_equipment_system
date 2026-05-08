from django.shortcuts import render,redirect
from django.conf import settings
import mysql.connector as sql

def index(request):
    db=settings.DATABASES['mysql']
    con=sql.connect(
        host=db['HOST'],
        user=db['USER'],
        password=db['PASSWORD'],
        database=db['NAME']
    )
    cursor=con.cursor(dictionary=True)
    cursor.execute("SELECT equipment_id,category_name,equipment_name,current_status FROM tbl_equipment AS e JOIN tbl_categories AS c ON e.category_id=c.category_id")
    equipments=cursor.fetchall()
    cursor.close()
    con.close()
    return render(request, 'equipment/index.html', {'equipments': equipments})

def add(request):
    if request.method=='POST':
        category_id=request.POST.get("category_id")
        equipment_name=request.POST.get("equipment_name")
        serial_number=request.POST.get("serial_number")
        purchase_date=request.POST.get("purchase_date")
        purchase_cost=request.POST.get("purchase_cost")
        current_status=request.POST.get("current_status")
        location=request.POST.get("location")
        
        db=settings.DATABASES['mysql']
        con=sql.connect(
            host=db['HOST'],
            user=db['USER'],
            password=db['PASSWORD'],
            database=db['NAME']
        )
        cursor=con.cursor()
        params=(category_id,equipment_name,serial_number,purchase_date,purchase_cost,current_status,location)
        cursor.callproc("sp_equipment_insert",params)
        con.commit()
        cursor.close()
        con.close()
        return redirect("/equipment")
    return render(request, 'equipment/add.html',{'categories':category()})


def edit(request,id):
    if request.method=='POST':
        category_id=request.POST.get("category_id")
        equipment_name=request.POST.get("equipment_name")
        serial_number=request.POST.get("serial_number")
        purchase_date=request.POST.get("purchase_date")
        purchase_cost=request.POST.get("purchase_cost")
        current_status=request.POST.get("current_status")
        location=request.POST.get("location")
        
        db=settings.DATABASES['mysql']
        con=sql.connect(
            host=db['HOST'],
            user=db['USER'],
            password=db['PASSWORD'],
            database=db['NAME']
        )
        cursor=con.cursor()
        params=(id,category_id,equipment_name,serial_number,purchase_date,purchase_cost,current_status,location)
        cursor.callproc("sp_equipment_update",params)
        con.commit()
        cursor.close()
        con.close()
        return redirect("/equipment")
    
    db=settings.DATABASES['mysql']
    con=sql.connect(
        host=db['HOST'],
        user=db['USER'],
        password=db['PASSWORD'],
        database=db['NAME']
    )
    cursor=con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tbl_equipment WHERE equipment_id =%s",(id,))
    equipment=cursor.fetchone()
    cursor.close()
    con.close()
    equipment['purchase_date']= equipment['purchase_date'].strftime('%Y-%m-%d') 
    return render(request, 'equipment/edit.html',{"equipment":equipment, 'categories':category()})

def delete(request,id):
    db=settings.DATABASES['mysql']
    con=sql.connect(
        host=db['HOST'],
        user=db['USER'],
        password=db['PASSWORD'],
        database=db['NAME']
    )
    cursor=con.cursor(dictionary=True)
    cursor.callproc("sp_equipment_delete",(id,))
    con.commit()
    cursor.close()
    con.close()
    
    
    return redirect("/equipment")

def category():
    db=settings.DATABASES['mysql']
    con=sql.connect(
        host=db['HOST'],
        user=db['USER'],
        password=db['PASSWORD'],
        database=db['NAME']
    )
    cursor=con.cursor(dictionary=True)
    cursor.execute("SELECT category_id,category_name FROM tbl_categories")
    categories=cursor.fetchall()
    cursor.close()
    con.close()
    return categories
    