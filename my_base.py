
#  Copyright 2016 by Dai Trying
#
#  This file is part of daixmms2skin.
#
#     daixmms2skin is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     daixmms2skin is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with daixmms2skin.  If not, see <http://www.gnu.org/licenses/>.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import my_func


class QCustomTableWidgetItem (QTableWidgetItem):
    def __init__(self, value):
        super(QCustomTableWidgetItem, self).__init__(str('%s' % value))

    def __lt__(self, other):
        if isinstance(other, QCustomTableWidgetItem):
            self_data_value = float(self.data(QtCore.Qt.EditRole))
            other_data_value = float(other.data(QtCore.Qt.EditRole))
            return self_data_value < other_data_value
        else:
            return QTableWidgetItem.__lt__(self, other)


class MyToolButton(QtWidgets.QToolButton):
    # noinspection PyUnusedLocal
    def __init__(self, parent=None):
        QtWidgets.QToolButton.__init__(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAutoRaise(True)
        self.setMinimumSize(QtCore.QSize(34, 34))
        self.setMaximumSize(QtCore.QSize(34, 34))
        self.setIconSize(QtCore.QSize(28, 28))


class MyTable(QtWidgets.QTableWidget):
    # noinspection PyUnusedLocal
    def __init__(self, parent=None):
        QtWidgets.QTableWidget.__init__(self)
        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().setDefaultSectionSize(18)
        self.verticalHeader().setHighlightSections(False)
        self.verticalHeader().setMinimumSectionSize(18)
        self.setColumnCount(12)
        self.setRowCount(0)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.setFont(font)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setLineWidth(0)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.setShowGrid(False)
        self.setGridStyle(QtCore.Qt.NoPen)

        item = QtWidgets.QTableWidgetItem()
        item.setText("Id")
        self.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Track")
        self.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Album")
        self.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Disc")
        self.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Title")
        self.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Artist")
        self.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Genre")
        self.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Album Artist")
        self.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Duration")
        self.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Plays")
        self.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("BitRate")
        self.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("File Size")
        self.setHorizontalHeaderItem(11, item)

    def set_row_data(self, pos, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12):
        self.setItem(pos, 0, QCustomTableWidgetItem(c1))
        self.item(pos, 0).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.setItem(pos, 1, QCustomTableWidgetItem(c2))
        self.item(pos, 1).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.setItem(pos, 2, QTableWidgetItem(c3))
        self.setItem(pos, 3, QCustomTableWidgetItem(c4))
        self.item(pos, 3).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.setItem(pos, 4, QTableWidgetItem(c5))
        self.setItem(pos, 5, QTableWidgetItem(c6))
        self.setItem(pos, 6, QTableWidgetItem(c7))
        self.setItem(pos, 7, QTableWidgetItem(c8))
        self.setItem(pos, 8, QTableWidgetItem(my_func.ms_int_to_time(c9)))
        self.item(pos, 8).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.setItem(pos, 9, QCustomTableWidgetItem(c10))
        self.item(pos, 9).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.setItem(pos, 10, QCustomTableWidgetItem(c11))
        self.setItem(pos, 11, QTableWidgetItem(my_func.convert_to_size(c12)))


class UiChoose(object):
    def set_up_ui(self, Choose):
        Choose.setObjectName("Choose")
        Choose.resize(303, 103)
        Choose.setWindowTitle("Choose Playlist")
        self.gridLayout = QtWidgets.QGridLayout(Choose)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Choose)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setText("Please select the Playlist To use")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.playlist_choice = QtWidgets.QComboBox(Choose)
        self.playlist_choice.setObjectName("playlist_choice")
        self.gridLayout.addWidget(self.playlist_choice, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Choose)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.buttonBox.accepted.connect(Choose.accept)
        self.buttonBox.rejected.connect(Choose.reject)
        QtCore.QMetaObject.connectSlotsByName(Choose)


