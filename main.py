import csv

class Karyawan:
    def __init__(self, id, nama, posisi, gaji):
        self.id = id
        self.nama = nama
        self.posisi = posisi
        self.gaji = gaji

    def __repr__(self):
        return f'Karyawan({self.id}, {self.nama}, {self.posisi}, {self.gaji})'

class SistemManajemenKepegawaian:
    def __init__(self):
        self.karyawan = []
        self.file = ""

    def add_karyawan(self, id, nama, posisi, gaji):
        pegawai = Karyawan(id, nama, posisi, gaji)
        self.karyawan.append(pegawai)

    def remove_karyawan(self, id):
        self.karyawan = [pgw for pgw in self.karyawan if pgw.id != id]

    def update_karyawan(self, id, nama=None, posisi=None, gaji=None):
        for pgw in self.karyawan:
            if pgw.id == id:
                if nama: pgw.nama = nama
                if posisi: pgw.posisi = posisi
                if gaji: pgw.gaji = gaji
                break

    def display_karyawan(self):
        for pgw in self.karyawan:
            print(pgw)

    def import_csv(self, file):
        self.file = file
        with open(file, mode='r') as berkas:
            csv_reader = csv.DictReader(berkas)
            for row in csv_reader:
                self.add_karyawan(row['id'], row['nama'], row['posisi'], int(row['gaji']))

    def export_csv(self, file=None):
        file = file or self.file
        with open(file, mode='w', newline='') as berkas:
            fieldnames = ['id', 'nama', 'posisi', 'gaji']
            csv_writer = csv.DictWriter(berkas, fieldnames=fieldnames)
            csv_writer.writeheader()
            for pgw in self.karyawan:
                csv_writer.writerow({'id': pgw.id, 'nama': pgw.nama, 'posisi': pgw.posisi, 'gaji': pgw.gaji})

    def add_karyawan_ke_csv(self, file, id, nama, posisi, gaji):
        with open(file, mode='a', newline='') as berkas:
            csv_writer = csv.writer(berkas)
            csv_writer.writerow([id, nama, posisi, gaji, ""])
        self.add_karyawan(id, nama, posisi, gaji)


def menu():
    ems = SistemManajemenKepegawaian()
    while True:
        print("\n----- Sistem Manajemen Kepegawaian -----")
        print("1. Tambah Data")
        print("2. Hapus Data")
        print("3. Edit Data")
        print("4. Tampilkan Data")
        print("5. Import File CSV")
        print("6. Keluar")
        opsi = input("Masukkan Pilihan: ")

        if opsi == '1':
            print("Menambahkan Data")
            file = input("Nama File: ")
            id = input("Id Karyawan: ")
            nama = input("Nama Karyawan: ")
            posisi = input("Posisi Karyawan: ")
            gaji = int(input("Gaji: "))
            ems.add_karyawan_ke_csv(file, id, nama, posisi, gaji)

        elif opsi == '2':
            print("Menghapus Data")
            id = input("Id Karyawan: ")
            ems.remove_karyawan(id)
            ems.export_csv()

        elif opsi == '3':
            print("Mengubah Data")
            id = input("Id Karyawan: ")
            nama = input("Nama Karyawan: ")
            posisi = input("Posisi Karyawan: ")
            gaji = input("Gaji: ")
            gaji = int(gaji) if gaji else None
            ems.update_karyawan(id, nama, posisi, gaji)
            ems.export_csv()

        elif opsi == '4':
            print("Data Karyawan:")
            ems.display_karyawan()

        elif opsi == '5':
            print("Import File CSV")
            file = input("Nama File CSV: ")
            ems.import_csv(file)
            
        elif opsi == '6':
            print("Keluar Dari Program...")
            break

        else:
            print("Silakan Masukkan Opsi Yang Valid.")

if __name__ == "__main__":
    menu()
