import argparse
from pathlib import Path

import yaml

from crawler.crawler import Crawler

if __name__ == '__main__':

    def get_arrgs() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Crawler')
        parser.add_argument('--path', type=Path, help='Path to yaml settings file', default='./settings.yaml')
        return parser.parse_args()


    args = get_arrgs()
    assert args.path.is_file(), "File not found"
    with open(args.path) as settings_file:
        try:
            settings = yaml.load(settings_file, Loader=yaml.BaseLoader)
            search_string = settings["settings"]["search_string"]
            p_count = int(settings["settings"]["pages_count"])
        except:
            raise "Not able to load settings"
    assert p_count > 0 and len(search_string) != 0, "Incorrect settings"

    crawler = Crawler(search_string=search_string)
    crawler.process()
