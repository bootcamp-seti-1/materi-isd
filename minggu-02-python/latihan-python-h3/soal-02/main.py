tugas = []


def tambah(judul):
judul = judul.strip()
    if judul = "":
        print("Judul tidak boleh kosong")
        return
    tugas.append({"judul": judul, "selesai": False})


def selesai(nomor):
    if nomor < 1 or nomor > len(tugas)
        print("Nomor tidak ada")
        return
    tugas[nomor - 1]["selesai"] = True


def ringkasan():
    total = len(tugas)
    jumlah_selesai = 0
    for item in tugas:
        if item["selesai"]:
            jumlah_selesai += 1
    print(f"Total {total} | selesai {jumlah_selesai} | belum {total - jumlah_selesai}")


tambah("bangun pagi")
tambah("   ")
tambah("sarapan")
tambah("berangkat")
tambah("")
selesai(2)
selesai(7)
ringkasan()
