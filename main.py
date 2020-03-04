import argparse
from pathlib import Path

import yaml

from crawler.crawler import Crawler


def prepare_name(title):
    for c in '\/:*?"<>|':
        title = title.replace(c, '')
    return args.save_path / title


def get_arrgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Crawler')
    parser.add_argument('--path', type=Path, help='Path to yaml settings file', default='./settings.yaml')
    parser.add_argument('--save_path', type=Path, help='Path to yaml settings file', default='./result')
    parser.add_argument('--api_key', type=str, help='Google api token', default="AIzaSyA3xVLjVs1vad8HBv40t8QOvEGLdWKWpK4")
    parser.add_argument('--cse_id', type=str, help='Google Custom engine id', default="012485294846830293341:qaewpfzaaoq")
    return parser.parse_args()


if __name__ == '__main__':

    args = get_arrgs()
    assert args.path.is_file(), "File not found"
    with open(args.path) as settings_file:
        try:
            settings = yaml.load(settings_file, Loader=yaml.BaseLoader)
            search_string = settings["settings"]["search_string"]
            p_count = int(settings["settings"]["pages_count"])
        except:
            print("Not able to load settings")
            raise
    assert p_count > 0 and len(search_string) != 0, "Incorrect settings"
    assert p_count <= 10, "10 search results is limit for Google Custom engine"

    jsons = Crawler(search_string=search_string, p_count=p_count, api_key=args.api_key, cse_id=args.cse_id).process()

    for title, content in jsons:
        with open(prepare_name(title), "w+") as save_file:
            yaml.dump(content, save_file)
