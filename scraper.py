from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

TOKEN = "8099249320:AAH0_rr2Whrc5hEcBJkBiColVpqxsu74_ZU"  # Öz Tokenini yaz
tapaz_link = "https://tap.az/elanlar/elektronika/noutbuklar?keywords_source=search_suggestion&order=&q%5Buser_id%5D=&q%5Bcontact_id%5D=&q%5Bprice%5D%5B%5D=&q%5Bprice%5D%5B%5D=&q%5Bregion_id%5D=418&q%5Bkeywords%5D=macbook&log=true"

def scrape_first_product(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return "❌ Tap.az-a daxil ola bilmədim."

    soup = BeautifulSoup(r.text, "html.parser")

    # 1. İlk məhsulun linkini tap
    product_link_tag = soup.select_one("div.products > div.products-i > a")
    if not product_link_tag:
        return "❌ Heç bir məhsul tapılmadı."

    product_url = "https://tap.az" + product_link_tag["href"]

    # 2. Məhsul səhifəsinə keç və məlumatları topla
    r2 = requests.get(product_url, headers=headers)
    if r2.status_code != 200:
        return "❌ Məhsul səhifəsinə daxil ola bilmədim."

    product_soup = BeautifulSoup(r2.text, "html.parser")

    title = product_soup.find("h1")
    price = product_soup.find("div", class_="price")
    desc = product_soup.find("div", class_="product-description__content")

    title = title.text.strip() if title else "Başlıq yoxdur"
    price = price.text.strip() if price else "Qiymət yoxdur"
    desc = desc.text.strip() if desc else "Təsvir yoxdur"

    return f"📦 <b>{title}</b>\n💰 <b>Qiymət:</b> {price}\n📄 <b>Təsvir:</b> {desc}"

# === Bot komandası ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = scrape_first_product(tapaz_link)
    await update.message.reply_html(result)

# === Botun işə salınması ===
def main():
    app = ApplicationBuilder().token("8099249320:AAH0_rr2Whrc5hEcBJkBiColVpqxsu74_ZU").build()
    app.add_handler(CommandHandler("start", start))
    print("Bot işə düşdü.")
    app.run_polling()

if __name__ == "__main__":
    main()
