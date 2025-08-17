import ast
from card_handler import Card

def waves_parser(cards: dict[int, Card], decrypted: str) -> str:
    waves_str,_ = decrypted.split("&", 1)

    _, waves = waves_str.split("=", 1)

    waves = waves.replace('"w":', '')
    waves_list = ast.literal_eval(waves)

    floor_value = 1
    return_string = ""

    for wave in waves_list:
        # Ideally I don't print anything if drops are missing.
        return_string += f"Floor {floor_value} Drops\n"
        return_string += "\n"
        return_string += f"    Card Information \n\n"
        for monster in wave:
            if monster[3] > 0:
                return_string += f"    ID {cards[monster[3]].adjusted_id} Name {cards[monster[3]].name}\n\n"
        floor_value+=1
    
    return return_string