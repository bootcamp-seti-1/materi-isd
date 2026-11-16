from tugas import PengelolaTugas

kerja = PengelolaTugas()
rumah = PengelolaTugas()

kerja.tambah("kirim penawaran")
kerja.tambah("rapat vendor")
kerja.tambah("review kode")
rumah.tambah("cuci motor")

kerja.selesai(1)
rumah.selesai(1)

selesai_di_rumah = 0
for item in rumah.daftar:
    if item.selesai:
        selesai_di_rumah += 1

print(len(kerja.daftar), len(rumah.daftar), selesai_di_rumah)
