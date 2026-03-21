# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import secrets
import string
import base64
import zlib
import marshal
import json
from pathlib import Path
from math import ceil
import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime, UTC
try:
    from Crypto.Cipher import AES
    from Crypto.Hash import HMAC, SHA256
except ImportError:
    print('Error: pycryptodome required. Install with: pip install pycryptodome')
    sys.exit(1)
try:
    from argon2.low_level import hash_secret_raw, Type
except ImportError:
    print('Error: argon2-cffi required. Install with: pip install argon2-cffi')
    sys.exit(1)
try:
    from colorama import init, Fore, Style
    init()
except ImportError:
    print('Error: colorama required. Install with: pip install colorama')
    sys.exit(1)

logo_ascii = """
                                                         .+#%@@%#+.                                     
                                                    .#@@@@@@@@@@@@@@@@#.                                
                                                  +@@@@@@@@@@@@@@@@@@@@@@*                              
                                                .%@@@@@@@@@@@@@@@@@@@@@@@@%.                            
                                                %@@@@@@@@@@@@@@@@@@@@@@@@@@%                            

                                               %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                          
                                                -..........................-.                           
                                                %@@@@@@00@@@@@@@@@@@%@@@@@@%                            
                                                %@@@#     .%@@@@%.     *@@@%                            
                                                . :+00+--+%@#::#@%*--+00+: .                            
                                                                           .                            
                                                 :                        :                             
                                                  -                      =                              
                                                    -                  -                                
                                                       -=          --                                   
                                               -+#%@@@@@@=        =@@@@@@%#+-                           
                                            *@@@@@@@@@@@@=        =@@@@@@@@@@@@*                        
                                          *@@@@@@@@@@@@@@+        +@@@@@@@@@@@@@@#                      
                                         *@@@@@@@@@@@@@@@@%=    -%@@@@@@@@@@@@@@@@#                     
                                        -@@@@@@@@@@@@@@@@@@@%#*0@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-

"""


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)

# ==================== CONFIGURATION ====================
SALT_LEN = 16
NONCE_LEN = 12
TAG_LEN = 16
ARGON_TIME = 2
ARGON_MEMORY = 65536
ARGON_PARALLELISM = 1
KEY_LEN = 32
HMAC_BLOCK = 32
ARGON_TYPE = Type.ID

# Couleurs UI
UI_COLOR = Fore.LIGHTCYAN_EX
ERROR_COLOR = Fore.RED
RESET = Style.RESET_ALL

# Dossier de sortie FIXE
USERNAME = os.getenv('USERNAME') or os.getenv('USER') or 'default'
OUTPUT_DIR = Path(f'C:/Users/{USERNAME}/OneDrive/Bureau/BLUE_SPIDER_free/1-Output')
# =======================================================

def rand_ident(n=10):
    alphabet = string.ascii_letters + '_'
    return secrets.choice(alphabet) + ''.join((secrets.choice(alphabet + string.digits) for _ in range(n - 1)))

def derive_key_argon2(password: str, salt: bytes) -> bytes:
    pwd_b = (password if password is not None else '').encode('utf-8')
    return hash_secret_raw(secret=pwd_b, salt=salt, time_cost=ARGON_TIME, memory_cost=ARGON_MEMORY, parallelism=ARGON_PARALLELISM, hash_len=KEY_LEN, type=ARGON_TYPE)

def keystream_hmac_counter(key: bytes, length: int) -> bytes:
    blocks = ceil(length / HMAC_BLOCK)
    out = bytearray()
    for i in range(blocks):
        ctr = i.to_bytes(8, 'big')
        h = HMAC.new(key, digestmod=SHA256)
        h.update(ctr)
        out.extend(h.digest())
    return bytes(out[:length])

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes((x ^ y for x, y in zip(a, b)))

def b64enc(b: bytes) -> str:
    return base64.b64encode(b).decode('ascii')

