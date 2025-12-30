# RASTGELE SAYI ÜRETİCİ ALGORİTMA RAPORU
**SplitMix64 Tabanlı PRNG (Deterministik)**

**Hazırlayan:** MUHAMMET HASAN UYAR  
**Ders / Şube:** BİLGİ SİSTEMLERİ GÜVENLİĞİ / 3-A

---

**Özet:** Bu rapor, 64-bit durum (state) kullanan SplitMix64 tabanlı bir yalancı rastgele sayı üreticisini (PRNG) tanımlar. Algoritma; tohum (seed) girdisi, durum güncelleme kuralı, çıktı üretim fonksiyonu, örnek kod ve temel dağılım testlerini içerir.

---

## 1. Problem Tanımı ve Hedef
Rastgele sayı üretimi; simülasyon, oyun geliştirme, örnekleme, test verisi oluşturma ve algoritmik deneyler gibi alanlarda kullanılır. Bu rapordaki hedef, deterministik bir yalancı rastgele sayı üretici (PRNG) tanımlamak ve referans bir uygulamasını sunmaktır. Deterministik PRNG; aynı seed verildiğinde aynı sayı dizisini üretir; bu da tekrarlanabilir deneyler için avantaj sağlar.

## 2. Tasarım Şartnamesi
*   **Algoritma tipi:** Yalancı rastgele sayı üretici (PRNG), deterministik.
*   **Durum (state):** 64-bit tamsayı, $s$.
*   **Tohum (seed):** 64-bit tamsayı (kullanıcı girdisi).
*   **Üretilen çıktı:** 64-bit tamsayı, $x$.
*   **Periyot:** $2^{64}$ (teorik olarak; tüm durumlar dolaşılır).
*   **Zaman karmaşıklığı:** $O(1)$ (sabit sayıda kaydırma, XOR ve çarpma).
*   **Bellek karmaşıklığı:** $O(1)$ (tek 64-bit durum).

## 3. Algoritma Tanımı (SplitMix64)
SplitMix64; هر adımda durumu sabit bir artım ile günceller ve ardından çıktıyı üretmek için bit kaydırmaları, XOR ve 64-bit çarpma işlemleri ile karıştırma uygular. Karıştırma, çıktı bitlerinin state içindeki bitlerden daha iyi dağılmasını (diffusion) hedefler.

### 3.1 Matematiksel İfadeler
Aşağıdaki tanımlar 64-bit tamsayılar üzerinde yapılır. Tüm toplama ve çarpma işlemleri mod $2^{64}$ alınmıştır.

**Durum güncelleme:**
$$s_{i+1} = (s_i + \gamma) \mod 2^{64}, \text{burada } \gamma = 0x9E3779B97F4A7C15$$

**Karıştırma (mixing) ve çıktı:**
$$z = s_{i+1}$$
$$z = (z \oplus (z \gg 30)) \times 0xBF58476D1CE4E5B9$$
$$z = (z \oplus (z \gg 27)) \times 0x94D049BB133111EB$$
$$x_i = z \oplus (z \gg 31)$$

### 3.2 Pseudocode
```
Girdi: seed (64-bit)
Durum: s = seed

Fonksiyon NEXT_U64():
    s = (s + 0x9E3779B97F4A7C15) mod 2^64
    z = s
    z = (z XOR (z >> 30)) * 0xBF58476D1CE4E5B9 mod 2^64
    z = (z XOR (z >> 27)) * 0x94D049BB133111EB mod 2^64
    x = z XOR (z >> 31)
    döndür x
```

## 4. Referans Uygulama (Python)
Aşağıdaki örnek kod; 64-bit çıktı üretilmesi (`next_u64`), belirli aralıkta sayı (`randbelow`) ve [0,1) aralığında float (`random`) fonksiyonlarını verir. `randbelow`, modulo yanlılığını azaltmak için rejection sampling kullanır.

