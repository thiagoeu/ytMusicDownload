import os
import yt_dlp
import tkinter as tk
from tkinter import messagebox

def download_playlist():
    playlist_url = url_entry.get()
    folder_name = folder_entry.get()

    if not playlist_url or not folder_name:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    # Caminho da pasta Downloads do Windows
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    output_dir = os.path.join(downloads_dir, folder_name)

    # Cria a pasta se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Configurações de download
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: print(f'Download progress: {d["downloaded_bytes"] / d["total_bytes"] * 100:.2f}%')]
    }

    # Faz o download da playlist
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([playlist_url])
            messagebox.showinfo("Sucesso", "Download concluído!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha no download: {e}")
            return

    # Renomeia os arquivos para garantir a extensão .mp3
    for filename in os.listdir(output_dir):
        if not filename.endswith('.mp3'):
            old_file = os.path.join(output_dir, filename)
            new_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.mp3")
            os.rename(old_file, new_file)

    messagebox.showinfo("Sucesso", "Arquivos renomeados para .mp3!")

# Criação da janela principal
root = tk.Tk()
root.title("Downloader de Playlist do YouTube")

# Criação dos campos de entrada
tk.Label(root, text="URL da Playlist:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

tk.Label(root, text="Nome da Pasta:").pack(pady=5)
folder_entry = tk.Entry(root, width=50)
folder_entry.pack(pady=5)

# Botão de download
download_button = tk.Button(root, text="Baixar MP3", command=download_playlist)
download_button.pack(pady=20)

# Inicia a interface
root.mainloop()
