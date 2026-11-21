"""
Game Battle OOP - versi grafis (Tkinter Canvas, tanpa install library tambahan)
Konsep OOP:
  - Class & Constructor (__init__)
  - Encapsulation (_hp + property)
  - Inheritance (Pahlawan -> Penyihir, Monster -> Naga)
  - Polymorphism (serang() dan gambar() berbeda di tiap class)
"""
import random
import tkinter as tk
from tkinter import messagebox


# ===================== CLASS KARAKTER =====================
class Karakter:
    def __init__(self, nama, hp, kekuatan):
        self.nama = nama
        self._hp = hp                 # atribut private (encapsulation)
        self.hp_maks = hp
        self.kekuatan = kekuatan
        self.tag = f"k{id(self)}"     # penanda gambar di canvas
        self.x = 0

    @property
    def hp(self):
        return self._hp

    def masih_hidup(self):
        return self._hp > 0

    def terima_damage(self, d):
        self._hp = max(0, self._hp - d)

    def pulihkan(self, n):
        self._hp = min(self.hp_maks, self._hp + n)

    def serang(self, target):
        """Mengembalikan (teks, damage, spesial)."""
        d = random.randint(self.kekuatan - 3, self.kekuatan + 3)
        target.terima_damage(d)
        return f"{self.nama} menyerang {target.nama}!", d, False

    def gambar(self, c, x, y):
        """Menggambar karakter di canvas (x, y = posisi kaki)."""
        self.x = x
        c.create_rectangle(x - 15, y - 60, x + 15, y, fill="gray", tags=self.tag)


# ===================== PAHLAWAN & PENYIHIR =====================
class Pahlawan(Karakter):
    def __init__(self, nama, hp=100, kekuatan=15):
        super().__init__(nama, hp, kekuatan)
        self.potion = 2

    def serang(self, target):  # polymorphism
        d = random.randint(self.kekuatan - 3, self.kekuatan + 3)
        krit = random.random() < 0.25
        if krit:
            d *= 2
        target.terima_damage(d)
        teks = f"KRITIKAL! {self.nama} menebas {target.nama}!" if krit else f"{self.nama} menebas {target.nama}!"
        return teks, d, krit

    def pakai_potion(self):
        if self.potion <= 0:
            return None
        self.potion -= 1
        self.pulihkan(30)
        return f"{self.nama} minum potion (+30 HP)."

    def gambar(self, c, x, y):  # polymorphism
        self.x, t = x, self.tag
        c.create_rectangle(x - 14, y - 30, x - 3, y, fill="#455a64", tags=t)
        c.create_rectangle(x + 3, y - 30, x + 14, y, fill="#455a64", tags=t)
        c.create_rectangle(x - 16, y - 62, x + 16, y - 28, fill="#1e88e5", tags=t)
        c.create_oval(x - 14, y - 92, x + 14, y - 62, fill="#ffcc99", tags=t)
        c.create_arc(x - 15, y - 96, x + 15, y - 66, start=0, extent=180, fill="#b0bec5", tags=t)
        c.create_oval(x + 3, y - 82, x + 8, y - 77, fill="black", tags=t)
        c.create_line(x + 12, y - 50, x + 48, y - 85, width=5, fill="#cfd8dc", tags=t)
        c.create_line(x + 8, y - 52, x + 22, y - 38, width=5, fill="#795548", tags=t)


class Penyihir(Pahlawan):
    def __init__(self, nama):
        super().__init__(nama, hp=80, kekuatan=20)

    def serang(self, target):  # polymorphism
        d = random.randint(self.kekuatan - 2, self.kekuatan + 6)
        target.terima_damage(d)
        return f"{self.nama} melempar BOLA API ke {target.nama}!", d, False

    def gambar(self, c, x, y):  # polymorphism
        self.x, t = x, self.tag
        c.create_polygon(x - 22, y, x + 22, y, x + 12, y - 62, x - 12, y - 62, fill="#6a1b9a", tags=t)
        c.create_oval(x - 14, y - 94, x + 14, y - 64, fill="#ffcc99", tags=t)
        c.create_polygon(x - 24, y - 90, x + 24, y - 90, x, y - 140, fill="#4a148c", tags=t)
        c.create_oval(x + 3, y - 82, x + 8, y - 77, fill="black", tags=t)
        c.create_line(x + 26, y - 5, x + 26, y - 105, width=4, fill="#8d6e63", tags=t)
        c.create_oval(x + 19, y - 120, x + 33, y - 106, fill="#ff9800", outline="#ffeb3b", width=2, tags=t)


