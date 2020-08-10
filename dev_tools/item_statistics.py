import shutil

import numpy as np
from tqdm import tqdm

import module.config.server as server

<<<<<<< HEAD

server.server = 'en'  # Don't need to edit, it's used to avoid error.

print(os.getcwd())
=======
server.server = 'cn'  # Edit your server here.
>>>>>>> 20bfc4f8fc37908f15e5748fa538289e1ac74255

from module.logger import logger
from module.statistics.battle_status import BattleStatusStatistics
from module.statistics.get_items import GetItemsStatistics
from module.statistics.utils import *

<<<<<<< HEAD

"""
Set your folder here
Examples: xxx/campaign_7_2
"""
IMAGE_FOLDER = 'screenshots/xx'
STATUS_ITEMS_INTERVAL = 10
# 0.9 is sometimes unable to distinguish between equipment of different rarities
TEMPLATE_THRESHOLD = 0.95

BATTLE_STATUS_FOLDER = f'{IMAGE_FOLDER}/status'
GET_ITEMS_FOLDER = f'{IMAGE_FOLDER}/get_items'
TEMPLATE_FOLDER = f'{IMAGE_FOLDER}/item_template'
TEMPLATE_ARCHIVE_FOLDER = f'screenshots/item_template_archive'

for f_ in [TEMPLATE_FOLDER]:
    if not os.path.exists(f_):
        os.mkdir(f_)
BATTLE_STATUS_TIMESTAMP = np.array([int(f.split('.')[0]) for f in os.listdir(BATTLE_STATUS_FOLDER)])
ITEM_GRIDS_1_ODD = ButtonGrid(origin=(336, 298), delta=(128, 0), button_shape=(96, 96), grid_shape=(5, 1))
ITEM_GRIDS_1_EVEN = ButtonGrid(origin=(400, 298), delta=(128, 0), button_shape=(96, 96), grid_shape=(4, 1))
ITEM_GRIDS_2 = ButtonGrid(origin=(336, 227), delta=(128, 142), button_shape=(96, 96), grid_shape=(5, 2))
ENEMY_GENRE_BUTTON = Button(area=(782, 285, 961, 319), color=(), button=(), name='ENEMY_GENRE')




class AmountOcr(Ocr):
    def ocr(self, image):
        start_time = time.time()

        image_list = [self.pre_process(i) for i in image]
        result_list = self.cnocr.ocr_for_single_lines(image_list)
        result_list = [self.after_process(result) for result in result_list]

        if len(self.buttons) == 1:
            result_list = result_list[0]
        logger.attr(name='%s %ss' % (self.name, str(round(time.time() - start_time, 3)).ljust(5, '0')),
                    text=str(result_list))

        return result_list

    def after_process(self, raw):
=======
STATUS_ITEMS_INTERVAL = 10


class DropStatistics(BattleStatusStatistics, GetItemsStatistics):
    def __init__(self, folder):
>>>>>>> 20bfc4f8fc37908f15e5748fa538289e1ac74255
        """
        Args:
            folder (str): Such as <your_drop_screenshot_folder>/campaign_7_2
        """
<<<<<<< HEAD
        raw = super().after_process(raw)
        if not raw:
            result = 0
        else:
            result = int(raw)

        return result


AMOUNT_OCR = AmountOcr([], back=(-200, -200, -200), lang='digit', name='Amount_ocr')
ENEMY_GENRE_OCR = Ocr(ENEMY_GENRE_BUTTON, lang='cnocr', use_binary=False, back=(127, 127, 127))


class ImageError(Exception):
    pass


class ItemTemplate:
    def __init__(self, image):
        self.image = np.array(image)

    def match(self, image):
        res = cv2.matchTemplate(self.image, np.array(image), cv2.TM_CCOEFF_NORMED)
        _, similarity, _, _ = cv2.minMaxLoc(res)
        return similarity > TEMPLATE_THRESHOLD

    def save(self, name):
        image = Image.fromarray(self.image)
        image.save(f'{TEMPLATE_FOLDER}/{name}.png')

    def save_archive(self, name):
        image = Image.fromarray(self.image)
        image.save(f'{TEMPLATE_ARCHIVE_FOLDER}/{name}.png')

