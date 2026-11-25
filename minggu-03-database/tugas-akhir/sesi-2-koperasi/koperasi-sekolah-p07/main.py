from koperasi import Koperasi

koperasi = Koperasi()

while True:
    try:
        baris = input()
    except EOFError:
        break
    kata = baris.split()
    if kata == ["laporan"]:
        koperasi.laporan()
    elif kata == ["stok"]:
        koperasi.stok()
    elif len(kata) == 2 and kata[0] == "saldo":
        koperasi.saldo(kata[1])
    elif len(kata) == 2 and kata[0] == "batal":
        koperasi.batal(kata[1])
    elif len(kata) == 3 and kata[0] == "isi":
        koperasi.isi(kata[1], kata[2])
    elif len(kata) == 4 and kata[0] == "beli":
        koperasi.beli(kata[1], kata[2], kata[3])
