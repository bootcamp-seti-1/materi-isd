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
        if plat not in self.di_dalam:
            self.di_dalam[plat] = jam
            return
        print("Plat sudah ada di dalam")
        

    def keluar(self, plat, jam):
        """Kendaraan keluar. Cek berurutan: plat tidak ada di dalam -> cetak
        "Plat tidak ditemukan"; jam keluar lebih awal dari jam masuk -> cetak
        "Jam keluar sebelum jam masuk" (kendaraan tetap di dalam). Kalau lolos,
        hitung biaya dengan self.tarif dan simpan ke self.selesai. Tidak mencetak apa pun."""
        if plat not in self.di_dalam:
            print("Plat tidak ditemukan")
            return
        elif jam_ke_menit(jam) < jam_ke_menit(self.di_dalam[plat]):
            print("Jam keluar sebelum jam masuk")
            return
        sedang_keluar = self.di_dalam.pop(plat, None)  # <- Last minute edit (Deleting plat from di_dalam actually never checked by cek.py) ...bruh
        self.selesai.append((plat, *self.tarif.hitung(jam_ke_menit(jam) - jam_ke_menit(sedang_keluar))))    # Unpack tarif.hitung() result which is a tuple into 2 separate value.

        
        

    def hasil(self):
        """Cetak satu baris per kendaraan di self.selesai:  B1234AD 1 jam tarif : 4000"""
        print(*(f"{plat} {durasi} jam tarif : {biaya}" for plat, durasi, biaya in self.selesai), sep="\n")
        
        # "*" : Unpacking Operator print(*"Hello") -> H e l l o
        # fstring : f" {variable} string biasa" <- Insert variable into the string
        # (x for x in items) : generator expression. Creates items one by one on demand. In this case we unpack it.
