import fbchat_wrapper as fbw
import os
import random
import requests
from bs4 import BeautifulSoup
from pytube import YouTube, Search
from gtts import gTTS
# from revChatGPT.ChatGPT import Chatbot
from datetime import datetime as dt
# try:
#     chatbot = Chatbot({
#     "session_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..AIXK6DBSfwehdwMT.P2Gl_QsAMU-dJW7BtGWO1Hra6Im2SUgYQiM13CjGfTwc5aIBgYqrD-uEfNHPFBS1lCwnZEH8Kt7TAGMlW9TLTeFTD8nMi7gSEwoRY9PU27K3hNiMOZ7hVUPxCwOXiNOy6bAmPsuxdNcv90gJ0j_rGYexnLCOWJZpLA240csDIpK6HziWPQdqNjwZpUxuTNIj-GRdSjIFiT0AeeGPAR16QLlGfub_MqqEC28Oa4TjdplvTVB1vZ7RgOnC_KscmGOTNwOGYl9sVkf8h3hOYK5nboeBEZp67ciqsOGuj5QUflhNwZDyCbTICtmM2DLgvIeEIoZTvHrlnnzLaY9AQYgqsnbUV6dZ87NnUgtSEmeS0La8uIPGPHu0fsn7Vm7sFAZ9ehZOZRZeBfwnJsJxxMtuUsz41UKAVP5IXiTTy5MljBsg6ps9pkyKSDpTT-nJRPZOS_rLBWmdNBrHgdx_jDs7FZwmyZVjBioicexudu5xgHCXlMLaPJFszIC27K0cVjPS7cUH9t-X4dVcWgnoqIQRd0sZZyVC8EAdxXPhBXSz_oJFgjbtzZD2aQux52Awp0N2iGxW_PKgV1PHFy7spcnmbwaBPK7UIUTeRY-pGLbPtkWSnYXmHxpG7NsfcGBqqvnWLAAbXYw8kG5DvRMWx4WSOTnlJbm_6nx2Gm2QSqnsPomiP6ncidh19pPrxJg-Z-UhbVTjgWYmWFSmdzWyqyDJDQ0sEu9_xuESAz5P4-XMqTHIK1Hn-D2Qc_9lH8RlYVZOqbAOvExi9ES8l3Ohp-qe3j1YANNpbqYscFnWLnREy-ckHiF3wCahy1xJJ3EPILdrpcJ68uuwZ09kvAknsFEzVTq1aE3PjzNfGmzk4qMm7Kej_15KEnAIKbSS2RuJiQBSkw20b5YomF4S08plnujZl09KZLfkAg3_lGf7mWBG0tC7TPoXzp0X29GG5fOYovISE9JG8pnif9CUa2tsgnwRg8x-h4UiQeXdZosJG6oFQ2S-mU_LNc48ExNTypA-IAknnt1ThRPhvpGBqOi-kHafvEB2znHSqFbjyYMyrdphQ4VtSk0alsqOTjUE4yzoiR6e8BMBEOWKopdwj8ZIMrN6flLfcVO3mtgwJ6F4sXaJnVc2t5GQeRnPn6If3ktADcOZtqh6QIAvtCcvOhqC6PwqjRHXv7_XQVgx4iavSPHbdDfIgDAz6rhFeLBeAL-fcKb2Ul3ZxUK6vckj0U2VXM4jqyVgQBkEYLkZs88CGt92pUr0BJ7p7FR7ek46wmD_q_0plcpu99ycM0GXX8Y7KBaV9B6dTHz8nd795IczRgZgBBXr6mOa_vaF7m3UhLagg8KfJiTDTcisgs0G5D-1ZHnuWxwYcXcf5aXd8Z-QnwZTUn8GGqRBrTwhqNaQ8DemNzeSy7KBQZMSbhsYzV-aeec3EIJjRBJ3oT1rFsTM6RP_BwiMJ70LNLH12asRQaEoUlvXfRWmPvOOBOdUdvLIuuwLdKJoNtGyTBeZBLspMVkjnu5Oc30_25yz8dDlhbZ62Wp9WIvJFlYaFfqQomX0CV1NI11he9Y2p4nfXnmWiDGbddl-92OjHOCt4AerJ0snViZvdykS4pfBve4oUijB4HEnOxZJY_DwyJN-kAC-ctMjaJTBYrNfB4tVZQ6Gw9MBcmUyvszXjrJAy2ONYKDPkS5U8bTzOmFVFtvUabSOo2rbsemEq48xsV2jgzVJsSZO94z7hgHAmBPB0KE0RFO7SJMU4XxtK5CWIMBFmuDTXceU8X01WZ42Qbx8UYwLm4uIIwbJWpiArevYvMPd35UnrY_sk1kjrSsn25PiNSLgXGkGlxzifV5DlLBSuRI4hGtUjP-5y4-Jvcxw90TUA7ZzNcoyyAFkxVdCZy0a5Wq06jn3sczTATtNdT7W3Q3H0MosnI52xpjQBGCUbRRIdf7qU4IvsEUlWS5hjOaamKz0CYfj-viskaMwdz2xOBAMgLYTcRi5RWdq74wmHGs1NRbQUPZrlW055aXbwgxP7RUpJ4GB9C9qH71EOWXtlb0C36Utbb81kOeWwOSTVNuz2kdm2p4prmjEsozy3WI9WyAZELzuagVmiL_PLFXhxwukaUfqR-odsXR9TayWbAATWlj9HTUAidmXXcjNNHtdoOyVv3x1dEJoTrcJ81qMV7uUMl3GTCt7GrPBdH_bb3dUsPnWXnHwnL4L8TBh3_h6nMuhU180Cy7rkocmbPVdjf4T70hwZ4-Xd-72UNooHJISXWTmmWLotprDsLk8oG6-xDUPqCoOQd76dbTtli-Fwt2NRGtq7gAKRImnFUChEWDcx_-y4Ehjv9t__9egDzs7tZMTlmxbMCVMwBL0Avndty1GPdfADNFK6nZL6gXxi4-nPeUN3_wG5HuwgGdPmgS42A0ePJUb0FO1Jzgkq-ckkhIs_5CXB54Fo3JS6Od8r_KEnrsZKVrn0L4V3i62L3bKU9u5vToYmyjQRXZtUa1wTNQ-hD1AducMLKb3118wg0X2jgyctBbwqaZvQCMOLaMQcSK8757ZERUKEiSfN4UbhCauWIwEGmmr7Hnncg.SL3VdMlONELEx4iYWVaeCQ"
#     }, conversation_id=None, parent_id=None)
#     chatbot.refresh_session()
#     chatbot.reset_chat()
# except:
#     print("ai failed to setup")
#     AISETUP = False
# else:
#     AISETUP = True
# finally:
#     pass
# def airespond(prompt) -> str:
#     if AISETUP:
#         return str(chatbot.ask(prompt, conversation_id=None, parent_id=None)["message"])
#     else:
#         return "ai nefunguje dačo sa dogabalo"

