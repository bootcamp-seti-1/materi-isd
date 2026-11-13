catatan = {}


def hadir(nama):
    if nama in catatan:
        print(f"{nama} sudah tercatat")
        return
    catatan[nama] = "hadir"


def izin(nama, alasan):
    if nama in catatan:
        print(f"{nama} sudah tercatat")
        return
    catatan[nama] = "izin: " + alasan


def jumlah_hadir():
    jumlah = 0
    for status in catatan.values():
        if status == "hadir":
            jumlah += 1
    return jumlah


def jumlah_izin():
    jumlah = 0
    for status in catatan.values():
        if status.startswith("izin"):
            jumlah += 1
    return jumlah


def rekap():
    print(f"Hadir {jumlah_hadir()} | izin {jumlah_izin()}")
