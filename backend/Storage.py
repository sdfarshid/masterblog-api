import json


def load_json_file() -> list:
    try:
        with open("./data/posts.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("File not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []



def write_file(data: list[dict]) -> bool:
    try:
        with open("./data/posts.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False
