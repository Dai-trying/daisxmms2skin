#!/usr/bin/env python3

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
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with daixmms2client. If not, see <http://www.gnu.org/licenses/>.

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMenu, QDialog, QMessageBox)
from PyQt5 import QtCore
from PyQt5.QtGui import (QIcon, QPixmap)
import my_base
import my_func
import eq_func
import xmmsfun
from connector import XMMSConnector
from copy import deepcopy
import os
import urllib

# noinspection PyUnresolvedReferences
import resource_rc
from urllib.parse import urlparse


class EditId3Tag(QDialog, my_base.Ui_EditId3Info):
    def __init__(self, parent, data, genres):
        super(EditId3Tag, self).__init__(parent)
        self.data = data
        self.genres = genres
        self.setupUi(self)
        self.ml_id_label.setText("Media Library Id " + str(self.data['id']))
        self.title_lineEdit.setText(self.data['title'])
        self.artist_lineEdit.setText(self.data['artist'])
        self.track_spinBox.setValue(self.data['tracknr'])
        self.album_lineEdit.setText(self.data['album'])
        self.disc_spinBox.setValue(self.data['partofset'])
        self.performer_lineEdit.setText(self.data['performer'])
        self.genre_combo.insertItem(0, "")
        for item in self.genres:
            self.genre_combo.addItem(item)
        self.genre_combo.setCurrentText(self.data['genre'])

    def get_values(self):
        return {'performer': self.performer_lineEdit.text(), 'partofset': self.disc_spinBox.text(),
                'genre': self.genre_combo.currentText(), 'id': self.data['id'], 'album': self.album_lineEdit.text(),
                'title': self.title_lineEdit.text(), 'artist': self.artist_lineEdit.text(),
                'tracknr': self.track_spinBox.text()}


class PlaylistChoose(QDialog, my_base.UiChoose):
    def __init__(self, parent, data):
        super(PlaylistChoose, self).__init__(parent)
        self.data = data
        self.set_up_ui(self)
        a = 0
        self.playlist_choice.insertItem(a, "")
        a += 1
        for item in self.data:
            if item.startswith("_") or item == "Default":
                pass
            else:
                self.playlist_choice.insertItem(a, item)
                a += 1

    def get_values(self):
        return self.playlist_choice.currentText()