"""
Ideal workflow:
Run dev_tools/item_statistics on a directory. it generates templates and stores a copy
in both the map and in the archive

At your leisure, you can rename the templates in either directory.

On the next pass, the script scans for matching templates in both directories and
attempts to match the names accordingly.

Assumptions:
Templates are essentially unique.


Pseudocode:

instantiate map list and master list
    for each entry in map list:
        if name is int:
            check master list for match
            if match and match name is not int:
                use master name


for item in image:
    match item to map list
    if item in map list:
        if name is number:
            search master list

    if item not in map list:
        if item in master list:
            use master list name, duplicate entry in map list
        if item not in master list
            add new template (numbered) to both lists
"""

class ItemTemplateGroup:
    def __init__(self):
        # all templates
        self.templates_archive = {}
        # map templates
        self.templates = {}

        for file in os.listdir(TEMPLATE_ARCHIVE_FOLDER):
            name = file[:-4]
            image = Image.open(f'{TEMPLATE_ARCHIVE_FOLDER}/{file}').convert('RGB')
            self.templates_archive[name] = ItemTemplate(image)

        for file in os.listdir(TEMPLATE_FOLDER):
            name = file[:-4]
            image = Image.open(f'{TEMPLATE_FOLDER}/{file}').convert('RGB')
            self.templates[name] = ItemTemplate(image)

        # Ensures names match. If mismatched, resolve the mismatch
        for name, template in self.templates.items():
            for name_archive, template_archive in self.templates_archive.items():
                if template.match(template_archive.image) and name_archive != name:
                    logger.warning(f"template name mismatch between template collections")

                    # If both names mismatched and numeric/numeric or nonnumeric/nonnumeric,
                    # assign them a new numeric id.
                    if (name_archive.isdigit() and name.isdigit()) or (not name_archive.isdigit() and not name.isdigit()):
                        if (not name_archive.isdigit()) and (not name.isdigit()):
                            logger.warning(f"Identical template has different names, assigning new numeric ID")
                        if name_archive.isdigit() and name.isdigit():
                            logger.warning(f"Mismatched numeric IDs, assigning a new one")
                        os.remove(f'{TEMPLATE_FOLDER}/{name}.png')
                        os.remove(f'{TEMPLATE_ARCHIVE_FOLDER}/{name_archive}.png')
                        self.templates.pop(name)
                        self.templates_archive.pop(name_archive)

                        name = [int(n) for n in self.templates_archive.keys() if n.isdigit()]
                        if len(name):
                            name = str(max(name) + 1)
                        else:
                            name = str(len(self.templates.keys()) + 1)

                        logger.info(f'Generating replacement template: {name}')
                        self.templates[name] = template
                        self.templates_archive[name] = template

                        template.save(name)
                        template_archive.save_archive(name)


                    # Change the numeric name to the non-numeric one.
                    else:
                        if name.isdigit():
                            logger.info(f"renaming template in map directory: {name} -> {name_archive}")
                            os.remove(f'{TEMPLATE_FOLDER}/{name}.png')
                            self.templates.pop(name)
                            self.templates[name_archive] = template
                            template_archive.save(name_archive)
                        elif name_archive.isdigit():
                            logger.info(f"renaming template in archive: {name_archive} -> {name}")
                            os.remove(f'{TEMPLATE_ARCHIVE_FOLDER}/{name_archive}.png')
                            self.templates_archive.pop(name_archive)
                            self.templates_archive[name] = template
                            template.save_archive(name)
        # Ensures every template in the map folder also exists in the archive
        for name, template in self.templates.items():
            if name not in self.templates_archive.keys():
                logger.warning(f"map template {name} missing from archive! Added")
                template.save_archive(name)
    def match(self, item):
        for name, template in self.templates.items():
            if template.match(item.image):
                return name
        for name, template in self.templates_archive.items():
            if template.match(item.image):
                self.templates[name] = template
                template.save(name)
                return name

        template = ItemTemplate(item.get_template())
        name = [int(n) for n in self.templates_archive.keys() if n.isdigit()]
        if len(name):
            name = str(max(name) + 1)
        else:
            name = str(len(self.templates_archive.keys()) + 1)

        logger.info(f'New item template: {name}')
        self.templates[name] = template
        self.templates_archive[name] = template
        template.save(name)
        template.save_archive(name)
        return name



