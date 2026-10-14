from typing import ClassVar

from BaseClasses import MultiWorld
from Options import PerGameCommonOptions
from worlds.AutoWorld import World

from .options import CrashoutCrewOptions

class CrashoutCrewWorldBase(World):
    options_dataclass: ClassVar[type[PerGameCommonOptions]] = CrashoutCrewOptions
    options: CrashoutCrewOptions  # pyright: ignore[reportIncompatibleVariableOverride]

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        super().__init__(multiworld=multiworld, player=player)
        self.plain_cell_count: int = 0
        self.other_cell_type_count: int = 0