class DaiClient(QMainWindow, my_base.UiMainWindow):

    def __init__(self, parent=None):
        super(DaiClient, self).__init__(parent)
        self.VERSION = "0.2-1"
        self.setup_ui(self)
        self.My_Library = []
        self.Play_Lists = []
        self.Now_Playing = ""
        self.added_ml_ids = []
        self.changed_ml_ids = []
        self.my_props = ["id", "tracknr", "album", "partofset", "title", "artist", "genre", "performer", "duration",
                         "timesplayed", "bitrate", "size"]
        self.genre_list = ["Blues", "Classic Rock", "Country", "Dance", "Disco", "Funk", "Grunge", "Hip-Hop", "Jazz",
                           "Metal", "New Age", "Oldies", "Other", "Pop", "R&B", "Rap", "Reggae", "Rock", "Techno",
                           "Industrial", "Alternative", "Ska", "Death Metal", "Pranks", "Soundtrack", "Euro-Techno",
                           "Ambient", "Trip-Hop", "Vocal", "Jazz+Funk", "Fusion", "Trance", "Classical", "Instrumental",
                           "Acid", "House", "Game", "Sound Clip", "Gospel", "Noise", "Alt. Rock", "Bass", "Soul",
                           "Punk", "Space", "Meditative", "Instrumental Pop", "Instrumental Rock", "Ethnic", "Gothic",
                           "Darkwave", "Techno-Industrial", "Electronic", "Pop-Folk", "Eurodance", "Dream",
                           "Southern Rock", "Comedy", "Cult", "Gangsta Rap", "Top 40", "Christian Rap", "Pop/Funk",
                           "Jungle", "Native American", "Cabaret", "New Wave", "Psychedelic", "Rave", "Showtunes",
                           "Trailer", "Lo-Fi", "Tribal", "Acid Punk", "Acid Jazz", "Polka", "Retro", "Musical",
                           "Rock & Roll", "Hard Rock", "Folk", "Folk-Rock", "National Folk", "Swing", "Fast-Fusion",
                           "Bebop", "Latin", "Revival", "Celtic", "Bluegrass", "Avantgarde", "Gothic Rock",
                           "Progressive Rock", "Psychedelic Rock", "Symphonic Rock", "Slow Rock", "Big Band", "Chorus",
                           "Easy Listening", "Acoustic", "Humour", "Speech", "Chanson", "Opera", "Chamber Music",
                           "Sonata", "Symphony", "Booty Bass", "Primus", "Porn Groove", "Satire", "Slow Jam", "Club",
                           "Tango", "Samba", "Folklore", "Ballad", "Power Ballad", "Rhythmic Soul", "Freestyle", "Duet",
                           "Punk Rock", "Drum Solo", "A Cappella", "Euro-House", "Dance Hall", "Goa", "Drum & Bass",
                           "Club-House", "Hardcore", "Terror", "Indie", "BritPop", "Afro-Punk", "Polsk Punk", "Beat",
                           "Christian Gangsta Rap", "Heavy Metal", "Black Metal", "Crossover", "Contemporary Christian",
                           "Christian Rock", "Merengue", "Salsa", "Thrash Metal", "Anime", "JPop", "Synthpop",
                           "Abstract", "Art Rock", "Baroque", "Bhangra", "Big Beat", "Breakbeat", "Chillout",
                           "Downtempo", "Dub", "EBM", "Eclectic", "Electro", "Electroclash", "Emo", "Experimental",
                           "Garage", "Global", "IDM", "Illbient", "Industro-Goth", "Jam Band", "Krautrock", "Leftfield",
                           "Lounge", "Math Rock", "New Romantic", "Nu-Breakz", "Post-Punk", "Post-Rock", "Psytrance",
                           "Shoegaze", "Space Rock", "Trop Rock", "World Music", "Neoclassical", "Audiobook",
                           "Audio Theatre", "Neue Deutsche Welle", "Podcast", "Indie Rock", "G-Funk", "Dubstep",
                           "Garage Rock", "Psybient", "Unknown"]
        self.xmms = xmmsfun.xmms
        XMMSConnector(self.xmms)
        self.reader_status = "Available"
        eq_func.myself = self
        self.home()
        my_func.load_media_to_library(self)
        my_func.load_play_lists(self)
        my_func.load_now_playing(self)
        my_func.first_set_now_stuff(self)
        my_func.set_play_status(self)
        self.tab_change()
        self.tabWidget.removeTab(self.tabWidget.indexOf(self.tabSettings))
        my_func.load_config_data(self)
        eq_func.set_eq_disabled()

    def home(self):
        self.xmms.broadcast_collection_changed(self.bc_col_ch)
        self.xmms.broadcast_config_value_changed(self.bc_cnf_vl_ch)
        self.xmms.broadcast_mediainfo_reader_status(self.bc_mi_rd_st)
        self.xmms.broadcast_medialib_entry_added(self.bc_ml_en_ad)
        self.xmms.broadcast_medialib_entry_changed(self.bc_ml_en_ch)
        self.xmms.broadcast_playback_current_id(self.bc_pb_cu_id)
        self.xmms.broadcast_playback_status(self.bc_pb_st)
        self.xmms.broadcast_playback_volume_changed(self.bc_pb_vo_ch)
        self.xmms.broadcast_playlist_changed(self.bc_pl_ch)
        self.xmms.broadcast_playlist_current_pos(self.bc_pl_cu_ps)
        self.xmms.broadcast_playlist_loaded(self.bc_pl_ld)
        self.xmms.signal_playback_playtime(self.set_progress)

        self.combo_pl_names.currentIndexChanged.connect(self.pl_entries_reload)

        self.toolPrevious.clicked.connect(xmmsfun.xmms_prev)
        self.toolPause.clicked.connect(xmmsfun.xmms_pause)
        self.toolPlay.clicked.connect(xmmsfun.xmms_play)
        self.toolNext.clicked.connect(xmmsfun.xmms_next)
        self.toolStop.clicked.connect(xmmsfun.xmms_stop)
        self.toolShuffle.clicked.connect(xmmsfun.xmms_shuffle)
        self.toolEject.clicked.connect(self.clear_playlist_contents)
        self.toolDelete.clicked.connect(self.delete_playlist)
        self.toolSettings.clicked.connect(self.settings_tab_activated)
        self.btn_ok.clicked.connect(self.save_settings)
        self.btn_cancel.clicked.connect(self.cancel_settings)

        self.table_pl_entries.__class__.dropEvent = self.my_drag_n_drop_event
        self.tabWidget.currentChanged.connect(self.tab_change)
        self.tableNowPlaying.doubleClicked.connect(xmmsfun.xmms_jump_to_track)
        self.tableMediaLibrary.doubleClicked.connect(self.edit_id3_tag)
        self.tableMediaLibrary.customContextMenuRequested.connect(self.open_ml_menu)
        self.combo_pl_names.customContextMenuRequested.connect(self.open_pl_menu)
        self.table_pl_entries.horizontalHeader().setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table_pl_entries.horizontalHeader().customContextMenuRequested.connect(self.pl_header_menu)

        for slide in eq_func.sliders:
            this_ref = eval("self." + slide + "_slider")
            this_ref.valueChanged.connect(self.handle_sliders)

        self.enable_button.released.connect(eq_func.toggle_equalizer)
        self.xmms.configval_list(self.handle_config_val_list)

    def handle_sliders(self, val):
        var_to_set = "equalizer." + self.sender().objectName()
        if xmmsfun.xmms_change_config_value(var_to_set, str(val / 10.0)):
            ref = eval("self." + self.sender().objectName() + "_label")
            ref.setText(str(val / 10.0))

    def edit_id3_tag(self, song):

        ml_id = self.tableMediaLibrary.item(song.row(), 0).text()
        track_info = my_func.get_info_by_ml_id(self, int(ml_id))

        dlg = EditId3Tag(self, track_info, sorted(self.genre_list, key=lambda s: s.lower()))
        if dlg.exec_():
            value = dlg.get_values()

            file_info = my_func.get_xmms_db_info(int(ml_id))
            file_with_path = file_info.value()['url'].replace("file://", "")
            test_file_name = urllib.parse.unquote_plus(file_with_path)
            test_file_name2 = urllib.parse.unquote(test_file_name)

            if os.path.isfile(test_file_name2):
                if my_func.set_id3_tag(test_file_name2, value) is False:
                    QMessageBox.information(self, 'FILE PERMISSION ERROR', "I cannot write the information to the file,"
                                                                           "\nit is likely that I do not have "
                                                                           "sufficient priviliges.")
            else:
                QMessageBox.information(self, 'FILE NAME ERROR', "I cannot write the information to the file,\nit may "
                                                                 "contain characters that are not readable to me.")

    def handle_config_val_list(self, val):
        chained = False
        dict_val = val.value()
        order = 0
        for key in dict_val:
            if key.startswith("effect.order"):
                if dict_val[key] == "equalizer":
                    chained = True
                elif len(dict_val[key]) == 0:
                    pass
                else:
                    order += 1
        if not chained:
            val = "effect.order.%d" % order
            self.xmms.configval_set(val, "equalizer")

    def save_settings(self):
        self.toolSettings.setDisabled(False)
        self.tabWidget.removeTab(self.tabWidget.indexOf(self.tabSettings))
        my_func.save_config_data(self)

    def cancel_settings(self):
        self.toolSettings.setDisabled(False)
        self.tabWidget.removeTab(self.tabWidget.indexOf(self.tabSettings))
        my_func.load_config_data(self)

    def settings_tab_activated(self):
        self.toolSettings.setDisabled(True)
        self.tabWidget.addTab(self.tabSettings, "Settings")
        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.tabSettings))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            if self.tabWidget.currentWidget().objectName() == "tabNp":
                my_func.remove_entry_from_now_playing(self)
            elif self.tabWidget.currentWidget().objectName() == "tabPl":
                my_func.remove_entry_from_playlist(self)
        event.accept()

    def pl_header_menu(self, position):
        if len(self.combo_pl_names) <= 0:
            return
        menu = QMenu()
        ascending = menu.addAction("Sort Ascending")
        pl_icon_ascending = QIcon()
        pl_icon_ascending.addPixmap(QPixmap(":/icons/sort-ascending.png"), QIcon.Normal, QIcon.Off)
        ascending.setIcon(pl_icon_ascending)
        descending = menu.addAction("Sort Descending")
        pl_icon_descending = QIcon()
        pl_icon_descending.addPixmap(QPixmap(":/icons/sort-descending.png"), QIcon.Normal, QIcon.Off)
        descending.setIcon(pl_icon_descending)
        action = menu.exec_(self.combo_pl_names.mapToGlobal(position))
        if action == ascending:
            col = self.my_props[self.table_pl_entries.columnAt(position.x())]
            xmmsfun.xmms_sort_playlist(self.combo_pl_names.currentText(), col)
        elif action == descending:
            col = self.my_props[self.table_pl_entries.columnAt(position.x())]
            xmmsfun.xmms_reverse_sort_playlist(self.combo_pl_names.currentText(), col)

    def get_playlist(self):
        all_pls = []
        for pl in self.Play_Lists:
            if pl['Name'].startswith("_") or pl['Name'] == "Default":
                pass
            else:
                all_pls.append(pl['Name'])
        dlg = PlaylistChoose(self, sorted(all_pls, key=lambda s: s.lower()))
        if dlg.exec_():
            value = dlg.get_values()
            if value != "":
                return value
        return False

    def open_pl_menu(self, position):
        menu = QMenu()
        # if len(self.combo_pl_names) > 0:
        play_now = menu.addAction("Play this playlist now")
        pl_now_icon = QIcon()
        pl_now_icon.addPixmap(QPixmap(":icons/play.png"), QIcon.Normal, QIcon.Off)
        play_now.setIcon(pl_now_icon)
        add_to_current = menu.addAction("Add this playlist to Now Playing")
        add_curr_icon = QIcon()
        add_curr_icon.addPixmap(QPixmap(":icons/add.png"), QIcon.Normal, QIcon.Off)
        add_to_current.setIcon(add_curr_icon)
        new_playlist = menu.addAction("Add New Playlist")
        new_pl_icon = QIcon()
        new_pl_icon.addPixmap(QPixmap(":icons/playlist_add.png"), QIcon.Normal, QIcon.Off)
        new_playlist.setIcon(new_pl_icon)
        create_from_albums = menu.addAction("Create play lists from Album names")
        create_icon = QIcon()
        create_icon.addPixmap(QPixmap(":icons/book_cd.png"), QIcon.Normal, QIcon.Off)
        create_from_albums.setIcon(create_icon)
        if len(self.combo_pl_names) <= 0:
            play_now.setEnabled(False)
            add_to_current.setEnabled(False)
        action = menu.exec_(self.combo_pl_names.mapToGlobal(position))
        if action == play_now:
            my_func.play_list_now(self)
        if action == add_to_current:
            my_func.add_play_list_to_now(self)
        if action == new_playlist:
            my_func.add_new_playlist(self)
        if action == create_from_albums:
            my_func.make_playlists_from_albums(self)

    def open_ml_menu(self, position):
        menu = QMenu()
        import_files = menu.addAction("Import files to Library")
        imp_f_icon = QIcon()
        imp_f_icon.addPixmap(QPixmap(":icons/audio.png"), QIcon.Normal, QIcon.Off)
        import_files.setIcon(imp_f_icon)
        import_dirs = menu.addAction("Import directory to Library")
        imp_d_icon = QIcon()
        imp_d_icon.addPixmap(QPixmap(":icons/folder.png"), QIcon.Normal, QIcon.Off)
        import_dirs.setIcon(imp_d_icon)
        remove_from_library = menu.addAction("Remove tracks from Library")
        rem_icon = QIcon()
        rem_icon.addPixmap(QPixmap(":icons/remove.png"), QIcon.Normal, QIcon.Off)
        remove_from_library.setIcon(rem_icon)
        menu.addSeparator()
        add_to_now_playing_action = menu.addAction("Add selection to Now Playing")
        add_np_icon = QIcon()
        add_np_icon.addPixmap(QPixmap(":icons/add.png"), QIcon.Normal, QIcon.Off)
        add_to_now_playing_action.setIcon(add_np_icon)
        replace_now_playing_with_selection_action = menu.addAction("Replace Now Playing with selection")
        replace_now_playing_with_selection_action.setIcon(add_np_icon)
        menu.addSeparator()
        add_to_existing_play_list_action = menu.addAction("Add To Existing Playlist")
        add_pl_icon = QIcon()
        add_pl_icon.addPixmap(QPixmap(":icons/playlist.png"), QIcon.Normal, QIcon.Off)
        add_to_existing_play_list_action.setIcon(add_pl_icon)
        add_to_new_play_list_action = menu.addAction("Add To NEW Playlist")
        new_pl_icon = QIcon()
        new_pl_icon.addPixmap(QPixmap(":icons/playlist_add.png"), QIcon.Normal, QIcon.Off)
        add_to_new_play_list_action.setIcon(new_pl_icon)

        if len(self.changed_ml_ids) > 0:
            update_media_library = menu.addAction("Update with " + str(len(self.changed_ml_ids)) + " changed entries")
        if len(self.combo_pl_names) <= 0:
            add_to_existing_play_list_action.setEnabled(False)
        action = menu.exec_(self.tableMediaLibrary.mapToGlobal(position))
        if action == add_to_existing_play_list_action:
            pl_name = self.get_playlist()
            if pl_name is not False:
                my_func.ml_selection_to_play_list(self, pl_name)
        elif action == add_to_new_play_list_action:
            pl_name = my_func.add_new_playlist(self)
            if pl_name is not False:
                my_func.ml_selection_to_play_list(self, pl_name)
        elif action == add_to_now_playing_action:
            my_func.ml_selection_to_now_playing(self)
        elif action == replace_now_playing_with_selection_action:
            my_func.ml_selection_replace_now_playing(self)
        elif action == import_files:
            my_func.import_files(self)
        elif action == import_dirs:
            my_func.import_directory(self)
        elif action == remove_from_library:
            id_list = my_func.get_ml_selection(self)
            if my_func.check_now_playing_contains(id_list):
                # noinspection PyTypeChecker,PyCallByClass,PyArgumentList
                QMessageBox.warning(self, "Cannot do that!", "Cannot remove files that are in the current playlist")
            else:
                # noinspection PyTypeChecker,PyCallByClass
                reply = QMessageBox.question(self, 'Message', "Are you sure to remove the " +
                                             str(len(id_list)) + " selected tracks?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    my_func.remove_ml_id_list_from_library(self, id_list)
        try:
            # noinspection PyUnboundLocalVariable
            if action == update_media_library:
                my_func.update_the_library(self)
        except UnboundLocalError:
            pass

    def my_drag_n_drop_event(self, event):
        if event.source().objectName() == "table_pl_entries":
            pl_name = self.combo_pl_names.currentText()
        elif event.source().objectName() == "tableNowPlaying":
            pl_name = "Default"
        if event.source().rowAt(event.pos().y()) == -1:
            return
        if event.source().objectName() == "table_pl_entries" or event.source().objectName() == "tableNowPlaying":
            # noinspection PyUnboundLocalVariable
            xmmsfun.xmms_move_playlist_entry(event.source().currentRow(), event.source().rowAt(event.pos().y()),
                                             pl_name)

    def tab_change(self):
        if self.tabWidget.currentWidget().objectName() == "tabNp":
            self.toolEject.setDisabled(False)
            self.toolShuffle.setDisabled(False)
            self.toolDelete.setDisabled(True)
        elif self.tabWidget.currentWidget().objectName() == "tabPl":
            self.toolEject.setDisabled(False)
            self.toolShuffle.setDisabled(True)
            self.toolDelete.setDisabled(False)
        elif self.tabWidget.currentWidget().objectName() == "tabMl":
            self.toolEject.setDisabled(True)
            self.toolShuffle.setDisabled(True)
            self.toolDelete.setDisabled(True)
        elif self.tabWidget.currentWidget().objectName() == "tabSettings":
            self.toolEject.setDisabled(True)
            self.toolShuffle.setDisabled(True)
            self.toolDelete.setDisabled(True)

    def clear_playlist_contents(self):
        if self.tabWidget.currentWidget().objectName() == "tabNp":
            xmmsfun.xmms_clear_playlist_tracks("Default")
        elif self.tabWidget.currentWidget().objectName() == "tabPl":
            pl_name = self.combo_pl_names.currentText()
            if pl_name != "":
                xmmsfun.xmms_clear_playlist_tracks(pl_name)

    def delete_playlist(self):
        pl_name = self.combo_pl_names.currentText()
        xmmsfun.xmms_delete_playlist(pl_name)

    def set_progress(self, info):
        my_func.set_pb(self, info)
        pass

    def pl_entries_reload(self):
        my_func.load_pl_entries_table(self)

    def bc_col_ch(self, result):
        my_func.collection_changed(self, result)

    def bc_cnf_vl_ch(self, result):
        pass

    def bc_mi_rd_st(self, result):
        if result.value() == 1:
            self.reader_status = "Busy"
        elif result.value() == 0:
            self.reader_status = "Available"
            my_func.update_new_changed_ml_id_list(self, deepcopy(self.changed_ml_ids))

    def bc_ml_en_ad(self, result):
        if my_func.is_in_library(self, result.value()):
            pass
        else:
            self.added_ml_ids.append(result.value())

    def bc_ml_en_ch(self, result):
        if self.reader_status == "Available":
            my_func.update_ml_id(self, result.value())
        else:
            if result.value() in self.changed_ml_ids:
                pass
            else:
                self.changed_ml_ids.append(result.value())

    def bc_pb_cu_id(self, result):
        my_func.set_now_stuff_from_broadcast(self, result)

    def bc_pb_st(self, result):
        my_func.play_status_control(self, result)

    def bc_pb_vo_ch(self, result):
        pass

    def bc_pl_ch(self, result):
        my_func.playlist_changed(self, result)

    def bc_pl_cu_ps(self, result):
        my_func.playlist_position_change(self, result)

    def bc_pl_ld(self, result):
        pass

    def closeEvent(self, event):
        my_func.save_col_sizes(self)
        event.accept()


def main():
    app = QApplication(sys.argv)
    form = DaiClient()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
