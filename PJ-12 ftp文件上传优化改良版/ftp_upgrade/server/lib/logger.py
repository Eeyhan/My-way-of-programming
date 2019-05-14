#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import logging,sys,os
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from conf import settings

def mylog(log_type):
    log_file = settings.log_file[log_type]
    filehand = logging.FileHandler(log_file)
    filehand.setLevel(settings.level)
    formater = logging.Formatter(settings.log_format)
    filehand.setFormatter(formater)
    logger = logging.getLogger(log_type)
    logger.handlers.clear()
    logger.setLevel(settings.level)

    logger.addHandler(filehand)
    return logger