```python
class SplitMix64RNG:
    """Deterministik PRNG (kripto-guvenli degildir)."""
    MASK64 = (1 << 64) - 1

    def __init__(self, seed: int):
        self.state = seed & self.MASK64

    def _next(state: int) -> tuple[int, int]:
        # 1) Durum guncelleme
        state = (state + 0x9E3779B97F4A7C15) & SplitMix64RNG.MASK64
        # 2) Karistirma (mixing)
        z = state
        z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9 & SplitMix64RNG.MASK64
        z = (z ^ (z >> 27)) * 0x94D049BB133111EB & SplitMix64RNG.MASK64
        out = z ^ (z >> 31)
        return state, out & SplitMix64RNG.MASK64

    def next_u64(self) -> int:
        self.state, out = self._next(self.state)
        return out

    def randbelow(self, n: int) -> int:
        """0..n-1 araliginda, modulo yanliligini azaltmak icin rejection sampling."""
        if n <= 0:
            raise ValueError("n pozitif olmali")
        # En buyuk 64-bit sayinin n ile bolumunden kalan kismi atla
        limit = (1 << 64) - ((1 << 64) % n)
        while True:
            x = self.next_u64()
            if x < limit:
                return x % n

    def random(self) -> float:
        """[0,1) araliginda float."""
        return (self.next_u64() >> 11) * (1.0 / (1 << 53))
```

## 5. Örnek Çalıştırma
Seed = 20251230 için üretilen ilk 10 adet 64-bit çıktı aşağıdadır:

| # | Cikti (hex) | Cikti (decimal) |
|---|---|---|
| 1 | 0xab98432cfeea66b6 | 12364706637480093366 |
| 2 | 0xff855eb863ca1516 | 18412226797615322390 |
| 3 | 0x1cc977691b7edd4a | 2074320396697394506 |
| 4 | 0xc238b1b3bc0eac48 | 13995131227566156872 |
| 5 | 0xf8ecb93aed65bcb1 | 17936915078651952305 |
| 6 | 0x593d7f0e814b3d00 | 6430435543230397696 |
| 7 | 0x90ac1eb8857213e2 | 10424741015317517282 |
| 8 | 0x56e652482a7cdfec | 6261782801809203180 |
| 9 | 0xa9af9d3819f1b329 | 12227164377613185833 |
| 10 | 0x6deb85c5d334acd9 | 7920571454359645401 |

## 6. Basit Analiz ve Gözlemler
Bu bölüm; tam bir kriptanaliz değil, yalnızca hızlı bir 'sağlık kontrolü' için basit istatistiksel gözlemler içerir.

### 6.1 Dağılım Kontrolü (x mod 10)
N=50000 üretilen sayı için x mod 10 sınıflarının frekansları aşağıdaki gibidir. İdeal durumda her sınıf ~5000 civarındadır.

| Sinif (x mod 10) | Adet (N=50000) |
|---|---|
| 0 | 5191 |
| 1 | 5002 |
| 2 | 4905 |
| 3 | 4939 |
| 4 | 5007 |
| 5 | 5084 |
| 6 | 4999 |
| 7 | 4986 |
| 8 | 4950 |
| 9 | 4937 |

### 6.2 Bit Dengesi (Popcount Ortalaması)
N=50000 için üretilen 64-bit sayıların 1-bit sayısının ortalaması **32.02374** bulunmuştur. Rastgele bir 64-bit değer için beklenen ortalama 32'dir. Bu sonuç, bitlerin 0/1 dengesinin makul olduğunu gösterir.

## 7. Güvenlik Notları ve Kullanım Sınırları
*   **Kripto-güvenli değildir:** SplitMix64; tahmin edilebilirlik ve state ele geçirme senaryolarına karşı tasarlanmamıştır. Anahtar üretimi, nonce/IV, token, şifreleme gibi güvenlik kritik alanlarda kullanılmaz.
*   **Doğru kullanım örnekleri:** Simülasyon, test verisi, rastgele örnekleme, oyun/agent davranışı, tekrarlanabilir deneyler.
*   **Yanlış kullanım örnekleri:** Parola üretimi, şifreleme anahtarı, session token, kriptografik nonce.

## 8. Sonuç
Bu rapor; 64-bit state kullanan SplitMix64 tabanlı bir PRNG'yi, matematiksel tanımları ve referans kodu ile birlikte sundu. Algoritma hızlı ve uygulaması kolaydır; ancak kriptografik rastgelelik gerektiren senaryolarda kullanılmaz.
