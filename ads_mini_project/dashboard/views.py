from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import pandas as pd
from django.conf import settings
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from wordcloud import WordCloud

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

        

        dc = DeviceCompare()
        spec_img_path, img_path, word_cloud_path = dc.controll_devicecomparepolarity(device_1_name, device_2_name)

        print("==========")
        print(spec_img_path)
        print("\n")
        print(img_path)
        print("\n")
        print(word_cloud_path)
        print("==========")
        
        img_dict = {
            "status": "True",
            "img_1": spec_img_path[0],
            "img_2": spec_img_path[1],
            "img_3": spec_img_path[2],
            "img_4": spec_img_path[3],
            "img_5": img_path[0],
            "img_6": word_cloud_path[0],
            "img_7": word_cloud_path[1]
        }

        print(img_dict)
        
        return JsonResponse(img_dict)
    else:
        return JsonResponse({"message": "This is a test message - bad"})



class DeviceCompare:
    def __init__(self):
        self.df = pd.read_excel(f"{settings.STATIC_DIR}/excel_data/master.xlsx")
        self.available_spec =['display','battery','camera','cpu','ram']

    #controller for device comparison
    def controll_devicecomparepolarity(self,deviceName1, deviceName2):
        device_list = [deviceName1, deviceName2]
        spec_img_path = []
        img_path = []
        word_cloud_path = []
        #generate figure for each spec's polarity
        for spec in self.available_spec:
            spec_img_path.append(self.devicecomparepolarity(deviceName1, deviceName2, spec))
        
        #generate figure for overall polarity
        img_path.append(self.devicecomparepolarity(deviceName1,deviceName2, None))

        #generate word cloud for each device
        for device in device_list:
            word_cloud_path.append(self.createworldcloud(device))


        return (spec_img_path,img_path,word_cloud_path)


    #compare two devices polarity
    def devicecomparepolarity(self,deviceName1, deviceName2, spec):
        fig, ax = plt.subplots(figsize=(10, 6))

        # self.df[self.df['PDName'] =='Samsung Galaxy S22 Ultra 5G']

        # # Group the DataFrame by year and month, and calculate the count of positive polarity
        # self.df[self.df['PDName'] =='Samsung Galaxy S23 Ultra']

        if spec is None:
            self.df[(self.df['PDName'] ==f'{deviceName1}') & self.df['Cleansed']]['polarity'].plot(kind='kde', ax=ax, color='blue')
            self.df[(self.df['PDName'] ==f'{deviceName2}') & self.df['Cleansed']]['polarity'].plot(kind='kde', ax=ax, color='red')

        else:
            # Create a density plot of the polarity
            self.df[(self.df['PDName'] ==f'{deviceName1}') & self.df['Cleansed'].str.contains(f'{spec}')]['polarity'].plot(kind='kde', ax=ax, color='blue')
            self.df[(self.df['PDName'] ==f'{deviceName2}') & self.df['Cleansed'].str.contains(f'{spec}')]['polarity'].plot(kind='kde', ax=ax, color='red')

        # Set the title and labels
        if spec is None:
            ax.set_title(f'Positive Reviews between 2 devices')
        else:
            ax.set_title(f'Positive Reviews between 2 devices on {spec}')
        ax.set_xlabel('Value')
        ax.set_ylabel('Density')

        #add legend
        ax.legend([f'{deviceName1}', f'{deviceName2}'])

        # Display the plot
        if spec is None:
            image_path = f'{settings.STATIC_DIR}/image/{deviceName1.replace(" ","")}_{deviceName2.replace(" ","")}.png'
            plt.savefig(image_path)
            image_path = f'/static/image/{deviceName1.replace(" ","")}_{deviceName2.replace(" ","")}.png'
        else:
            image_path = f'{settings.STATIC_DIR}/image/{deviceName1.replace(" ","")}_{deviceName2.replace(" ","")}_{spec}.png'
            plt.savefig(image_path)
            image_path = f'/static/image/{deviceName1.replace(" ","")}_{deviceName2.replace(" ","")}_{spec}.png'
        
        return image_path

    #
    def createworldcloud(self,deviceName):
        # Create a WordCloud object
        df_temp = self.df[(self.df['PDName'] ==deviceName)]['Cleansed']
        df_temp = df_temp.convert_dtypes(convert_string=True)
        df_temp.dropna(inplace=True)

        wordcloud = WordCloud(width=800, height=400, max_words=100, background_color='white').generate(' '.join(df_temp))

        # Display the WordCloud
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.set_title(f'{deviceName} Word Cloud')
        ax.axis('off')

        # Display the plot
        img_path = f'{settings.STATIC_DIR}/image/wc_{deviceName.replace(" ","")}.png'
        plt.savefig(img_path)
        img_path = f'/static/image/wc_{deviceName.replace(" ","")}.png'
        return img_path
    



