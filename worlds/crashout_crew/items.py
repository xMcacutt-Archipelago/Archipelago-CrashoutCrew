import dataclasses
import enum
from math import ceil
from typing import ClassVar, Self

from BaseClasses import Item, ItemClassification

from .constants import *
from .world_base import CrashoutCrewWorldBase

class CrashoutCrewItem(Item):
    game: str = GAME_NAME

@dataclasses.dataclass(frozen=True)
class ItemData:
    item_name: str
    code: int
    classification: ItemClassification
    amount: int = 1

def get_item_with_right_classification(world: CrashoutCrewWorldBase, item_name: str) -> CrashoutCrewItem:
    """returns the item when provided the name"""
    filtered_item_list: list[CrashoutCrewItems] = [item for item in CrashoutCrewItems if item.item_name == item_name]
    # print(f"item_name: {item_name}")
    return CrashoutCrewItem(name=filtered_item_list[0].item_name, code=filtered_item_list[0].code, classification=filtered_item_list[0].classification, player=world.player)


def create_items(world: CrashoutCrewWorldBase) -> None:
    total_location_count = len(world.multiworld.get_unfilled_locations(world.player))
    for item in CrashoutCrewItems:
        if item.item_name not in world.items_created_dict.keys():
            world.items_created_dict[item.item_name] = 0

        contracts = world.options.two_order_contracts.value + world.options.three_order_contracts.value + world.options.four_order_contracts.value
        bells = contracts * SHIFTS_PER_CONTRACT
        if item.classification is ItemClassification.progression:
            if item.item_name == BELL_ITEM:
                for _ in range(bells):
                    world.multiworld.itempool.append(world.create_item(name=item.item_name))
                    world.items_created_dict[item.item_name] += 1
                    total_location_count -= 1
        if item.classification is ItemClassification.useful:
            for _ in range(item.amount):
                world.multiworld.itempool.append(world.create_item(name=item.item_name))
                world.items_created_dict[item.item_name] += 1
                total_location_count -= 1

    # print(f"filler to place: {total_location_count}")
    world.items_created_dict[world.player] = total_location_count
    for _ in range(total_location_count):
        world.multiworld.itempool.append(world.create_item(name=world.get_filler_item_name()))
        total_location_count -= 1

    # print(f"items_created_dict: {world.items_created_dict}")

class CrashoutCrewItems(enum.Enum):
    BELL = ItemData(item_name=BELL_ITEM, code=0x1, classification=ItemClassification.progression)
    BOOST = ItemData(item_name=SHOP_ITEM_BOOST, code=0x2, classification=ItemClassification.useful)
    CHARGE = ItemData(item_name=SHOP_ITEM_CHARGE, code=0x3, classification=ItemClassification.useful)
    BUTTON = ItemData(item_name=SHOP_ITEM_BUTTON, code=0x4, classification=ItemClassification.useful)
    EXTINGUISHER = ItemData(item_name=SHOP_ITEM_EXTINGUISHER, code=0x5, classification=ItemClassification.useful)
    SCRUB = ItemData(item_name=SHOP_ITEM_SCRUB, code=0x6, classification=ItemClassification.useful)
    SCRUBBIE = ItemData(item_name=SHOP_ITEM_SCRUBBIE, code=0x7, classification=ItemClassification.useful)
    SHELF = ItemData(item_name=SHOP_ITEM_SHELF, code=0x8, classification=ItemClassification.useful)
    SPRINKLER = ItemData(item_name=SHOP_ITEM_SPRINKLER, code=0x9, classification=ItemClassification.useful)
    STURDY = ItemData(item_name=SHOP_ITEM_STURDY, code=0xa, classification=ItemClassification.useful)
    TELE = ItemData(item_name=SHOP_ITEM_TELE, code=0xb, classification=ItemClassification.useful)
    TRASH = ItemData(item_name=SHOP_ITEM_TRASH, code=0xc, classification=ItemClassification.useful)
    VAC = ItemData(item_name=SHOP_ITEM_VAC, code=0xd, classification=ItemClassification.useful)
    LEAF = ItemData(item_name=SHOP_ITEM_LEAF, code=0xe, classification=ItemClassification.useful)
    XL_SPRINKLER = ItemData(item_name=SHOP_ITEM_XL_SPRINKLER, code=0xf, classification=ItemClassification.useful)
    WATER_BALLOON = ItemData(item_name=SHOP_ITEM_WATER_BALLOON, code=0x10, classification=ItemClassification.useful)
    WILD = ItemData(item_name=SHOP_ITEM_WILD, code=0x11, classification=ItemClassification.useful)
    NITRO = ItemData(item_name=SHOP_ITEM_NITRO, code=0x12, classification=ItemClassification.useful)
    AROMA = ItemData(item_name=SHOP_ITEM_AROMA, code=0x13, classification=ItemClassification.useful)
    DRIFT = ItemData(item_name=SHOP_ITEM_DRIFT, code=0x14, classification=ItemClassification.useful)
    SHIELD = ItemData(item_name=SHOP_ITEM_SHIELD, code=0x15, classification=ItemClassification.useful)
    CHAIN = ItemData(item_name=SHOP_ITEM_CHAIN, code=0x16, classification=ItemClassification.useful)
    CUP = ItemData(item_name=SHOP_ITEM_CUP, code=0x17, classification=ItemClassification.useful)
    FAN = ItemData(item_name=SHOP_ITEM_FAN, code=0x18, classification=ItemClassification.useful)
    GRIP = ItemData(item_name=SHOP_ITEM_GRIP, code=0x19, classification=ItemClassification.useful)
    SPOILER = ItemData(item_name=SHOP_ITEM_SPOILER, code=0x1a, classification=ItemClassification.useful)
    COSMETIC = ItemData(item_name=COSMETIC_ITEM, code=0x20, classification=ItemClassification.filler)
    UPGRADE_SPEED = ItemData(item_name=UPGRADE_ITEM_SPEED, code=0x30, classification=ItemClassification.useful, amount=3)
    UPGRADE_STRENGTH = ItemData(item_name=UPGRADE_ITEM_STRENGTH, code=0x31, classification=ItemClassification.useful, amount=3)
    UPGRADE_BOOST = ItemData(item_name=UPGRADE_ITEM_BOOST, code=0x32, classification=ItemClassification.useful, amount=3)
    UPGRADE_STRESS = ItemData(item_name=UPGRADE_ITEM_STRESS, code=0x33, classification=ItemClassification.useful, amount=3)
    #TRAP_ITEM = ItemData(item_name=TRAP_ITEM_NAME, code=0x200, classification=ItemClassification.trap)

    def __new__(cls, item_data: ItemData) -> Self:
        obj = object.__new__(cls)
        obj._value_ = item_data
        return obj

    def __init__(self, item_data: ItemData) -> None:
        self.item_name: str = item_data.item_name
        self.code: int = item_data.code
        self.classification: ItemClassification = item_data.classification
        self.amount: int = item_data.amount