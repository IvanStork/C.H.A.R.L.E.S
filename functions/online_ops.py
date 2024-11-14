import requests
import speech_recognition as sr
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config
import openai
from openai import OpenAI

from engine import speak

def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def play_on_youtube(video):
    kit.playonyt(video)

def search_on_google(query):
    kit.search(query)

def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+31{number}", message)

EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")


def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False

NEWS_API_KEY = config("NEWS_API_KEY")


def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=nl&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]

OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")


def get_weather_report(city):
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"

def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]

def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']

OPENAI_KEY = config("OPENAI_KEY")
openai.api_key = OPENAI_KEY
def chat_gpt_talk(): #function to have a chat with chatgpt
    client = OpenAI(api_key = OPENAI_KEY)
    r = sr.Recognizer()# initialize recognizer
    def record_text(): #function to record the spoken text
        while(1):
            try:
                with sr.Microphone() as source2:#use microphone as source
                    r.adjust_for_ambient_noise(source2,duration=0.2)

                    print("I am listening")

                    audio2 = r.listen(source2)#listen for input

                    MyText = r.recognize_google(audio2)#use google to convert audio to text

                    return MyText
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

            except sr.UnknownValueError:
                print("Unknown error occurred")

    def send_to_chatgpt(messages, model = "gpt-3.5-turbo"):
        response = client.chat.completions.create(
            model = model,
            messages = messages,
            max_tokens = 100,
            n = 1,
            stop=None,
            temperature = 0.5
        )

        message = response.choises[0].message.content
        messages.append(response.choises[0].message)
        return message

    messages = [{"role":"user","content":"please act as if you were a butler from now on. Your name is CHARLIE"}]
    try:
        while(1):
            text = record_text()
            messages.append({"role":"user","content":text})
            response = send_to_chatgpt(messages)
            speak(response)

            print(response)

    except KeyboardInterrupt:
        print("Stopped conversation")