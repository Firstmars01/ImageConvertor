import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os


class ImageToIcoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertisseur Image → ICO")
        self.root.geometry("550x450")
        self.root.resizable(False, False)

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()

        # Tailles d'icônes disponibles
        self.sizes = [16, 32, 48, 64, 128, 256]
        self.size_vars = {}

        self._build_ui()

    def _build_ui(self):
        # --- Titre ---
        title = tk.Label(self.root, text="Convertisseur PNG / JPG → ICO",
                         font=("Segoe UI", 16, "bold"))
        title.pack(pady=(15, 10))

        # --- Fichier d'entrée ---
        frame_input = ttk.LabelFrame(self.root, text="Fichier source", padding=10)
        frame_input.pack(fill="x", padx=20, pady=5)

        entry_input = ttk.Entry(frame_input, textvariable=self.input_path, state="readonly")
        entry_input.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_browse_input = ttk.Button(frame_input, text="Parcourir…", command=self._browse_input)
        btn_browse_input.pack(side="right")

        # --- Fichier de sortie ---
        frame_output = ttk.LabelFrame(self.root, text="Fichier de sortie", padding=10)
        frame_output.pack(fill="x", padx=20, pady=5)

        entry_output = ttk.Entry(frame_output, textvariable=self.output_path, state="readonly")
        entry_output.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_browse_output = ttk.Button(frame_output, text="Parcourir…", command=self._browse_output)
        btn_browse_output.pack(side="right")

        # --- Tailles d'icônes ---
        frame_sizes = ttk.LabelFrame(self.root, text="Tailles d'icônes (pixels)", padding=10)
        frame_sizes.pack(fill="x", padx=20, pady=10)

        for i, size in enumerate(self.sizes):
            var = tk.BooleanVar(value=(size == 256))  # 256x256 coché par défaut
            self.size_vars[size] = var
            cb = ttk.Checkbutton(frame_sizes, text=f"{size} × {size}", variable=var)
            cb.grid(row=i // 3, column=i % 3, sticky="w", padx=15, pady=3)

        # --- Boutons ---
        frame_buttons = ttk.Frame(self.root)
        frame_buttons.pack(pady=20)

        btn_convert = ttk.Button(frame_buttons, text="Convertir", command=self._convert)
        btn_convert.pack(side="left", padx=10, ipadx=20, ipady=5)

        btn_quit = ttk.Button(frame_buttons, text="Quitter", command=self.root.quit)
        btn_quit.pack(side="left", padx=10, ipadx=20, ipady=5)

        # --- Barre de statut ---
        self.status = tk.StringVar(value="Prêt.")
        status_bar = tk.Label(self.root, textvariable=self.status, anchor="w",
                              relief="sunken", font=("Segoe UI", 9))
        status_bar.pack(fill="x", side="bottom", padx=5, pady=5)

    def _browse_input(self):
        path = filedialog.askopenfilename(
            title="Sélectionner une image",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Tous les fichiers", "*.*"),
            ]
        )
        if path:
            self.input_path.set(path)
            # Proposer automatiquement un chemin de sortie
            base = os.path.splitext(path)[0]
            self.output_path.set(base + ".ico")
            self.status.set(f"Image sélectionnée : {os.path.basename(path)}")

    def _browse_output(self):
        path = filedialog.asksaveasfilename(
            title="Enregistrer l'icône sous…",
            defaultextension=".ico",
            filetypes=[("Icône", "*.ico"), ("Tous les fichiers", "*.*")]
        )
        if path:
            self.output_path.set(path)

    def _convert(self):
        input_file = self.input_path.get()
        output_file = self.output_path.get()

        # Validations
        if not input_file:
            messagebox.showwarning("Attention", "Veuillez sélectionner un fichier image source.")
            return

        if not output_file:
            messagebox.showwarning("Attention", "Veuillez choisir un emplacement pour le fichier de sortie.")
            return

        selected_sizes = [s for s, var in self.size_vars.items() if var.get()]
        if not selected_sizes:
            messagebox.showwarning("Attention", "Veuillez cocher au moins une taille d'icône.")
            return

        # Conversion
        try:
            self.status.set("Conversion en cours…")
            self.root.update()

            img = Image.open(input_file)
            # Convertir en RGBA si nécessaire (les ICO supportent la transparence)
            if img.mode != "RGBA":
                img = img.convert("RGBA")

            icon_sizes = [(s, s) for s in sorted(selected_sizes)]
            img.save(output_file, format="ICO", sizes=icon_sizes)

            self.status.set(f"Icône créée : {os.path.basename(output_file)}")
            messagebox.showinfo("Succès",
                                f"L'icône a été créée avec succès !\n\n"
                                f"{output_file}\n"
                                f"Tailles : {', '.join(f'{s}×{s}' for s in sorted(selected_sizes))}")

        except Exception as e:
            self.status.set("Erreur lors de la conversion.")
            messagebox.showerror("Erreur", f"Impossible de convertir l'image :\n\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToIcoApp(root)
    root.mainloop()

