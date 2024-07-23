# Importing Libraries 
import os 
import math
import sys
import shutil
from collections import defaultdict

# pcloud automatic transfer creates duplicates
# this script runs through the files and find duplicates based on their name and size (rounded kb sized, for some reason the exact size change)
# then files are moved to another folder for a manual delete
#
# input: 
#   - source directory
#   - duplicates destination directory
#   - boolean to enable the move or not
# DestDir can be on another drive (shutil should support this)
#
# ex: PS D:\MYSCRIPTS> python.exe .\findDuplicates.py 'P:\Automatic Upload\test' 'P:\Automatic Upload\duplicate' true


def findAndMove_duplicates(sInputDir, sDestDir, bMove):
    files_by_size = defaultdict(list)
    duplicates = defaultdict(list)
    
    # Parcours le répertoire et stocke les fichiers par taille
    for root, dirs, files in os.walk(sInputDir):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_size_kb = math.floor(os.path.getsize(file_path) / 1024)
            files_by_size[file_size_kb].append(file_path)
    
    # Vérifie les fichiers de même taille pour les doublons de nom
    for file_size, file_list in files_by_size.items():
        if len(file_list) > 1:
            for i in range(len(file_list)):
                for j in range(i + 1, len(file_list)):

                    file_path1 = file_list[i]
                    file_path2 = file_list[j]
                    file_name1 = os.path.basename(file_path1)
                    file_name2 = os.path.basename(file_path2)
                    
                    # Récupère les noms de fichier sans extension
                    base_name1 = os.path.splitext(file_name1)[0]
                    base_name2 = os.path.splitext(file_name2)[0]
					
                    # Vérifie si l'un des noms de fichier contient l'autre
                    if base_name1 in base_name2 or base_name2 in base_name1:
                        if(len(base_name1)<len(base_name2)):
                            duplicates[base_name1].append(file_path2)
                        else :
                            duplicates[base_name2].append(file_path1)

    # Affiche les doublons trouvés
    for base_name, file_paths in duplicates.items():
        unique_paths = list(set(file_paths))
        if len(unique_paths) > 1:
            print(f"Doublons trouvés pour le fichier de base '{base_name}':")
            for file_path in unique_paths:
                print(f" - {file_path}")
                targetFile = sDestDir+"\\"+os.path.basename(file_path)
                print(f" -> {targetFile}")
                if (bMove) :
                    if(os.path.isfile(file_path)):
                        shutil.move(file_path, targetFile)
                    else:
                        print(f"[error] Impossible to move file {file_path}")

# Utilisation du script
if len(sys.argv) == 4 :
    inputDir = sys.argv[1]
    destDir = sys.argv[2]
    move = sys.argv[3].casefold() == "true".casefold()
    
    print("------------------------------")
    print(f"Input directory to check:     {inputDir}")
    print(f"Destination directory:        {destDir}")
    print(f"Move the duplicate files ?:   {move}")
    print("------------------------------")
    
    findAndMove_duplicates(inputDir, destDir, move)
elif len(sys.argv) == 1:
    print("Usage python.exe .\\findDuplicates.py SourceDirectory DestinationDirectory MoveFiles(true/false)?")

else:
    print("Invalid number or args")
