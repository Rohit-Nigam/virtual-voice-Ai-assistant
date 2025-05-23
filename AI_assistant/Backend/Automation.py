from AppOpener import close,open as appopen
from webbrowser import open as webopen
from pywhatkit import search,playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import os
import asyncio


env_vars=dotenv_values(".env")
GroqAPIKey=env_vars.get("GroqAPIKey")

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

useragent = "AppleWebKit/537.36(KHTML,like Gecko) Chrome/100.0.4896.75 safari/537.36"

client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "your satisfaction is my top priority; feel free to reach out if there's anything else i can help you with.","I'm at your service for any aditional questions or support you may need-don't hesitate to ask,Thank you",
]

messages=[]

SystemChatBot=[{"role":"system","content": f"Hello. I am {os.environ['Username']},You're a content writer. You have to Write content like letter,codes,applications,essays,notes,songs,poems,captions,stories,etc."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):

    def OpenNotepad(File):
        default_text_editor = "notepad.exe"
        subprocess.Popen([default_text_editor,File])

    def ContentWriteAI(prompt):
        messages.append({r"role":"user","content":f"{prompt}"})
        completion=client.chat.completions.create(
            model = "mixtral-8x7b-32768",
            messages=SystemChatBot+messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None,
        )
        Answer=""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer+=chunk.choices[0].delta.content
        Answer = Answer.replace("</s>","")
        messages.append({"role":"assistant","content":Answer})
        return Answer
    Topic: str = Topic.replace("Content","")
    ContentByAI=ContentWriteAI(Topic)

    with open(rf"Data/{Topic.lower().replace(' ','')}.text","w",encoding="utf-8")as file:
        file.write(ContentByAI)
        file.close()
    OpenNotepad(rf"Data/{Topic.lower().replace(' ','')}.text")
    return True
# Content("caption for instagram post of travelling in mumbai suggest 10")

def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)

def PlayYoutube(query):
    playonyt(query)
    return True
# PlayYoutube("hollywood Avatar movie")


def openApp(app,sess=requests.session()):
    try:
        appopen(app,match_closest=True,output=True,throw_error=True)
    except:
        def exract_links(html):
            if html is None:
                return[]
            soup = BeautifulSoup(html,'html.parser')
            links = soup.find_all('a',{"jsname":"UWcKNb"})
            return[link.get('href')for link in links]
        def search_google(query):
            url=f"https://www.google.com/search?q={query}"
            headers={"User-Agent": useragent}
            response=sess.get(url,headers=headers)
            if response.status_code==200:
                return response.text
            else:
                print("Faild to retrive search results,")
            return None
        
        html=search_google(app)
# 
        link_list = exract_links(html)
        if link_list:
            link = link_list[0]
            webbrowser.open(link)
        else:
            print("No links found in the extracted HTML.")
# 
        # if html:
        #     link=exract_links(html)[0]
        #     webopen(link)
        return True
# openApp("open facebook")

def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app,match_closet=True , output=True
                  , throw_error=True)
            return True
        except:
            return False
        
def System(command):
    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute")
    
    def volume_up():
        keyboard.press_and_release("volume up")
    
    def volume_down():
        keyboard.press_and_release("volume down")

    if command=="mute":
        mute()
    elif command=="unmute":
        unmute()
    elif command=="volume up":
        volume_up()
    elif command=="volume down":
        volume_down()

    return True

async def TranslateAndExecute(commands:list[str]):
    funcs =[]
    for command in commands:
        if command.startswith("open"):
            if "open it" in command:
                pass
            if "open file" == command:
                pass
            else:
                fun=asyncio.to_thread(openApp,command.removeprefix("open"))
                funcs.append(fun)
        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp,command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube,command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content,command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch,command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch,command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System,command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No Function Found , for{command}")

    results=await asyncio.gather(*funcs)
    for result in results:
        if isinstance(result,str):
            yield result
        else:
            yield result
async def Automation(commands:list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True