import csv
import os
from pathlib import Path
from typing import Union


def read_list_from_csv(csv_path: Union[Path, str]) -> list[str]:
    """this csv no title and contain only 1 column"""
    csv_list = []
    with open(csv_path, 'r', encoding='utf-8') as csv_f:
        csv_reader = csv.reader(csv_f)
        for row in csv_reader:
            csv_list.append(row[0])

    return csv_list

def list_file_type_in_dir(dir: Path, file_type_list: list[str], recur: bool = True) -> list[str]:
    rest_raw_file_list = os.listdir(dir)
    video_list = []

    while rest_raw_file_list:
        file = rest_raw_file_list.pop()

        if os.path.isdir(dir / file) and recur:
            rest_raw_file_list.extend(
                [f'{file}\{sub_file}' for sub_file in os.listdir(dir / file)]
            )
        else:
            for f_type in file_type_list:
                if file.endswith(f_type):
                    video_list.append(file)
                    break

    return video_list

def file_belong_to_which_company(file_name: str, company_list: list[str]) -> str:
    for com in company_list:
        if com in file_name:
            return com
        
    return ''

def recognize_company_in_video_name(company_list: list[str], video_name: str) -> str:
    for com in company_list:
        if com in video_name:
            return video_name
    return ''


COMPANY_CSV_PATH = './h_video_company.csv'
class HVideoManager:
    COMPANY_LIST = read_list_from_csv(COMPANY_CSV_PATH)
    VIDEO_TYPE_LIST = ['mp4', 'mkv']
    UNCATEGORIZED_DIR = 'uncategorized'

    def __init__(self, from_dir: Union[Path, str] = '', to_dir: Union[Path, str] = '') -> None:
        self._from_dir_path = Path(from_dir) if isinstance(from_dir, str) else from_dir
        self._to_dir_path = Path(to_dir) if isinstance(to_dir, str) else to_dir

        if not os.path.isdir(self._from_dir_path):
            raise ImportError(f'{self._from_dir_path} is not directory')
        if not os.path.isdir(self._to_dir_path):
            raise ImportError(f'{self._to_dir_path} is not directory') 
        
        print(f'Classify h-video from {self._from_dir_path} to {self._to_dir_path}')

    def classify(self) -> None:
        video_list = list_file_type_in_dir(dir=self._from_dir_path, file_type_list=self.VIDEO_TYPE_LIST)

        if not os.path.isdir(self._to_dir_path / self.UNCATEGORIZED_DIR):
            os.mkdir(self._to_dir_path / self.UNCATEGORIZED_DIR)
        
        for video in video_list[:30]:
            video_name = os.path.basename(video)
            
            old_path = self._from_dir_path / video
            new_path = self._to_dir_path / self.UNCATEGORIZED_DIR / video_name

            company = recognize_company_in_video_name(company_list=self.COMPANY_LIST, file_name=video_name)
            if company:
                os.path.isdir(self._to_dir_path / company) or os.mkdir(self._to_dir_path / company)
                new_path = self._to_dir_path / company / video_name

            os.rename(old_path, new_path)
            print(f'Move {old_path} to {new_path}')

