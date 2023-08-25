import logging
import os.path
path_logs = "logs/dora.log"
if not os.path.exists(path_logs):
    open(path_logs, 'w')

logger = logging.Logger('Dora', logging.INFO)
handler = logging.FileHandler(path_logs, mode='a')
formatter = logging.Formatter("%(asctime)s %(name)s: %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

