
#  Copyright 2016 by Dai Trying
#
#  This file is part of daixmms2client.
#
#     daixmms2client is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     daixmms2client is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with daixmms2client.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
import xmmsclient
import subprocess
from xmmsclient import collections as c


def start_xmms2d():
    bash_command = "xmms2-launcher"
    os.system(bash_command)


def is_running(process):
    try:
        call = subprocess.check_output("pidof '{}'".format(process), shell=True)
        return True
    except subprocess.CalledProcessError:
        return False


if not is_running("xmms2d"):
    start_xmms2d()

xmms = xmmsclient.XMMS("DaiClient")
try:
    xmms.connect(os.getenv("XMMS_PATH"))
except IOError:
    sys.exit(99)


def xmms_play():
    """
    Plays the currently selected track
    :return: bool
    """
    result = xmms.playback_start()
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_pause():
    """
    Pauses the currently playing track
    :return: bool
    """
    result = xmms.playback_pause()
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_next():
    """
    Skips to the next track in playlist
    :return: bool
    """
    result = xmms.playlist_set_next_rel(1)
    result.wait()
    if result.is_error():
        if result.value() == "Can't set pos outside the current playlist!":
            return False
        else:
            return False
    result = xmms.playback_tickle()
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_prev():
    """
    Skips back to previous track in playlist
    :return: bool
    """
    result = xmms.playlist_set_next_rel(-1)
    result.wait()
    if result.is_error():
        if result.value() == "Can't set pos outside the current playlist!":
            return False
        else:
            return False
    result = xmms.playback_tickle()
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_stop():
    """
    Stops PLay back
    :return: bool
    """
    result = xmms.playback_stop()
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_shuffle():
    """
    Shuffles currently selected playlist
    :return: bool
    """
    result = xmms.playlist_shuffle()
    result.wait()
    if result.is_error():
        return False
    return True


# noinspection SpellCheckingInspection
def xmms_get_all_library_list():
    """
    Get full list of audio tracks from medialib
    :return: XmmsResult
    """
    # noinspection PyUnresolvedReferences
    ids = c.Match(field="id", value="*")
    result = xmms.coll_query_infos(ids, ["id", "artist", "title", "album", "genre", "bitrate", "performer",
                                         "duration", "timesplayed", "size", "partofset", "tracknr"])
    result.wait()
    if result.is_error():
        return False
    return result


def xmms_get_list_of_play_lists():
    """
    Get list of available play lists
    :return: XmmsResult or False on error
    """
    result = xmms.playlist_list()
    result.wait()
    if result.is_error():
        return False
    return result


def xmms_get_playlist_entries(playlist):
    """
    Get media lib id's for given playlist
    :param playlist: (str) playlist name
    :return: XmmsResult or False on error
    """
    result = xmms.playlist_list_entries(str(playlist))
    result.wait()
    if result.is_error():
        return False
    else:
        return result


def xmms_get_now_playing_entries():
    """
    Get media lib id's for currently playing playlist
    :return: XmmsResult of False on error
    """
    result = xmms.playlist_list_entries()
    result.wait()
    if result.is_error():
        return False
    return result


def xmms_get_now_playing_ml_id():
    """
    Get media lib id for currently playing track
    :return: (int) media lib id
    """
    result = xmms.playback_current_id()
    result.wait()
    if result.is_error():
        return False
    return result.value()


def xmms_get_play_status():
    """
    Get current playback status
    :return: XmmsResult (int)
    """
    result = xmms.playback_status()
    result.wait()
    if result.is_error():
        return False
    return result


def xmms_get_now_playing_pl_id():
    """
    Get current position of playlist
    :return: XmmsResult (int)
    """
    result = xmms.playlist_current_pos()
    result.wait()
    if result.is_error():
        return False
    return result


def xmms_remove_entry_from_now_playing_playlist(pl_row):
    """
    Remove entry from current playlist at given position
    :param pl_row: int
    :return: bool
    """
    result = xmms.playlist_remove_entry(pl_row)
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_remove_entry_from_playlist(pl_row, plist):
    """
    remove entry from given playlist at given position
    :param pl_row: int
    :param plist: str
    :return: bool
    """
    result = xmms.playlist_remove_entry(pl_row, playlist=plist)
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_move_playlist_entry(old, new, plist):
    """
    Move playlist entry from given position to given position in given playlist
    :param old: int
    :param new: int
    :param plist: str
    :return: bool
    """
    result = xmms.playlist_move(old, new, playlist=str(plist))
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_clear_playlist_tracks(play_list):
    """
    Clear all tracks in given playlist
    :param play_list: str
    :return: bool
    """
    result = xmms.playlist_clear(play_list)
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_create_playlist(pl_name):
    """
    Create new playlist
    :param pl_name: str
    :return: bool
    """
    result = xmms.playlist_create(str(pl_name))
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_delete_playlist(pl_name):
    """
    Delete playlist from media lib
    :param pl_name: str
    :return: bool
    """
    result = xmms.playlist_remove(pl_name)
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_get_media_lib_info_by_ml_id(ml_id):
    """
    Get track information from media lib for given media lib id
    :param ml_id: int
    :return: XmmsResult or False on error
    """
    result = xmms.medialib_get_info(ml_id)
    result.wait()
    if result.is_error():
        return False
    else:
        return result


def xmms_add_ml_id_to_playlist(ml_id, plist):
    """
    Add given media lib id to given playlist
    :param ml_id: int
    :param plist: str
    :return: bool
    """
    result = xmms.playlist_add_id(ml_id, str(plist))
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_jump_to_track(track):
    """
    Jump to given position in current playlist and start playback
    :param track: int
    :return: bool
    """
    result = xmms.playlist_set_next(track.row())
    result.wait()
    if result.is_error():
        if result.value() == "Can't set pos outside the current playlist!":
            return False
        else:
            return False
    result = xmms.playback_tickle()
    result.wait()
    if result.is_error():
        return False
    xmms_play()
    return True


def xmms_media_lib_remove_entry(ml_id):
    """
    Remove entry from media lib
    :param ml_id: int
    :return: bool
    """
    result = xmms.medialib_remove_entry(ml_id)
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_sort_playlist(pl_name, field):
    """
    Sort given playlist on given field
    :param pl_name: str
    :param field: str
    :return: bool
    """
    my_sort = (field, '')
    result = xmms.playlist_sort(my_sort, playlist=pl_name)
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_reverse_sort_playlist(pl_name, field):
    """
    Sort given playlist on given field in reverse order
    :param pl_name: str
    :param field: str
    :return: bool
    """
    my_sort = ("-" + field, '')
    result = xmms.playlist_sort(my_sort, playlist=pl_name)
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_import_file(filename):
    """
    Import given file to media lib
    :param filename: str (filename with full path)
    :return: bool
    """
    result = xmms.medialib_add_entry('file://' + filename)
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_import_path(file_path):
    """
    Import (recursively) all files from a given file path
    :param file_path: str
    :return: bool
    """
    result = xmms.medialib_import_path('file://' + file_path)
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_change_config_value(data, value):
    """
    Set given config value with given value
    :param data: str
    :param value: int
    :return: bool
    """
    result = xmms.config_set_value(data, str(value))
    result.wait()
    if result.is_error():
        return False
    return True


def xmms_get_config_value(data):
    """
    Retrieve config value for given config key
    :param data: str
    :return: int or False on error
    """
    result = xmms.config_get_value(data)
    result.wait()
    if result.is_error():
        return False
    return result.value()


def xmms_server_rehash(ml_id):
    result = xmms.medialib_rehash(ml_id)
    result.wait()
    if result.is_error():
        return False
    return True