# majo ma ban, dezider ma ban, zdeno ma ban, a aj julo (už nie????)
# treba novy ucet (už nie???)
# facebook nema rad botov
# vpn?
client = fbw.Wrapper(prefix="!", email="0915255307", password="kubstein")

@client.Command("oneskorenie", [], "oneskorenie")
def oneskorenie(ts,**kwargs):
    print(ts, dt.now().timestamp())
    client.reply(int((dt.now().timestamp())-(ts/1000)))

# @client.Command("ai", ["prompt"], "umela inteligencia lol")
# def majoai(args, **kwargs):
#     prompt = args["prompt"]
#     print(prompt)
#     client.reply(airespond(prompt))

@client.Command("help", [], "pošle help")
def majohelp(**kwargs):
    """
    Aplication command
    """
    client.sendFile(client.utils_genHelpImg())


@client.Command("say", ["sprava"], "napíše vec")
def say(args, **kwargs):
    """
    Aplication command
    """
    if args:
        print(args)
        client.reply(args["sprava"])


@client.Command("tts", ["vec"], "povie vec")
def tts(args, **kwargs):
    """
    Aplication command
    """
    filename = "tts.mp3"
    slovo = args["vec"]
    slovo.replace("\n", "").replace(":", "").replace("'", "").replace("\\", "")
    if not len(slovo) + 4 > 1000:
        gTTS(slovo, lang="sk").save(filename)
        client.sendFile(filename)


