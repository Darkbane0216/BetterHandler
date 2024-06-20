import json
import os


def load_rise_data(json_file_path):
    if os.path.isfile(json_file_path):
        with open(json_file_path, 'r') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None
    else:
        print(f"Error: The file '{json_file_path}' does not exist.")
        return None


def format_weaknesses(weaknesses):
    formatted_weaknesses = []
    for weakness in weaknesses:
        condition = weakness.get("condition", "")
        stars = weakness.get("stars", 0)
        star_str = "*" * stars
        if condition and stars != 0:
            formatted_weaknesses.append(f"{weakness['element'].upper()} ({condition}) - {star_str}")
        elif stars != 0:
            formatted_weaknesses.append(f"{weakness['element'].upper()} - {star_str}")
    return " \n ".join(formatted_weaknesses)


def format_resistances(resistances):
    formatted_resistances = []
    for resistance in resistances:
        formatted_resistances.append(f"{resistance['element'].upper()}")
    return " \n ".join(formatted_resistances)


def search_rise_db(name, data):
    results = []
    for monster in data:
        if name.lower() in monster.get("name", "").lower():
            formatted_monster = {
                "name": monster.get("name", "N/A"),
                "weaknesses": format_weaknesses(monster.get("weaknesses", [])),
                "resistances": format_resistances(monster.get("resistances", []))
            }
            results.append(formatted_monster)
    return results
