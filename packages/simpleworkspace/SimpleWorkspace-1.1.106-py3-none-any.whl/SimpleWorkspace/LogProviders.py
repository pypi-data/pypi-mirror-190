from __future__ import annotations as _annotations
import datetime as _datetime
import gzip as _gzip
import logging as _logging
from logging.handlers import RotatingFileHandler as _RotatingFileHandler
import time as _time
import os as _os
from SimpleWorkspace.Enums.ByteEnum import ByteEnum as _ByteEnum
import sys as _sys

class _BaseLogger:
    @staticmethod
    def DefaultFormatter(useUTCTime=True):
        if useUTCTime:
            formatter = _logging.Formatter(fmt="%(asctime)s.%(msecs)03d+0000 %(levelname)s <%(module)s,%(lineno)s>: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            formatter.converter = _time.gmtime
        else:
            timeZoneStr = _time.strftime("%z") # "+0200"
            formatter = _logging.Formatter(fmt="%(asctime)s.%(msecs)03d" + timeZoneStr + " %(levelname)s <%(module)s,%(lineno)s>: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        return formatter
    @staticmethod
    def RegisterAsUnhandledExceptionHandler(logger):
        def UncaughtExeceptionHandler(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt): #avoid registering console aborts such as ctrl+c etc
                _sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

            logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

        _sys.excepthook = UncaughtExeceptionHandler
    



class RotatingFileLogger:
    @staticmethod
    def GetLogger(filepath, minimumLogLevel=_logging.DEBUG, maxBytes=_ByteEnum.MB.value * 100, maxRotations=10, useUTCTime=True, registerGlobalUnhandledExceptions=False):
        def rotator(source, dest):
            with open(source, "rb") as sf:
                gzip_fp = _gzip.open(dest, "wb")
                gzip_fp.writelines(sf)
                gzip_fp.close()
            _os.remove(source)

        logger = _logging.getLogger("__ROTATINGFILELOGGER_" + str(hash(f"{filepath}{minimumLogLevel}{maxBytes}{maxRotations}{useUTCTime}")))
        if(registerGlobalUnhandledExceptions):
            _BaseLogger.RegisterAsUnhandledExceptionHandler(logger)
        if(logger.hasHandlers()):
            return logger
        logger.setLevel(minimumLogLevel)
        handler = _RotatingFileHandler(filepath, maxBytes=maxBytes, backupCount=maxRotations)
        handler.rotator = rotator
        handler.namer = lambda name: name + ".gz"
        handler.setFormatter(_BaseLogger.DefaultFormatter(useUTCTime=useUTCTime))
        logger.addHandler(handler)

        return logger


class FileLogger:
    @staticmethod
    def GetLogger(filepath, minimumLogLevel=_logging.DEBUG, useUTCTime=True, registerGlobalUnhandledExceptions=False):
        logger = _logging.getLogger("__FILELOGGER_" + str(hash(f"{filepath}{minimumLogLevel}{useUTCTime}")))
        if(registerGlobalUnhandledExceptions):
            _BaseLogger.RegisterAsUnhandledExceptionHandler(logger)
        if(logger.hasHandlers()):
            return logger
        logger.setLevel(minimumLogLevel)
        handler = _logging.FileHandler(filepath)
        handler.setFormatter(_BaseLogger.DefaultFormatter(useUTCTime=useUTCTime))
        logger.addHandler(handler)
        return logger

class StdoutLogger:
    @staticmethod
    def GetLogger(minimumLogLevel=_logging.DEBUG, useUTCTime=False, registerGlobalUnhandledExceptions=False):
        stdoutLogger = _logging.getLogger("__STDOUTLOGGER__" + str(hash(f"{minimumLogLevel}{useUTCTime}")))
        if(registerGlobalUnhandledExceptions):
            _BaseLogger.RegisterAsUnhandledExceptionHandler(stdoutLogger)
        if(stdoutLogger.hasHandlers()):
            return stdoutLogger
        stdoutLogger.setLevel(minimumLogLevel)
        stdoutLogger.addHandler(StdoutLogger.CreateHandler(useUTCTime))
        return stdoutLogger
    
    @staticmethod
    def CreateHandler(useUTCTime = False):
        handler = _logging.StreamHandler(_sys.stdout)
        handler.setFormatter(_BaseLogger.DefaultFormatter(useUTCTime=useUTCTime))
        return handler


class DummyLogger:
    @staticmethod
    def GetLogger():
        dummyLogger = _logging.getLogger("@@BLACKHOLE@@")
        if(dummyLogger.hasHandlers()):
            return dummyLogger
        dummyLogger.addHandler(_logging.NullHandler())
        dummyLogger.propagate = False
        return dummyLogger

