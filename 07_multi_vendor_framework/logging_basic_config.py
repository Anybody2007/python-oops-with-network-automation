import logging

def logging_basic_config():
    logging.basicConfig(level=logging.INFO, filename="multivendor_fw.log", format="%(asctime)s, %(levelname)s, %(message)s", force=True)