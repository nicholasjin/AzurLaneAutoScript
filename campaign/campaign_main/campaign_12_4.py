from module.campaign.campaign_base import CampaignBase
from module.map.map_base import CampaignMap
from module.map.map_grids import SelectedGrids, RoadGrids
from module.logger import logger


MAP = CampaignMap('12-4')
MAP.shape = 'K8'
MAP.map_data = '''
    MB MB ME -- ME ++ ++ ++ MB MB ++
    ME ++ -- ME -- MA ++ ++ ME ME ++
    -- ME -- ME ME -- ME ME -- ME --
    ++ -- ME ++ ++ ME ME -- ++ ++ ME
    ++ ME ME -- ME ME -- ME -- ++ --
    ++ -- ME ME -- ME ME ++ -- -- ME
    ME -- ME -- ME -- ME -- -- ME --
    -- -- -- ME SP SP ++ ++ ++ ME --
'''
MAP.weight_data = '''
    10 10 10 10 10 10 10 10 10 10 10
    10 10 10 10 10 10 10 10 10 10 10
    10 10 10 10 10 10 10 10 10 10 10
    10 10 10 10 10 10 10 10 10 10 20
    10 10 10 10 10 10 10 10 10 10 20
    10 10 10 10 10 10 10 10 10 10 10
    10 10 10 10 10 10 10 10 10 10 10
    10 10 10 10 10 10 10 10 10 10 10
'''
MAP.camera_data = ['D3', 'D6', 'H3', 'H6']
MAP.spawn_data = [
    {'battle': 0, 'enemy': 2},
    {'battle': 1, 'enemy': 2},
    {'battle': 2, 'enemy': 2},
    {'battle': 3, 'enemy': 1},
    {'battle': 4, 'enemy': 1},
    {'battle': 5},
    {'battle': 6, 'boss': 1},
]
# MAP.in_map_swipe_preset_data = (2, 1)

A1, B1, C1, D1, E1, F1, G1, H1, I1, J1, K1, \
A2, B2, C2, D2, E2, F2, G2, H2, I2, J2, K2, \
A3, B3, C3, D3, E3, F3, G3, H3, I3, J3, K3, \
A4, B4, C4, D4, E4, F4, G4, H4, I4, J4, K4, \
A5, B5, C5, D5, E5, F5, G5, H5, I5, J5, K5, \
A6, B6, C6, D6, E6, F6, G6, H6, I6, J6, K6, \
A7, B7, C7, D7, E7, F7, G7, H7, I7, J7, K7, \
A8, B8, C8, D8, E8, F8, G8, H8, I8, J8, K8, \
    = MAP.flatten()

# ROAD_MAIN = RoadGrids([[B6, C5]])

road_main = RoadGrids([[B6, C5]])

class Config:
    INTERNAL_LINES_FIND_PEAKS_PARAMETERS = {
        'height': (120, 255 - 40),
        'width': 2,
        'prominence': 10,
        'distance': 35,
    }


class Campaign(CampaignBase):
    MAP = MAP

    def battle_0(self):
        if self.battle_count > 3:
            self.pick_up_ammo()

        if self.clear_roadblocks([road_main]):
            return True
        if self.clear_potential_roadblocks([road_main]):
            return True
        return self.battle_default()

    # def battle_2(self):
    #     self.pick_up_ammo()
    #     if self.clear_roadblocks([road_main]):
    #         return True
    #     if self.clear_potential_roadblocks([road_main]):
    #         return True
    #     return self.battle_default()

    def battle_3(self):
        self.pick_up_ammo()
        if self.clear_roadblocks([road_main]):
            return True
        if self.clear_potential_roadblocks([road_main]):
            return True
        return self.battle_default()

    def battle_4(self):
        if self.clear_roadblocks([road_main]):
            return True
        if self.clear_potential_roadblocks([road_main]):
            return True
        return self.battle_default()

    def battle_6(self):

        boss = self.map.select(is_boss=True)
        if boss:
            if not self.check_accessibility(boss[0], fleet='boss'):
                if self.clear_roadblocks([road_main]):
                    return True

        return self.fleet_boss.clear_boss()
