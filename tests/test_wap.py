import time

from env import SCREENS_PATH
from page_objects.application import Application


def test_wap(app: Application):
    # 1) go to Twitch
    app.visit()

    # 2) click in the search icon
    # 3) input StarCraft II
    app.header.search_and_select_first_search_item('StarCraft II')

    # 4) scroll down 2 times
    app.search_list.wait_for_page_loading()
    app.search_list.smooth_scroll(x=0, y=800)
    # Wait is added for the demonstration purposes
    time.sleep(1)
    app.search_list.smooth_scroll(x=800, y=1_600)
    # 5) Select one streamer
    app.search_list.open_random_streamer()

    # 6) on the streamer page wait until all is load
    # Some streamers will have a modal or pop-up before loading the video,
    # the Auto test case should be able to handle this pop-up.
    app.stream.wait_for_video_loading()
    # 6) and take a screenshot
    app.browser.save_screenshot(str(SCREENS_PATH.path('wap')) + '.png')
