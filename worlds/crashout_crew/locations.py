import dataclasses

from BaseClasses import Location, LocationProgressType
from rule_builder.rules import Rule, True_
from .world_base import CrashoutCrewWorldBase
from .constants import DELIVERIES_PER_SHIFT, MAX_CONTRACTS, SHIFTS_PER_CONTRACT


@dataclasses.dataclass(frozen=True)
class LocationData:
    loc_name: str
    code: int | None
    region: str
    rule: Rule[CrashoutCrewWorldBase] = dataclasses.field(default_factory=True_[CrashoutCrewWorldBase])
    locked_item: str | None = None
    progress_type: LocationProgressType = LocationProgressType.DEFAULT


def generate_location_list() -> list[LocationData]:
    _location_data: list[LocationData] = []

    for contract_index in range(MAX_CONTRACTS):
        for shift_index in range(SHIFTS_PER_CONTRACT):
            for delivery_index in range(DELIVERIES_PER_SHIFT[shift_index]):
                loc_data: LocationData = LocationData(
                    loc_name=f"Contract {contract_index + 1} - Shift {shift_index + 1} - Delivery {delivery_index + 1}",
                    code = 0x30 * contract_index + 0x9 * shift_index + delivery_index + 2,
                    region = f"Contract {contract_index + 1} - Shift {shift_index + 1}",
                )
                _location_data.append(loc_data)
            loc_data: LocationData = LocationData(
                loc_name=f"Contract {contract_index + 1} - Shift {shift_index + 1}",
                code=0x30 * contract_index + 0x9 * shift_index + 1,
                region=f"Contract {contract_index + 1}",
            )
            _location_data.append(loc_data)

    return _location_data


FULL_LOCATION_LIST: list[LocationData] = generate_location_list()

