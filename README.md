# Telegram AI Bot (Qwen + Camb)

## 1. Tayyorlash
1. BotFather'dan **YANGI** token oling (eskisini `/revoke` qiling, chunki u ochiq yuborilgan edi).
2. `.env.example` faylini `.env` deb nomlang va o'z tokeningizni kiriting:
   ```
   BOT_TOKEN=sizning_tokeningiz
   ```

## 2. Local test (ixtiyoriy)
```bash
pip install -r requirements.txt
python bot.py
```

## 3. Cloud'ga joylash

### Variant A — Railway.app (eng oson)
1. railway.app'da yangi loyiha oching, "Deploy from GitHub repo" tanlang (yoki fayllarni yuklang).
2. Variables bo'limiga `BOT_TOKEN` ni qo'shing.
3. Railway avtomatik `requirements.txt` va `Procfile`ni o'qib botni ishga tushiradi.

### Variant B — Render.com
1. "New Background Worker" yarating.
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `python bot.py`
4. Environment tab'da `BOT_TOKEN` qo'shing.

### Variant C — Docker (istalgan VPS/cloud)
```bash
docker build -t telegram-ai-bot .
docker run -d --env-file .env telegram-ai-bot
```

## Eslatma
Bot `/start`, `/qwen`, `/camb` orqali Telegram Web App tugmalarini ko'rsatadi.
Agar qwen.ai yoki camb.ai saytlari iframe ichida ochilishni bloklasa
(X-Frame-Options / CSP), tugma bosilganda bo'sh oyna chiqishi mumkin —
bu sizning kodingizdagi xato emas, balki saytning xavfsizlik sozlamasi.
