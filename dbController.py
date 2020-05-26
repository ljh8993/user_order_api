class DB(object):
    def __init__(self, product='mysql'):
        self.product = product
        self.conn, self.cs = None, None
        if not self.cs:
            self.setup()

    def setup(self):
        self._setup_mysql()

    def _setup_mysql(self):
        import pymysql
        from secretKey import DATABASE
        self.conn = pymysql.connect(host=DATABASE["host"],
                                    user=DATABASE["user"],
                                    passwd=DATABASE["passwd"],
                                    db=DATABASE["db"],
                                    port=DATABASE["port"],
                                    charset=DATABASE["charset"])
        self.conn.autocommit(False)
        self.cs = self.conn.cursor()
        self.conn, self.cs = self.conn, self.cs

    def fetchone(self):
        return self.cs.fetchone()

    def _build_dict(self, aSet):
        names, rs = [x[0] for x in self.cs.description], []
        for s in aSet:
            if not s:
                return [None]
            rs.append(dict(zip(names, s)))
        return rs

    def fetchone_dict(self):
        return self._build_dict([self.cs.fetchone()])[0]

    def fetchall(self):
        return self.cs.fetchall()

    def fetchall_dict(self):
        return self._build_dict(self.fetchall())

    def execute(self, *args, **kwargs):
        self.cs.execute(*args, **kwargs)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        if self.cs: self.cs.close()
        if self.conn: self.conn.close()
        self.cs = self.conn = None
