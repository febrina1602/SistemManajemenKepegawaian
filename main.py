import csv
from queue import PriorityQueue

class Karyawan:
    def __init__(self, id, nama, posisi, gaji, Tugas=None):
        self.id = id
        self.nama = nama
        self.posisi = posisi
        self.gaji = gaji
        self.Tugas = Tugas if Tugas is not None else PriorityQueue()

    def __repr__(self):
        return f'Karyawan({self.id}, {self.nama}, {self.posisi}, {self.gaji}, Tugas1: {self.get_tugas_list()})'

    def get_tugas_list(self):
        return list(self.Tugas.queue)

    def __lt__(self, other):
        if self.Tugas.empty():
            return False
        if other.Tugas.empty():
            return True
        return self.Tugas.queue[0][0] < other.Tugas.queue[0][0]

class SistemManajemenKepegawaian:
    def __init__(self):
        self.karyawan = []
        self.priority_q = PriorityQueue()
        self.file = ""

    def add_karyawan(self, id, nama, posisi, gaji, Tugas=None):
        pegawai = Karyawan(id, nama, posisi, gaji, Tugas)
        self.karyawan.append(pegawai)
        self.rebuild_priority_q()
            

    def remove_karyawan(self, id):
        find_pgw = False
        for pgw in self.karyawan:
            if pgw.id == id:
                self.karyawan.remove(pgw)
                self.rebuild_priority_q()
                print(f"Karyawan dengan ID {id} telah dihapus.")
                find_pgw = True
                break
        if not find_pgw:
            print(f"Karyawan dengan ID {id} tidak ditemukan.")



    def update_karyawan(self, id, nama=None, posisi=None, gaji=None):
        find_pgw = False
        for pgw in self.karyawan:
            if pgw.id == id:
                find_pgw = True
                if nama: pgw.nama = nama
                if posisi: pgw.posisi = posisi
                if gaji: pgw.gaji = gaji
                self.rebuild_priority_q()
                break
            
        if not find_pgw:
            print(f"Karyawan dengan ID {id} tidak ditemukan.")

    def add_tugas(self, id, tugas, prioritas):
        for pgw in self.karyawan:
            if pgw.id == id:
                pgw.Tugas.put((prioritas, tugas))
                self.rebuild_priority_q()
                print("Tugas berhasil ditambahkan.")
                return 
        print(f"Karyawan dengan ID {id} tidak ditemukan.")

    def remove_tugas(self, id, tugas):
        find_pgw = False 
        for pgw in self.karyawan:
            if pgw.id == id:
                find_pgw = True 
                temp_queue = PriorityQueue()
                while not pgw.Tugas.empty():
                    pri, tgs = pgw.Tugas.get()
                    if tgs != tugas:
                        temp_queue.put((pri, tgs))
                pgw.Tugas = temp_queue
                self.rebuild_priority_q()
                break
        
        if not find_pgw:
            print(f"Karyawan dengan ID {id} tidak ditemukan.")


    def display_karyawan(self):
        if not self.karyawan:
            print("Data karyawan tidak tersedia.")
        else:
            for pgw in self.karyawan:
                print(pgw)

    def import_csv(self, file):
        self.file = file
        try:
            with open(file, mode='r') as berkas:
                csv_reader = csv.DictReader(berkas)
                for row in csv_reader:
                    Tugas = PriorityQueue()
                    if row['Tugas']:
                        for tugas in row['Tugas'].split(';'):
                            pri, tgs = tugas.split(',')
                            Tugas.put((int(pri), tgs))
                    self.add_karyawan(row['id'], row['nama'], row['posisi'], int(row['gaji']), Tugas)
            print("File berhasil diimport.")
        except FileNotFoundError:
            print(f"File '{file}' tidak ditemukan.")
        except IOError as e:
            print(f"Terjadi kesalahan saat membaca file: {e}")
        except Exception as e:
            print(f"Terjadi kesalahan saat mengimpor file: {e}")


    def export_csv(self, file=None):
        file = file or self.file
        try:
            with open(file, mode='w', newline='') as berkas:
                fieldnames = ['id', 'nama', 'posisi', 'gaji', 'Tugas']
                csv_writer = csv.DictWriter(berkas, fieldnames=fieldnames)
                csv_writer.writeheader()
                for pgw in self.karyawan:
                    Tugas = ';'.join([f"{pri},{tgs}" for pri, tgs in pgw.get_tugas_list()])
                    csv_writer.writerow({'id': pgw.id, 'nama': pgw.nama, 'posisi': pgw.posisi, 'gaji': pgw.gaji, 'Tugas': Tugas})
            print(f"File '{file}' telah berhasil disimpan.")
        except IOError:
            print(f"Gagal menyimpan file '{file}'. Pastikan Anda memiliki izin yang tepat atau path yang benar.")

    def add_karyawan_ke_csv(self, file, id, nama, posisi, gaji):
        try:
            gaji = int(gaji)
            with open(file, mode='a', newline='') as berkas:
                csv_writer = csv.writer(berkas)
                csv_writer.writerow([id, nama, posisi, gaji, ""])
            self.add_karyawan(id, nama, posisi, gaji)
            print("Data berhasil ditambahkan.")
        except ValueError:
            print("Gaji harus dalam format angka.")
        except IOError as e:
            print(f"Error: {e}")


    def sort_karyawan(self, key):
        if key == 'id':
            self.karyawan.sort(key=lambda pgw: pgw.id)
        elif key == 'nama':
            self.karyawan.sort(key=lambda pgw: pgw.nama)
        elif key == 'posisi':
            self.karyawan.sort(key=lambda pgw: pgw.posisi)
        elif key == 'gaji':
            self.karyawan.sort(key=lambda pgw: pgw.gaji)

    def search_karyawan(self, id):
        for pgw in self.karyawan:
            if pgw.id == id:
                return pgw
        return None

    def display_priority_q(self):
        if self.priority_q.empty():
            print("Tidak ada tugas yang tersedia.")
        else:
            sorted_queue = sorted(self.priority_q.queue, key=lambda x: x[0])
            for pri, pgw in sorted_queue:
                print(f'prioritas: {pri}, Karyawan: {pgw}')

    def rebuild_priority_q(self):
        self.priority_q = PriorityQueue()
        for pgw in self.karyawan:
            if not pgw.Tugas.empty():
                highest_priority_task = pgw.Tugas.get()
                self.priority_q.put((highest_priority_task[0], pgw))
                pgw.Tugas.put(highest_priority_task)

