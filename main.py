from pathlib import Path
from counter import MessageCounter
from viewer import DataViewer


def process_data(data_folder: Path, results_file: Path) -> None:
    data_files = list(data_folder.iterdir())
    if not data_files:
        raise FileNotFoundError(
            "No files found in the 'data' folder."
            "\nPlease move your downloaded data files into the 'data' folder and try again."
        )

    counter = MessageCounter(data_files, results_file)

    print(f"Processing data files...")
    counter.process_files()
    print("Processing completed!\n")


def main():
    results_file = Path(__file__).parent / "results.json"

    if not results_file.exists():  # have not processed data
        data_folder = Path(__file__).parent / "data"
        if not data_folder.exists():
            data_folder.mkdir()

        process_data(data_folder, results_file)

    viewer = DataViewer(results_file)
    viewer.print_conversation_names()

    while True:
        print("-" * 50)
        while not (
            conversation_name := viewer.get_conversation_name(
                input("\nEnter conversation (number or name): ")
            )
        ):
            pass
        viewer.print_stats(conversation_name)


if __name__ == "__main__":
    main()