@client.Command("gfoto", ["vec"], "najde na googly fotku")
def googlefoto(args, **kwargs):
    """
    Aplication command
    """
    from google_images_search import GoogleImagesSearch

    gis = GoogleImagesSearch(
        "AIzaSyA3YguR6_IFNDMzVzfazCW11JlsN_ZKnjQ", "720a9ec42ba2344e9"
    )
    _searchparams = {"q": args["vec"], "num": 5, "fileType": "jpg"}
    gis.search(search_params=_searchparams)
    for image in gis.results():
        try:
            client.sendFile(image.url)
        except Exception:
            pass


@client.Command("pracuješ", [], "zisti ci majo pracuje")
def pracujes(**kwargs):
    """
    Aplication command
    """
    count = client.utils_threadCount() - 2
    if count:
        client.reply(f"jj {count}")
    else:
        client.reply("nn")


@client.Command("zmaz", ["kolko"], "zmaze spravy")
def zmaz(args, thread, **kwargs):
    """
    Aplication command
    """
    thread_id = thread[0]
    test = 0
    num = int(args["kolko"])
    messages = client.fetchThreadMessages(thread_id=thread_id, limit=10 * num)
    for message in messages:
        if message.author == client.uid and not message.unsent:
            if test < num:
                client.unsend(message.uid)
                test += 1
    client.reply(f"zmazané {num} správ.")


@client.Command("yt", ["link/vec"], "pošle video")
def vid(args, thread, **kwargs):
    """
    Aplication command
    """
    if client.utils_isURL(args["link/vec"]):
        filename = "video.mp4"
        filename2 = "video1.mp4"
        video = YouTube(args["link/vec"]).streams.filter(file_extension="mp4").first()
        video.download(output_path=os.getcwd(), filename=filename)
        client.utils_compressVideo(filename, filename2)
        os.remove(filename)
    else:
        filename = "video.mp4"
        filename2 = "video1.mp4"
        search = Search(args["link/vec"])
        video_results = search.results[0]
        video_results.streams.filter(file_extension="mp4").first().download(
            output_path=os.getcwd(), filename=filename
        )
        client.utils_compressVideo(input=filename, output=filename2)
        os.remove(filename)

    client.sendFile(filename2, args["link/vec"],thread=thread)


@client.Command("slovnik", ["vec"], "najde vec na slovniku")
def slovnik(args, **kwargs):
    """
    Aplication command
    """
    slovo = args["vec"]
    end = ""
    rt = requests.get(f"https://slovnik.juls.savba.sk/?w={slovo}", timeout=2)
    soup = BeautifulSoup(rt.content)
    try:
        for x in soup.body.form.section.div.find_all("p"):
            end += x.get_text() + "\n"

        client.reply(end.strip())
    except AttributeError:
        client.reply("take slovo nie je")


@client.Command("nazor", ["vec"], "da nazor na vec")
def nazor(args, **kwargs):
    """
    Aplication command
    """
    if random.randint(1, 2) == 1:
        client.reply("👍")
    else:
        client.reply("🤢🤮👎")

@client.Command("sprava", ["meno[i]/id","sprava"], "posle spravu")
def sprava(args, **kwargs):
    id = args["meno[i]/id"]
    sprava = args["sprava"]
    thread = client.utils_getThreadFromUserIndex(id)
    client.sendmsg(sprava,thread)

@client.Command("ludia", ["meno"], "vyhlada ludi")
def ludia(args, **kwargs):
    meno = args["meno"]
    _ = ""
    for i,x in enumerate(client.utils_searchForUsers(meno)):
        name = client.utils_getUserName(x)
        _+= f"{i} | {name} | {x}\n"
    client.reply(_)

@client.Command("spravy", ["meno[i]/id"], "posle konverzaciu")
def spravy(args, **kwargs):
    id = args["meno[i]/id"]
    thread = client.utils_getThreadFromUserIndex(id)
    spravy = client.fetchThreadMessages(thread[0], limit=50)
    spravy.reverse()
    for message in spravy:
        list += f"{client.fetchUserInfo(message.author)[message.author].name} -> {message.text}\n"

@client.Command("uinfo", ["meno[i]/id"], "zisti info")
def userinfo(args, **kwargs):
    id= client.utils_getIDFromUserIndex(args["meno[i]/id"])
    user = client.fetchUserInfo(id)[id]
    pfp = user.photo
    url = user.url
    count = user.message_count or 0
    name = user.name
    message = f"""
    {name}:
        Správy: {count}
        Url: {url}
    """
    thread = client.reply(message)
    client.sendFile(pfp,"Fotka:",thread)

client.listen(markAlive=True)
