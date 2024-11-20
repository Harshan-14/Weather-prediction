from flask import Flask,render_template
from tkinter import *
from tkinter import ttk
import requests

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd



# Load the Excel file into a DataFrame for Delhi
df_delhi = pd.read_excel(r"E:\DAV project Practice\Flask\mydir\delhi.xlsx")

# Convert 'datetime' column to datetime format
df_delhi['datetime'] = pd.to_datetime(df_delhi['datetime'])

# Group temperature data by month and calculate average temperature for Delhi
monthly_avg_temp_delhi_2022 = df_delhi[df_delhi['Year'] == 2022].groupby(df_delhi['datetime'].dt.month)['temp'].mean().tolist()
monthly_avg_temp_delhi_2023 = df_delhi[df_delhi['Year'] == 2023].groupby(df_delhi['datetime'].dt.month)['temp'].mean().tolist()

# Group precipitation data by month and calculate average precipitation amount and probability for Delhi
monthly_avg_precip_amount_delhi_2022 = df_delhi[df_delhi['Year'] == 2022].groupby(df_delhi['datetime'].dt.month)['precip'].mean().tolist()
monthly_avg_precip_prob_delhi_2022 = df_delhi[df_delhi['Year'] == 2022].groupby(df_delhi['datetime'].dt.month)['precipprob'].mean().tolist()
monthly_avg_precip_amount_delhi_2023 = df_delhi[df_delhi['Year'] == 2023].groupby(df_delhi['datetime'].dt.month)['precip'].mean().tolist()
monthly_avg_precip_prob_delhi_2023 = df_delhi[df_delhi['Year'] == 2023].groupby(df_delhi['datetime'].dt.month)['precipprob'].mean().tolist()

# Group solar radiation or solar energy data by month and calculate average values for Delhi
monthly_avg_solar_radiation_delhi_2022 = df_delhi[df_delhi['Year'] == 2022].groupby(df_delhi['datetime'].dt.month)['solarradiation'].mean().tolist()
monthly_avg_solar_radiation_delhi_2023 = df_delhi[df_delhi['Year'] == 2023].groupby(df_delhi['datetime'].dt.month)['solarradiation'].mean().tolist()

months_delhi = df_delhi['datetime'].dt.month_name().unique().tolist()

