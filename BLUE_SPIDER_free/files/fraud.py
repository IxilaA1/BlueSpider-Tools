# Générateur de carte d'identité - Version corrigée avec chemin automatique
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont
import qrcode
import random
import os
import sys
import platform
import hashlib
import getpass
from datetime import datetime
from pathlib import Path

class IDCardGenerator:
    """Générateur de cartes d'identité"""
    
    def __init__(self, root):
        self.root = root
        self.root.title('🪪 Générateur de Carte d\'Identité')
        self.root.geometry('900x500')
        self.root.configure(bg='#1a1a1a')
        
        # Configuration
        self.bg_color = '#ffffff'
        self.text_color = '#000000'
        self.font_path = self.get_available_font()
        
        # Variables
        self.use_qr = ctk.BooleanVar(value=True)
        self.qr_url = ctk.StringVar(value='')
        
        # Configuration UI
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')
        
        self.setup_ui()
    
    def get_available_font(self):
        """Retourne une police disponible"""
        fonts = ['arial.ttf', 'DejaVuSans.ttf', 'LiberationSans-Regular.ttf', 'segoeui.ttf', 'tahoma.ttf']
        for font in fonts:
            try:
                ImageFont.truetype(font, 10)
                return font
            except:
                continue
        return None
    
    def get_output_path(self):
        """Retourne le chemin avec username automatique"""
        try:
            # Récupérer le nom d'utilisateur
            username = os.getlogin()
        except:
            try:
                username = getpass.getuser()
            except:
                username = os.environ.get('USERNAME', 'utilisateur')
        
        # Chemin principal (OneDrive)
        base_path = Path(f"C:/Users/{username}/OneDrive/Bureau/BLUE_SPIDER_free/1-Output")
        
        # Si OneDrive n'existe pas, utiliser Desktop
        if not base_path.parent.parent.exists():  # Vérifie si OneDrive/Bureau existe
            base_path = Path(f"C:/Users/{username}/Desktop/BLUE_SPIDER_free/1-Output")
        
        # Créer le dossier
        try:
            base_path.mkdir(parents=True, exist_ok=True)
        except:
            # Fallback ultime : dossier temporaire
            import tempfile
            base_path = Path(tempfile.gettempdir()) / "BLUE_SPIDER_free" / "1-Output"
            base_path.mkdir(parents=True, exist_ok=True)
        
        return str(base_path)
    
    def setup_ui(self):
        """Interface utilisateur"""
        main_frame = ctk.CTkFrame(self.root, fg_color='#2c2c2c', corner_radius=10)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Titre
        title = ctk.CTkLabel(
            main_frame, 
            text='🪪 Générateur de Carte d\'Identité', 
            font=ctk.CTkFont(family='Arial', size=24, weight='bold'), 
            text_color='#4CAF50'
        )
        title.pack(pady=10)
        
        # Afficher le chemin de sauvegarde
        try:
            save_path = self.get_output_path()
            path_label = ctk.CTkLabel(
                main_frame,
                text=f"📁 Sauvegarde : {save_path}",
                font=ctk.CTkFont(size=10),
                text_color='#888888',
                wraplength=800
            )
            path_label.pack(pady=5)
        except:
            pass
        
        # Formulaire
        form_frame = ctk.CTkFrame(main_frame, fg_color='#333333')
        form_frame.pack(padx=20, pady=10, fill='x')
        
        fields = [
            ('Société', 'company'),
            ('Nom complet', 'name'),
            ('Genre', 'gender'),
            ('Âge', 'age'),
            ('Date naissance', 'dob'),
            ('Groupe sanguin', 'blood'),
            ('Téléphone', 'mobile'),
            ('Adresse', 'address')
        ]
        
        self.entries = {}
        for label, key in fields:
            row = ctk.CTkFrame(form_frame, fg_color='#333333')
            row.pack(fill='x', pady=2)
            
            ctk.CTkLabel(
                row, 
                text=label, 
                font=ctk.CTkFont(size=12), 
                text_color='white'
            ).pack(side='left', padx=5)
            
            entry = ctk.CTkEntry(
                row, 
                width=250, 
                font=ctk.CTkFont(size=12), 
                fg_color='#444444', 
                text_color='white'
            )
            entry.pack(side='right', padx=5)
            self.entries[key] = entry
        
        # QR Code
        qr_frame = ctk.CTkFrame(main_frame, fg_color='#333333')
        qr_frame.pack(padx=20, pady=10, fill='x')
        
        ctk.CTkCheckBox(
            qr_frame, 
            text='Ajouter QR code', 
            variable=self.use_qr, 
            fg_color='#4CAF50', 
            hover_color='#45a049',
            font=ctk.CTkFont(size=12)
        ).pack(side='left', padx=5)
        
        ctk.CTkLabel(
            qr_frame, 
            text='URL (optionnel):', 
            font=ctk.CTkFont(size=12), 
            text_color='white'
        ).pack(side='left', padx=5)
        
        ctk.CTkEntry(
            qr_frame, 
            textvariable=self.qr_url, 
            width=250, 
            font=ctk.CTkFont(size=12), 
            fg_color='#444444', 
            text_color='white'
        ).pack(side='left', padx=5)
        
        # Bouton Générer
        btn_frame = ctk.CTkFrame(main_frame, fg_color='#333333')
        btn_frame.pack(padx=20, pady=10, fill='x')
        
        ctk.CTkButton(
            btn_frame, 
            text='🪄 Générer la carte', 
            command=self.generate_card, 
            fg_color='#4CAF50', 
            text_color='white', 
            font=ctk.CTkFont(size=14, weight='bold'),
            height=40
        ).pack(fill='x', pady=5)
    
    def generate_card(self):
        """Génère la carte"""
        try:
            # Récupérer les données
            data = {key: e.get().strip() for key, e in self.entries.items()}
            
            # Vérification
            if not all(data.values()):
                messagebox.showerror('Erreur', 'Tous les champs sont requis !')
                return
            
            # Création de l'image
            image = Image.new('RGB', (800, 600), self.bg_color)
            draw = ImageDraw.Draw(image)
            
            # Chargement des polices
            try:
                if self.font_path:
                    font_title = ImageFont.truetype(self.font_path, 50)
                    font_text = ImageFont.truetype(self.font_path, 30)
                    font_small = ImageFont.truetype(self.font_path, 25)
                else:
                    font_title = font_text = font_small = ImageFont.load_default()
            except:
                font_title = font_text = font_small = ImageFont.load_default()
            
            # Titre et ID
            draw.text((30, 20), data['company'], fill=self.text_color, font=font_title)
            idno = random.randint(100000, 999999)
            draw.text((550, 30), f'ID {idno}', fill=self.text_color, font=font_text)
            
            # Informations
            y = 120
            spacing = 50
            fields = [
                ('Nom', 'name'),
                ('Genre', 'gender'),
                ('Âge', 'age'),
                ('Né(e) le', 'dob'),
                ('Groupe', 'blood'),
                ('Tél', 'mobile'),
                ('Adresse', 'address')
            ]
            
            for label, key in fields:
                text = f'{label}: {data[key]}'
                draw.text((30, y), text, fill=self.text_color, font=font_small)
                y += spacing
            
            # QR Code
            if self.use_qr.get():
                qr_data = self.qr_url.get().strip()
                if not qr_data:
                    qr_data = f"{data['company']} | {data['name']} | ID: {idno}"
                qr = qrcode.make(qr_data).resize((150, 150))
                image.paste(qr, (600, 400))
            
            # Sauvegarde
            output_dir = self.get_output_path()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(output_dir, f'carte_{timestamp}_{idno}.png')
            image.save(filename)
            
            messagebox.showinfo('Succès', f'✅ Carte sauvegardée !\n\nEmplacement :\n{filename}')
            
        except Exception as e:
            messagebox.showerror('Erreur', f'Erreur : {str(e)}')

if __name__ == '__main__':
    # Nettoyage écran
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Affichage infos
    print("=" * 60)
    print("🪪 GÉNÉRATEUR DE CARTE D'IDENTITÉ")
    print("=" * 60)
    
    try:
        username = os.getlogin()
        print(f"👤 Utilisateur : {username}")
        print(f"📁 Dossier cible : C:\\Users\\{username}\\OneDrive\\Bureau\\BLUE_SPIDER_free\\1-Output")
        print(f"📁 Fallback : C:\\Users\\{username}\\Desktop\\BLUE_SPIDER_free\\1-Output")
    except:
        print("👤 Utilisateur : (non détecté)")
    
    print("=" * 60)
    print("✅ Lancement de l'interface...")
    print("=" * 60)
    
    # Lancement
    root = ctk.CTk()
    app = IDCardGenerator(root)
    root.mainloop()