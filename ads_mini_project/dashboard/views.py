from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import pandas as pd
from django.conf import settings

# Create your views here.
#@login_required
def home(request):
    return render(request, "dashboard/home.html")

def display(request):
    if request.method == "POST":
        device_1_name = request.POST.get("device_1")
        device_2_name = request.POST.get("device_2")
        print(f"here is the data: {device_1_name} from ajax")
        print(f"here is the data: {device_2_name} from ajax")

        # df = pd.read_excel(f"{settings.STATIC_DIR}/excel_data/master.xlsx")
        # print(df.head())

        # #get unique value for column PDName
        # pd_name = df["PDName"].unique()
        # print(pd_name)



        
        return JsonResponse({
            "status": "True",
            "img_1": "/static/image/xiaomi-14-ultra-1.jpg",
            "img_2": "/static/image/xiaomi-14-ultra-1.jpg",
            "img_3": "/static/image/xiaomi-14-ultra-1.jpg",
            "img_4": "/static/image/xiaomi-14-ultra-1.jpg",
        })
    else:
        return JsonResponse({"message": "This is a test message - bad"})