# ===================== MONSTER =====================
class Monster(Karakter):
    def __init__(self, nama, hp, kekuatan, warna="#7cb342", skala=1.0):
        super().__init__(nama, hp, kekuatan)
        self.warna = warna
        self.skala = skala

    def gambar(self, c, x, y):  # polymorphism
        self.x, t, s = x, self.tag, self.skala
        c.create_rectangle(x - 14 * s, y - 28 * s, x - 3 * s, y, fill="#33691e", tags=t)
        c.create_rectangle(x + 3 * s, y - 28 * s, x + 14 * s, y, fill="#33691e", tags=t)
        c.create_rectangle(x - 18 * s, y - 70 * s, x + 18 * s, y - 25 * s, fill=self.warna, tags=t)
        c.create_oval(x - 17 * s, y - 106 * s, x + 17 * s, y - 68 * s, fill=self.warna, tags=t)
        c.create_polygon(x - 15 * s, y - 95 * s, x - 36 * s, y - 102 * s, x - 15 * s, y - 80 * s, fill=self.warna, tags=t)
        c.create_polygon(x + 15 * s, y - 95 * s, x + 36 * s, y - 102 * s, x + 15 * s, y - 80 * s, fill=self.warna, tags=t)
        c.create_oval(x - 11 * s, y - 92 * s, x - 5 * s, y - 85 * s, fill="red", tags=t)
        c.create_oval(x + 3 * s, y - 92 * s, x + 9 * s, y - 85 * s, fill="red", tags=t)
        c.create_line(x - 12 * s, y - 76 * s, x + 8 * s, y - 76 * s, width=2, fill="black", tags=t)


class Naga(Monster):
    def __init__(self):
        super().__init__("Naga Api", 120, 14, warna="#c62828")

    def serang(self, target):  # polymorphism
        if random.random() < 0.3:
            d = self.kekuatan * 2
            target.terima_damage(d)
            return f"{self.nama} menyemburkan API PANAS!", d, True
        return super().serang(target)

    def gambar(self, c, x, y):  # polymorphism
        self.x, t = x, self.tag
        c.create_polygon(x - 5, y - 70, x + 25, y - 140, x + 55, y - 60, fill="#ef6c00", tags=t)  # sayap
        c.create_polygon(x + 30, y - 25, x + 85, y - 5, x + 35, y - 45, fill="#b71c1c", tags=t)  # ekor
        c.create_oval(x - 45, y - 80, x + 38, y - 10, fill=self.warna, tags=t)  # badan
        c.create_rectangle(x - 35, y - 25, x - 20, y, fill="#8e0000", tags=t)
        c.create_rectangle(x + 8, y - 25, x + 23, y, fill="#8e0000", tags=t)
        c.create_oval(x - 78, y - 118, x - 28, y - 70, fill=self.warna, tags=t)  # kepala
        c.create_polygon(x - 70, y - 115, x - 62, y - 135, x - 55, y - 115, fill="#ffeb3b", tags=t)
        c.create_polygon(x - 50, y - 115, x - 42, y - 135, x - 35, y - 115, fill="#ffeb3b", tags=t)
        c.create_oval(x - 66, y - 102, x - 58, y - 94, fill="#ffeb3b", tags=t)
        c.create_oval(x - 52, y - 102, x - 44, y - 94, fill="#ffeb3b", tags=t)


