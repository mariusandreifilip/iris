# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tracking Protection can be turned off for individual sites'
        self.test_case_id = '107431'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):
        tracking_protection_shield_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED
        tracking_protection_shield_deactivated_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED
        cnn_site_logo_pattern = Pattern('cnn_logo.png')
        cnn_blocked_content_pattern = Pattern('cnn_blocked_content.png')
        disable_blocking_button_pattern = Pattern('turn_off_blocking_for_site_button.png')
        enable_blocking_button_pattern = Pattern('turn_on_blocking_for_site_button.png')
        tracking_content_detected_message_pattern = Pattern('tracking_content_detected_message.png')
        tracking_attempts_blocked_message_pattern = Pattern('tracking_attempts_blocked_message.png')
        back_button_pattern = Pattern("back_button.png")
        trackers_button_pattern = Pattern("trackers_button.png")
        blocked_tracker_label_pattern = Pattern('blocked_label.png')
        trackers_icon_pattern = Pattern("trackers_icon.png")

        new_private_window()
        private_browsing_tab_logo_displayed = exists(PrivateWindow.private_window_pattern)
        assert_true(self, private_browsing_tab_logo_displayed, 'A new private window is successfully opened')

        navigate("https://edition.cnn.com")
        website_displayed = exists(cnn_site_logo_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, website_displayed, 'The website is successfully displayed')

        tracking_protection_shield_displayed = exists(tracking_protection_shield_pattern)
        assert_true(self, tracking_protection_shield_displayed, 'The tracking protection shield is displayed')

        restore_firefox_focus()
        cnn_blocked_content_displayed = scroll_until_pattern_found(cnn_blocked_content_pattern, type, (Key.DOWN,))
        assert_false(self, cnn_blocked_content_displayed,
                     'Websites content that contain tracking elements are not displayed on the page')

        click(tracking_protection_shield_pattern)
        disable_blocking_button_displayed = exists(disable_blocking_button_pattern)
        assert_true(self, disable_blocking_button_displayed, 'The \'Site information\' panel is displayed')

        trackers_button_available = exists(trackers_button_pattern)
        assert_true(self, trackers_button_available,
                    '\'Trackers\' button is displayed on the \'Site information\' panel')

        click(trackers_button_pattern)
        successfully_blocked_trackers_displayed = exists(blocked_tracker_label_pattern)
        assert_true(self, successfully_blocked_trackers_displayed,
                    'A list of successfully blocked trackers is displayed.')

        back_button_displayed = exists(back_button_pattern)
        assert_true(self, back_button_displayed, '\'Back\' button is displayed on the \'Site information panel\'')

        click(back_button_pattern)
        click(disable_blocking_button_pattern)
        website_displayed = exists(cnn_site_logo_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, website_displayed, 'The website successfully refreshes')

        tracking_protection_shield_deactivated_displayed = exists(tracking_protection_shield_deactivated_pattern)
        assert_true(self, tracking_protection_shield_deactivated_displayed,
                    'The \'tracking protection shield\' is displayed as deactivated (strikethrough)')

        mouse_move(tracking_protection_shield_deactivated_pattern)
        tracking_content_detected_message_displayed = exists(tracking_content_detected_message_pattern)
        assert_true(self, tracking_content_detected_message_displayed,
                    'On hover, the tracking protection shield displays a \'Tracking content detected\' tooltip message.')

        cnn_blocked_content_displayed = scroll_until_pattern_found(cnn_blocked_content_pattern, type, (Key.DOWN,))
        assert_true(self, cnn_blocked_content_displayed,
                    'Websites content that contain tracking elements are displayed on the page')

        click(tracking_protection_shield_deactivated_pattern)
        enable_blocking_button_displayed = exists(enable_blocking_button_pattern)
        assert_true(self, enable_blocking_button_displayed, 'The \'Site information\' panel is displayed')

        trackers_button_available = exists(trackers_button_pattern)
        assert_true(self, trackers_button_available,
                    '\'Trackers\' button is displayed on the \'Site information\' panel')

        click(trackers_button_pattern)
        list_of_active_trackers_displayed = exists(trackers_icon_pattern) and not exists(blocked_tracker_label_pattern)
        assert_true(self, list_of_active_trackers_displayed, 'A list of active trackers is successfully displayed.')

        back_button_displayed = exists(back_button_pattern)
        assert_true(self, back_button_displayed, '\'Back\' button is displayed on the \'Site information panel\'')

        click(back_button_pattern)
        click(enable_blocking_button_pattern)
        website_displayed = exists(cnn_site_logo_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, website_displayed, 'The website successfully refreshes')

        tracking_protection_shield_displayed = exists(tracking_protection_shield_pattern)
        assert_true(self, tracking_protection_shield_displayed,
                    'The tracking protection shield is displayed as active')

        mouse_move(tracking_protection_shield_pattern)
        tracking_attempts_blocked_message_displayed = exists(tracking_attempts_blocked_message_pattern)
        assert_true(self, tracking_attempts_blocked_message_displayed,
                    'On hover, the tracking protection shield displays a \'Tracking attempts blocked\' tooltip message.')

        cnn_blocked_content_displayed = scroll_until_pattern_found(cnn_blocked_content_pattern, type, (Key.DOWN,))
        assert_false(self, cnn_blocked_content_displayed,
                     'Websites content that contain tracking elements are not displayed on the page')

        click(tracking_protection_shield_pattern)
        site_information_panel_displayed = exists(trackers_button_pattern)
        assert_true(self, site_information_panel_displayed, 'The \'Site information\' panel is displayed')

        click(trackers_button_pattern)
        successfully_blocked_trackers_displayed = exists(blocked_tracker_label_pattern)
        assert_true(self, successfully_blocked_trackers_displayed,
                    'A list of successfully blocked trackers is displayed.')

        close_window()