class UiMainWindow(object):
    # noinspection PyAttributeOutsideInit
    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.setWindowTitle("Dai's Xmms2 Skin")
        main_window.resize(720, 400)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/xmms.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main_window.setWindowIcon(icon)

        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")

        self.gridLayout_4 = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.toolPrevious = MyToolButton(self.central_widget)
        self.toolPrevious.setObjectName("toolButton")
        self.toolPrevious.setText("back")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolPrevious.setIcon(icon1)
        self.toolPrevious.setToolTip("Previous Track")

        self.toolPlay = MyToolButton(self.central_widget)
        self.toolPlay.setObjectName("toolButton_2")
        self.toolPlay.setText("play")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolPlay.setIcon(icon2)
        self.toolPlay.setToolTip("Play")

        self.toolPause = MyToolButton(self.central_widget)
        self.toolPause.setObjectName("toolButton_3")
        self.toolPause.setText("pause")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolPause.setIcon(icon3)
        self.toolPause.setToolTip("Pause")

        self.toolStop = MyToolButton(self.central_widget)
        self.toolStop.setObjectName("toolButton_4")
        self.toolStop.setText("stop")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolStop.setIcon(icon4)
        self.toolStop.setToolTip("Stop")

        self.toolNext = MyToolButton(self.central_widget)
        self.toolNext.setObjectName("toolButton_5")
        self.toolNext.setText("next")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolNext.setIcon(icon5)
        self.toolNext.setToolTip("Next Track")

        self.toolShuffle = MyToolButton(self.central_widget)
        self.toolShuffle.setObjectName("toolButton_6")
        self.toolShuffle.setText("shuffle")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/shuffle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolShuffle.setIcon(icon6)
        self.toolShuffle.setToolTip("Shuffle Tracks")

        self.toolEject = MyToolButton(self.central_widget)
        self.toolEject.setObjectName("toolButton_7")
        self.toolEject.setText("eject")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/eject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolEject.setIcon(icon7)
        self.toolEject.setToolTip("Clear playlist")

        self.toolDelete = MyToolButton(self.central_widget)
        self.toolDelete.setObjectName("toolButton_8")
        self.toolDelete.setText("delete")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolDelete.setIcon(icon8)
        self.toolDelete.setToolTip("Delete Current Playlist")

        spacer_item = QtWidgets.QSpacerItem(265, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.toolSettings = MyToolButton(self.central_widget)
        self.toolSettings.setObjectName("toolButton_9")
        self.toolSettings.setText("Settings")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/config.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolSettings.setIcon(icon9)
        self.toolSettings.setToolTip("Settings")

        self.progressBar = QtWidgets.QProgressBar(self.central_widget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setMinimumSize(QtCore.QSize(350, 22))
        self.progressBar.setMaximumSize(QtCore.QSize(350, 22))

        self.line = QtWidgets.QFrame(self.central_widget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.horizontalLayout.addWidget(self.toolPrevious)
        self.horizontalLayout.addWidget(self.toolPlay)
        self.horizontalLayout.addWidget(self.toolPause)
        self.horizontalLayout.addWidget(self.toolStop)
        self.horizontalLayout.addWidget(self.toolNext)
        self.horizontalLayout.addWidget(self.line)
        self.horizontalLayout.addWidget(self.toolShuffle)
        self.horizontalLayout.addWidget(self.toolEject)
        self.horizontalLayout.addWidget(self.toolDelete)
        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.gridLayout_4.addItem(spacer_item, 0, 7, 1, 1)
        self.gridLayout_4.addWidget(self.toolSettings, 0, 8, 1, 1)
        self.gridLayout_4.addWidget(self.progressBar, 0, 9, 1, 1)

        self.tabWidget = QtWidgets.QTabWidget(self.central_widget)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tabMl")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableMediaLibrary = MyTable(self.tab)
        self.tableMediaLibrary.setObjectName("tableMediaLibrary")
        self.tableMediaLibrary.setSortingEnabled(True)
        self.tableMediaLibrary.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableMediaLibrary.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.gridLayout_3.addWidget(self.tableMediaLibrary, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tabPl")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setObjectName("gridLayout")
        self.combo_pl_names = QtWidgets.QComboBox(self.tab_2)
        self.combo_pl_names.setObjectName("combo_pl_names")
        self.combo_pl_names.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.combo_pl_names.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        spacer_item1 = QtWidgets.QSpacerItem(598, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.table_pl_entries = MyTable(self.tab_2)
        self.table_pl_entries.setObjectName("table_pl_entries")
        self.table_pl_entries.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.gridLayout.addWidget(self.combo_pl_names, 0, 0, 1, 1)
        self.gridLayout.addItem(spacer_item1, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.table_pl_entries, 1, 0, 1, 2)
        self.tabWidget.addTab(self.tab_2, "")

        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tabNp")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableNowPlaying = MyTable(self.tab_3)
        self.tableNowPlaying.setObjectName("tableNowPlaying")
        self.tableNowPlaying.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.gridLayout_2.addWidget(self.tableNowPlaying, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")

        self.tabSettings = QtWidgets.QWidget()
        self.tabSettings.setObjectName("tabSettings")
        self.lyt_tab_grid = QtWidgets.QGridLayout(self.tabSettings)
        self.lyt_tab_grid.setObjectName("lyt_tab_grid")
        self.lyt_vert_ml = QtWidgets.QVBoxLayout()
        self.lyt_vert_ml.setObjectName("lyt_vert_ml")
        self.label_ml = QtWidgets.QLabel(self.tabSettings)
        self.label_ml.setMinimumSize(QtCore.QSize(130, 0))
        self.label_ml.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_ml.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ml.setObjectName("label_ml")
        self.label_ml.setText("Media Library")
        self.lyt_vert_ml.addWidget(self.label_ml)
        self.rb_ml_0 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_ml_0.setAutoExclusive(False)
        self.rb_ml_0.setObjectName("rb_ml_id")
        self.rb_ml_0.setText("Id")
        self.lyt_vert_ml.addWidget(self.rb_ml_0)
        self.rb_ml_1 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_ml_1.setAutoExclusive(False)
        self.rb_ml_1.setObjectName("rb_ml_track")
        self.rb_ml_1.setText("Track")
        self.lyt_vert_ml.addWidget(self.rb_ml_1)
        self.rb_ml_2 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_ml_2.setAutoExclusive(False)
        self.rb_ml_2.setObjectName("rb_ml_album")
        self.rb_ml_2.setText("Album")
        self.lyt_vert_ml.addWidget(self.rb_ml_2)
        self.rb_ml_3 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_ml_3.setAutoExclusive(False)
        self.rb_ml_3.setObjectName("rb_ml_disc")
        self.rb_ml_3.setText("Disc No")
        self.lyt_vert_ml.addWidget(self.rb_ml_3)
        self.rb_ml_4 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_ml_4.setAutoExclusive(False)
        self.rb_ml_4.setObjectName("rb_ml_title")
        self.rb_ml_4.setText("Title")
        self.lyt_vert_ml.addWidget(self.rb_ml_4)
        self.rb_ml_5 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_ml_5.setAutoExclusive(False)
        self.rb_ml_5.setObjectName("rb_ml_artist")
        self.rb_ml_5.setText("Artist")
        self.lyt_vert_ml.addWidget(self.rb_ml_5)
        self.rb_ml_6 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_ml_6.setAutoExclusive(False)
        self.rb_ml_6.setObjectName("rb_ml_genre")
        self.rb_ml_6.setText("Genre")
        self.lyt_vert_ml.addWidget(self.rb_ml_6)
        self.rb_ml_7 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_ml_7.setAutoExclusive(False)
        self.rb_ml_7.setObjectName("rb_ml_performer")
        self.rb_ml_7.setText("Album Artist")
        self.lyt_vert_ml.addWidget(self.rb_ml_7)
        self.rb_ml_8 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_ml_8.setAutoExclusive(False)
        self.rb_ml_8.setObjectName("rb_ml_duration")
        self.rb_ml_8.setText("Duration")
        self.lyt_vert_ml.addWidget(self.rb_ml_8)
        self.rb_ml_9 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_ml_9.setAutoExclusive(False)
        self.rb_ml_9.setObjectName("rb_ml_plays")
        self.rb_ml_9.setText("Play Count")
        self.lyt_vert_ml.addWidget(self.rb_ml_9)
        self.rb_ml_10 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_ml_10.setAutoExclusive(False)
        self.rb_ml_10.setObjectName("rb_ml_bitrate")
        self.rb_ml_10.setText("BitRate")
        self.lyt_vert_ml.addWidget(self.rb_ml_10)
        self.rb_ml_11 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_ml_11.setAutoExclusive(False)
        self.rb_ml_11.setObjectName("rb_ml_filesize")
        self.rb_ml_11.setText("FileSize")
        self.lyt_vert_ml.addWidget(self.rb_ml_11)
        self.rb_ml_rows = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_ml_rows.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.rb_ml_rows.setAutoExclusive(False)
        self.rb_ml_rows.setObjectName("rb_ml_rows")
        self.rb_ml_rows.setText("Row Numbers")
        self.lyt_vert_ml.addWidget(self.rb_ml_rows)
        self.lyt_tab_grid.addLayout(self.lyt_vert_ml, 1, 0, 4, 1)
        self.line_4 = QtWidgets.QFrame(self.tabSettings)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.lyt_tab_grid.addWidget(self.line_4, 1, 2, 4, 2)
        self.lyt_vert_pl = QtWidgets.QVBoxLayout()
        self.lyt_vert_pl.setObjectName("lyt_vert_pl")
        self.label_pl = QtWidgets.QLabel(self.tabSettings)
        self.label_pl.setMinimumSize(QtCore.QSize(130, 0))
        self.label_pl.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_pl.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pl.setObjectName("label_pl")
        self.label_pl.setText("Playlist Manager")
        self.lyt_vert_pl.addWidget(self.label_pl)
        self.rb_pl_0 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_pl_0.setAutoExclusive(False)
        self.rb_pl_0.setObjectName("rb_pl_id")
        self.rb_pl_0.setText("Id")
        self.lyt_vert_pl.addWidget(self.rb_pl_0)
        self.rb_pl_1 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_pl_1.setAutoExclusive(False)
        self.rb_pl_1.setObjectName("rb_pl_track")
        self.rb_pl_1.setText("Track")
        self.lyt_vert_pl.addWidget(self.rb_pl_1)
        self.rb_pl_2 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_pl_2.setAutoExclusive(False)
        self.rb_pl_2.setObjectName("rb_pl_album")
        self.rb_pl_2.setText("Album")
        self.lyt_vert_pl.addWidget(self.rb_pl_2)
        self.rb_pl_3 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_pl_3.setAutoExclusive(False)
        self.rb_pl_3.setObjectName("rb_pl_disc")
        self.rb_pl_3.setText("Disc No")
        self.lyt_vert_pl.addWidget(self.rb_pl_3)
        self.rb_pl_4 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_pl_4.setAutoExclusive(False)
        self.rb_pl_4.setObjectName("rb_pl_title")
        self.rb_pl_4.setText("Title")
        self.lyt_vert_pl.addWidget(self.rb_pl_4)
        self.rb_pl_5 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_pl_5.setAutoExclusive(False)
        self.rb_pl_5.setObjectName("rb_pl_artist")
        self.rb_pl_5.setText("Artist")
        self.lyt_vert_pl.addWidget(self.rb_pl_5)
        self.rb_pl_6 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_pl_6.setAutoExclusive(False)
        self.rb_pl_6.setObjectName("rb_pl_genre")
        self.rb_pl_6.setText("Genre")
        self.lyt_vert_pl.addWidget(self.rb_pl_6)
        self.rb_pl_7 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_pl_7.setAutoExclusive(False)
        self.rb_pl_7.setObjectName("rb_pl_performer")
        self.rb_pl_7.setText("Album Artist")
        self.lyt_vert_pl.addWidget(self.rb_pl_7)
        self.rb_pl_8 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_pl_8.setAutoExclusive(False)
        self.rb_pl_8.setObjectName("rb_pl_duration")
        self.rb_pl_8.setText("Duration")
        self.lyt_vert_pl.addWidget(self.rb_pl_8)
        self.rb_pl_9 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_pl_9.setAutoExclusive(False)
        self.rb_pl_9.setObjectName("rb_pl_plays")
        self.rb_pl_9.setText("Play Count")
        self.lyt_vert_pl.addWidget(self.rb_pl_9)
        self.rb_pl_10 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_pl_10.setAutoExclusive(False)
        self.rb_pl_10.setObjectName("rb_pl_bitrate")
        self.rb_pl_10.setText("BitRate")
        self.lyt_vert_pl.addWidget(self.rb_pl_10)
        self.rb_pl_11 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_pl_11.setAutoExclusive(False)
        self.rb_pl_11.setObjectName("rb_pl_filesize")
        self.rb_pl_11.setText("FileSize")
        self.lyt_vert_pl.addWidget(self.rb_pl_11)
        self.rb_pl_rows = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_pl_rows.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.rb_pl_rows.setAutoExclusive(False)
        self.rb_pl_rows.setObjectName("rb_pl_rows")
        self.rb_pl_rows.setText("Row Numbers")
        self.lyt_vert_pl.addWidget(self.rb_pl_rows)
        self.lyt_tab_grid.addLayout(self.lyt_vert_pl, 1, 4, 4, 1)
        self.line_5 = QtWidgets.QFrame(self.tabSettings)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.lyt_tab_grid.addWidget(self.line_5, 1, 6, 4, 2)
        self.lyt_vert_np = QtWidgets.QVBoxLayout()
        self.lyt_vert_np.setObjectName("lyt_vert_np")
        self.label_np = QtWidgets.QLabel(self.tabSettings)
        self.label_np.setMinimumSize(QtCore.QSize(130, 0))
        self.label_np.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_np.setAlignment(QtCore.Qt.AlignCenter)
        self.label_np.setObjectName("label_np")
        self.label_np.setText("Now Playing")
        self.lyt_vert_np.addWidget(self.label_np)
        self.rb_np_0 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_np_0.setAutoExclusive(False)
        self.rb_np_0.setObjectName("rb_np_id")
        self.rb_np_0.setText("Id")
        self.lyt_vert_np.addWidget(self.rb_np_0)
        self.rb_np_1 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_np_1.setAutoExclusive(False)
        self.rb_np_1.setObjectName("rb_np_track")
        self.rb_np_1.setText("Track")
        self.lyt_vert_np.addWidget(self.rb_np_1)
        self.rb_np_2 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_np_2.setAutoExclusive(False)
        self.rb_np_2.setObjectName("rb_np_album")
        self.rb_np_2.setText("Album")
        self.lyt_vert_np.addWidget(self.rb_np_2)
        self.rb_np_3 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_np_3.setAutoExclusive(False)
        self.rb_np_3.setObjectName("rb_np_disc")
        self.rb_np_3.setText("Disc No")
        self.lyt_vert_np.addWidget(self.rb_np_3)
        self.rb_np_4 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_np_4.setAutoExclusive(False)
        self.rb_np_4.setObjectName("rb_np_title")
        self.rb_np_4.setText("Title")
        self.lyt_vert_np.addWidget(self.rb_np_4)
        self.rb_np_5 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_np_5.setAutoExclusive(False)
        self.rb_np_5.setObjectName("rb_np_artist")
        self.rb_np_5.setText("Artist")
        self.lyt_vert_np.addWidget(self.rb_np_5)
        self.rb_np_6 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_np_6.setAutoExclusive(False)
        self.rb_np_6.setObjectName("rb_np_genre")
        self.rb_np_6.setText("Genre")
        self.lyt_vert_np.addWidget(self.rb_np_6)
        self.rb_np_7 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_np_7.setAutoExclusive(False)
        self.rb_np_7.setObjectName("rb_np_performer")
        self.rb_np_7.setText("Album Artist")
        self.lyt_vert_np.addWidget(self.rb_np_7)
        self.rb_np_8 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_np_8.setAutoExclusive(False)
        self.rb_np_8.setObjectName("rb_np_duration")
        self.rb_np_8.setText("Duration")
        self.lyt_vert_np.addWidget(self.rb_np_8)
        self.rb_np_9 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_np_9.setAutoExclusive(False)
        self.rb_np_9.setObjectName("rb_np_plays")
        self.rb_np_9.setText("Play Count")
        self.lyt_vert_np.addWidget(self.rb_np_9)
        self.rb_np_10 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_np_10.setAutoExclusive(False)
        self.rb_np_10.setObjectName("rb_np_bitrate")
        self.rb_np_10.setText("BitRate")
        self.lyt_vert_np.addWidget(self.rb_np_10)
        self.rb_np_11 = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_np_11.setAutoExclusive(False)
        self.rb_np_11.setObjectName("rb_np_filesize")
        self.rb_np_11.setText("FileSize")
        self.lyt_vert_np.addWidget(self.rb_np_11)
        self.rb_np_rows = QtWidgets.QRadioButton(self.tabSettings)
        self.rb_np_rows.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.rb_np_rows.setAutoExclusive(False)
        self.rb_np_rows.setObjectName("rb_np_rows")
        self.rb_np_rows.setText("Row Numbers")
        self.lyt_vert_np.addWidget(self.rb_np_rows)
        self.lyt_tab_grid.addLayout(self.lyt_vert_np, 1, 8, 4, 2)
        spaceritem = QtWidgets.QSpacerItem(27, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyt_tab_grid.addItem(spaceritem, 2, 5, 1, 1)
        spaceritem1 = QtWidgets.QSpacerItem(27, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyt_tab_grid.addItem(spaceritem1, 2, 7, 1, 1)
        spaceritem2 = QtWidgets.QSpacerItem(97, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyt_tab_grid.addItem(spaceritem2, 2, 10, 1, 1)
        spaceritem3 = QtWidgets.QSpacerItem(27, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyt_tab_grid.addItem(spaceritem3, 3, 3, 1, 1)
        spaceritem4 = QtWidgets.QSpacerItem(27, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyt_tab_grid.addItem(spaceritem4, 4, 1, 1, 1)
        spaceritem5 = QtWidgets.QSpacerItem(457, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyt_tab_grid.addItem(spaceritem5, 5, 0, 1, 9)
        self.btn_ok = QtWidgets.QPushButton(self.tabSettings)
        self.btn_ok.setMinimumSize(QtCore.QSize(100, 25))
        self.btn_ok.setMaximumSize(QtCore.QSize(100, 25))
        self.btn_ok.setFlat(False)
        self.btn_ok.setObjectName("btn_ok")
        self.btn_ok.setText("Save")
        self.lyt_tab_grid.addWidget(self.btn_ok, 5, 9, 1, 1)
        self.btn_cancel = QtWidgets.QPushButton(self.tabSettings)
        self.btn_cancel.setMinimumSize(QtCore.QSize(100, 25))
        self.btn_cancel.setMaximumSize(QtCore.QSize(100, 25))
        self.btn_cancel.setFlat(False)
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_cancel.setText("Cancel")
        self.lyt_tab_grid.addWidget(self.btn_cancel, 5, 10, 1, 1)
        self.label_title = QtWidgets.QLabel(self.tabSettings)
        self.label_title.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_title.setFont(font)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.label_title.setText("D   I   S   P   L   A   Y       O   R       H   I   D   E       C   O   L   U   M   N   S")
        self.lyt_tab_grid.addWidget(self.label_title, 0, 0, 1, 11)
        self.tabWidget.addTab(self.tabSettings, "")

        self.gridLayout_4.addWidget(self.tabWidget, 1, 0, 1, 10)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "Media Library")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Playlist Manager")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "Now Playing")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSettings), "Settings")

        main_window.setCentralWidget(self.central_widget)

        # self.menu_bar = QtWidgets.QMenuBar(main_window)
        # self.menu_bar.setGeometry(QtCore.QRect(0, 0, 720, 24))
        # self.menu_bar.setObjectName("menu_bar")
        # main_window.setMenuBar(self.menu_bar)

        # self.status_bar = QtWidgets.QStatusBar(main_window)
        # self.status_bar.setObjectName("status_bar")
        # main_window.setStatusBar(self.status_bar)

        self.tabWidget.setCurrentIndex(0)
        # QtCore.QMetaObject.connectSlotsByName(main_window)
