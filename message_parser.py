from vars import vars

def get_message_type(text):
    for cat in vars.cat_list:
        if cat in text:
            return vars.cat_str

    for girl in vars.girl_list:
        if girl in text:
            return vars.girl_str
    return vars.invalid_str