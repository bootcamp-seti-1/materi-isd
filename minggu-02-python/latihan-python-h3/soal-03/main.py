tugas = []


def tambah(judul):
    judul = judul.strip()
    if judul == "":
        print("Judul tidak boleh kosong")
        return
    tugas.append({"judul": judul, "selesai": False})
    print(f"Ditambahkan: {judul}")


def tampilkan():
    for nomor, item in enumerate(tugas, start=1):
        tanda = "x" if item["selesai"] else " "
        print(f"{nomor}. [{tanda}] {item['judul']}")


def selesai(nomor):
    if nomor < 1 or nomor > len(tugas):
        print("Nomor tidak ada")
        return
    tugas[nomor - 1]["selesai"] = True
    print(f"Selesai: {tugas[nomor - 1]['judul']}")


def ringkasan():
    total = len(tugas)
    jumlah_selesai = 0
    for item in tugas:
        if item["selesai"]:
            jumlah_selesai += 1
    print(f"Total {total} | selesai {jumlah_selesai} | belum {total - jumlah_selesai}")


print("sakura-tasks. Perintah: add JUDUL, list, done NOMOR, stats, keluar")

while True:
    perintah = input("> ")
    if perintah == "keluar":
        break
    elif perintah == "list":
        tampilkan()
    elif perintah == "stats":
        ringkasan()
    elif perintah.startswith("add "):
        tambah(perintah[4:])
    elif perintah.startswith("done "):
        nomor = perintah[5:]
        if nomor.isdigit():
            selesai(int(nomor))
        else:
            print("Nomor harus angka")
    else:
        print("Perintah tidak dikenal")
