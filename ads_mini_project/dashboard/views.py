from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from django.conf import settings
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from wordcloud import WordCloud
import time

# Create your views here.
def home(request):
    return render(request, "dashboard/home.html")

def display(request):
    if request.method == "POST":
        device_1_name = request.POST.get("device_1")
        device_2_name = request.POST.get("device_2")

        #get the class object
        dc = DeviceCompare()
        spec_img_path, img_path, word_cloud_path, p_n_trend_path = dc.controll_devicecomparepolarity(device_1_name, device_2_name)
        
        img_dict = {
            "status": "True",
            "img_1": spec_img_path[0],
            "img_2": spec_img_path[1],
            "img_3": spec_img_path[2],
            "img_4": spec_img_path[3],
            "img_5": img_path[0],
            "img_6": word_cloud_path[0],
            "img_7": word_cloud_path[1],
            "img_8": p_n_trend_path[0],
            "img_9": p_n_trend_path[1]
        }
        
        return JsonResponse(img_dict)
    else:
        return JsonResponse({"message": "This is a test message - bad"})



class DeviceCompare:
    def __init__(self):
        self.df = pd.read_excel(f"{settings.STATIC_DIR}/excel_data/master.xlsx")
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d %b %Y')
        self.df['year'] = self.df['Date'].dt.year
        self.df['month'] = self.df['Date'].dt.month
        self.df['day'] = self.df['Date'].dt.day
        self.available_spec =['display','battery','camera','cpu','ram']

    #controller for device comparison
    def controll_devicecomparepolarity(self,deviceName1, deviceName2):
        """
        this function is used to run each function to generate the figure
        """
        device_list = [deviceName1, deviceName2]
        spec_img_path = []
        img_path = []
        word_cloud_path = []
        p_n_trend = []
        #generate figure for each spec's polarity
        for spec in self.available_spec:
            spec_img_path.append(self.devicecomparepolarity(deviceName1, deviceName2, spec))
        
        #generate figure for overall polarity
        img_path.append(self.devicecomparepolarity(deviceName1,deviceName2, None))

        #generate word cloud for each device
        for device in device_list:
            word_cloud_path.append(self.createworldcloud(device))
        time.sleep(5)
        for device in device_list:
            p_n_trend.append(self.post_neg_trend(device))


        return (spec_img_path,img_path,word_cloud_path,p_n_trend)

    def devicecomparepolarity(self,deviceName1, deviceName2, spec):
        """
        this function is used to compare the polarity of 2 devices
        """
        try:
            matplotlib.use('Agg')
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
            
            plt.clf()
            return image_path
        except Exception as e:
            print(e)
            return f'/static/image/not_found.png'

    def createworldcloud(self,deviceName):
        """
        this function is used to create word cloud for inputted device name
        """
        try:
            matplotlib.use('Agg')
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
            plt.clf()
            return img_path
        except Exception as e:
            print(e)
            return f'/static/image/not_found.png'
    
    def post_neg_trend(self,device_name):
        """
        this function is used to create positive and negative trend for inputted device name
        """
        launchdate = ""
        try:
            matplotlib.use('Agg')
            self.df['date_m_y'] = pd.to_datetime(self.df[['year', 'month']].assign(DAY=1), format='%Y-%m')

            limiteddf = self.df[(self.df['PDName'] ==f'{device_name}')]

            x= limiteddf.groupby(['date_m_y'])['date_m_y'].sample(n=1, random_state=42)
            lowest = len(x)    
            y1 = limiteddf[limiteddf['polarity']>0].groupby(['date_m_y'])['polarity'].mean()
            y2 = limiteddf[limiteddf['polarity']<0].groupby(['date_m_y'])['polarity'].mean()
            
            #get device's launch date
            launch_date_str = limiteddf.iloc[0][6]
            print("====")
            print(launch_date_str)
            print("====")
            date_format = "%Y, %B %d" 
            launch_date  = dt.datetime.strptime(launch_date_str , date_format)
            print("====")
            print(launch_date)
            print("====")


            #to prevent data size not equal
            if(len(y1) != len(y2)):
                lowest = min(len(y1), len(y2))
            if(len(y1)!=lowest):
                y1 = y1[:lowest]
            if(len(y2)!=lowest):
                y2 = y2[:lowest]
            if(len(x)!=lowest):
                x = x[:lowest]


            # plot the data
            plt.plot(x, y1, label=f'Positive') # plot the first set of values with a label
            plt.plot(x, y2, label=f'Negative') # plot the second set of values with a label

            plt.axvline(launch_date, color='g', linestyle='-.',label="Device Launch date")

            # format the x axis labels
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

            # adjust the plot layout
            plt.gcf().autofmt_xdate()

            # add a legend
            plt.legend()
            plt.title(f'Positive and Negative Trend for {device_name}')

            # show the plot
            img_path = f'{settings.STATIC_DIR}/image/{device_name.replace(" ","")}_trend.png'
            plt.savefig(img_path)
            plt.clf()
            img_path = f'/static/image/{device_name.replace(" ","")}_trend.png'
            return img_path
        except Exception as e:
            print(e)
            return f'/static/image/not_found.png'


