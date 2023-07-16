# API Jadwal Shalat

API sederhana untuk mendapatkan jadwal perkiraan waktu shalat, menggunakan:
  - Library [PrayTimes](https://praytimes.org) untuk kalkulasi jadwal
  - [Flask](https://flask.palletsprojects.com) (Python) sebagai _web framework_

## Project Status

Proyek ini tidak lagi aktif dikembangkan. Saya punya rencana untuk berpindah ke framework [FastAPI]([url](https://fastapi.tiangolo.com/)), tapi tidak untuk sekarang. Beri tahu saya jika Anda ingin berkontribusi, jadi kita bisa _collab_!

## Endpoint

### 1. `[GET] /`

Deskripsi: Hanya placeholder untuk halaman _home_.

Parameter: _None_

### 2. `[GET] /shalat`

Deskripsi: Jadwal shalat (_default_ untuk hari ini).

Parameter:

  - `tanggal`: Tanggal **(%d-%m-%Y)** (default: Hari ini)
  - `latitude`: _Latitude_ lokasi (default: Tulungagung, Jawa Timur)
  - `longtitude`: _Longtitude_ lokasi (default: Tulungagung, Jawa Timur)
  - `metode`: Metode kalkulasi jadwal (default: **Kemenag**)

Contoh:
`/shalat?tanggal=26-02-2023&latitude=-8.0667&longtitude=111.9`

### 3. `[GET] /range_shalat`

Deskripsi: Range jadwal shalat.

Parameter:
  - `start`: Tanggal mulainya jadwal **(%d-%m-%Y)**
  - `end`: Tanggal berakhirnya jadwal **(%d-%m-%Y)**
  - `latitude`: _Latitude_ lokasi (default: Tulungagung, Jawa Timur)
  - `longtitude`: _Longtitude_ lokasi (default: Tulungagung, Jawa Timur)
  - `metode`: Metode kalkulasi jadwal (default: **Kemenag**)

Contoh:
`/range_shalat?start=24-02-2023&end=26-02-2023&latitude=-8.0667&longtitude=111.9`
