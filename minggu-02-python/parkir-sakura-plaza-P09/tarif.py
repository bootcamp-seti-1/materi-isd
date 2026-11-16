# Semua angka harga ada di file ini. Jangan menaruh angka tarif di file lain.
JAM_PERTAMA = 4000
JAM_BERIKUTNYA = 2000
GRATIS_MENIT = 15
MAKSIMUM = 20000

import math

class Tarif:
    def hitung(self, durasi):
        """durasi dalam menit (0 atau lebih).

        Kembalikan dua nilai: jumlah jam yang ditagih dan biayanya.
        - Durasi GRATIS_MENIT atau kurang: gratis, yaitu 0 jam dan biaya 0.
        - Selebihnya dibulatkan ke atas per jam, dan biaya tidak boleh melebihi MAKSIMUM.
        """
        # TODO: tulis perhitungannya di sini
        if durasi <= GRATIS_MENIT:
            return 0, 0
        jam = math.ceil(durasi / 60)
        if jam == 1:
            biaya = JAM_PERTAMA
        else:
            biaya = JAM_PERTAMA + (jam - 1) * JAM_BERIKUTNYA

        if biaya > MAKSIMUM:
            biaya = MAKSIMUM

        return jam, biaya 