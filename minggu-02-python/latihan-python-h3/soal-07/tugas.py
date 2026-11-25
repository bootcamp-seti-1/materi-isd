class Tugas:
    def __init__(self, judul):
        self.judul = judul
        self.selesai = False

    def tandai_selesai(self):
        self.selesai = True

    def __str__(self):
        tanda = "x" if self.selesai else " "
        return f"[{tanda}] {self.judul}"


class PengelolaTugas:
    def __init__(self):
        self.daftar = []

    def tambah(self, judul):
        judul = judul.strip()
        if judul == "":
            print("Judul tidak boleh kosong")
            return
        self.daftar.append(Tugas(judul))
        print(f"Ditambahkan: {judul}")

    def tampilkan(self):
        for nomor, item in enumerate(self.daftar, start=1):
            print(f"{nomor}. {item}")

    def selesai(self, nomor):
        if nomor < 1 or nomor > len(self.daftar):
            print("Nomor tidak ada")
            return
        item = self.daftar[nomor - 1]
        item.tandai_selesai()
        print(f"Selesai: {item.judul}")

    def ringkasan(self):
        total = len(self.daftar)
        jumlah_selesai = 0
        for item in self.daftar:
            if item.selesai:
                jumlah_selesai += 1
        print(f"Total {total} | selesai {jumlah_selesai} | belum {total - jumlah_selesai}")
