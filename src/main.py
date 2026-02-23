# importando Tkinter
from tkinter import *
from tkinter import Tk, messagebox

# importando pillow
from PIL import Image, ImageTk

import csv
import subprocess
import ctypes

# ================= CORES (TEMA ESCURO) =================
co0 = "#0f172a"   # fundo principal
co1 = "#020617"   # fundo secundário
co2 = "#22c55e"   # verde
co3 = "#ef4444"   # vermelho
co4 = "#e5e7eb"   # texto claro
co5 = "#3b82f6"   # azul
co6 = "#1e293b"   # campos / lista

# ---------------- FUNÇÕES DE SISTEMA ----------------


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def flush_dns():
    subprocess.run("ipconfig /flushdns", shell=True)


def pode_escrever_hosts(caminho):
    try:
        with open(caminho, 'a'):
            return True
    except PermissionError:
        return False


def gerar_variacoes(site):
    return list(set([
        site,
        "www." + site,
        "m." + site
    ]))

# ---------------- JANELA ----------------


janela = Tk()
janela.title("")
janela.geometry("390x350")
janela.configure(background=co1)
janela.resizable(width=False, height=False)

# Frames
frame_logo = Frame(janela, width=400, height=60, bg=co1)
frame_logo.grid(row=0, column=0)

frame_corpo = Frame(janela, width=400, height=400, bg=co1)
frame_corpo.grid(row=1, column=0)

# Logo
imagem = Image.open("logo.png")
imagem = imagem.resize((44, 44), Image.LANCZOS)
Imagem = ImageTk.PhotoImage(imagem)

Label(frame_logo, image=Imagem, bg=co1).place(x=20, y=3)
Label(
    frame_logo,
    text="Bloqueador de Sites",
    font=("Segoe UI", 22, "bold"),
    bg=co1,
    fg=co4
).place(x=70, y=10)

Label(frame_logo, bg=co5, width=445, height=1).place(x=0, y=57)

# ---------------- VARIÁVEIS ----------------

iniciar = BooleanVar()

# ---------------- FUNÇÕES ----------------


def ver_sites():
    Listbox.delete(0, END)
    try:
        with open("sites.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                Listbox.insert(END, row[0])
    except FileNotFoundError:
        pass


def salvar_site(site):
    with open("sites.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([site])
    messagebox.showinfo("Sucesso", "Site adicionado com sucesso!")
    ver_sites()


def deletar_site():
    site = Listbox.get(ACTIVE)
    if not site:
        return

    nova_lista = []
    with open("sites.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != site:
                nova_lista.append(row)

    with open("sites.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(nova_lista)

    messagebox.showinfo("Sucesso", "Site removido com sucesso!")
    ver_sites()


def adicionar_site():
    site = e_site.get()
    if site:
        e_site.delete(0, END)
        salvar_site(site)


def bloquear_site():
    hosts = r"C:\Windows\System32\drivers\etc\hosts"
    redirect = "127.0.0.1 "

    if not is_admin():
        messagebox.showerror("Erro", "Execute o programa como ADMINISTRADOR")
        return

    if not pode_escrever_hosts(hosts):
        messagebox.showerror("Erro", "Sem permissão para editar o hosts")
        return

    sites = []
    with open("sites.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            sites.extend(gerar_variacoes(row[0]))

    if iniciar.get():
        with open(hosts, "r+") as file:
            conteudo = file.read()
            for site in sites:
                linha = redirect + site
                if linha not in conteudo:
                    file.write(linha + "\n")
    else:
        with open(hosts, "r+") as file:
            linhas = file.readlines()
            file.seek(0)
            for linha in linhas:
                if not any(site in linha for site in sites):
                    file.write(linha)
            file.truncate()

    flush_dns()


def bloqueador_site():
    iniciar.set(True)
    bloquear_site()
    messagebox.showinfo("Sucesso", "Sites bloqueados com sucesso!")


def desbloquear_site():
    iniciar.set(False)
    bloquear_site()
    messagebox.showinfo("Sucesso", "Sites desbloqueados com sucesso!")

# ---------------- INTERFACE ----------------


Label(
    frame_corpo,
    text="Digite o site que deseja bloquear *",
    font=("Segoe UI", 10, "bold"),
    bg=co1,
    fg=co4
).place(x=20, y=20)

e_site = Entry(
    frame_corpo,
    width=21,
    font=("Segoe UI", 14),
    bg=co6,
    fg=co4,
    insertbackground=co4,
    relief=FLAT,
    highlightthickness=1,
    highlightbackground=co5,
    highlightcolor=co5
)
e_site.place(x=23, y=50)

Button(
    frame_corpo,
    text="Adicionar",
    command=adicionar_site,
    bg=co5,
    fg=co4,
    width=10,
    relief=FLAT,
    cursor="hand2",
    activebackground=co2
).place(x=267, y=50)

Button(
    frame_corpo,
    text="Remover",
    command=deletar_site,
    bg=co5,
    fg=co4,
    width=10,
    relief=FLAT,
    cursor="hand2",
    activebackground=co3
).place(x=267, y=100)

Button(
    frame_corpo,
    text="Desbloquear",
    command=desbloquear_site,
    bg=co2,
    fg=co1,
    width=10,
    relief=FLAT,
    cursor="hand2",
    activebackground=co5
).place(x=267, y=150)

Button(
    frame_corpo,
    text="Bloquear",
    command=bloqueador_site,
    bg=co3,
    fg=co1,
    width=10,
    relief=FLAT,
    cursor="hand2",
    activebackground=co2
).place(x=267, y=200)

Listbox = Listbox(
    frame_corpo,
    width=33,
    height=10,
    font=("Segoe UI", 10),
    bg=co6,
    fg=co4,
    selectbackground=co5,
    selectforeground=co1,
    relief=FLAT,
    highlightthickness=1,
    highlightbackground=co5
)
Listbox.place(x=23, y=100)

ver_sites()
janela.mainloop()
