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
    cursor.execute("SELECT maintenance_id,equipment_name,maintenance_date,maintenance_type,cost FROM tbl_maintenance AS m JOIN tbl_equipment AS e ON m.equipment_id=e.equipment_id")
    maintenance=cursor.fetchall()
    cursor.close()
    con.close()
    
    return render(request, 'maintenance/index.html', {'maintenance': maintenance})

def add(request):
    if request.method=='POST':
        equipment_id=request.POST.get("equipment_id")
        maintenance_date=request.POST.get("maintenance_date")
        maintenance_type=request.POST.get("maintenance_type")
        description=request.POST.get("description")
        cost=request.POST.get("cost")
        performed_by=request.POST.get("performed_by")
        
        db=settings.DATABASES['mysql']
        con=sql.connect(
            host=db['HOST'],
            user=db['USER'],
            password=db['PASSWORD'],
            database=db['NAME']
        )
        cursor=con.cursor()
        params=(equipment_id,maintenance_date,maintenance_type,description,cost,performed_by)
        cursor.callproc("sp_maintenance_insert",params)
        con.commit()
        cursor.close()
        con.close()
        return redirect("/maintenance")
    return render(request, 'maintenance/add.html',{'equipments':equipments()})


def edit(request,id):
    if request.method=='POST':
        equipment_id=request.POST.get("equipment_id")
        maintenance_date=request.POST.get("maintenance_date")
        maintenance_type=request.POST.get("maintenance_type")
        description=request.POST.get("description")
        cost=request.POST.get("cost")
        performed_by=request.POST.get("performed_by")
        
        db=settings.DATABASES['mysql']
        con=sql.connect(
            host=db['HOST'],
            user=db['USER'],
            password=db['PASSWORD'],
            database=db['NAME']
        )
        cursor=con.cursor()
        params=(id,equipment_id,maintenance_date,maintenance_type,description,cost,performed_by)
        cursor.callproc("sp_maintenance_update",params)
        con.commit()
        cursor.close()
        con.close()
        return redirect("/maintenance")
    
    db=settings.DATABASES['mysql']
    con=sql.connect(
        host=db['HOST'],
        user=db['USER'],
        password=db['PASSWORD'],
        database=db['NAME']
    )
    cursor=con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tbl_maintenance WHERE maintenance_id =%s",(id,))
    maintenance=cursor.fetchone()
    cursor.close()
    con.close()
    maintenance['maintenance_date']= maintenance['maintenance_date'].strftime('%Y-%m-%d') 
    return render(request, 'maintenance/edit.html',{"maintenance":maintenance, 'equipments':equipments()})

def delete(request,id):
    db=settings.DATABASES['mysql']
    con=sql.connect(
        host=db['HOST'],
        user=db['USER'],
        password=db['PASSWORD'],
        database=db['NAME']
    )
    cursor=con.cursor(dictionary=True)
    cursor.callproc("sp_maintenance_delete",(id,))
    con.commit()
    cursor.close()
    con.close()
    
    
    return redirect("/maintenance")

def equipments():
    db=settings.DATABASES['mysql']
    con=sql.connect(
        host=db['HOST'],
        user=db['USER'],
        password=db['PASSWORD'],
        database=db['NAME']
    )
    cursor=con.cursor(dictionary=True)
    cursor.execute("SELECT equipment_id,equipment_name FROM tbl_equipment")
    equipments=cursor.fetchall()
    cursor.close()
    con.close()
    return equipments
    