import medic2medic
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.debug('often makes a very good meal of %s', 'visiting tourists')

app = medic2medic.create_app()

if __name__ == "__main__":
    app.run()