template_group = ItemTemplateGroup()


class Item:
    def __init__(self, image):
        self.image = image
        self.is_valid = np.mean(np.array(image.convert('L')) > 127) > 0.1
        self.name = 'Default_item'
        self.amount = 1
        if self.is_valid:
            self.name = template_group.match(self)
            if not self.name.startswith('_') and '_' in self.name:
                self.name = '_'.join(self.name.split('_')[:-1])

    def __str__(self):
        return f'{self.name}_x{self.amount}'

    @property
    def has_amount(self):
        return 'T' in self.name or self.name == '物资'
=======
        self.folder = folder
        self.template_folder = os.path.join(self.folder, 'item_template')
        if not os.path.exists(self.template_folder):
            shutil.copytree('./assets/stats_basic', self.template_folder)
        self.load_template_folder(self.template_folder)
        self.battle_status = load_folder(os.path.join(folder, 'status'))
        self.get_items = load_folder(os.path.join(folder, 'get_items'))
        self.battle_status_timestamp = np.array([int(f) for f in self.battle_status])

    def _items_to_status(self, get_items):
        """
        Args:
            get_items (str): get_items image filename.
>>>>>>> 20bfc4f8fc37908f15e5748fa538289e1ac74255

        Returns:
            str: battle_status image filename.
        """
        interval = np.abs(self.battle_status_timestamp - int(get_items))
        if np.min(interval) > STATUS_ITEMS_INTERVAL * 1000:
            raise ImageError(f'Timestamp: {get_items}, battle_status image not found.')
        return str(self.battle_status_timestamp[np.argmin(interval)])

    def extract_template(self, image=None, folder=None):
        """
        Extract and save new templates into 'item_template' folder.
        """
        for ts, file in tqdm(self.get_items.items()):
            try:
                image = load_image(file)
                super().extract_template(image, folder=self.template_folder)
            except:
                logger.warning(f'Error image: {ts}')

    def stat_drop(self, timestamp):
        """
        Args:
            timestamp (str): get_items image timestamp.

        Returns:
            list: Drop data.
        """
        get_items = load_image(self.get_items[timestamp])
        battle_status_timestamp = self._items_to_status(timestamp)
        battle_status = load_image(self.battle_status[battle_status_timestamp])

        enemy_name = self.stats_battle_status(battle_status)
        items = self.stats_get_items(get_items)
        data = [[timestamp, battle_status_timestamp, enemy_name, item.name, item.amount] for item in items]
        return data

    def generate_data(self):
        """
        Yields:
            list: Drop data.
        """
        for ts, file in tqdm(self.get_items.items()):
            try:
                data = self.stat_drop(ts)
                yield data
            except:
                logger.warning(f'Error image: {ts}')


"""
Args:
    FOLDER:   Alas drop screenshot folder.
              Examples: '<your_drop_screenshot_folder>/campaign_7_2'
    CSV_FILE: Csv file to save.
              Examples: 'c72.csv'
"""
<<<<<<< HEAD
# ts = 1593301640807
# items = Items(ts)
# for item in items.items:
#     print(item.amount, item.name)
=======
FOLDER = ''
CSV_FILE = ''
drop = DropStatistics(FOLDER)
>>>>>>> 20bfc4f8fc37908f15e5748fa538289e1ac74255

"""
First run:
    1. Uncomment this, and run.
    2. Rename templates in <your_drop_screenshot_folder>/campaign_7_2/item_template, for example.
"""
<<<<<<< HEAD
from tqdm import tqdm
for ts in tqdm([int(f.split('.')[0]) for f in os.listdir(GET_ITEMS_FOLDER)]):
    try:
        items = Items(ts)
    except Exception:
        logger.warning(f'Error image: {ts}')
        continue
=======
# drop.extract_template()
>>>>>>> 20bfc4f8fc37908f15e5748fa538289e1ac74255

"""
Second Run:
    1. Comment the code in first run.
    2. Uncomment this, and run.
"""
# import csv
# with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csv_file:
#     writer = csv.writer(csv_file)
#     for d in drop.generate_data():
#         writer.writerows(d)
