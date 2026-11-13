# Semua angka harga ada di file ini. Jangan menaruh angka tarif di file lain.
JAM_PERTAMA = 4000
JAM_BERIKUTNYA = 2000
GRATIS_MENIT = 15
MAKSIMUM = 20000


class Tarif:
    def hitung(self, durasi:int) -> tuple[int, int]:
        """durasi dalam menit (0 atau lebih).

        Kembalikan dua nilai: jumlah jam yang ditagih dan biayanya.
        - Durasi GRATIS_MENIT atau kurang: gratis, yaitu 0 jam dan biaya 0.
        - Selebihnya dibulatkan ke atas per jam, dan biaya tidak boleh melebihi MAKSIMUM.
        """
        if durasi <= GRATIS_MENIT:
            return 0, 0

        jam_lebih = 0 if durasi <= 60 else -(-(durasi - 60) // 60) # -(-x // y) Upside down floor division, x input y threshold
        total_jam = 1 + jam_lebih
        
        return total_jam, min(MAKSIMUM, JAM_PERTAMA + jam_lebih * JAM_BERIKUTNYA)