def menu():
    ems = SistemManajemenKepegawaian()
    while True:
        print("\n----- Sistem Manajemen Kepegawaian -----")
        print("1. Import File CSV")
        print("2. Tambah Data")
        print("3. Edit Data")
        print("4. Hapus Data")
        print("5. Tampilkan Data")
        print("6. Sort Data")
        print("7. Search Data")
        print("8. Tambah Tugas")
        print("9. Hapus Tugas")
        print("10. Tampilkan Tugas")
        print("11. Simpan File CSV")
        print("12. Keluar")
        opsi = input("Masukkan Pilihan: ")

        if opsi == '1':
            print("Import File CSV")
            file = input("Nama File CSV: ")
            ems.import_csv(file)
            
        elif opsi == '2':
            print("Menambahkan Data")
            file = input("Nama File: ")
            id = input("Id Karyawan: ")
            nama = input("Nama Karyawan: ")
            posisi = input("Posisi Karyawan: ")
            gaji = int(input("Gaji: "))
            ems.add_karyawan_ke_csv(file, id, nama, posisi, gaji)

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
            print("Menghapus Data")
            id = input("Id Karyawan: ")
            ems.remove_karyawan(id)
            ems.export_csv()

        elif opsi == '5':
            print("Data Karyawan:")
            ems.display_karyawan()

        elif opsi == '6':
            key = input("Urutkan Berdasarkan (id, nama, posisi, gaji): ")
            ems.sort_karyawan(key)
            ems.display_karyawan()

        elif opsi == '7':
            id = input("Cari Berdasarkan Id: ")
            pgw = ems.search_karyawan(id)
            if pgw:
                print("Data Ditemukan:", pgw)
            else:
                print("Data Tidak Ditemukan.")

        elif opsi == '8':
            print("Menambahkan Tugas")
            id = input("Id Karyawan: ")
            tugas = input("Deskripsi Tugas: ")
            prioritas = int(input("Prioritas Tugas (Angka Terendah Menjadi Prioritas Tinggi): "))
            ems.add_tugas(id, tugas, prioritas)
            ems.export_csv()

        elif opsi == '9':
            print("Menghapus Tugas")
            id = input("Id Karyawan: ")
            tugas = input("Deskripsi Tugas: ")
            ems.remove_tugas(id, tugas)
            ems.export_csv()

        elif opsi == '10':
            print("Prioritas Tugas:")
            ems.display_priority_q()

        elif opsi == '11':
            print("Simpan File CSV")
            export_file = input("File CSV: ")
            ems.export_csv(export_file)
            
        elif opsi == '12':
            print("Keluar Dari Program...")
            break

        else:
            print("Silakan Masukkan Opsi Yang Valid.")

if __name__ == "__main__":
    menu()
