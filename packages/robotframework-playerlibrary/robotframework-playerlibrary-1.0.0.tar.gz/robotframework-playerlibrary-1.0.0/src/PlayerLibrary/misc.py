from robotlibcore import keyword


class Misc:

    @keyword('setup custom locator', tags=["deprecated"])
    def setup_custom_locator(self):
        pass

    @keyword('Set Library Search Order', tags=["deprecated"])
    def set_library_search_order(self):
        pass

    @keyword('wait for page to be ready', tags=["deprecated"])
    def wait_for_page_to_be_ready(self):
        pass
