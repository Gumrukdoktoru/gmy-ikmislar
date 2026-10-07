"""GMY sınav PDF'inden soruları ve kırmızı basılmış (resmî) cevapları çıkarır.

Kullanım:
    python3 kirmizi_cevap_cikar.py SINAV.pdf CIKTI.json

Çıktı: [{"no": 1, "kok": "...", "siklar": {"A": "...", ...}, "cevap": "D"}, ...]
Ekrana cevap anahtarını (100 harf) ve ayrıştırılamayan soruları yazar.

Yöntem: Sayfalar iki sütuna bölünür, karakterler satırlara gruplanır, kırmızı
(1,0,0) karakter dizileri « » ile işaretlenir. Kapak ve "kurallar" sayfaları
atlanır. Bir şıkkın metninin yarıdan fazlası kırmızıysa o şık cevaptır.
Gereksinim: pdfplumber.
"""
import json
import re
import sys

import pdfplumber

KIRMIZI = (1.0, 0.0, 0.0)
GURULTU = re.compile(
    r'^(.*SINAVI 20\d\d$|.*BAKANLIĞI$|T\.C\.( TİCARET)?$|TİCARET$|.*YARDIMCILI(ĞI)?$|'
    r'TİCARET BAKANLIĞI|GÜMRÜK MÜŞAVİR YARDIMCILI|[AB] Kitapçığı|[AB]$|Diğer [Ss]ayfa|\d{1,2}$|\d{1,2} Diğer)')
SIK_SONU_GURULTU = re.compile(r'\s+(GÜMRÜK MÜ|ŞAVİR|BAKANLIĞI|RDIMCILI|ARDIMCI|[AB] Kitapçığı)')


def kirmizi_mi(c):
    renk = c.get('non_stroking_color')
    return renk is not None and tuple(renk) == KIRMIZI


def dogrusallastir(pdf_yolu):
    """Her sayfa için, sütun sırasıyla, kırmızı dizileri « » ile işaretli satır listesi döndürür."""
    sayfalar = []
    with pdfplumber.open(pdf_yolu) as pdf:
        for p in pdf.pages:
            orta = p.width / 2
            karakterler = [c for c in p.chars if c['text'].strip() or c['text'] == ' ']
            satirlar_out = []
            for sutun in (0, 1):
                cs = [c for c in karakterler if (c['x0'] < orta - 5) == (sutun == 0)]
                cs.sort(key=lambda c: (round(c['top']), c['x0']))
                satirlar = []
                for c in cs:
                    if satirlar and abs(satirlar[-1][0] - c['top']) < 3:
                        satirlar[-1][1].append(c)
                    else:
                        satirlar.append([c['top'], [c]])
                for _, sc in satirlar:
                    sc.sort(key=lambda c: c['x0'])
                    metin, onceki, kirmizida = '', None, False
                    for c in sc:
                        k = kirmizi_mi(c) if c['text'].strip() else kirmizida
                        if k and not kirmizida:
                            metin += '«'
                        if not k and kirmizida:
                            metin += '»'
                        kirmizida = k
                        if onceki is not None and c['x0'] - onceki['x1'] > 1.5 and not metin.endswith(' '):
                            metin += ' '
                        metin += c['text']
                        onceki = c
                    if kirmizida:
                        metin += '»'
                    if metin.strip():
                        satirlar_out.append(metin.strip())
            sayfalar.append(satirlar_out)
    return sayfalar


def ayristir(sayfalar):
    # kapak (ilk sayfa) ve "kurallar" sayfası atlanır
    secili = [s for i, s in enumerate(sayfalar)
              if i > 0 and 'KURALLAR' not in ' '.join(s).replace('«', '').replace('»', '')]
    satirlar = [l for s in secili for l in s
                if not GURULTU.match(l.replace('«', '').replace('»', '').strip())]
    sorular, cur, beklenen = [], None, 1
    for l in satirlar:
        duz = l.replace('«', '').replace('»', '')
        m = re.match(r'^(\d{1,3})\.\s*(.*)', duz)
        if m and int(m.group(1)) == beklenen:
            cur = {'no': beklenen, 'ham': [l[l.index('.') + 1:]]}
            sorular.append(cur)
            beklenen += 1
            continue
        if cur is not None:
            cur['ham'].append(l)
    sonuc = []
    for q in sorular:
        metin = ' '.join(x.strip() for x in q['ham'])
        kirmizi, durum, temiz = [], False, ''
        for ch in metin:
            if ch == '«':
                durum = True
                continue
            if ch == '»':
                durum = False
                continue
            temiz += ch
            kirmizi.append(durum)
        sira, istenen = [], 'A'
        for o in re.finditer(r'(?:(?<=\s)|^)([A-E])\)\s', temiz):
            if o.group(1) == istenen:
                sira.append(o)
                istenen = chr(ord(istenen) + 1)
                if istenen > 'E':
                    break
        kok = temiz[:sira[0].start()].strip() if sira else temiz
        siklar, cevap = {}, []
        for i, o in enumerate(sira):
            son = sira[i + 1].start() if i + 1 < len(sira) else len(temiz)
            mm = SIK_SONU_GURULTU.search(temiz[o.end():son])
            if mm:
                son = o.end() + mm.start()
            siklar[o.group(1)] = temiz[o.end():son].strip()
            govde = [r for r, c in zip(kirmizi[o.start():son], temiz[o.start():son]) if not c.isspace()]
            if govde and sum(govde) / len(govde) > 0.5:
                cevap.append(o.group(1))
        sonuc.append({'no': q['no'], 'kok': re.sub(r'\s+', ' ', kok), 'siklar': siklar, 'cevap': ''.join(cevap)})
    return sonuc


if __name__ == '__main__':
    pdf_yolu, cikti = sys.argv[1], sys.argv[2]
    veri = ayristir(dogrusallastir(pdf_yolu))
    json.dump(veri, open(cikti, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    sorunlu = [q['no'] for q in veri if len(q['cevap']) != 1 or len(q['siklar']) != 5]
    print('soru:', len(veri), '| anahtar:', ''.join(q['cevap'] or '?' for q in veri))
    print('ayrıştırılamayan:', sorunlu or 'yok')
