import json
from pathlib import Path
from collections import Counter
from zipfile import ZipFile
from itertools import chain


class MessageCounter:
    def __init__(self, data_files: list[Path], results_file: Path) -> None:
        self.data_files = data_files
        self.results_file = results_file
        self.master_count = {}

    @staticmethod
    def _format_string(string: str) -> str:
        return string.encode("iso-8859-1").decode("utf-8")

    @staticmethod
    def _is_flat_dict(dictionary: dict) -> bool:
        return isinstance(dictionary, dict) and not any(
            isinstance(value, dict) for value in dictionary.values()
        )

    @staticmethod
    def _sort_dict_descending_values(dictionary: dict) -> None:
        if MessageCounter._is_flat_dict(dictionary):
            sorted_dict = dict(dictionary.most_common())
            dictionary.clear()
            dictionary.update(sorted_dict)
            return

        for key, value in dictionary.items():
            if not isinstance(value, dict):
                continue
            MessageCounter._sort_dict_descending_values(dictionary[key])

    @staticmethod
    def _extract_and_delete_zip(zip_data_file: Path) -> None:
        extract_folder = zip_data_file.with_suffix("")
        extract_folder.mkdir(exist_ok=True)

        # Extract the contents of the zip file into the created folder
        with ZipFile(zip_data_file, "r") as zip_ref:
            zip_ref.extractall(extract_folder)

        # Delete the original zip file
        zip_data_file.unlink()

    def _process_message(self, message: dict) -> None:
        sender_name = self._format_string(message["sender_name"])
        self.conversation_count["messages"]["Total"] += 1
        self.conversation_count["messages"][sender_name] += 1

        if "content" in message:
            self.conversation_count["chars"]["Total"] += len(message["content"])
            self.conversation_count["chars"][sender_name] += len(message["content"])

        for reaction in message.get("reactions", []):
            actor = reaction["actor"]
            actor = self._format_string(actor)
            self.conversation_count["reactions"]["Total"] += 1
            self.conversation_count["reactions"][actor] += 1

        if "sticker" in message:
            self.conversation_count["stickers"]["Total"] += 1
            self.conversation_count["stickers"][sender_name] += 1

        if "photos" in message:
            self.conversation_count["photos"]["Total"] += len(message["photos"])
            self.conversation_count["photos"][sender_name] += len(message["photos"])

        if "videos" in message:
            self.conversation_count["videos"]["Total"] += len(message["videos"])
            self.conversation_count["videos"][sender_name] += len(message["videos"])

        if "files" in message:
            self.conversation_count["files"]["Total"] += len(message["files"])
            self.conversation_count["files"][sender_name] += len(message["files"])

        if "share" in message:
            self.conversation_count["shares"]["Total"] += 1
            self.conversation_count["shares"][sender_name] += 1

        if "call_duration" in message:
            self.conversation_count["calls"]["Total"] += 1
            self.conversation_count["calls"][sender_name] += 1

    def _process_messages(self, message_file: Path) -> None:
        with open(message_file, "r") as message_file:
            data = json.load(message_file)

        for message in data["messages"]:
            self._process_message(message)

    def _process_conversation(self, conversation_folder: Path) -> None:
        if not (conversation_folder / "message_1.json").exists():
            return  # no messages to process

        last_underscore_index = conversation_folder.name.rfind("_")
        if last_underscore_index == -1:
            return  # ignore names without "_" (from Facebook itself, not real users)

        conversation_name = conversation_folder.name[:last_underscore_index]
        if conversation_name.startswith("."):
            return  # miscellaneous file

        # handle duplicates
        if conversation_name in self.master_count:
            i = 1
            while f"{conversation_name}_{i}" in self.master_count:
                i += 1
            conversation_name += f"_{i}"

        self.master_count[conversation_name] = {
            "messages": Counter(),
            "chars": Counter(),
            "reactions": Counter(),
            "stickers": Counter(),
            "photos": Counter(),
            "videos": Counter(),
            "files": Counter(),
            "shares": Counter(),
            "calls": Counter(),
        }
        self.conversation_count = self.master_count[conversation_name]

        i = 1
        while (message_file := conversation_folder / f"message_{i}.json").exists():
            self._process_messages(message_file)
            i += 1

        # remove empty fields
        self.master_count[conversation_name] = {
            key: value
            for key, value in self.master_count[conversation_name].items()
            if value
        }

    def _process_file(self, data_file: Path) -> None:
        if data_file.name.startswith("."):
            return  # miscellaneous file

        if data_file.suffix.lower() == ".zip":
            self._extract_and_delete_zip(data_file)
            data_file = data_file.with_suffix("")

        inbox_path = data_file / "your_facebook_activity" / "messages" / "inbox"
        archived_path = data_file / "your_facebook_activity" / "messages" / "archived_threads"
        e2ee_cutover_path = data_file / "your_facebook_activity" / "messages" / "e2ee_cutover"

        for conversation_folder in chain(inbox_path.iterdir(), archived_path.iterdir(), e2ee_cutover_path.iterdir()):
            self._process_conversation(conversation_folder)

    def process_files(self) -> None:
        for data_file in self.data_files:
            self._process_file(data_file)

        # sort conversations alphabetically, then descending values
        self.master_count = dict(sorted(self.master_count.items()))
        self._sort_dict_descending_values(self.master_count)

        with open(self.results_file, "w") as output_file:
            json.dump(self.master_count, output_file, indent=4)
