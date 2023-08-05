def handle_fields_special_chatacters(field: str) -> str:
    special_characters_map = {"-": "_"}
    if any(special_char in field for special_char in special_characters_map.keys()):
        # the name that the field has in the filesystem
        for special_char in special_characters_map.keys():
            field = field.replace(special_char, special_characters_map[special_char])
    return field
