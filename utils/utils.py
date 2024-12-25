def allowed_file(filename, exts):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in exts


def merge_complex(base, update):
    """
    Fusionne récursivement deux structures (dictionnaires ou listes).
    - Pour les dictionnaires, les clés communes sont fusionnées récursivement.
    - Pour les listes, les doublons sont supprimés.
    """
    if isinstance(base, dict) and isinstance(update, dict):
        # Fusionner les dictionnaires
        merged = base.copy()
        for key, value in update.items():
            if key in merged:
                merged[key] = merge_complex(merged[key], value)
            else:
                merged[key] = value
        return merged

    elif isinstance(base, list) and isinstance(update, list):
        # Fusionner les listes sans doublons
        return list({*base, *update})

    else:
        # Remplacer la valeur par celle d'update
        return update
