# Copyright (C) 2021-2023 Trevor Bayless <trevorbayless1@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations
from cli_chess.modules.material_difference import MaterialDifferenceView
from cli_chess.modules.common import get_piece_unicode_symbol
from cli_chess.utils.config import board_config
from chess import Color, PIECE_TYPES, PIECE_SYMBOLS, KING
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.material_difference import MaterialDifferenceModel


class MaterialDifferencePresenter:
    def __init__(self, model: MaterialDifferenceModel):
        self.model = model
        self.show_diff = self.model.board_model.get_variant_name() != "horde"

        orientation = self.model.get_board_orientation()
        self.view_upper = MaterialDifferenceView(self, self.format_diff_output(not orientation), self.show_diff)
        self.view_lower = MaterialDifferenceView(self, self.format_diff_output(orientation), self.show_diff)

        self.model.e_material_difference_model_updated.add_listener(self.update)
        board_config.e_board_config_updated.add_listener(self.update)

    def update(self) -> None:
        """Updates the material differences for both sides"""
        orientation = self.model.get_board_orientation()
        self.view_upper.update(self.format_diff_output(not orientation))
        self.view_lower.update(self.format_diff_output(orientation))

    def format_diff_output(self, color: Color) -> str:
        """Returns the formatted difference of the color passed in as a string"""
        output = ""
        material_difference = self.model.get_material_difference(color)
        score = self.model.get_score(color)
        use_unicode = board_config.get_boolean(board_config.Keys.USE_UNICODE_PIECES)

        for piece_type in PIECE_TYPES:
            for count in range(material_difference[piece_type]):
                symbol = get_piece_unicode_symbol(PIECE_SYMBOLS[piece_type]) if use_unicode else PIECE_SYMBOLS[piece_type].upper()
                output = symbol + output if piece_type != KING else output + symbol  # Add king to end for 3check

        if score > 0:
            output += f"+{score}"

        return output
