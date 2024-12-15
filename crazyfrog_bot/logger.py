import logging

def create_logger(name: str, settings: dict[str, dict[str, str]], settings_pattern: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s\t%(name)s: %(message)s')
    for logger_setting in [settings[k] for k in settings.keys() if k.startswith(settings_pattern)]:
        handler = logging.StreamHandler() if logger_setting['Type'] == 'stdout' else logging.FileHandler(logger_setting['File'])
        handler.setFormatter(formatter)
        handler.setLevel(logging.getLevelNamesMapping()[logger_setting['Level']])
        logger.addHandler(handler)
    return logger
