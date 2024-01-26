from json import load

file_name = "./storage/data.json"


def load_data() -> dict:
    with open(file_name, "r") as fr:
        data = load(fr)
    return data

def view_json_file():
    if input("Confirm view message log (Y - yes, No - n): ").lower() == 'y':
        dict_messages = load_data()
        for time_message in dict_messages:
            print(f"Time - {time_message}."\
                  f" Username - {dict_messages[time_message]['username']},"\
                  f" message - {dict_messages[time_message]['message']}")
        print()

if __name__ == '__main__':
    view_json_file()