# ===================== CLASS GAME (GUI) =====================
class GameApp:
    LEBAR, TINGGI = 560, 300
    KAKI_Y = 240

    def __init__(self, root):
        self.root = root
        root.title("Game Battle OOP")
        root.resizable(False, False)
        self.frame = None
        self.tampil_menu()

    def bersihkan(self):
        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self.root, padx=12, pady=12)
        self.frame.pack()

    # ---------- Menu ----------
    def tampil_menu(self):
        self.bersihkan()
        tk.Label(self.frame, text="GAME BATTLE OOP", font=("Arial", 22, "bold")).pack(pady=12)
        tk.Label(self.frame, text="Nama karakter:").pack()
        self.entry = tk.Entry(self.frame, font=("Arial", 12), justify="center")
        self.entry.insert(0, "Hero")
        self.entry.pack(pady=6)
        tk.Label(self.frame, text="Pilih kelas:").pack(pady=(14, 4))
        tk.Button(self.frame, text="Pahlawan (HP 100, bisa kritikal)", width=34, bg="#1e88e5", fg="white",
                  font=("Arial", 11, "bold"), command=lambda: self.mulai("pahlawan")).pack(pady=4)
        tk.Button(self.frame, text="Penyihir (HP 80, sihir kuat)", width=34, bg="#6a1b9a", fg="white",
                  font=("Arial", 11, "bold"), command=lambda: self.mulai("penyihir")).pack(pady=4)

    def mulai(self, kelas):
        nama = self.entry.get().strip() or "Hero"
        self.pemain = Penyihir(nama) if kelas == "penyihir" else Pahlawan(nama)
        self.daftar = [Monster("Goblin", 50, 8), Monster("Orc", 80, 12, "#5d7a3a", 1.3), Naga()]
        self.indeks = 0
        self.musuh = self.daftar[0]
        self.sibuk = False
        self.tampil_battle()

    # ---------- Layar battle ----------
    def tampil_battle(self):
        self.bersihkan()
        self.stage = tk.Label(self.frame, font=("Arial", 10))
        self.stage.pack()
        self.c = tk.Canvas(self.frame, width=self.LEBAR, height=self.TINGGI, highlightthickness=1)
        self.c.pack()
        self.gambar_latar()
        self.pemain.gambar(self.c, 120, self.KAKI_Y)
        self.buat_bar(self.pemain)
        self.muncul_musuh()

        self.lbl_log = tk.Label(self.frame, font=("Arial", 11), height=2, wraplength=540)
        self.lbl_log.pack(pady=6)
        tombol = tk.Frame(self.frame)
        tombol.pack()
        self.btn_serang = tk.Button(tombol, text="SERANG", width=14, bg="#e53935", fg="white",
                                    font=("Arial", 11, "bold"), command=self.aksi_serang)
        self.btn_serang.grid(row=0, column=0, padx=8)
        self.btn_potion = tk.Button(tombol, text="POTION", width=14, bg="#2e9d4f", fg="white",
                                    font=("Arial", 11, "bold"), command=self.aksi_potion)
        self.btn_potion.grid(row=0, column=1, padx=8)
        self.log(f"Musuh muncul: {self.musuh.nama}!")
        self.render()

    def gambar_latar(self):
        c = self.c
        c.create_rectangle(0, 0, self.LEBAR, 235, fill="#87ceeb", width=0)
        c.create_rectangle(0, 235, self.LEBAR, self.TINGGI, fill="#5fae5a", width=0)
        c.create_oval(500, 15, 540, 55, fill="#ffeb3b", width=0)
        for cx, cy in ((90, 40), (300, 25)):
            for dx in (0, 25, 50):
                c.create_oval(cx + dx, cy, cx + dx + 40, cy + 25, fill="white", width=0)

    def muncul_musuh(self):
        self.musuh.gambar(self.c, 440, self.KAKI_Y)
        self.buat_bar(self.musuh)

    def buat_bar(self, k):
        c, x, ui = self.c, k.x, "ui" + k.tag
        c.create_rectangle(x - 45, 98, x + 45, 108, fill="#222", tags=ui)
        k.bar = c.create_rectangle(x - 45, 98, x + 45, 108, fill="#43a047", width=0, tags=ui)
        k.label = c.create_text(x, 86, font=("Arial", 10, "bold"), fill="white", tags=ui)

    def render(self):
        for k in (self.pemain, self.musuh):
            rasio = k.hp / k.hp_maks
            warna = "#43a047" if rasio > 0.5 else "#f9a825" if rasio > 0.25 else "#e53935"
            self.c.coords(k.bar, k.x - 45, 98, k.x - 45 + 90 * rasio, 108)
            self.c.itemconfig(k.bar, fill=warna)
            self.c.itemconfig(k.label, text=f"{k.nama}  {k.hp}/{k.hp_maks}")
        self.stage.config(text=f"Pertarungan {self.indeks + 1} dari {len(self.daftar)}")
        self.btn_potion.config(text=f"POTION ({self.pemain.potion})")

    def log(self, teks):
        self.lbl_log.config(text=teks)

    def tombol(self, aktif):
        s = "normal" if aktif else "disabled"
        self.btn_serang.config(state=s)
        self.btn_potion.config(state=s)

    # ---------- Animasi ----------
    def gerak(self, tag, dx, dy, selesai, langkah=10):
        def step(i):
            if i < langkah:
                self.c.move(tag, dx / langkah, dy / langkah)
                self.root.after(16, step, i + 1)
            else:
                selesai()
        step(0)

    def getar(self, tag, selesai):
        urutan = [8, -16, 16, -16, 8]
        def step(i):
            if i < len(urutan):
                self.c.move(tag, urutan[i], 0)
                self.root.after(35, step, i + 1)
            else:
                selesai()
        step(0)

    def popup(self, x, teks, warna):
        t = self.c.create_text(x, 140, text=teks, font=("Arial", 22, "bold"), fill=warna)
        def naik(i):
            if i < 20:
                self.c.move(t, 0, -2)
                self.root.after(30, naik, i + 1)
            else:
                self.c.delete(t)
        naik(0)

    def serangan(self, a, b, arah, selesai):
        jarak = arah * 190
        def kena():
            teks, dmg, spesial = a.serang(b)
            self.log(teks)
            self.popup(b.x, f"-{dmg}", "yellow" if spesial else "red")
            self.render()
            self.getar(b.tag, lambda: self.gerak(a.tag, -jarak, 0, selesai))
        self.gerak(a.tag, jarak, 0, kena)

    # ---------- Alur game ----------
    def aksi_serang(self):
        if self.sibuk:
            return
        self.sibuk = True
        self.tombol(False)
        self.serangan(self.pemain, self.musuh, 1, self.setelah_pemain)

    def aksi_potion(self):
        if self.sibuk:
            return
        pesan = self.pemain.pakai_potion()
        if pesan is None:
            self.log("Potion habis!")
            return
        self.sibuk = True
        self.tombol(False)
        self.log(pesan)
        self.popup(self.pemain.x, "+30", "lime")
        self.render()
        self.root.after(600, self.giliran_musuh)

    def setelah_pemain(self):
        if not self.musuh.masih_hidup():
            self.musuh_kalah()
        else:
            self.root.after(400, self.giliran_musuh)

    def giliran_musuh(self):
        self.serangan(self.musuh, self.pemain, -1, self.setelah_musuh)

    def setelah_musuh(self):
        if not self.pemain.masih_hidup():
            messagebox.showinfo("Game Over", "Kamu kalah... Coba lagi!")
            self.tampil_menu()
        else:
            self.sibuk = False
            self.tombol(True)

    def musuh_kalah(self):
        self.log(f"{self.musuh.nama} dikalahkan!")
        def hapus():
            self.c.delete(self.musuh.tag)
            self.c.delete("ui" + self.musuh.tag)
            self.indeks += 1
            if self.indeks >= len(self.daftar):
                messagebox.showinfo("MENANG!", "Selamat! Kamu mengalahkan semua musuh!")
                self.tampil_menu()
                return
            self.musuh = self.daftar[self.indeks]
            self.muncul_musuh()
            self.log(f"Musuh muncul: {self.musuh.nama}!")
            self.render()
            self.sibuk = False
            self.tombol(True)
        self.gerak(self.musuh.tag, 0, 70, lambda: self.root.after(300, hapus))


if __name__ == "__main__":
    root = tk.Tk()
    GameApp(root)
    root.mainloop()