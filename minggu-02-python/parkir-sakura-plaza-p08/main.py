from parkir import Parkir

parkir = Parkir()

while True:
    try:
        baris = input()
    except EOFError:
        break
    kata = baris.split()
    if kata == ["hasil"]:
        parkir.hasil()
    elif len(kata) == 3 and kata[1] == "masuk":
        parkir.masuk(kata[0], kata[2])
    elif len(kata) == 3 and kata[1] == "keluar":
        parkir.keluar(kata[0], kata[2])
