from app_services import App
import logging

TARGETS = ['datajob', 'foranalysts', 'datasciencejobs']
KEYWORDS = r'data|analytic|analyst|analysis|data engineer|инженер данных|dwh|etl|postgresql|postgres|spark|airflow|kafka'


def __main__():
    log = logging.getLogger('APP_RUN')
    oh_app = App(TARGETS, log)
    oh_app.extract_new_increment()
    oh_app.transform_new_increment(KEYWORDS)
    return 0


if __name__ == __main__():
    __main__()
