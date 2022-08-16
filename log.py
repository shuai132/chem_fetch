class log:
    debug = True

    def d(*args):
        if log.debug:
            print('LOGD:', *args)

    def i(*args):
        print('LOGI:', *args)

    def w(*args):
        print('LOGW:', *args)

    def e(*args):
        print('LOGE:', *args)
