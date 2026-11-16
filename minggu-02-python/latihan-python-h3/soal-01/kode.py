tugas = []


def tambah(judul):
    tugas.append({"judul": judul, "selesai": False})


def selesai(nomor):
    tugas[nomor - 1]["selesai"] = True


tambah("rapat pagi")
tambah("balas email")
tambah("review kode")
tambah("makan siang")
tambah("kirim laporan")

selesai(2)
selesai(5)
selesai(2)
