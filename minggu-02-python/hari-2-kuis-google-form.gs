/**
 * Kuis Hari 2 (Modul dan OOP), SETI-P Minggu 2.
 * Membuat Google Form kuis lengkap: 10 soal, kunci jawaban, poin, dan pembahasan.
 *
 * KHUSUS TRAINER. File ini berisi kunci jawaban. Jangan dibagikan ke peserta.
 *
 * Cara pakai:
 * 1. Buka https://script.google.com, klik "Proyek baru".
 * 2. Hapus isi file Code.gs, tempel seluruh isi file ini.
 * 3. Pilih fungsi "buatKuis" di menu atas, klik "Jalankan".
 * 4. Pertama kali: klik "Tinjau izin", pilih akunmu, lalu "Lanjutan" dan
 *    "Buka ... (tidak aman)" (peringatan ini normal untuk skrip buatan sendiri), lalu "Izinkan".
 * 5. Link formulir muncul di "Log eksekusi" (bagian bawah). Formulirnya juga ada di Google Drive-mu.
 *
 * Catatan:
 * - Peserta mengisi ID (contoh P08), bukan nama, dan email tidak dikumpulkan.
 * - Tiap soal 2 poin, jadi total 20 (sama dengan bobot kuis di W1).
 * - Jalankan buatKuis sekali saja. Setiap dijalankan, formulir baru dibuat.
 */

const JUDUL = "Kuis Hari 2 - Modul dan OOP (SETI-P Minggu 2)";
const POIN_PER_SOAL = 2;           // 10 soal x 2 poin = 20
const TAMPILKAN_PEMBAHASAN = true; // false = peserta tidak melihat penjelasan setelah menjawab

// "benar" = nomor opsi yang benar, dihitung dari 0 (0 = A, 1 = B, 2 = C, 3 = D)
const SOAL = [
  {
    judul: "Kamu punya file tugas.py berisi fungsi tambah. Supaya main.py bisa memanggil tugas.tambah(\"sarapan\"), baris yang dipakai di main.py adalah …",
    opsi: ["include tugas", "import tugas", "open(\"tugas.py\")", "def tugas():"],
    benar: 1,
    pembahasan: "import tugas memuat modul dari file tugas.py, lalu isinya dipanggil dengan titik: tugas.tambah(...)."
  },
  {
    judul: "Hubungan class dan objek yang benar adalah …",
    opsi: [
      "Class dan objek adalah dua nama untuk hal yang sama",
      "Objek adalah cetakan, class adalah hasil cetakannya",
      "Class adalah cetakan, objek adalah hasil cetakannya",
      "Class hanya untuk angka, objek hanya untuk teks"
    ],
    benar: 2,
    pembahasan: "Class adalah cetakan. Objek adalah hasil cetakannya, dan satu class bisa menghasilkan banyak objek."
  },
  {
    judul: "Pada def tandai_selesai(self):, kata self berarti …",
    opsi: [
      "Objek yang sedang memanggil method itu",
      "Nama file tempat class berada",
      "Kata kunci untuk keluar dari method",
      "Judul tugas"
    ],
    benar: 0,
    pembahasan: "self menunjuk objek yang sedang memanggil method. Pada t.tandai_selesai(), self adalah t."
  },
  {
    judul: "Method __init__ dijalankan ketika …",
    opsi: [
      "Program ditutup",
      "Method lain selesai dijalankan",
      "print dipanggil",
      "Objek baru dibuat, misalnya Tugas(\"mandi\")"
    ],
    benar: 3,
    pembahasan: "__init__ dijalankan otomatis saat objek dibuat, untuk mengisi data awalnya."
  },
  {
    judul: "Apa yang tampil dari kode ini? (class Tugas seperti di Bagian C)",
    kode: "a = Tugas(\"mandi\")\nb = Tugas(\"makan\")\na.tandai_selesai()\nprint(a)\nprint(b)",
    opsi: [
      "[x] mandi lalu [x] makan",
      "[x] mandi lalu [ ] makan",
      "[ ] mandi lalu [ ] makan",
      "Error"
    ],
    benar: 1,
    pembahasan: "Hanya a yang ditandai selesai. Setiap objek punya data sendiri, jadi b tidak ikut berubah."
  },
  {
    judul: "Setelah menulis from tugas import PengelolaTugas di main.py, cara membuat objek pengelola adalah …",
    opsi: [
      "tugas.PengelolaTugas()",
      "new PengelolaTugas()",
      "import PengelolaTugas()",
      "PengelolaTugas()"
    ],
    benar: 3,
    pembahasan: "Dengan from tugas import PengelolaTugas, class dipanggil langsung tanpa awalan tugas. Objek dibuat dengan PengelolaTugas(), tanpa kata new."
  },
  {
    judul: "Pernyataan yang menggambarkan pemrograman prosedural adalah …",
    opsi: [
      "Program disusun sebagai urutan langkah (fungsi) yang memproses data yang terpisah dari fungsi itu",
      "Data dan fungsi selalu dibungkus bersama di dalam class",
      "Fungsi tidak boleh dipakai sama sekali",
      "Hanya bisa dipakai di bahasa Java"
    ],
    benar: 0,
    pembahasan: "Prosedural menyusun program sebagai urutan fungsi yang memproses data terpisah, seperti sakura-tasks di Hari 1."
  },
  {
    judul: "Situasi yang paling cocok memakai OOP adalah …",
    opsi: [
      "Skrip 15 baris yang dijalankan sekali lalu dibuang",
      "Menghitung 2 + 2",
      "Mencetak satu kalimat ke layar",
      "Aplikasi dengan banyak entitas yang masing-masing punya data dan perilakunya sendiri, seperti tugas, pengguna, dan pesanan"
    ],
    benar: 3,
    pembahasan: "OOP paling terasa manfaatnya saat ada banyak entitas yang masing-masing punya data dan perilaku sendiri. Untuk skrip kecil, prosedural sudah cukup."
  },
  {
    judul: "Pernyataan yang benar tentang OOP dan bahasa pemrograman adalah …",
    opsi: [
      "OOP adalah cara menyusun program yang bisa dipakai di banyak bahasa, misalnya Python, Java, JavaScript, dan C#",
      "OOP hanya bisa dipakai di Java",
      "Python tidak mendukung OOP",
      "OOP wajib memakai kata self di semua bahasa"
    ],
    benar: 0,
    pembahasan: "OOP adalah cara menyusun program, bukan milik satu bahasa. Ejaannya berbeda (Python memakai self, Java dan JavaScript memakai this), tetapi konsepnya sama."
  },
  {
    judul: "Keuntungan memakai class PengelolaTugas dibanding satu variabel global daftar adalah …",
    opsi: [
      "Program otomatis berjalan lebih cepat",
      "Data tugas otomatis tersimpan ke file",
      "Bisa punya beberapa pengelola yang masing-masing punya daftar sendiri",
      "Tidak perlu lagi memakai self"
    ],
    benar: 2,
    pembahasan: "Setiap objek PengelolaTugas punya self.daftar sendiri, jadi bisa ada beberapa pengelola yang terpisah. Penyimpanan ke file tidak dibahas hari ini."
  }
];