def build_blob_with_meta(source_code: str, password: str) -> str:
    """
    Crée un blob avec deux parties:
    - Partie 1: Code normal (toujours exécutable avec clé vide)
    - Partie 2: Code protégé (nécessite la bonne clé)
    """
    # Sépare le code en deux parties (normal et protégé)
    # On utilise un marqueur spécial dans le code source
    if '# PROTECTED_START' in source_code:
        parts = source_code.split('# PROTECTED_START')
        normal_code = parts[0]
        protected_code = '# PROTECTED_START' + parts[1]
    else:
        # Si pas de marqueur, tout est normal
        normal_code = source_code
        protected_code = ""
    
    # Compile le code normal
    normal_code_obj = compile(normal_code, '<obf>', 'exec')
    normal_marsh = marshal.dumps(normal_code_obj)
    normal_comp = zlib.compress(normal_marsh, level=9)
    
    # Compile le code protégé (si existant)
    if protected_code:
        protected_code_obj = compile(protected_code, '<protected>', 'exec')
        protected_marsh = marshal.dumps(protected_code_obj)
        protected_comp = zlib.compress(protected_marsh, level=9)
    else:
        protected_comp = b''
    
    # Génère le sel et la clé
    salt = secrets.token_bytes(SALT_LEN)
    
    # Chiffre le code normal avec clé vide
    empty_key = derive_key_argon2('', salt)
    ks_normal = keystream_hmac_counter(empty_key, len(normal_comp))
    xored_normal = xor_bytes(normal_comp, ks_normal)
    
    nonce1 = secrets.token_bytes(NONCE_LEN)
    cipher1 = AES.new(empty_key, AES.MODE_GCM, nonce=nonce1)
    ct1 = cipher1.encrypt(xored_normal)
    tag1 = cipher1.digest()
    
    # Prépare les métadonnées
    meta = {
        'has_protected': bool(protected_code),
        'key_hint': base64.b64encode(password.encode() if password else b'').decode() if password else ''
    }
    meta_json = json.dumps(meta, separators=(',', ':')).encode('utf-8')
    meta_comp = zlib.compress(meta_json, level=9)
    
    # Si un mot de passe est fourni, on chiffre le code protégé
    if protected_code and password:
        protected_key = derive_key_argon2(password, salt)
        ks_protected = keystream_hmac_counter(protected_key, len(protected_comp))
        xored_protected = xor_bytes(protected_comp, ks_protected)
        
        nonce_protected = secrets.token_bytes(NONCE_LEN)
        cipher_protected = AES.new(protected_key, AES.MODE_GCM, nonce=nonce_protected)
        ct_protected = cipher_protected.encrypt(xored_protected)
        tag_protected = cipher_protected.digest()
        
        protected_blob = nonce_protected + tag_protected + ct_protected
    else:
        protected_blob = b''
    
    # Assemble tout
    normal_payload = nonce1 + tag1 + ct1
    normal_len = len(normal_payload).to_bytes(8, 'big')
    protected_len = len(protected_blob).to_bytes(8, 'big')
    
    assembled = salt + normal_len + normal_payload + protected_len + protected_blob + meta_comp
    
    return b64enc(assembled)

def make_minimal_loader(big_b64):
    blob_var = rand_ident(8)
    
    loader = f'''# ultra-minimal loader (packed payload)
import base64 as _b64, zlib as _zl, marshal as _m, sys as _sys
{blob_var} = {repr(big_b64)}

# Variables globales pour le déverrouillage
_KEY_CACHE = None
_IS_UNLOCKED = False
_PROTECTED_CODE = None

def _load_and_execute():
    """Charge et exécute le code (toujours possible)"""
    global _PROTECTED_CODE
    
    try:
        assembled = _b64.b64decode({blob_var})
    except Exception:
        _sys.exit('Malformed payload')

    s, n, t = {SALT_LEN}, {NONCE_LEN}, {TAG_LEN}
    salt = assembled[:s]
    
    # Lit la longueur du payload normal
    normal_len = int.from_bytes(assembled[s:s+8], 'big')
    pstart, pend = s + 8, s + 8 + normal_len
    normal_payload = assembled[pstart:pend]
    
    # Lit la longueur du payload protégé
    protected_start = pend
    protected_len = int.from_bytes(assembled[protected_start:protected_start+8], 'big')
    protected_payload = assembled[protected_start+8:protected_start+8+protected_len]
    
    # Métadonnées à la fin
    meta_blob = assembled[protected_start+8+protected_len:]

    # Extrait les composants du payload normal
    nonce1, tag1, ct1 = normal_payload[:n], normal_payload[n:n+t], normal_payload[n+t:]

    try:
        from argon2.low_level import hash_secret_raw, Type as _Type
    except Exception:
        _sys.exit('argon2-cffi required')

    def derive(p):
        return hash_secret_raw(secret=(p.encode('utf-8')), salt=salt, 
                              time_cost={ARGON_TIME}, memory_cost={ARGON_MEMORY}, 
                              parallelism={ARGON_PARALLELISM}, hash_len={KEY_LEN}, 
                              type=_Type.ID)

    # Décrypte toujours avec la clé vide pour le code normal
    empty_key = derive('')
    
    from Crypto.Cipher import AES as _AES
    
    # Décrypte le payload normal
    cipher1 = _AES.new(empty_key, _AES.MODE_GCM, nonce=nonce1)
    try:
        xored_normal = cipher1.decrypt_and_verify(ct1, tag1)
    except Exception:
        _sys.exit('Corrupted normal payload')

    # Reconstruit le keystream pour le code normal
    ln = len(xored_normal)
    blocks = (ln + {HMAC_BLOCK} - 1) // {HMAC_BLOCK}
    out = bytearray()
    for i in range(blocks):
        ctr = i.to_bytes(8, 'big')
        from Crypto.Hash import HMAC, SHA256
        h = HMAC.new(empty_key, digestmod=SHA256)
        h.update(ctr)
        out.extend(h.digest())
    ks = bytes(out[:ln])
    normal_bytes = bytes(a ^ b for a, b in zip(xored_normal, ks))

    # Décompresse et charge le code normal
    try:
        normal_marsh = _zl.decompress(normal_bytes)
        normal_code = _m.loads(normal_marsh)
    except Exception as e:
        _sys.exit(f'Normal code error: {{e}}')

    # Charge les métadonnées
    try:
        meta_json = _zl.decompress(meta_blob)
        meta = __import__('json').loads(meta_json.decode('utf-8'))
    except Exception:
        meta = {{'has_protected': False}}

    # Si il y a du code protégé, on le garde pour déverrouillage plus tard
    if meta.get('has_protected') and protected_payload:
        nonce_prot, tag_prot, ct_prot = protected_payload[:n], protected_payload[n:n+t], protected_payload[n+t:]
        _PROTECTED_CODE = (salt, nonce_prot, tag_prot, ct_prot, derive)
    
    return normal_code

def unlock_protected(password):
    """Déverrouille le code protégé avec le mot de passe"""
    global _KEY_CACHE, _IS_UNLOCKED
    
    if _PROTECTED_CODE is None:
        return False, "No protected code available"
    
    salt, nonce_prot, tag_prot, ct_prot, derive = _PROTECTED_CODE
    
    try:
        # Dérive la clé avec le mot de passe fourni
        key = derive(password)
        
        from Crypto.Cipher import AES as _AES
        cipher = _AES.new(key, _AES.MODE_GCM, nonce=nonce_prot)
        xored_protected = cipher.decrypt_and_verify(ct_prot, tag_prot)
        
        # Reconstruit le keystream
        ln = len(xored_protected)
        blocks = (ln + {HMAC_BLOCK} - 1) // {HMAC_BLOCK}
        out = bytearray()
        for i in range(blocks):
            ctr = i.to_bytes(8, 'big')
            from Crypto.Hash import HMAC, SHA256
            h = HMAC.new(key, digestmod=SHA256)
            h.update(ctr)
            out.extend(h.digest())
        ks = bytes(out[:ln])
        protected_bytes = bytes(a ^ b for a, b in zip(xored_protected, ks))
        
        # Charge le code protégé
        protected_marsh = _zl.decompress(protected_bytes)
        protected_code = _m.loads(protected_marsh)
        
        # Exécute le code protégé dans le contexte global
        exec(protected_code, globals(), globals())
        
        _KEY_CACHE = key
        _IS_UNLOCKED = True
        return True, "Protected code unlocked successfully!"
        
    except Exception as e:
        return False, f"Invalid key or corrupted data: {{e}}"

def _r():
    """Point d'entrée principal - toujours exécuté"""
    # Charge et exécute le code normal
    normal_code = _load_and_execute()
    
    # Injecte les fonctions de déverrouillage dans le contexte
    globals()['unlock'] = unlock_protected
    globals()['is_unlocked'] = lambda: _IS_UNLOCKED
    
    # Exécute le code normal
    exec(normal_code, globals(), globals())

if __name__ == '__main__':
    _r()
'''
    return loader

