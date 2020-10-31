import logging

fmtStr = "%(asctime)s: %(levelname)s: %(funcName)s Line:%(lineno)d %(message)s"
dateStr = "%m/%d/%Y %I:%M:%S %p"
logging.basicConfig(filename="_log.log",
                    filemode='w',
                    level=logging.DEBUG,
                    format=fmtStr,
                    datefmt=dateStr)