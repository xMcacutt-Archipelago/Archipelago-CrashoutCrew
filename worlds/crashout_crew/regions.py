from BaseClasses import Region, Location, Item, ItemClassification, Entrance
from rule_builder.rules import Rule, True_, Has
from . import SHIFTS_PER_CONTRACT
from .world_base import CrashoutCrewWorldBase
from .constants import BELL_ITEM


def create_region(world: CrashoutCrewWorldBase, region_name: str):
    region: Region = Region(name=region_name, player=world.player, multiworld=world.multiworld)
    for loc_data in world.location_list:
        if loc_data.region == region_name:
            location: Location = Location(name=loc_data.loc_name, player=world.player, address=loc_data.code, parent=region)
            world.set_rule(spot=location, rule=loc_data.rule)
            location.progress_type = loc_data.progress_type
            if loc_data.locked_item is not None:
                location.place_locked_item(Item(name=loc_data.locked_item, classification=ItemClassification.progression, code=None, player=world.player))
            region.locations.append(location)
    world.multiworld.regions.append(region)


def create_regions(world: CrashoutCrewWorldBase) -> None:
    create_region(world=world, region_name="Menu")
    contracts = world.options.two_order_contracts.value + world.options.three_order_contracts.value + world.options.four_order_contracts.value
    for contract in range(contracts):
        create_region(world=world, region_name=f"Contract {contract  + 1}")
        connect_region_to_region(world, "Menu", f"Contract {contract + 1}", Has(BELL_ITEM, 5 * contract))
        for shift in range(SHIFTS_PER_CONTRACT):
            create_region(world=world, region_name=f"Contract {contract + 1} - Shift {shift + 1}")
            connect_region_to_region(world, f"Contract {contract + 1}", f"Contract {contract + 1} - Shift {shift + 1}", rule=True_[CrashoutCrewWorldBase]())


def connect_region_to_region(world: CrashoutCrewWorldBase, source: str, target: str, rule: Rule[CrashoutCrewWorldBase]) -> None:
    source_region: Region = world.get_region(source)
    target_region: Region = world.get_region(target)
    entrance: Entrance = source_region.connect(connecting_region=target_region, name=f"{source} -> {target}")
    world.set_rule(spot=entrance, rule=rule)
