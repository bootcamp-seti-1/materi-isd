# Let's simulate the execution of main.py with masukan.txt after implementing `update`.

def run_simulation():
    tugas = []

    def tambah(judul):
        judul = judul.strip()
        if judul == "":
            print("Judul tidak boleh kosong")
            return
        tugas.append({"judul": judul, "selesai": False})
        print(f"Ditambahkan: {judul}")

    def tampilkan():
        for nomor, item in enumerate(tugas, start=1):
            tanda = "x" if item["selesai"] else " "
            print(f"{nomor}. [{tanda}] {item['judul']}")

    def selesai(nomor):
        if nomor < 1 or nomor > len(tugas):
            print("Nomor tidak ada")
            return
        tugas[nomor - 1]["selesai"] = True
        print(f"Selesai: {tugas[nomor - 1]['judul']}")

    def update_tugas(perintah_str):
        parts = perintah_str.split(" ", 2)
        if len(parts) < 2:
            print("Judul tidak boleh kosong") 
            return
        nomor_str = parts[1]
        if not nomor_str.isdigit():
            print("Nomor harus angka")
            return
        nomor = int(nomor_str)
        if nomor < 1 or nomor > len(tugas):
            print("Nomor tidak ada")
            return
        
        judul_baru = parts[2] if len(parts) > 2 else ""
        judul_baru = judul_baru.strip()
        if judul_baru == "":
            print("Judul tidak boleh kosong")
            return
        
        judul_lama = tugas[nomor - 1]["judul"]
        tugas[nomor - 1]["judul"] = judul_baru
        print(f"Diubah: {judul_lama} -> {judul_baru}")

    masukan = [
        "add rapat tim",
        "add kirim laporan",
        "add review kode",
        "add makan siang",
        "done 2",
        "update 1 rapat vendor",
        "update 2 laporan bulanan",
        "update 9 apa saja",
        "update abc apa saja",
        "update 3",
        "update 4    ",
        "list",
        "keluar"
    ]

    for perintah in masukan:
        if perintah == "keluar":
            break
        elif perintah == "list":
            tampilkan()
        elif perintah.startswith("add "):
            tambah(perintah[4:])
        elif perintah.startswith("done "):
            nomor = perintah[5:]
            if nomor.isdigit():
                selesai(int(nomor))
            else:
                print("Nomor harus angka")
        elif perintah.startswith("update "):
            update_tugas(perintah)
        else:
            pass

run_simulation()