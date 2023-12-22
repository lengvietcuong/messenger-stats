import json
from pathlib import Path
from emoji import emojize
from tabulate import tabulate


EMOJIS = {
    "account": emojize(":bust_in_silhouette:"),
    "messages": emojize(":speech_balloon:"),
    "chars": emojize(":information:"),
    "reactions": emojize(":smiling_face_with_heart-eyes:"),
    "stickers": emojize(":shooting_star:"),
    "photos": emojize(":framed_picture:"),
    "videos": emojize(":video_camera:"),
    "files": emojize(":file_folder:"),
    "shares": emojize(":link:"),
    "calls": emojize(":mobile_phone:"),
}


class DataViewer:
    def __init__(self, results_file: Path) -> None:
        self.results_file = results_file
        self._load_data()

    def _load_data(self) -> None:
        with open(self.results_file, "r") as results_file:
            self.data = json.load(results_file)
        self.conversation_names = list(self.data.keys())

    def print_conversation_names(self) -> None:
        print("Your conversations:")
        for i, conversation_name in enumerate(self.conversation_names, start=1):
            print(f"{i}. {conversation_name}")

    def get_conversation_name(self, key: str) -> str | None:
        if key.isnumeric():
            index = int(key) - 1
            if not 0 <= index <= len(self.conversation_names) - 1:
                print(f"Conversation number {key} not found.")
                return
            return self.conversation_names[index]

        if key not in self.data:
            print(f"Conversation '{key}' not found.")
            return
        return key

    def print_stats(self, conversation_name: str) -> None:
        print(f"\n{EMOJIS["account"]} {conversation_name}")
        for key, value in self.data[conversation_name].items():
            print(f"\n{EMOJIS[key]} {key}")
            print(tabulate(value.items(), tablefmt="fancy_grid"))
