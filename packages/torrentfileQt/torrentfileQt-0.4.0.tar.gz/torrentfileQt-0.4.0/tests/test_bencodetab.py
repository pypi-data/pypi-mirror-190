#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################################################################
# Copyright 2020 AlexPDev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################
"""Module for testing procedures on Bencode editor module."""

import os

import pytest

from tests import (MockEvent, switchTab, temp_file, torrent_versions, waitfor,
                   wind)
from torrentfileQt import bencodeTab


class MockReturn:
    """Mock class for testing."""

    value = None


def mock_func(_):
    """Mock function for testing."""
    return MockReturn.value


bencodeTab.browse_folder = mock_func
bencodeTab.browse_torrent = mock_func


def test_fix():
    """Fix pytest warnings."""
    assert wind


@pytest.fixture(params=torrent_versions())
def torrent_file(request: object) -> str:
    """Function fixture for test suite."""
    size = 28
    path = temp_file(size)
    maker = request.param
    outfile = path + ".torrent"
    torrent = maker(
        path=path,
        announce=["url1", "url2"],
        source="source",
        piece_length=2**19,
        outfile=outfile,
    )
    torrent.write()
    return outfile


def test_bencode_load_file(wind, torrent_file):
    """Test bencode tab widget functions."""
    widget = wind.tabs.bencodeEditWidget
    switchTab(wind.stack, widget=widget)
    MockReturn.value = torrent_file
    widget.load_file()
    model = widget.treeview.model()
    assert waitfor(3, lambda: model.rowCount() > 0)
    assert widget.clear_contents()


def test_bencode_load_folder(wind, torrent_file):
    """Test bencode tab widget functions."""
    widget = wind.tabs.bencodeEditWidget
    switchTab(wind.stack, widget=widget)
    MockReturn.value = os.path.dirname(torrent_file)
    widget.load_folder()
    model = widget.treeview.model()
    assert waitfor(3, lambda: model.rowCount() > 0)
    assert widget.clear_contents()


def test_bencode_drag_enter_event(wind, torrent_file):
    """Test bencode tab widget functions."""
    widget = wind.tabs.bencodeEditWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(torrent_file)
    assert widget.dragEnterEvent(event)


def test_bencode_drag_enter_no_event(wind):
    """Test bencode tab widget functions."""
    widget = wind.tabs.bencodeEditWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(None)
    assert not widget.dragEnterEvent(event)


def test_bencode_drag_move_event(wind, torrent_file):
    """Test bencode tab widget functions."""
    widget = wind.tabs.bencodeEditWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(torrent_file)
    assert widget.dragMoveEvent(event)


def test_bencode_drag_move_no_event(wind):
    """Test bencode tab widget functions."""
    widget = wind.tabs.bencodeEditWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(None)
    assert not widget.dragMoveEvent(event)


def test_bencode_drop_event(wind, torrent_file):
    """Test bencode tab widget functions."""
    widget = wind.tabs.bencodeEditWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(torrent_file)
    assert widget.dropEvent(event)


def test_bencode_drop_no_event(wind):
    """Test bencode tab widget functions."""
    widget = wind.tabs.bencodeEditWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(None)
    assert not widget.dropEvent(event)


def test_bencode_thread(wind, torrent_file):
    """Test bencode tab widget functions."""
    widget = wind.tabs.bencodeEditWidget
    switchTab(wind.stack, widget=widget)
    bencodeTab.Thread.start = bencodeTab.Thread.run
    widget.load_thread([torrent_file])
    assert widget.treeview.rowCount() > 0
    model = widget.treeview.model()
    tree = widget.treeview
    topindex = model.index(0, 0)
    topitem = model.itemFromIndex(topindex)
    child_index = model.index(0, 0, parent=topindex)
    rect = widget.treeview.visualRect(child_index)
    widget.treeview.setSelection(rect,
                                 tree.selectionModel().SelectionFlag.Select)
    widget.insert_view_item()
    model.insertRow(0, child_index)
    model.removeRows(0, 4, child_index)
    topitem.setIcon(model.data_icon)
    model.setData(child_index, "newdata")
    widget.remove_view_item()
    widget.save_action.trigger()
    assert waitfor(3, lambda: widget.treeview.rowCount() > 0)
    assert widget.clear_contents()
