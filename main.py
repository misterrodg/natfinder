import json
import requests

NAT_BASE_URL = "https://www.notams.faa.gov/common/nat.html"

EASTBOUND_TRACK_IDS = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    # 'I' Is not used.
    "J",
    "K",
    "L",
    "M",
]

WESTBOUND_TRACK_IDS = [
    # 'O' Is not used.
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]


def to_json_file(json_data: dict, file_path: str):
    with open(file_path, "w") as json_file:
        json.dump(json_data, json_file)


def fetch_html_as_lines(url: str) -> list[str]:
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()


def search_in_lines(lines: list[str], search_strings: list[str]) -> list[str]:
    found_lines = []
    for line in lines:
        for string in search_strings:
            if line.startswith(f"{string} "):
                found_lines.append(line)
    return found_lines


def main() -> None:
    search_strings = EASTBOUND_TRACK_IDS + WESTBOUND_TRACK_IDS
    lines = fetch_html_as_lines(NAT_BASE_URL)
    found_lines = search_in_lines(lines, search_strings)
    result = []

    if len(found_lines) > 0:
        for line in found_lines:
            line_array = line.split(" ")
            nat_id = line_array[0]
            nat_points = line_array[1:]
            result.append({nat_id: nat_points})

    if len(result) > 0:
        json_dict = {"tracks": result}
        to_json_file(json_dict, "./data/tracks.json")


if __name__ == "__main__":
    main()
