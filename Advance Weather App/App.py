import customtkinter as ctk
import requests

# CTkinter setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Weather API setup
API_KEY = "0b08f527636503961cb67a016a69768a" 
def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15, 1)

def get_weather_icon(description):
    description = description.lower()
    if "cloud" in description:
        return "☁️"
    elif "rain" in description:
        return "🌧️"
    elif "clear" in description:
        return "☀️"
    elif "snow" in description:
        return "❄️"
    elif "mist" in description or "fog" in description:
        return "🌫️"
    else:
        return "🌡️"

def get_bg_color(description):
    description = description.lower()
    if "clear" in description:
        return "#1E90FF"
    elif "rain" in description:
        return "#37474F"
    elif "cloud" in description:
        return "#546E7A"
    elif "snow" in description:
        return "#90A4AE"
    else:
        return "#455A64"

def fetch_weather():
    city = city_entry.get()
    if city.strip() == "":
        status_label.configure(text="Please enter a city name.", text_color="red")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        if data["cod"] != 200:
            status_label.configure(text=f"City not found!", text_color="red")
            return

        weather = data["weather"][0]["description"]
        icon = get_weather_icon(weather)
        temp = kelvin_to_celsius(data["main"]["temp"])
        humidity = data["main"]["humidity"]

        # Update background color
        color = get_bg_color(weather)
        app.configure(fg_color=color)

        weather_label.configure(text=f"{icon} {weather.capitalize()}")
        temp_label.configure(text=f"🌡️ {temp}°C")
        humidity_label.configure(text=f"💧 Humidity: {humidity}%")

        # 5 Day Forecast
        forecast_frame.configure(fg_color="#212121")
        for widget in forecast_frame.winfo_children():
            widget.destroy()

        days = []
        for forecast in forecast_data["list"]:
            date = forecast["dt_txt"].split(" ")[0]
            if date not in days:
                days.append(date)
                day_weather = forecast["weather"][0]["description"]
                day_icon = get_weather_icon(day_weather)
                day_temp = kelvin_to_celsius(forecast["main"]["temp"])

                card = ctk.CTkFrame(master=forecast_frame, width=120, height=100, corner_radius=10, fg_color="#2E2E2E")
                card.pack(side="left", padx=5, pady=5)
                day_label = ctk.CTkLabel(master=card, text=f"{date}\n{day_icon}\n{day_temp}°C", font=("Roboto", 14))
                day_label.pack(padx=10, pady=10)

                if len(days) >= 5:
                    break

        status_label.configure(text="Successfully fetched!", text_color="lightgreen")

    except Exception as e:
        status_label.configure(text="Error fetching data!", text_color="red")
        print(e)

# App Window
app = ctk.CTk()
app.geometry("500x700")
app.title("Weather App (Advanced)")

# Heading
title_label = ctk.CTkLabel(app, text="☁️ Weather Forecast ☀️", font=("Roboto", 26, "bold"))
title_label.pack(pady=20)

# Search Frame
search_frame = ctk.CTkFrame(master=app, fg_color="#1E1E1E", corner_radius=15)
search_frame.pack(pady=10, padx=20, fill="x")

city_entry = ctk.CTkEntry(master=search_frame, placeholder_text="Enter City Name...", height=40, font=("Roboto", 16))
city_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")

search_button = ctk.CTkButton(master=search_frame, text="Search", height=40, command=fetch_weather, font=("Roboto", 16))
search_button.pack(side="right", padx=10, pady=10)

# Weather Info Frame
info_frame = ctk.CTkFrame(master=app, fg_color="#1F1F1F", corner_radius=20)
info_frame.pack(pady=20, padx=20, fill="both", expand=False)

weather_label = ctk.CTkLabel(master=info_frame, text="", font=("Roboto", 22))
weather_label.pack(pady=10)

temp_label = ctk.CTkLabel(master=info_frame, text="", font=("Roboto", 20))
temp_label.pack(pady=5)

humidity_label = ctk.CTkLabel(master=info_frame, text="", font=("Roboto", 20))
humidity_label.pack(pady=5)

# 5-Day Forecast
forecast_title = ctk.CTkLabel(master=app, text="5-Day Forecast", font=("Roboto", 22, "bold"))
forecast_title.pack(pady=10)

forecast_frame = ctk.CTkFrame(master=app, fg_color="#2A2A2A", corner_radius=15)
forecast_frame.pack(pady=10, padx=20, fill="x")

# Status
status_label = ctk.CTkLabel(master=app, text="", font=("Roboto", 14))
status_label.pack(pady=10)

# Run
app.mainloop()
