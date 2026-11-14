# Semua angka harga ada di file ini. Jangan menaruh angka tarif di file lain.
JAM_PERTAMA = 4000
JAM_BERIKUTNYA = 2000
GRATIS_MENIT = 15
MAKSIMUM = 20000


class Tarif:
    def hitung(self, durasi):
        """durasi dalam menit (0 atau lebih).

        Kembalikan dua nilai: jumlah jam yang ditagih dan biayanya.
        - Durasi GRATIS_MENIT atau kurang: gratis, yaitu 0 jam dan biaya 0.
        - Selebihnya dibulatkan ke atas per jam, dan biaya tidak boleh melebihi MAKSIMUM.
        """
        # TODO: tulis perhitungannya di sini

        # Cek apakah durasi gratis (15 menit atau kurang)
        if durasi <= GRATIS_MENIT:
            return 0, 0

        # Bulatkan ke atas per jam (60 menit)
        # Contoh: 1 menit -> 1 jam, 61 menit -> 2 jam
        import math
        jam = math.ceil(durasi / 60)

        # Hitung biaya: jam pertama 4000, jam berikutnya 2000
        biaya = JAM_PERTAMA + (jam - 1) * JAM_BERIKUTNYA

        # Pastikan biaya tidak melebihi batas maksimum
        if biaya > MAKSIMUM:
            biaya = MAKSIMUM
        return jam, biaya
