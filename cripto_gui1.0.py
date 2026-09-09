"""
cripto_gui.py — Interface gráfica (Tkinter) para o criptografador de texto
por chave alfanumérica (mesma lógica de cripto.py).

Tkinter já vem embutido no Python (não precisa instalar nada),
funciona no Python 3.10 sem problemas.

Criado por: @gustavo.pertum com ajuda do @Claudeai
"""

import tkinter as tk
from tkinter import messagebox


def encrypt(texto: str, chave: str) -> str:
    resultado = []
    for i, char in enumerate(texto):
        desloc = ord(chave[i % len(chave)])
        codigo = (ord(char) + desloc) % 256
        resultado.append(codigo)
    return "".join(f"{b:02x}" for b in resultado)


def decrypt(texto_cifrado: str, chave: str) -> str:
    texto_cifrado = texto_cifrado.strip()
    bytes_cifrados = [
        int(texto_cifrado[i:i + 2], 16)
        for i in range(0, len(texto_cifrado), 2)
    ]
    resultado = []
    for i, b in enumerate(bytes_cifrados):
        desloc = ord(chave[i % len(chave)])
        codigo = (b - desloc) % 256
        resultado.append(chr(codigo))
    return "".join(resultado)


class CriptoApp:
    def __init__(self, root):
        self.root = root
        root.title("Criptografador de Texto")
        root.geometry("480x380")
        root.resizable(False, False)

        pad = {"padx": 10, "pady": 5}

        tk.Label(root, text="Chave:").pack(anchor="w", **pad)
        self.entry_chave = tk.Entry(root, width=50)
        self.entry_chave.insert(0, "kqzd35c")
        self.entry_chave.pack(**pad)

        tk.Label(root, text="Texto (digite aqui para criptografar,\nou cole um hex para decifrar):").pack(anchor="w", **pad)
        self.text_input = tk.Text(root, height=5, width=55)
        self.text_input.pack(**pad)

        frame_botoes = tk.Frame(root)
        frame_botoes.pack(pady=8)

        tk.Button(frame_botoes, text="Criptografar", width=15,
                  command=self.criptografar).grid(row=0, column=0, padx=5)
        tk.Button(frame_botoes, text="Decifrar", width=15,
                  command=self.decifrar).grid(row=0, column=1, padx=5)
        tk.Button(frame_botoes, text="Limpar", width=15,
                  command=self.limpar).grid(row=0, column=2, padx=5)

        tk.Label(root, text="Resultado:").pack(anchor="w", **pad)
        self.text_output = tk.Text(root, height=5, width=55, fg="blue")
        self.text_output.pack(**pad)

    def get_chave(self):
        chave = self.entry_chave.get().strip()
        if not chave:
            messagebox.showerror("Erro", "Digite uma chave.")
            return None
        return chave

    def criptografar(self):
        chave = self.get_chave()
        if not chave:
            return
        texto = self.text_input.get("1.0", tk.END).rstrip("\n")
        try:
            resultado = encrypt(texto, chave)
            self.mostrar_resultado(resultado)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def decifrar(self):
        chave = self.get_chave()
        if not chave:
            return
        texto = self.text_input.get("1.0", tk.END).strip()
        try:
            resultado = decrypt(texto, chave)
            self.mostrar_resultado(resultado)
        except Exception:
            messagebox.showerror("Erro", "Texto cifrado inválido (esperado hexadecimal).")

    def mostrar_resultado(self, resultado):
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, resultado)

    def limpar(self):
        self.text_input.delete("1.0", tk.END)
        self.text_output.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CriptoApp(root)
    root.mainloop()