# Load the Excel file into a DataFrame for Mumbai and Delhi
df_mumbai_delhi = pd.read_excel(r"E:\DAV project Practice\Flask\mydir\mumbai_delhi.xlsx")


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Data Visualization")
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")
        
        # Add tabs for Delhi weather data
        self.frame_delhi_temp = ttk.Frame(self.notebook)
        self.frame_delhi_precip = ttk.Frame(self.notebook)
        self.frame_delhi_solar = ttk.Frame(self.notebook)
        
        self.notebook.add(self.frame_delhi_temp, text='Delhi Temperature')
        self.notebook.add(self.frame_delhi_precip, text='Delhi Precipitation')
        self.notebook.add(self.frame_delhi_solar, text='Delhi Solar Radiation')
        
        # Plot Delhi temperature data
        self.plot_delhi_temperature(self.frame_delhi_temp)
        
        # Plot Delhi precipitation data
        self.plot_delhi_precipitation(self.frame_delhi_precip)
        
        # Plot Delhi solar radiation data
        self.plot_delhi_solar_radiation(self.frame_delhi_solar)
        
        # Add tabs for Mumbai and Delhi weather data
        self.temperature_tab = ttk.Frame(self.notebook)
        self.humidity_tab = ttk.Frame(self.notebook)
        self.windspeed_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.temperature_tab, text='Mumbai & Delhi Temperature')
        self.notebook.add(self.humidity_tab, text='Mumbai & Delhi Humidity')
        self.notebook.add(self.windspeed_tab, text='Mumbai & Delhi Windspeed')
        
        # Plot Mumbai and Delhi temperature data
        self.plot_mumbai_delhi_temperature(self.temperature_tab)
        
        # Plot Mumbai and Delhi humidity data
        self.plot_mumbai_delhi_humidity(self.humidity_tab)
        
        # Plot Mumbai and Delhi windspeed data
        self.plot_mumbai_delhi_windspeed(self.windspeed_tab)

        # Initialize temp_label_delhi attribute
        self.temp_label_delhi = tk.Label(self.frame_delhi_temp, text="", anchor="w")
        self.temp_label_delhi.pack(side=tk.BOTTOM, fill=tk.X)

        
    def plot_delhi_temperature(self, tab):
        # Plot Delhi temperature data
        fig, ax = plt.subplots()
        ax.plot(months_delhi, monthly_avg_temp_delhi_2022, label='2022')
        ax.plot(months_delhi, monthly_avg_temp_delhi_2023, label='2023')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title('Delhi Temperature Data (2022-2023)')
        ax.legend()
        
        # Embed temperature plot in the tab
        canvas_temp_delhi = FigureCanvasTkAgg(fig, master=tab)
        canvas_temp_delhi.draw()
        canvas_temp_delhi.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        temp_label_delhi = tk.Label(tab, text="", anchor="w")
        temp_label_delhi.pack(side=tk.BOTTOM, fill=tk.X)
        
        canvas_temp_delhi.mpl_connect('motion_notify_event', self.on_plot_hover_temperature_delhi)
        
        
        
       

    def plot_delhi_precipitation(self, tab):
        # Plot Delhi precipitation data
        fig, ax = plt.subplots()
        ax.plot(months_delhi, monthly_avg_precip_amount_delhi_2022, label='Precip Amount (2022)')
        ax.plot(months_delhi, monthly_avg_precip_prob_delhi_2022, label='Precip Prob (2022)')
        ax.plot(months_delhi, monthly_avg_precip_amount_delhi_2023, label='Precip Amount (2023)')
        ax.plot(months_delhi, monthly_avg_precip_prob_delhi_2023, label='Precip Prob (2023)')
        ax.set_ylabel('Precipitation')
        ax.legend()
        
        # Embed precipitation plot in the tab
        canvas_precip_delhi = FigureCanvasTkAgg(fig, master=tab)
        canvas_precip_delhi.draw()
        canvas_precip_delhi.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        precip_label_delhi = tk.Label(tab, text="", anchor="w")
        precip_label_delhi.pack(side=tk.BOTTOM, fill=tk.X)
        
        canvas_precip_delhi.mpl_connect('motion_notify_event', self.on_plot_hover_precipitation_delhi)
        
        # Calculate min and max precipitation along with corresponding months
        min_precip_amount_2022 = min(monthly_avg_precip_amount_delhi_2022)
        min_precip_prob_2022 = min(monthly_avg_precip_prob_delhi_2022)
        min_precip_month_2022 = months_delhi[monthly_avg_precip_amount_delhi_2022.index(min_precip_amount_2022)]
        max_precip_amount_2022 = max(monthly_avg_precip_amount_delhi_2022)
        max_precip_prob_2022 = max(monthly_avg_precip_prob_delhi_2022)
        max_precip_month_2022 = months_delhi[monthly_avg_precip_amount_delhi_2022.index(max_precip_amount_2022)]
        
        min_precip_amount_2023 = min(monthly_avg_precip_amount_delhi_2023)
        min_precip_prob_2023 = min(monthly_avg_precip_prob_delhi_2023)
        min_precip_month_2023 = months_delhi[monthly_avg_precip_amount_delhi_2023.index(min_precip_amount_2023)]
        max_precip_amount_2023 = max(monthly_avg_precip_amount_delhi_2023)
        max_precip_prob_2023 = max(monthly_avg_precip_prob_delhi_2023)
        max_precip_month_2023 = months_delhi[monthly_avg_precip_amount_delhi_2023.index(max_precip_amount_2023)]
        
        # Description
        desc = f"This plot illustrates the average monthly precipitation trends in Delhi for the years 2022 and 2023. It shows both the precipitation amount and probability, allowing insights into rainfall patterns.\n\nMinimum Precipitation Amount (2022): {min_precip_amount_2022} ({min_precip_month_2022})\nMinimum Precipitation Probability (2022): {min_precip_prob_2022} ({min_precip_month_2022})\nMaximum Precipitation Amount (2022): {max_precip_amount_2022} ({max_precip_month_2022})\nMaximum Precipitation Probability (2022): {max_precip_prob_2022} ({max_precip_month_2022})\n\nMinimum Precipitation Amount (2023): {min_precip_amount_2023} ({min_precip_month_2023})\nMinimum Precipitation Probability (2023): {min_precip_prob_2023} ({min_precip_month_2023})\nMaximum Precipitation Amount (2023): {max_precip_amount_2023} ({max_precip_month_2023})\nMaximum Precipitation Probability (2023): {max_precip_prob_2023} ({max_precip_month_2023})"
        precip_label_delhi.config(text=desc)


    def plot_delhi_solar_radiation(self, tab):
        # Plot Delhi solar radiation data
        fig, ax = plt.subplots()
        ax.plot(months_delhi, monthly_avg_solar_radiation_delhi_2022, label='Solar Radiation (2022)')
        ax.plot(months_delhi, monthly_avg_solar_radiation_delhi_2023, label='Solar Radiation (2023)')
        ax.set_ylabel('Solar Radiation')
        ax.legend()
        
        # Embed solar radiation plot in the tab
        canvas_solar_delhi = FigureCanvasTkAgg(fig, master=tab)
        canvas_solar_delhi.draw()
        canvas_solar_delhi.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        solar_label_delhi = tk.Label(tab, text="", anchor="w")
        solar_label_delhi.pack(side=tk.BOTTOM, fill=tk.X)
        
        canvas_solar_delhi.mpl_connect('motion_notify_event', self.on_plot_hover_solar_radiation_delhi)
        
        # Calculate min and max solar radiation along with corresponding months
        min_solar_radiation_2022 = min(monthly_avg_solar_radiation_delhi_2022)
        max_solar_radiation_2022 = max(monthly_avg_solar_radiation_delhi_2022)
        min_solar_radiation_month_2022 = months_delhi[monthly_avg_solar_radiation_delhi_2022.index(min_solar_radiation_2022)]
        max_solar_radiation_month_2022 = months_delhi[monthly_avg_solar_radiation_delhi_2022.index(max_solar_radiation_2022)]
        
        min_solar_radiation_2023 = min(monthly_avg_solar_radiation_delhi_2023)
        max_solar_radiation_2023 = max(monthly_avg_solar_radiation_delhi_2023)
        min_solar_radiation_month_2023 = months_delhi[monthly_avg_solar_radiation_delhi_2023.index(min_solar_radiation_2023)]
        max_solar_radiation_month_2023 = months_delhi[monthly_avg_solar_radiation_delhi_2023.index(max_solar_radiation_2023)]
        
        # Description
        desc = f"This plot showcases the average monthly solar radiation trends in Delhi for the years 2022 and 2023. It provides insights into the variation of solar energy received over different months and between the two years.\n\nMinimum Solar Radiation (2022): {min_solar_radiation_2022} ({min_solar_radiation_month_2022})\nMaximum Solar Radiation (2022): {max_solar_radiation_2022} ({max_solar_radiation_month_2022})\n\nMinimum Solar Radiation (2023): {min_solar_radiation_2023} ({min_solar_radiation_month_2023})\nMaximum Solar Radiation (2023): {max_solar_radiation_2023} ({max_solar_radiation_month_2023})"
        solar_label_delhi.config(text=desc)

    def plot_mumbai_delhi_temperature(self, tab):
        # Create temperature plot for Mumbai and Delhi
        plt.figure(figsize=(10, 6))
        for city in df_mumbai_delhi['City'].unique():
            city_data = df_mumbai_delhi[df_mumbai_delhi['City'] == city]
            plt.plot(city_data['datetime'], city_data['temp'], label=city)

        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.title('Daily Temperature in Mumbai and Delhi (2022-2023)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Embed temperature plot in the tab
        canvas_temp = FigureCanvasTkAgg(plt.gcf(), master=tab)
        canvas_temp.draw()
        canvas_temp.get_tk_widget().pack(side='top', fill='both', expand=1)
        
        # Description
        desc = "This plot shows the daily temperature trends in Mumbai and Delhi from 2022 to 2023. It helps in comparing the temperature fluctuations between the two cities over the given period."
        desc_label = tk.Label(tab, text=desc)
        desc_label.pack()


    def plot_mumbai_delhi_humidity(self, tab):
        # Create humidity plot for Mumbai and Delhi
        plt.figure(figsize=(10, 6))
        for city in df_mumbai_delhi['City'].unique():
            city_data = df_mumbai_delhi[df_mumbai_delhi['City'] == city]
            plt.plot(city_data['datetime'], city_data['humidity'], label=city)

        plt.xlabel('Date')
        plt.ylabel('Humidity (%)')
        plt.title('Humidity Trends Comparison between Mumbai and Delhi over 2 Years')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Embed humidity plot in the tab
        canvas_humidity = FigureCanvasTkAgg(plt.gcf(), master=tab)
        canvas_humidity.draw()
        canvas_humidity.get_tk_widget().pack(side='top', fill='both', expand=1)
        
        # Description
        desc = "This plot illustrates the humidity trends in Mumbai and Delhi over the span of two years. It allows comparison of humidity levels between the two cities during the given time frame."
        desc_label = tk.Label(tab, text=desc)
        desc_label.pack()

    def plot_mumbai_delhi_windspeed(self, tab):
        # Create windspeed plot for Mumbai and Delhi
        plt.figure(figsize=(10, 6))
        for city in df_mumbai_delhi['City'].unique():
            city_data = df_mumbai_delhi[df_mumbai_delhi['City'] == city]
            plt.plot(city_data['datetime'], city_data['windspeed'], label=city)

        plt.xlabel('Date')
        plt.ylabel('Windspeed (m/s)')
        plt.title('Windspeed Trends Comparison between Mumbai and Delhi over 2 Years')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Embed windspeed plot in the tab
        canvas_windspeed = FigureCanvasTkAgg(plt.gcf(), master=tab)
        canvas_windspeed.draw()
        canvas_windspeed.get_tk_widget().pack(side='top', fill='both', expand=1)
        
        # Description
        desc = "This plot displays the windspeed trends in Mumbai and Delhi over the course of two years. It allows comparison of windspeed variations between the two cities during the given time period."
        desc_label = tk.Label(tab, text=desc)
        desc_label.pack()

    def on_plot_hover_temperature_delhi(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            month_index = int(round(x))  # Round to nearest month
            month_index = max(0, min(month_index, len(months_delhi) - 1))  # Clamp index within range
            year = '2022' if y in monthly_avg_temp_delhi_2022 else '2023'
            temperature = monthly_avg_temp_delhi_2022[month_index] if year == '2022' else monthly_avg_temp_delhi_2023[month_index]
            max_temp_month_2022 = months_delhi[monthly_avg_temp_delhi_2022.index(max(monthly_avg_temp_delhi_2022))]
            min_temp_month_2022 = months_delhi[monthly_avg_temp_delhi_2022.index(min(monthly_avg_temp_delhi_2022))]
            max_temp_month_2023 = months_delhi[monthly_avg_temp_delhi_2023.index(max(monthly_avg_temp_delhi_2023))]
            min_temp_month_2023 = months_delhi[monthly_avg_temp_delhi_2023.index(min(monthly_avg_temp_delhi_2023))]
            desc = f"Month: {months_delhi[month_index]} {year}\nTemperature: {temperature:.2f}°C\n\nMax Temp (2022): {max(monthly_avg_temp_delhi_2022):.2f}°C ({max_temp_month_2022})\nMin Temp (2022): {min(monthly_avg_temp_delhi_2022):.2f}°C ({min_temp_month_2022})\n\nMax Temp (2023): {max(monthly_avg_temp_delhi_2023):.2f}°C ({max_temp_month_2023})\nMin Temp (2023): {min(monthly_avg_temp_delhi_2023):.2f}°C ({min_temp_month_2023})"
            self.temp_label_delhi.config(text=desc)

            

    def on_plot_hover_precipitation_delhi(self, event):
        # Hover event handler for Delhi precipitation plot
        if event.inaxes:
            x, y = event.xdata, event.ydata
            month_index = int(x + 0.5)  # Round to nearest month
            year = '2022' if y in monthly_avg_precip_amount_delhi_2022 else '2023'
            precip_amount = monthly_avg_precip_amount_delhi_2022[month_index] if year == '2022' else monthly_avg_precip_amount_delhi_2023[month_index]
            precip_prob = monthly_avg_precip_prob_delhi_2022[month_index] if year == '2022' else monthly_avg_precip_prob_delhi_2023[month_index]
            self.precip_label_delhi.config(text=f"Month: {months_delhi[month_index]} {year}\nPrecipitation Amount: {precip_amount:.2f}\nProbability: {precip_prob:.2f}")

    def on_plot_hover_solar_radiation_delhi(self, event):
        # Hover event handler for Delhi solar radiation plot
        if event.inaxes:
            x, y = event.xdata, event.ydata
            month_index = int(x + 0.5)  # Round to nearest month
            year = '2022' if y in monthly_avg_solar_radiation_delhi_2022 else '2023'
            solar_radiation = monthly_avg_solar_radiation_delhi_2022[month_index] if year == '2022' else monthly_avg_solar_radiation_delhi_2023[month_index]
            self.solar_label_delhi.config(text=f"Month: {months_delhi[month_index]} {year}\nSolar Radiation: {solar_radiation:.2f}")




app = Flask(__name__)
def calculat():



    def data_get():
        city=city_name.get()
        data=requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=6ee658a34f6c851fe9a41365d07bd4b2").json()
        w_label1.config(text=data["weather"][0]["main"])
        wb_label1.config(text=data["weather"][0]["description"])
        temp_label1.config(text=str(int(data["main"]["temp"]-273.15)))
        per_label1.config(text=data["main"]["pressure"])




    win=Tk()
    #Title name change it
    win.title("Weather forecast")
    win.config(bg="black")
    win.geometry("500x570")

    name_label=Label(win,text="Weather App",font=("Time New Roman",30,"bold"))
    name_label.place(x=25,y=50,height=50,width=450)

    city_name=StringVar()
    list_name=["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"]
    com=ttk.Combobox(win,text="Weather App",values=list_name,font=("Time New Roman",20,"bold"),textvariable=city_name)


    com.place(x=25,y=120,height=50,width=450)

    w_label=Label(win,text="Weather Climate",font=("Time New Roman",20))
    w_label.place(x=25,y=260,height=50,width=210)

    w_label1=Label(win,text="",font=("Time New Roman",20))
    w_label1.place(x=250,y=260,height=50,width=210)

    wb_label=Label(win,text="Weather Description",font=("Time New Roman",16))
    wb_label.place(x=25,y=330,height=50,width=210)

    wb_label1=Label(win,text="",font=("Time New Roman",17))
    wb_label1.place(x=250,y=330,height=50,width=210)


    temp_label=Label(win,text="Temperature",font=("Time New Roman",20))
    temp_label.place(x=25,y=400,height=50,width=210)

    temp_label1=Label(win,text="",font=("Time New Roman",20))
    temp_label1.place(x=250,y=400,height=50,width=210)

    per_label=Label(win,text="Pressure",font=("Time New Roman",20))
    per_label.place(x=25,y=470,height=50,width=210)

    per_label1=Label(win,text="",font=("Time New Roman",20))
    per_label1.place(x=250,y=470,height=50,width=210)

    done_button=Button(win,text="Done",font=("Time New Roman",20,"bold"),command=data_get)
    done_button.place(y=190,height=50,width=100,x=200)


    win.mainloop()


@app.route("/")
def home():   
   
   return render_template("index.html")

@app.route("/analysis")
def analysis():
    answer=calculat()
    return "None"
    
@app.route("/prediction")
def prediction():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
    return "Execution complete"

    



app.run(host="127.0.0.1",port=5000,debug=True)

