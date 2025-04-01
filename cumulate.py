import os
import json

def count_links(directory):
    winery_links_count = 0
    wine_links_count = 0

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r") as file:
                try:
                    data = json.load(file)
                    if "winery" in filename:
                        if isinstance(data, list):
                            winery_links_count += len(data)
                        elif isinstance(data, dict):
                            winery_links_count += sum(len(links) for links in data.values())
                    elif "wine" in filename:
                        if isinstance(data, list):
                            wine_links_count += len(data)
                        elif isinstance(data, dict):
                            wine_links_count += sum(len(links) for links in data.values())
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file: {filename}")

    return winery_links_count, wine_links_count

if __name__ == "__main__":
    directory = os.path.dirname(__file__)  # Current directory
    winery_count, wine_count = count_links(directory)
    print(f"Total winery links: {winery_count}")
    print(f"Total wine links: {wine_count}")
