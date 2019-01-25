# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Session restore with media content in the background'
        self.test_case_id = '117045'
        self.test_suite_id = '68'
        self.blocked_by = {'id': '1520733', 'platform': Platform.WINDOWS}
        self.locales = ['en-US']

    def run(self):
        hamburger_menu_button_pattern = NavBar.HAMBURGER_MENU
        restore_previous_session_pattern = HamburgerMenu.RESTORE_PREVIOUS_SESSION
        speaker_icon_active_pattern = Pattern('speaker_icon_active.png').similar(0.9)
        blocked_media_icon_pattern = Pattern('blocked_media_icon.png')
        first_label_pattern = Pattern('one_label.png').similar(0.6)
        second_label_pattern = Pattern('two_label.png').similar(0.6)
        web_developer_tools_tab_pattern = Pattern('web_developer_tools_tab.png')
        double_icons = Pattern('double_icons.png')

        test_page_local = self.get_asset_path('index.html')
        navigate(test_page_local)

        first_label_exists = exists(first_label_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, first_label_exists, 'Page loaded')

        right_click(first_label_pattern)
        if Settings.is_linux():
            time.sleep(DEFAULT_UI_DELAY_LONG)
            type('t')
        else:
            type(Key.DOWN)
            type(Key.ENTER)

        blocked_media_icon_exists = exists(blocked_media_icon_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, blocked_media_icon_exists, 'Blocked media tab opened')

        second_label_exists = exists(second_label_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, second_label_exists, 'Second link exists')
        right_click(second_label_pattern)

        if Settings.is_linux():
            time.sleep(DEFAULT_UI_DELAY)
            type('t')
        else:
            type(Key.DOWN)
            type(Key.ENTER)

        new_tab()
        navigate('https://videos.cdn.mozilla.net/uploads/Web_Developer_Tools_in_Firefox_Aurora_10.webm')

        speaker_icon_active_exists = exists(speaker_icon_active_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, speaker_icon_active_exists, 'Third website loaded')

        right_click(blocked_media_icon_pattern)
        type('p')

        time.sleep(DEFAULT_UI_DELAY)

        right_click(blocked_media_icon_pattern)
        type('p')

        blocked_media_tab_pinned_exists = exists(double_icons, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, blocked_media_tab_pinned_exists, 'Tabs pinned')

        restart_firefox(self, self.browser.path, self.profile_path, self.base_local_web_url)

        wait_for_firefox_restart()

        click(hamburger_menu_button_pattern, DEFAULT_UI_DELAY)

        restore_previous_session_located = exists(restore_previous_session_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, restore_previous_session_located,
                    'The "Hamburger" menu is successfully displayed. "Restore previous session" menu item located')
        click(restore_previous_session_pattern)

        last_tab_restored = exists(web_developer_tools_tab_pattern, DEFAULT_FIREFOX_TIMEOUT)
        blocked_media_icon_exists = exists(double_icons, DEFAULT_FIREFOX_TIMEOUT)
        no_speaker_tabs = exists(speaker_icon_active_pattern, DEFAULT_FIREFOX_TIMEOUT)
        restore_session_check_result = last_tab_restored and blocked_media_icon_exists and (not no_speaker_tabs)
        assert_true(self, restore_session_check_result, 'Tabs are loaded and media blocked for all tabs')