function buatKuis() {
  const form = FormApp.create(JUDUL);
  form.setIsQuiz(true);
  form.setDescription(
    "Kerjakan sendiri tanpa membuka lembar hands-on. Pilih satu jawaban untuk tiap soal. " +
    "Tulis ID pesertamu (contoh: P08), bukan nama."
  );
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.setShowLinkToRespondAgain(false);
  form.setProgressBar(true);
  form.setConfirmationMessage("Terima kasih, jawabanmu sudah terkirim.");

  form.addTextItem()
    .setTitle("ID Peserta (contoh: P08)")
    .setHelpText("Tulis ID saja, bukan nama.")
    .setRequired(true);

  SOAL.forEach(function (s, i) {
    const item = form.addMultipleChoiceItem();
    item.setTitle("Soal " + (i + 1) + ". " + s.judul);
    if (s.kode) {
      item.setHelpText(s.kode);
    }
    item.setChoices(s.opsi.map(function (teks, j) {
      return item.createChoice(teks, j === s.benar);
    }));
    item.setPoints(POIN_PER_SOAL);
    item.setRequired(true);
    if (TAMPILKAN_PEMBAHASAN) {
      item.setFeedbackForCorrect(
        FormApp.createFeedback().setText("Benar. " + s.pembahasan).build()
      );
      item.setFeedbackForIncorrect(
        FormApp.createFeedback().setText("Belum tepat. " + s.pembahasan).build()
      );
    }
  });

  Logger.log("Formulir dibuat: " + SOAL.length + " soal, total " + (SOAL.length * POIN_PER_SOAL) + " poin.");
  Logger.log("Link untuk peserta : " + form.getPublishedUrl());
  Logger.log("Link untuk mengedit: " + form.getEditUrl());
}
