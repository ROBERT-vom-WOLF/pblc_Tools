import os
import shutil
from src.logger import get_logger
from pathlib import Path


def get_parent_dir(path):
    return os.path.dirname(path)


class ReName:
    def __init__(self, season_folder_paths_dict):
        self.season_folder_paths_dict = season_folder_paths_dict
        self.log = get_logger(__name__, r"src\log_files\rename_log.log")  # nopep8
        self.new_folders = []  # stores the new paths of the season-folders to not remove them after

    def remove_directory(self, path):
        try:
            shutil.rmtree(path)
            self.log.debug(f"Directory removed successfully >>> {path}")
        except Exception as e:
            self.log.error(f"Error while removing dir {path}: {e}")
            exit(1)

    def safely_remove_folder(self, folder):
        # if the given folder is a folder that was used before by the rename, it doesn't remove it
        folder = os.path.normpath(folder)
        for new_folder in self.new_folders:
            if os.path.normpath(new_folder) == folder:
                return
        self.remove_directory(folder)

    def rename_files(self):
        old_folders = []  # stores the old paths of the season-folders to remove them after
        self.new_folders = []  # stores the new paths of the season-folders to not remove them after

        for season_index in self.season_folder_paths_dict.keys():

            episode_counter = {}  # creates for every season a counter (default = 0) that defined the episode number

            for season_folder_path in self.season_folder_paths_dict[season_index]:

                season_number = season_index

                self.log.debug(f"active season path >>> {season_folder_path}")

                if not os.path.isdir(season_folder_path):
                    return

                self.log.debug(f"valid Season found! >>> {season_number}")
                old_folders.append(season_folder_path)

                if season_number not in episode_counter:
                    episode_counter[season_number] = 0  # add season number to the episode counter
                    self.log.debug(f"Created episode counter for season >>> {season_number} >>> {episode_counter}")

                new_season_folder_name = f'Season {season_number:02d}'
                new_season_folder_path = os.path.join(get_parent_dir(season_folder_path), new_season_folder_name)
                self.new_folders.append(new_season_folder_path)
                os.makedirs(new_season_folder_path, exist_ok=True)   # creates new dir

                for episode_file in os.listdir(season_folder_path):

                    self.log.info(f"Episode-File: {episode_file}")

                    episode_counter[season_number] += 1
                    episode_number = episode_counter[season_number]

                    file_extension = os.path.splitext(episode_file)[1]
                    new_episode_name = f'{Path(get_parent_dir(season_folder_path)).name} - s{season_number:02d}e{episode_number:02d}{file_extension}'  # nopep8
                    os.rename(
                        os.path.join(season_folder_path, episode_file),
                        os.path.join(new_season_folder_path, new_episode_name)
                    )

        for old_folder in old_folders:
            self.safely_remove_folder(old_folder)

        self.log.info("success!")
        return "success!"
