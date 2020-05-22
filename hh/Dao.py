import time,configparser,MySQLdb

class MysqlDao(object):
    __isinstance = False  # 设置一个私有变量，默认没有被实例化
    def __new__(cls, *args, **kwargs):
        if not cls.__isinstance:  # 如果被实例化了
            cls.__isinstance = object.__new__(cls)  # 否则实例化
        return cls.__isinstance  # 返回实例化的对象

    def __init__(self, host=None, port=None, db=None, user=None, password=None, charset=None):
        if host and port and db and user and password and charset:
            pass
        else:
            conf = configparser.ConfigParser()
            conf.read('config.ini', encoding='utf-8')
            if not host:
                host = conf.get('mysql', 'host')
            if not port:
                port = conf.get('mysql', 'port')
            if not db:
                db = conf.get('mysql', 'db')
            if not user:
                user = conf.get('mysql', 'user')
            if not password:
                password = conf.get('mysql', 'password')
            if not charset:
                charset = conf.get('mysql', 'charset')
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = int(port)
        self.charset = charset
        self.__reConn()
    def __del__(self):
        if self:
            self.close_con()

    def checkconn(self):
        try:
            self.conn = MySQLdb.connect(host=self.host, user=self.user, password=self.password, database=self.db, port=self.port, charset=self.charset)
            return True
        except Exception:
            return False

    def connIsOn(self):
        try:
            self.conn.ping()  # cping 校验连接是否异常
            _status = True
        except:
            _status = False
        return _status
    def __reConn(self, num=3, stime=1):  # 重试连接总次数为次,这里根据实际情况自己设置，三次还连不上，那还是什么
        _number = 0
        _status = True
        while _status and _number <= num:
            if self.connIsOn():
                _status = False
            else:
                if self.checkconn() == True:  # 重新连接,成功退出
                    _status = False
                    break
                _number += 1
                time.sleep(stime)  # 连接不成功,休眠1秒钟,继续循环，知道成功或重试次数结束
    def get_conn(self):
        self.__reConn()
        return self.conn
    def get_cur(self):
        self.__reConn()
        return self.conn.cursor()
    def close_con(self):
        if self.connIsOn():
            self.conn.close()
        return
    def commit_or_rollback(self, YN=True):
        if not self.connIsOn():
            return
        if YN:
            self.conn.commit()
        else:
            self.conn.rollback()
        return