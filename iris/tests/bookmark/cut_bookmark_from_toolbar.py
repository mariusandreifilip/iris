# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Cut items from "Bookmarks Toolbar"'
        self.test_case_id = '164371'
        self.test_suite_id = '2525'
        self.locale = ['en-US']
        self.exclude = [Platform.MAC, Platform.LINUX]

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        bookmark_cut_pattern = Pattern('bookmark_cut.png').similar(0.98)
        open_bookmark_toolbar_pattern = Pattern('open_bookmark_toolbar.png')
        most_visited_pattern = Pattern('drag_area.png')
        new_folder_pattern = Pattern('new_folder.png')
        bookmarks_folder_pattern = Pattern('bookmarks_folder.png')
        cut_item_pattern = Pattern('cut_bookmark.png')
        paste_item_pattern = Pattern('paste_bookmark.png')
        getting_started_bookmark_pattern = Pattern('getting_started_bookmark.png')

        navbar_offset, _ = NavBar.HOME_BUTTON.get_size()
        navbar_offset *= 1.5
        right_click(NavBar.HOME_BUTTON.target_offset(navbar_offset, 0))
        click(open_bookmark_toolbar_pattern)

        bookmark_in_toolbar = exists(getting_started_bookmark_pattern)
        assert_true(self, bookmark_in_toolbar, 'Bookmark is displayed in bookmark toolbar')

        right_click(most_visited_pattern)
        click(new_folder_pattern)
        paste('folder')
        type(Key.ENTER)
        right_click(getting_started_bookmark_pattern)
        click(cut_item_pattern)

        bookmark_is_cut = exists(bookmark_cut_pattern)
        assert_true(self, bookmark_is_cut, 'Bookmark displayed in toolbar as cut')

        click(bookmarks_folder_pattern)
        folder_dropdown_offset_x, folder_dropdown_offset_y = bookmarks_folder_pattern.get_size()
        folder_dropdown_offset_x //= 2
        folder_dropdown_offset_y *= 1.5
        right_click(bookmarks_folder_pattern.target_offset(folder_dropdown_offset_x, folder_dropdown_offset_y))
        click(paste_item_pattern)

        restore_firefox_focus()

        bookmark_removed_from_toolbar = not exists(getting_started_bookmark_pattern, DEFAULT_UI_DELAY)
        assert_true(self, bookmark_removed_from_toolbar, 'The bookmark is moved from toolbar')

        click(bookmarks_folder_pattern)

        bookmark_in_folder = exists(getting_started_bookmark_pattern)
        assert_true(self, bookmark_in_folder, '')
        restore_firefox_focus()
