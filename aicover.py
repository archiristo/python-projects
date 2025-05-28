import librosa
import soundfile as sf

# Ses dosyasını yükle
def ses_yukle(dosya_yolu):
    ses, sr = librosa.load(dosya_yolu, sr=None)
    return ses, sr

# Ses frekansını değiştirme (pitch shifting)
def ses_donusumu(ses, sr, yaritone):
    return librosa.effects.pitch_shift(ses, sr=sr, n_steps=yaritone)  # sr parametresini ekledik!

# İşlenmiş ses dosyasını kaydet
def ses_kaydet(dosya_adi, ses, sr):
    sf.write(dosya_adi, ses, sr)

# Kullanım
girilen_dosya = "NawalElZoghbi_AamBahkiMaHali.mp3"
cikis_dosya = "cover_sarki.mp3"

ses, sr = ses_yukle(girilen_dosya)
cover_ses = ses_donusumu(ses, sr, yaritone=5)  # Ses tonunu 5 yarıton yukarı çek
ses_kaydet(cikis_dosya, cover_ses, sr)

print("Cover şarkı oluşturuldu! 🎶✨")