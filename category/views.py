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
    cursor.execute("SELECT * FROM tbl_categories")
    categories=cursor.fetchall()
    cursor.close()
    con.close()

    return render(request, 'category/index.html', {'categories': categories})

def add(request):
    if request.method=='POST':
        category_name=request.POST.get("category_name")
        description=request.POST.get("description")
        
        db=settings.DATABASES['mysql']
        con=sql.connect(
            host=db['HOST'],
            user=db['USER'],
            password=db['PASSWORD'],
            database=db['NAME']
        )
        cursor=con.cursor()
        params=(category_name,description)
        cursor.callproc("sp_categories_insert",params)
        con.commit()
        cursor.close()
        con.close()
        return redirect("/category")
    return render(request, 'category/add.html')


def edit(request,id):
    if request.method=='POST':
        category_name=request.POST.get("category_name")
        description=request.POST.get("description")
        
        db=settings.DATABASES['mysql']
        con=sql.connect(
            host=db['HOST'],
            user=db['USER'],
            password=db['PASSWORD'],
            database=db['NAME']
        )
        cursor=con.cursor()
        params=(id,category_name,description)
        cursor.callproc("sp_categories_update",params)
        con.commit()
        cursor.close()
        con.close()
        return redirect("/category")
    
    db=settings.DATABASES['mysql']
    con=sql.connect(
        host=db['HOST'],
        user=db['USER'],
        password=db['PASSWORD'],
        database=db['NAME']
    )
    cursor=con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tbl_categories WHERE category_id =%s",(id,))
    category=cursor.fetchone()
    cursor.close()
    con.close()
    return render(request, 'category/edit.html',{"category":category})

def delete(request,id):
    db=settings.DATABASES['mysql']
    con=sql.connect(
        host=db['HOST'],
        user=db['USER'],
        password=db['PASSWORD'],
        database=db['NAME']
    )
    cursor=con.cursor(dictionary=True)
    cursor.callproc("sp_categories_delete",(id,))
    con.commit()
    cursor.close()
    con.close()
    
    
    return redirect("/category")