DROP TABLE IF EXISTS soal8_produk;

CREATE TABLE soal8_produk (
  id INT AUTO_INCREMENT PRIMARY KEY,
  toko CHAR(1) NOT NULL,
  nama VARCHAR(50) NOT NULL,
  harga INT NOT NULL
);

INSERT INTO soal8_produk (toko, nama, harga) VALUES
  ('A', 'Buku Tulis', 5000),
  ('A', 'Pulpen Hitam', 3000),
  ('A', 'Penghapus', 2000),
  ('A', 'Spidol Papan', 9000),
  ('B', 'Kaos Polos', 45000),
  ('B', 'Topi Rimba', 30000),
  ('B', 'Kaus Kaki', 15000),
  ('C', 'Kopi Bubuk', 25000),
  ('C', 'Gula Aren', 20000);
