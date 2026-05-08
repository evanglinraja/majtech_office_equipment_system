from django.shortcuts import render
from django.conf import settings
import mysql.connector as sql

# Create your views here.
def index(request):
    db=settings.DATABASES['mysql']
    con=sql.connect(
        host=db['HOST'],
        user=db['USER'],
        password=db['PASSWORD'],
        database=db['NAME']
    )
    cursor=con.cursor(dictionary=True)
    cursor.execute("""
                   select
(select count(*)from tbl_categories) as category,
(select count(*)from tbl_equipment) as equipment,
(select count(*)from tbl_maintenance) as maintenance,
(select sum(cost)from tbl_maintenance) as maintenance_cost;
                   """)
    dashboard=cursor.fetchone()
    cursor.close()
    con.close()
    return render(request,"dashboard/index.html",{'dashboard':dashboard})