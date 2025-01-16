import logging
import colorlog
from logging.handlers import RotatingFileHandler,TimedRotatingFileHandler
class LoggerHandler(logging.Logger):
    # 初始化 Logger
    def __init__(self,
                 name='root',
                 logger_level= 'DEBUG',
                 file=None,
                 logger_format = " [%(asctime)s] %(levelname)s [%(filename)s %(funcName)s] [ line:%(lineno)d ] %(message)s",
                 color = True
                 ):

        # 1、设置logger收集器，继承logging.Logger
        super().__init__(name)

        # 2、设置日志收集器level级别
        self.setLevel(logger_level)

        # 设置 handler 格式 有颜色版
        fmt = logging.Formatter(logger_format)
        if color:
            colorlog_fmt = colorlog.ColoredFormatter(
                '%(log_color)s[%(asctime)s] {%(filename)s:%(lineno)d}[%(funcName)s] %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                }
            )
            fmt = colorlog_fmt
        # 3、设置日志处理器
        # 定义默认日志文件最大字节数(5M)
        LOG_MAX_BYTES = 5 * 1024 * 1024
        # midnight: 表示日志文件在每天半夜时分滚动
        # interval: 间隔时间单位的个数，指等待多少个 when 的时间后 Logger 会自动重建新闻继续进行日志记录
        # backupCount: 表示日志文件的保留个数，假如为7，则会保留最近的7个日志文件
        # 定义默认日志文件备份个数
        LOG_BACKUP_COUNT = 31
        # 如果传递了文件，就会输出到file文件中
        if file:
            file_handler = TimedRotatingFileHandler(file,when="midnight", interval=1, 
            backupCount=LOG_BACKUP_COUNT,encoding='utf-8') # 追加模式
            file_handler.suffix = "%Y-%m-%d"
            # 4、设置 file_handler 级别
            file_handler.setLevel(logger_level)
            # 6、设置handler格式
            file_handler.setFormatter(fmt)
            # 7、添加handler
            self.addHandler(file_handler)

        # 默认都输出到控制台
        stream_handler = logging.StreamHandler()
        # 4、设置 stream_handler 级别
        stream_handler.setLevel(logger_level)
        # 6、设置handler格式
        stream_handler.setFormatter(fmt)
        # 7、添加handler
        self.addHandler(stream_handler)
