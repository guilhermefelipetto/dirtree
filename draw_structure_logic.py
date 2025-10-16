import os


def sort_entries(entries, root_path, sort_key):
    """
    ### Função auxiliar para ordenar as entradas com base na chave fornecida.
    
    - Mapeia a chave para uma tupla de ordenação (tipo, nome)
    - O primeiro elemento da tupla define a ordem primária (arquivo vs. diretório)
    - O segundo elemento define a ordem secundária (nome)
    """

    is_dir_first = "dirs_first" in sort_key
    is_reverse = "_za" in sort_key

    def get_sort_key(entry):
        full_path = os.path.join(root_path, entry)
        is_dir = os.path.isdir(full_path)
        
        # priorizar dir ou arquivos
        if is_dir_first:
            # Dir. primeiro: (False, nome) para dir, (True, nome) para arquivos
            type_order = not is_dir
        else:
            # Arquivos primeiro: (False, nome) para arquivos, (True, nome) para dir
            type_order = is_dir
            
        return (type_order, entry.lower())

    entries.sort(key=get_sort_key, reverse=is_reverse)
    return entries


def draw_tree(root_path,
              ignore_files=None,
              ignore_folders=None,
              ignore_extensions=None,
              always_include=None,
              root_sort_key="dirs_first_az", # Ex: "files_first_za"
              subdir_sort_key="dirs_first_az", # Ex: "dirs_first_az"
              prefix="",
              is_root=False):
    
    ignore_files = set(ignore_files or [])
    ignore_folders = set(ignore_folders or [])
    ignore_extensions = set(ignore_extensions or [])
    always_include = set(always_include or [])

    try:
        entries = os.listdir(root_path)
    except (PermissionError, FileNotFoundError):
        return ""

    # Filtra as entradas
    entries_filtered = []
    for entry in entries:
        full_path = os.path.join(root_path, entry)
        if entry.startswith(".") and entry not in always_include:
            continue
        if os.path.isdir(full_path) and entry in ignore_folders:
            continue
        if os.path.isfile(full_path):
            _name, ext = os.path.splitext(entry)
            if entry in ignore_files and entry not in always_include:
                continue
            if ext in ignore_extensions and entry not in always_include:
                continue
        entries_filtered.append(entry)

    # Ordena com base no nivel (root ou subdir)
    current_sort_key = root_sort_key if is_root else subdir_sort_key
    entries_filtered = sort_entries(entries_filtered, root_path, current_sort_key)

    # Gera a string da árvore
    tree_str = ""
    entries_count = len(entries_filtered)
    
    # Logica para linha de separacao entre pastas e arquivos no root
    if is_root:
        last_folder_index = -1
        first_file_index = -1
        
        for i, entry in enumerate(entries_filtered):
            if os.path.isdir(os.path.join(root_path, entry)):
                last_folder_index = i
            elif first_file_index == -1:
                first_file_index = i
        
        # Linha apenas se houver ambos e estiverem em sequencia
        if last_folder_index != -1 and first_file_index != -1 and last_folder_index == first_file_index - 1:
            separator_pos = first_file_index
        else:
            separator_pos = -1
            
    for i, entry in enumerate(entries_filtered):
        if is_root and i == separator_pos:
             tree_str += "│\n"

        full_path = os.path.join(root_path, entry)
        connector = "└── " if i == entries_count - 1 else "├── "
        display_name = entry + "/" if os.path.isdir(full_path) else entry

        tree_str += f"{prefix}{connector}{display_name}\n"

        if os.path.isdir(full_path):
            extension_prefix = "    " if i == entries_count - 1 else "│   "
            tree_str += draw_tree(
                full_path,
                ignore_files=ignore_files,
                ignore_folders=ignore_folders,
                ignore_extensions=ignore_extensions,
                always_include=always_include,
                root_sort_key=root_sort_key,
                subdir_sort_key=subdir_sort_key,
                prefix=prefix + extension_prefix,
                is_root=False
            )

    return tree_str
