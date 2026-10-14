import dataclasses
from typing import ClassVar

from Options import Range, OptionGroup, PerGameCommonOptions, Choice
from worlds.crashout_crew.constants import MAX_CONTRACTS


class TwoOrderContractsCount(Range):
    """
    How many contracts with two orders should be included
    """
    range_start = 0
    range_end = MAX_CONTRACTS / 5
    default = 3


class ThreeOrderContractsCount(Range):
    """
    How many contracts with three orders should be included
    """
    range_start = 0
    range_end = MAX_CONTRACTS / 5
    default = 3


class FourOrderContractsCount(Range):
    """
    How many contracts with four orders should be included
    """
    range_start = 0
    range_end = MAX_CONTRACTS / 5
    default = 3


crashout_crew_option_groups: list[OptionGroup] = \
[
    OptionGroup(
        "Contracts",
        [
            TwoOrderContractsCount,
            ThreeOrderContractsCount,
            FourOrderContractsCount
        ]
    ),
]

@dataclasses.dataclass
class CrashoutCrewOptions(PerGameCommonOptions):
    two_order_contracts: TwoOrderContractsCount
    three_order_contracts: ThreeOrderContractsCount
    four_order_contracts: FourOrderContractsCount