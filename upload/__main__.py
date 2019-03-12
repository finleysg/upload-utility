import argparse
import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

url = "https://mpgagolf.pythonanywhere.com/api/photos/"
token = ""


def send_file(file_path, year, tournament_id, tournament, course):
    file_name = os.path.basename(file_path)
    m = MultipartEncoder(
        fields={
            "photo_type": "Tournament Photos",
            "tournament": tournament_id,
            "year": year,
            "created_by": "admin",
            "caption": "",
            "tags": "{}|{}|{}".format(year, tournament, course),
            "raw_image": (file_name, open(file_path, "rb"), "image/jpeg")
        }
    )
    headers = {"Authorization": "Token {}".format(token), "Content-Type": m.content_type}
    return requests.post(url, data=m, headers=headers)
    # return m.to_string()


def process_files(folder):
    tags = os.path.split(folder)[1].split("-")
    year = tags[0]
    tournament_id = tags[1]
    tournament = tags[2].replace('_', ' ')
    course = tags[3].replace('_', ' ')
    for file in os.listdir(folder):
        print(send_file("{}\\{}".format(folder, file), year, tournament_id, tournament, course))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload all the images in a given folder")
    parser.add_argument("--folder", metavar="folder_name", required=True,
                        help="the name of the folder")
    args = parser.parse_args()
    process_files(args.folder)
