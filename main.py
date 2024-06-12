class Karyawan:
    def __init__(self, id, nama, posisi, gaji):
        self.id = id
        self.nama = nama
        self.posisi = posisi
        self.gaji = gaji


class SistemManajemenKepegawaian:
    def __init__(self):
        self.karyawan = []

    def add_karyawan(self, id, nama, posisi, gaji):
        karyawan = Karyawan(id, nama, posisi, gaji)
        self.karyawan.append(karyawan)

    def remove_karyawan(self, id):
        self.karyawan = [emp for emp in self.karyawan if emp.id != id]

    
    def display_karyawan(self):
        if not self.karyawan:
            print("Tidak ada data karyawan.")
        else:
            for emp in self.karyawan:
                print(emp)

def menu():
    ems = SistemManajemenKepegawaian()
    while True:
        print("\n----- Sistem Manajemen Kepegawaian -----")
        print("1. Tambah Data Karyawan")
        print("2. Hapus Data Karyawan")
        print("3. Tampilkan Data Karyawan")
        print("4. Exit")
        opsi = input("Masukkan pilihan: ")

        if opsi == '1':
            id = input("Masukkan ID Karyawan: ")
            nama = input("Masukkan Nama Karyawan: ")
            posisi = input("Masukkan Posisi Karyawan: ")
            gaji = int(input("Masukkan Gaji Karyawan: "))
            ems.add_karyawan(id, nama, posisi, gaji)

        elif opsi == '2':
            id = input("Masukkan ID Karyawan yang Ingin Dihapus: ")
            ems.remove_karyawan(id)

        elif opsi == '3':
            print("Data Karyawan EMS")
            ems.display_karyawan()
            
        elif opsi == '4':
            print("Keluar dari program...")
            break

        else:
            print("Silakan Masukkan Pilihan yang Valid.")

if __name__ == "__main__":
    menu()
