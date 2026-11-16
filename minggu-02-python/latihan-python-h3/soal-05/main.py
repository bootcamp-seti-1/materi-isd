from tugas import PengelolaTugas

pengelola = PengelolaTugas()

print("sakura-tasks. Perintah: add JUDUL, list, done NOMOR, stats, keluar")

while True:
    perintah = input("> ")
    if perintah == "keluar":
        break
    elif perintah == "list":
        pengelola.tampilkan()
    elif perintah == "stats":
        pengelola.ringkasan()
    elif perintah.startswith("add "):
        pengelola.tambah(perintah[4:])
    elif perintah.startswith("done "):
        nomor = perintah[5:]
        if nomor.isdigit():
            pengelola.selesai(int(nomor))
        else:
            print("Nomor harus angka")
    else:
        print("Perintah tidak dikenal")