def main():
    # Création automatique du dossier de sortie
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(ERROR_COLOR + f"Erreur lors de la création du dossier: {e}" + RESET)
        sys.exit(1)

    # Affiche la bannière
    banner = UI_COLOR + '''
╔══════════════════════════════════════════════════════════════════╗
║                    ObsfucSpectre - Générateur                    ║
╠══════════════════════════════════════════════════════════════════╣
║  • Code normal toujours exécutable                               ║
║  • Code protégé nécessite une clé pour déverrouiller             ║
║  • Utilise # PROTECTED_START pour marquer le code à protéger    ║
╚══════════════════════════════════════════════════════════════════╝
''' + RESET
    print(banner)
    
    print(UI_COLOR + f"Dossier de sortie: {OUTPUT_DIR}" + RESET)
    print()
    
    path = input(UI_COLOR + 'Path to Python file: ' + RESET).strip()
    file = Path(path)
    if not file.exists() or not file.is_file():
        print(ERROR_COLOR + 'Error: File not found' + RESET)
        sys.exit(1)
    
    pwd = input(UI_COLOR + 'Clé pour protéger le code sensible (laissez vide pour pas de protection): ' + RESET).strip()
    
    try:
        src = file.read_text(encoding='utf-8')
        print(UI_COLOR + 'Obfuscation en cours...' + RESET)
        big_b64 = build_blob_with_meta(src, pwd)
        loader_code = make_minimal_loader(big_b64)
        
        # Sauvegarde
        out = OUTPUT_DIR / f'{file.stem}_obf{file.suffix}'
        out.write_text(loader_code, encoding='utf-8')
        
        print(UI_COLOR + f'✅ Fichier obfusqué créé: {out}' + RESET)
        print(UI_COLOR + f'📁 Dossier: {OUTPUT_DIR}' + RESET)
        
        if pwd:
            print(UI_COLOR + '\n🔐 Note: Le code protégé nécessite la clé pour être déverrouillé' + RESET)
            print(UI_COLOR + f'    Dans le programme, utilise: unlock("votre_clé")' + RESET)
        
        input(UI_COLOR + "\nAppuyez sur Entrée pour continuer..." + RESET)
        
    except Exception as e:
        print(ERROR_COLOR + f'Error: {e}' + RESET)
        sys.exit(1)

if __name__ == '__main__':
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    clear_screen()
    main()