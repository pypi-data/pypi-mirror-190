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
from cli_chess.modules.board import BoardView
from cli_chess.modules.common import get_piece_unicode_symbol
from cli_chess.utils.config import board_config
import chess
from typing import List, Dict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.board import BoardModel


class BoardPresenter:
    def __init__(self, model: BoardModel) -> None:
        self.model = model
        self.board_config_values = board_config.get_all_values()
        self.view = BoardView(self, self.get_board_display())

        self.model.e_board_model_updated.add_listener(self.update)
        board_config.e_board_config_updated.add_listener(self._update_cached_config_values)

    def update(self, **kwargs) -> None: # noqa
        """Updates the board output"""
        # TODO: Update this so the view utilizes a lambda pointing to the presenter?
        #       This would allow for this update function to be removed
        self.view.update(self.get_board_display())

    def _update_cached_config_values(self):
        """Updates the 'board_config_values' variable with the
           latest configuration values from the board_config. Additionally,
           this will notify the board_view to update as there has been a change.
           This function is called automatically on board config updates
        """
        self.board_config_values = board_config.get_all_values()
        self.update()

    def make_move(self, move: str, human=True) -> None:
        """Sends a move to the board model to attempt to make.
           Raises an exception on invalid moves
        """
        try:
            self.model.make_move(move, human=human)
        except Exception as e:
            # TODO: Handle specific exceptions (Invalid move, ambiguous, etc )
            raise e

    def get_board_display(self) -> List[Dict]:
        """Returns a list containing the complete board display. Each item in the list
           is a dictionary containing the display data for that square (piece at,
           piece color, square color, square number, etc). This data is generally sent
           to the view to output the board display.
        """
        board_output = []
        board_squares = self.model.get_board_squares()

        # TODO: Update this implementation to use a dictionary so
        #       the following syntax can be used: board_output[chess.D2]?
        for square in board_squares:
            data = {'square_number': square,
                    'piece_str': self.get_piece_str(square),
                    'piece_display_color': self.get_piece_display_color(self.model.board.piece_at(square)),
                    'square_display_color': self.get_square_display_color(square),
                    'rank_label': self.get_rank_label(square),
                    'is_end_of_rank': self.is_square_end_of_rank(square)}
            board_output.append(data)

        return board_output

    def get_file_labels(self) -> str:
        """Returns a string containing the file labels. An empty
           string will be returned if showing the board coordinates
           is disabled in the configuration.
        """
        file_labels = ""
        show_board_coordinates = self.board_config_values[board_config.Keys.SHOW_BOARD_COORDINATES.value["name"]]

        if show_board_coordinates:
            file_labels = self.model.get_file_labels()

        return file_labels

    def get_file_label_color(self) -> str:
        """Returns the color to use for the file labels"""
        return self.board_config_values[board_config.Keys.FILE_LABEL_COLOR.value["name"]]

    def get_rank_label_color(self) -> str:
        """Returns the color to use for the rank labels"""
        return self.board_config_values[board_config.Keys.RANK_LABEL_COLOR.value["name"]]

    def get_rank_label(self, square: chess.Square) -> str:
        """Returns a label string if at the start of a rank
           otherwise an empty string will be returned
        """
        rank_label = ""
        rank_index = self.model.get_square_rank_index(square)
        show_board_coordinates = self.board_config_values[board_config.Keys.SHOW_BOARD_COORDINATES.value["name"]]

        if self.is_square_start_of_rank(square) and show_board_coordinates:
            rank_label = self.model.get_rank_label(rank_index)

        return rank_label

    def is_square_start_of_rank(self, square: chess.Square) -> bool:
        """Returns True if the square passed in is the start of a rank"""
        is_start_of_rank = False

        if self.model.is_white_orientation() and chess.BB_SQUARES[square] & chess.BB_FILE_A:
            is_start_of_rank = True
        elif not self.model.is_white_orientation() and chess.BB_SQUARES[square] & chess.BB_FILE_H:
            is_start_of_rank = True

        return is_start_of_rank

    def is_square_end_of_rank(self, square: chess.Square) -> bool:
        """Returns True if the square passed in is the last on the rank"""
        is_end_of_rank = False

        if self.model.is_white_orientation() and chess.BB_SQUARES[square] & chess.BB_FILE_H:
            is_end_of_rank = True
        elif not self.model.is_white_orientation() and chess.BB_SQUARES[square] & chess.BB_FILE_A:
            is_end_of_rank = True

        return is_end_of_rank

    def get_piece_str(self, square: chess.Square):
        """Returns the piece at the square as a string. Depending on configuration
           settings, this could be a unicode character, a letter, or an empty
           string if blindfold chess is enabled in the configuration, or there is
           not a piece at the square
        """
        piece = self.model.board.piece_at(square)
        piece_str = ""

        blindfold_chess = self.board_config_values[board_config.Keys.BLINDFOLD_CHESS.value["name"]]
        use_unicode_pieces = self.board_config_values[board_config.Keys.USE_UNICODE_PIECES.value["name"]]

        if piece and not blindfold_chess:
            piece_str = get_piece_unicode_symbol(piece.symbol()) if use_unicode_pieces else piece.symbol().upper()

        return piece_str

    def get_piece_display_color(self, piece: chess.Piece) -> str:
        """Returns a string with the color to display the
           piece based on configuration settings
        """
        piece_color = ""

        if piece:
            piece_is_light = True if piece.color else False
            if piece_is_light:
                piece_color = self.board_config_values[board_config.Keys.LIGHT_PIECE_COLOR.value["name"]]
            else:
                piece_color = self.board_config_values[board_config.Keys.DARK_PIECE_COLOR.value["name"]]

        return piece_color

    def get_square_display_color(self, square: chess.Square) -> str:
        """Returns a string with the color to display the
           square based on configuration settings, last move, and check.
        """
        if self.model.is_light_square(square):
            square_color = self.board_config_values[board_config.Keys.LIGHT_SQUARE_COLOR.value["name"]]
        else:
            square_color = self.board_config_values[board_config.Keys.DARK_SQUARE_COLOR.value["name"]]

        show_board_highlights = self.board_config_values[board_config.Keys.SHOW_BOARD_HIGHLIGHTS.value["name"]]
        if show_board_highlights:
            try:
                last_move = self.model.get_highlight_move()
                if bool(last_move) and (square == last_move.to_square or square == last_move.from_square):
                    square_color = self.board_config_values[board_config.Keys.LAST_MOVE_COLOR.value["name"]]
                    # TODO: Lighten last move square color if on light square
            except IndexError:
                pass

            if self.model.is_square_in_check(square):
                square_color = self.board_config_values[board_config.Keys.IN_CHECK_COLOR.value["name"]]

        return square_color

    def game_result(self) -> str:
        """Returns a string containing the result of the game"""
        game_result = self.model.board.result()
        is_checkmate = self.model.board.is_checkmate()
        output = ""

        if is_checkmate:
            output = "Checkmate - "
        if game_result == "1-0":
            output += "White is victorious"
        elif game_result == "0-1":
            output += "Black is victorious"
        elif game_result == "1/2-1/2":
            if self.model.board.is_stalemate():
                output = "Stalemate"
            else:
                output = "Draw"
        elif game_result == "*":
            output = "Draw"

        return output
