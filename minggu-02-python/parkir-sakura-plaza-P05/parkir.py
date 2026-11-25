from tarif import Tarif


def jam_ke_menit(teks):
    """Ubah "HH:MM" menjadi menit sejak 00:00 (08:05 -> 485)."""
    jam, menit = teks.split(":")
    return int(jam) * 60 + int(menit)


class Parkir:
    def __init__(self):
        self.tarif = Tarif()
        self.di_dalam = {}  # plat -> menit masuk
        self.selesai = []   # (plat, jam ditagih, biaya), urut siapa yang keluar duluan

    def masuk(self, plat, jam):
        """Catat kendaraan masuk. Kalau plat itu masih di dalam, cetak
        "Plat sudah ada di dalam". Kalau berhasil, tidak mencetak apa pun."""
        if plat in self.di_dalam:
            print("Plat sudah ada di dalam")
            return

        self.di_dalam[plat] = jam_ke_menit(jam)

    def keluar(self, plat, jam):
        """Kendaraan keluar. Cek berurutan: plat tidak ada di dalam -> cetak
        "Plat tidak ditemukan"; jam keluar lebih awal dari jam masuk -> cetak
        "Jam keluar sebelum jam masuk" (kendaraan tetap di dalam). Kalau lolos,
        hitung biaya dengan self.tarif dan simpan ke self.selesai. Tidak mencetak apa pun."""
        if plat not in self.di_dalam:
            print("Plat tidak ditemukan")
            return

        menit_keluar = jam_ke_menit(jam)
        menit_masuk = self.di_dalam[plat]
        if menit_keluar < menit_masuk:
            print("Jam keluar sebelum jam masuk")
            return

        jam, biaya = self.tarif.hitung(menit_keluar - menit_masuk)
        self.selesai.append((plat, jam, biaya))
        del self.di_dalam[plat]

    def hasil(self):
        """Cetak satu baris per kendaraan di self.selesai:  B1234AD 1 jam tarif : 4000"""
        for plat, jam, biaya in self.selesai:
            print(f"{plat} {jam} jam tarif : {biaya}")
