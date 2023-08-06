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

from cli_chess.modules.token_manager import TokenManagerModel
from cli_chess.utils.config import LichessConfig
from berserk.exceptions import BerserkError
from berserk import clients
from os import remove
from unittest.mock import Mock
import pytest


@pytest.fixture
def model_listener():
    return Mock()


@pytest.fixture
def model(model_listener: Mock, lichess_config: LichessConfig, monkeypatch):
    monkeypatch.setattr('cli_chess.modules.token_manager.token_manager_model.lichess_config', lichess_config)
    monkeypatch.setattr('cli_chess.modules.token_manager.token_manager_model._start_api', Mock())
    model = TokenManagerModel()
    model.e_token_manager_model_updated.add_listener(model_listener)
    return model


@pytest.fixture
def lichess_config():
    lichess_config = LichessConfig("unit_test_config.ini")
    yield lichess_config
    remove(lichess_config.full_filename)


def mock_fail_test_tokens(*args): # noqa
    raise BerserkError


def mock_success_test_tokens(*args): # noqa
    return {
        'lip_validToken': {
            'scopes': 'board:play,challenge:read,challenge:write',
            'userId': 'testUser',
            'expires': None
        }
    }


def test_validate_existing_linked_account(model: TokenManagerModel, lichess_config: LichessConfig, model_listener: Mock, monkeypatch):
    # Test with empty API token and username
    lichess_config.set_value(lichess_config.Keys.API_TOKEN, "")
    lichess_config.set_value(lichess_config.Keys.USERNAME, "")
    model.validate_existing_linked_account()
    assert lichess_config.get_value(lichess_config.Keys.API_TOKEN) == ""
    assert lichess_config.get_value(lichess_config.Keys.USERNAME) == ""

    # Test with existing username but missing API token
    lichess_config.set_value(lichess_config.Keys.USERNAME, "testUser")
    lichess_config.set_value(lichess_config.Keys.API_TOKEN, "")
    model.validate_existing_linked_account()
    assert lichess_config.get_value(lichess_config.Keys.API_TOKEN) == ""
    assert lichess_config.get_value(lichess_config.Keys.USERNAME) == ""

    # Test with invalid existing API token
    monkeypatch.setattr(clients.OAuth, "test_tokens", mock_fail_test_tokens)
    lichess_config.set_value(lichess_config.Keys.API_TOKEN, "lip_badToken")
    lichess_config.set_value(lichess_config.Keys.USERNAME, "testUser")
    model.validate_existing_linked_account()
    assert lichess_config.get_value(lichess_config.Keys.API_TOKEN) == ""
    assert lichess_config.get_value(lichess_config.Keys.USERNAME) == ""

    # Test with valid existing API token but missing username
    monkeypatch.setattr(clients.OAuth, "test_tokens", mock_success_test_tokens)
    lichess_config.set_value(lichess_config.Keys.API_TOKEN, "lip_validToken")
    lichess_config.set_value(lichess_config.Keys.USERNAME, "")
    model.validate_existing_linked_account()
    assert lichess_config.get_value(lichess_config.Keys.API_TOKEN) == "lip_validToken"
    assert lichess_config.get_value(lichess_config.Keys.USERNAME) == "testUser"

    # Test with valid API token and username
    monkeypatch.setattr(clients.OAuth, "test_tokens", mock_success_test_tokens)
    lichess_config.set_value(lichess_config.Keys.API_TOKEN, "lip_validToken")
    lichess_config.set_value(lichess_config.Keys.USERNAME, "testUser")
    model.validate_existing_linked_account()
    assert lichess_config.get_value(lichess_config.Keys.API_TOKEN) == "lip_validToken"
    assert lichess_config.get_value(lichess_config.Keys.USERNAME) == "testUser"

    # Verify model listener is called
    model_listener.reset_mock()
    model.validate_existing_linked_account()
    model_listener.assert_called()


def test_update_linked_account(model: TokenManagerModel, lichess_config: LichessConfig, model_listener: Mock, monkeypatch):
    # Test with empty api token
    assert not model.update_linked_account(api_token="")
    model_listener.assert_not_called()

    # Test a mocked invalid lichess api token and
    # verify existing user account data is not overwritten
    monkeypatch.setattr(clients.OAuth, "test_tokens", mock_fail_test_tokens)
    lichess_config.set_value(lichess_config.Keys.API_TOKEN, "lip_validToken")
    lichess_config.set_value(lichess_config.Keys.USERNAME, "testUser")
    assert not model.update_linked_account(api_token="lip_badToken")
    assert lichess_config.get_value(lichess_config.Keys.API_TOKEN) == "lip_validToken"
    assert lichess_config.get_value(lichess_config.Keys.USERNAME) == "testUser"
    model_listener.assert_not_called()

    # Test a mocked valid lichess api token
    monkeypatch.setattr(clients.OAuth, "test_tokens", mock_success_test_tokens)
    lichess_config.set_value(lichess_config.Keys.API_TOKEN, "")
    lichess_config.set_value(lichess_config.Keys.USERNAME, "")
    assert model.update_linked_account(api_token="lip_validToken")
    assert lichess_config.get_value(lichess_config.Keys.API_TOKEN) == "lip_validToken"
    assert lichess_config.get_value(lichess_config.Keys.USERNAME) == "testUser"
    model_listener.assert_called()


def test_save_account_data(model: TokenManagerModel, lichess_config: LichessConfig, model_listener: Mock):
    assert lichess_config.get_value(lichess_config.Keys.API_TOKEN) == ""
    assert lichess_config.get_value(lichess_config.Keys.USERNAME) == ""
    model_listener.assert_not_called()

    model.save_account_data(api_token="  lip_validToken  ", username="testUser")
    assert lichess_config.get_value(lichess_config.Keys.API_TOKEN) == "lip_validToken"
    assert lichess_config.get_value(lichess_config.Keys.USERNAME) == "testUser"
    model_listener.assert_called()


def test_get_linked_account_name(model: TokenManagerModel, lichess_config: LichessConfig):
    assert lichess_config.get_value(lichess_config.Keys.USERNAME) == ""
    assert model.get_linked_account_name() == ""

    lichess_config.set_value(lichess_config.Keys.USERNAME, "testUser  ")
    assert model.get_linked_account_name() == "testUser"


def test_notify_token_manager_model_updated(model: TokenManagerModel, model_listener: Mock):
    # Test registered successful move listener is called
    model._notify_token_manager_model_updated()
    model_listener.assert_called()

    # Unregister listener and test it's not called
    model_listener.reset_mock()
    model.e_token_manager_model_updated.remove_listener(model_listener)
    model._notify_token_manager_model_updated()
    model_listener.assert_not_called()
