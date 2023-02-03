from datetime import datetime


class log:
    debug = True

    @staticmethod
    def __print_impl(*args):
        print(datetime.now(), *args)

    def d(*args):
        if log.debug:
            log.__print_impl('LOGD:', *args)

    def i(*args):
        log.__print_impl('LOGI:', *args)

    def w(*args):
        log.__print_impl('LOGW:', *args)

    def e(*args):
        log.__print_impl('LOGE:', *args)
