import telebot
import requests
from mistralai import Mistral

# Tes clés API
TELEGRAM_TOKEN = "8592698957:AAFkmgZINn3dk4bMp68s1ruafjCkE1Nl3Y0"
MISTRAL_API_KEY = "3ply9AJAl180z53vk7aoOqslLApaUUou"
NEWS_API_KEY = "94c5621f005f4ba1b317980456d92b57"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
mistral = Mistral(api_key=MISTRAL_API_KEY)

def get_news(query, language="fr"):
    url = f"https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": language,
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if data["status"] == "ok" and data["articles"]:
        articles = data["articles"]
        texte = ""
        for a in articles:
            texte += f"- {a['title']} ({a['source']['name']})\n"
        return texte
    return "Aucune news trouvée."

def analyser_avec_ia(news_texte, sujet):
    prompt = f"""Tu es un expert en géopolitique mondiale.
Voici des titres d'actualités récentes sur : {sujet}

{news_texte}

Fais un résumé clair et simple en français de la situation géopolitique actuelle sur ce sujet. Sois concis (5-8 lignes max)."""

    response = mistral.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Commandes du bot
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, """🌍 Bonjour ! Je suis ton bot géopolitique !

Commandes disponibles :
/usa - Actualités USA / Trump
/france - Actualités France
/gabon - Actualités Gabon
/monde - Grandes puissances mondiales
/chercher [pays ou sujet] - Chercher n'importe quel sujet""")

@bot.message_handler(commands=['usa'])
def usa(message):
    bot.reply_to(message, "🔍 Je cherche les news sur les USA...")
    news = get_news("Trump United States geopolitics", language="en")
    analyse = analyser_avec_ia(news, "les États-Unis et Trump")
    bot.reply_to(message, f"🇺🇸 **USA / Trump**\n\n{analyse}")

@bot.message_handler(commands=['france'])
def france(message):
    bot.reply_to(message, "🔍 Je cherche les news sur la France...")
    news = get_news("France géopolitique diplomatie")
    analyse = analyser_avec_ia(news, "la France sur la scène géopolitique")
    bot.reply_to(message, f"🇫🇷 **France**\n\n{analyse}")

@bot.message_handler(commands=['gabon'])
def gabon(message):
    bot.reply_to(message, "🔍 Je cherche les news sur le Gabon...")
    news = get_news("Gabon actualité politique", language="fr")
    if "Aucune" in news:
        news = get_news("Gabon news", language="en")
    analyse = analyser_avec_ia(news, "la situation au Gabon")
    bot.reply_to(message, f"🇬🇦 **Gabon**\n\n{analyse}")

@bot.message_handler(commands=['monde'])
def monde(message):
    bot.reply_to(message, "🔍 Je cherche les news géopolitiques mondiales...")
    news = get_news("geopolitics world powers China Russia Europe", language="en")
    analyse = analyser_avec_ia(news, "la géopolitique mondiale et les grandes puissances")
    bot.reply_to(message, f"🌍 **Monde**\n\n{analyse}")

@bot.message_handler(commands=['chercher'])
def chercher(message):
    sujet = message.text.replace("/chercher", "").strip()
    if not sujet:
        bot.reply_to(message, "Écris un sujet après /chercher\nExemple : /chercher Chine Taiwan")
        return
    bot.reply_to(message, f"🔍 Je cherche les news sur : {sujet}...")
    news = get_news(sujet)
    if "Aucune" in news:
        news = get_news(sujet, language="en")
    analyse = analyser_avec_ia(news, sujet)
    bot.reply_to(message, f"🔎 **{sujet}**\n\n{analyse}")

print("Bot lancé !")
bot.polling()


