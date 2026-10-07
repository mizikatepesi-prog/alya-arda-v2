import os

# Bu dosyanın bulunduğu klasörü bul
BU_DOSYANIN_KLASORU = os.path.dirname(os.path.abspath(__file__))
KARAKTER_KLASORU = os.path.join(BU_DOSYANIN_KLASORU, "karakterler")

KARAKTER_DOSYALARI = {
    "alya": "alya_sistem.txt",
    "arda": "arda_sistem.txt",
}

GORUNEN_ISIMLER = {
    "🌸 Alya": "alya",
    "🐞 Arda": "arda",
}

_prompt_onbellek = {}


def karakter_promptu_yukle(karakter_anahtar):
    if karakter_anahtar in _prompt_onbellek:
        return _prompt_onbellek[karakter_anahtar]

    if karakter_anahtar not in KARAKTER_DOSYALARI:
        raise ValueError(f"Bilinmeyen karakter: {karakter_anahtar}")

    dosya_adi = KARAKTER_DOSYALARI[karakter_anahtar]
    yol = os.path.join(KARAKTER_KLASORU, dosya_adi)

    if not os.path.exists(yol):
        raise FileNotFoundError(
            f"Dosya bulunamadı: {yol}\n"
            f"Aranan klasör: {KARAKTER_KLASORU}\n"
            f"Klasördeki dosyalar: {os.listdir(KARAKTER_KLASORU) if os.path.exists(KARAKTER_KLASORU) else 'klasör yok'}"
        )

    with open(yol, "r", encoding="utf-8") as f:
        icerik = f.read().strip()

    _prompt_onbellek[karakter_anahtar] = icerik
    return icerik