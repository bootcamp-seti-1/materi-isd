from absensi import Absensi

kelas_a = Absensi()
kelas_b = Absensi()

kelas_a.hadir("Rina")
kelas_a.hadir("Dimas")
kelas_a.izin("Sari", "sakit")
kelas_a.hadir("Rina")

kelas_b.hadir("Rina")
kelas_b.izin("Budi", "acara keluarga")
kelas_b.izin("Tono", "urusan bank")

kelas_a.rekap()
kelas_b.rekap()
