# Alya Arda v2
import streamlit as st
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from karakter_yukle import karakter_promptu_yukle, GORUNEN_ISIMLER
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_ADI = "openai/gpt-oss-120b"

VERI_KLASORU = "veri"
KULLANICI_DOSYASI = os.path.join(VERI_KLASORU, "kullanicilar.json")
SOHBET_KLASORU = os.path.join(VERI_KLASORU, "sohbetler")
PROMPT_KLASORU = "."

os.makedirs(VERI_KLASORU, exist_ok=True)
os.makedirs(SOHBET_KLASORU, exist_ok=True)

if not os.path.exists(KULLANICI_DOSYASI):
    with open(KULLANICI_DOSYASI, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=2)

def kullanicilari_yukle():
    with open(KULLANICI_DOSYASI, "r", encoding="utf-8") as f:
        return json.load(f)

def kullanici_kaydet(kullanici_id, bilgiler):
    kullanicilar = kullanicilari_yukle()
    kullanicilar[kullanici_id] = bilgiler
    with open(KULLANICI_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(kullanicilar, f, ensure_ascii=False, indent=2)

def yeni_kullanici_id_uret():
    kullanicilar = kullanicilari_yukle()
    return f"kullanici_{len(kullanicilar) + 1:03d}"

def prompt_yukle(karakter):
    if karakter == "alya":
        dosya = os.path.join(PROMPT_KLASORU, "karakterler", "alya_sistem.txt")
    else:
        dosya = os.path.join(PROMPT_KLASORU, "karakterler", "arda_sistem.txt")
    with open(dosya, "r", encoding="utf-8") as f:
        return f.read()

def sohbet_yukle(kullanici_id):
    dosya = os.path.join(SOHBET_KLASORU, f"{kullanici_id}.json")
    if os.path.exists(dosya):
        with open(dosya, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sohbet_kaydet(kullanici_id, mesajlar):
    dosya = os.path.join(SOHBET_KLASORU, f"{kullanici_id}.json")
    with open(dosya, "w", encoding="utf-8") as f:
        json.dump(mesajlar, f, ensure_ascii=False, indent=2)

def groq_cevap_al(sistem_promptu, mesajlar):
    client = Groq(api_key=GROQ_API_KEY)
    tam_mesajlar = [{"role": "system", "content": sistem_promptu}] + mesajlar
    cevap = client.chat.completions.create(
        model=MODEL_ADI,
        messages=tam_mesajlar,
        temperature=0.8,
        max_tokens=500
    )
    return cevap.choices[0].message.content

st.set_page_config(
    page_title="Alya & Arda",
    page_icon="🌸",
    layout="centered"
)

if "kullanici" not in st.session_state:
    st.session_state.kullanici = None

if st.session_state.kullanici is None:
    st.markdown(
        """
        <h1 style='text-align: center; color: #ff6b9d; font-weight: 800; font-size: 42px;'>
            🌸 Alya & Arda 🐞
        </h1>
        <p style='text-align: center; font-size: 22px; color: #2d3436; font-weight: 600;'>
            Sana eşlik edecek bir arkadaş seç
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🎂 Yaşın kaç?")
    yas = st.number_input(
        "Yaşın kaç?",
        min_value=10,
        max_value=99,
        value=25,
        step=1,
        label_visibility="collapsed"
    )

    st.markdown("### 👤 Cinsiyetin?")
    cinsiyet = st.radio(
        "Cinsiyetin?",
        ["Kadın", "Erkek", "Belirtmek istemiyorum"],
        index=None,
        label_visibility="collapsed"
    )

    st.markdown("### 💬 Kiminle konuşmak istersin?")
    karakter = st.radio(
        "Kiminle konuşmak istersin?",
        ["🌸 Alya", "🐞 Arda"],
        index=None,
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### ✅ Onaylar")
    onay_18 = st.checkbox("18 yaşından büyüğüm.")
    onay_kvkk = st.checkbox(
        "KVKK aydınlatma metnini okudum, kişisel verilerimin işlenmesine onay veriyorum."
    )

    st.divider()

    if st.button("Başla", type="primary", use_container_width=True):
        if cinsiyet is None:
            st.error("Lütfen cinsiyetini seç.")
        elif karakter is None:
            st.error("Lütfen bir karakter seç.")
        elif not onay_18:
            st.error("Devam etmek için 18 yaşından büyük olduğunu onaylaman gerekiyor.")
        elif not onay_kvkk:
            st.error("Devam etmek için KVKK metnini onaylaman gerekiyor.")
        else:
            karakter_adi = karakter.replace("🌸 ", "").replace("🐞 ", "").lower()
            kullanici_id = yeni_kullanici_id_uret()
            bilgiler = {
                "yas": yas,
                "cinsiyet": cinsiyet,
                "karakter": karakter_adi,
                "onay_18": onay_18,
                "onay_kvkk": onay_kvkk,
                "kayit_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "sehir": None,
                "meslek": None
            }
            kullanici_kaydet(kullanici_id, bilgiler)
            st.session_state.kullanici = {"id": kullanici_id, **bilgiler}
            st.rerun()

else:
    k = st.session_state.kullanici
    kullanici_id = k["id"]
    karakter = k["karakter"]

    if karakter == "alya":
        st.markdown(
            "<h1 style='text-align: center; color: #ff6b9d;'>🌸 Alya</h1>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<h1 style='text-align: center; color: #ff6b9d;'>🐞 Arda</h1>",
            unsafe_allow_html=True
        )

    if "mesajlar" not in st.session_state:
        st.session_state.mesajlar = sohbet_yukle(kullanici_id)

    for mesaj in st.session_state.mesajlar:
        with st.chat_message(mesaj["role"]):
            st.write(mesaj["content"])

    yeni_mesaj = st.chat_input("Bir şey yaz...")

    if yeni_mesaj:
        st.session_state.mesajlar.append({"role": "user", "content": yeni_mesaj})
        with st.chat_message("user"):
            st.write(yeni_mesaj)

        with st.chat_message("assistant"):
            with st.spinner("Yazıyor..."):
                try:
                    sistem_promptu = prompt_yukle(karakter)
                    cevap = groq_cevap_al(sistem_promptu, st.session_state.mesajlar)
                    st.write(cevap)
                    st.session_state.mesajlar.append({"role": "assistant", "content": cevap})
                    sohbet_kaydet(kullanici_id, st.session_state.mesajlar)
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")

    with st.sidebar:
        st.write(f"**Yaş:** {k['yas']}")
        st.write(f"**Cinsiyet:** {k['cinsiyet']}")
        st.write(f"**Karakter:** {karakter.capitalize()}")
        st.divider()
        if st.button("Çıkış Yap"):
            st.session_state.kullanici = None
            st.session_state.mesajlar = []
            st.rerun()
