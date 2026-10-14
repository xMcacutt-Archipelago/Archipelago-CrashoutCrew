from typing import ClassVar, override, Mapping, Any

from BaseClasses import MultiWorld, ItemClassification, CollectionState, Region, Item
from rule_builder.rules import Has, CanReachLocation

from .constants import GAME_NAME, SHIFTS_PER_CONTRACT, DELIVERIES_PER_SHIFT
from .items import CrashoutCrewItem, get_item_with_right_classification, CrashoutCrewItems, create_items
from .locations import LocationData, generate_location_list, FULL_LOCATION_LIST
from .options import CrashoutCrewOptions
from .regions import create_regions
from .world_base import CrashoutCrewWorldBase


class CrashoutCrewWorld(CrashoutCrewWorldBase):
    """
    Work together in online co-op with up to 4 players to fulfill orders of increasingly chaotic, physics-based boxes.
    Time is money, and safety is no concern… just try not to crash out!
    """
    game: ClassVar[str] = GAME_NAME
    # item_name_groups = item_name_groups
    # location_name_groups = location_name_groups
    item_name_to_id: ClassVar[dict[str, int]] = {item.item_name: item.code for item in CrashoutCrewItems}
    location_name_to_id: ClassVar[dict[str, int]] = {loc_data.loc_name: loc_data.code for loc_data in FULL_LOCATION_LIST if loc_data.code is not None}
    topology_present: bool = True


    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

        self.location_list: list[LocationData] = []
        self.items_created_dict: dict[str, int] = {}


    @override
    def get_filler_item_name(self) -> str:
        return self.random.choice([item.item_name for item in CrashoutCrewItems if item.classification is ItemClassification.filler])


    @override
    def create_item(self, name: str) -> CrashoutCrewItem:
        return get_item_with_right_classification(world=self, item_name=name)


    def generate_early(self) -> None:
        super().generate_early()
        self.location_list = generate_location_list()
        contracts = self.options.two_order_contracts.value + self.options.three_order_contracts.value + self.options.four_order_contracts.value
        if contracts == 0:
            self.options.two_order_contracts.value = 1


    def create_regions(self) -> None:
        create_regions(world=self)
        contracts = self.options.two_order_contracts.value + self.options.three_order_contracts.value + self.options.four_order_contracts.value
        self.set_completion_rule(CanReachLocation(location_name=f"Contract {contracts} - Shift {SHIFTS_PER_CONTRACT} - Delivery {DELIVERIES_PER_SHIFT[len(DELIVERIES_PER_SHIFT) - 1]}"))


    def create_items(self) -> None:
        create_items(world=self)


    def fill_slot_data(self) -> Mapping[str, Any]:
        # self.make_puml()
        return \
        {
            "TwoOrderContracts": self.options.two_order_contracts.value,
            "ThreeOrderContracts": self.options.three_order_contracts.value,
            "FourOrderContracts": self.options.four_order_contracts.value,
        }


    def make_puml(self) -> None:
        if self.player_name[0:1].isdigit():
            return

        from Utils import visualize_regions
        temp_state: CollectionState = self.multiworld.get_all_state()
        temp_state.update_reachable_regions(self.player)

        reachable_regions: set[Region] = set(temp_state.reachable_regions[self.player])
        unreachable_regions: set[Region] = set()
        for region in self.multiworld.regions:
            if region not in reachable_regions:
                unreachable_regions.add(region)

        visualize_regions(self.get_region(self.origin_region_name), f"{self.player_name}_world.puml", show_entrance_names=True, regions_to_highlight=unreachable_regions)
