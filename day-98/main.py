import os
import shutil
from datetime import datetime


source_dir = r"C:\Users\TuUsuario\Documentos"  
backup_dir = r"C:\Backups\Documentos"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_name = f"Backup_{timestamp}"
backup_path = os.path.join(backup_dir, backup_name)


if not os.path.exists(backup_path):
    os.makedirs(backup_path)


for item in os.listdir(source_dir):
    source_item = os.path.join(source_dir, item)
    backup_item = os.path.join(backup_path, item)
    
    if os.path.isdir(source_item):
        shutil.copytree(source_item, backup_item)  # Copia subcarpetas
    else:
        shutil.copy2(source_item, backup_item)  # Copia archivos

print(f"Respaldo completado en: {backup_path}")
