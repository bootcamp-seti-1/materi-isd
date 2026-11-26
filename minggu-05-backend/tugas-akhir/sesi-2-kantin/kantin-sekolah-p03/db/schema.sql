DROP TABLE IF EXISTS kantin_orders;
DROP TABLE IF EXISTS kantin_menus;

CREATE TABLE kantin_menus (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  category ENUM('makanan', 'minuman') NOT NULL,
  price INT NOT NULL,
  stock INT NOT NULL DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE kantin_orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  menu_id INT NOT NULL,
  qty INT NOT NULL,
  total INT NOT NULL,
  status ENUM('baru', 'batal') NOT NULL DEFAULT 'baru',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (menu_id) REFERENCES kantin_menus(id)
);
