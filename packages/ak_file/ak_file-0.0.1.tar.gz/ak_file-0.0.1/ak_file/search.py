import os

def find_files_w_extension(folder_path:str, extension:str, search_subdir:bool=False) -> list[str]:
    "Returns a list of files in the directory with matching extension"
    file_list = []
    if search_subdir:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(extension.lower()):
                    file_list.append(os.path.join(root, file))
    else:
        file_list = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith(extension.lower())]
    
    return file_list