import sqlite3

DB_FILE = "cars.sqlite3"
# DB_FILE = "D:/PycharmProjects/excercises/cars.sqlite3"
# import os
# print(os.path.abspath(DB_FILE))

def getConnection():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn

class Car:

    TABLE_NAME = 'CARS'
    TABLE_HEADERS = {'BRAND','MODEL','P_YEAR','DESC','PRICE_DESC','PRICE'}
    TABLE_HEADERS_PRS = {'برند','مدل','سال تولید','توضیح','توضیح قیمت','قیمت'}

    def __init__(self):
        self.brand = ""
        self.model = ""
        self.pYear = 0
        self.desc = ""
        self.priceDesc = ""
        self.price = 0
        pass

    def insert(self):
        try:
            conn = getConnection()
            cur = conn.cursor()
            cmd = """INSERT INTO %s VALUES('%s','%s',%d,'%s','%s',%d)"""\
                   %(Car.TABLE_NAME,self.brand,self.model,self.pYear,self.desc,self.priceDesc,self.price)
            cur.execute(cmd)
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            pass
        except sqlite3.Error as e:
            print(e)

        return cur.lastrowid

    def __str__(self):
        return "Car:{brand: %s, brand: %s, pYear: %i, desc: %s, priceDescription: %s, price: %i}"\
            %(self.brand, self.model, self.pYear, self.desc, self.priceDesc, self.price)

    @staticmethod
    def createTable():
        try:
            conn = getConnection()
            conn.cursor().execute(
            """CREATE TABLE IF NOT EXISTS %s(
            BRAND VARCHAR(100),
            MODEL VARCAHR(100),
            P_YEAR INT,
            DESC TEXT,
            PRICE_DESC TEXT,
            PRICE INT,
            PRIMARY KEY(BRAND, MODEL, P_YEAR, DESC, PRICE_DESC, PRICE)
            );"""%Car.TABLE_NAME)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def deleteAll():
        conn = getConnection()
        cur = conn.cursor()
        cmd =  """DELETE FROM %s;"""%(Car.TABLE_NAME)
        cur.execute(cmd)
        conn.commit()
        conn.close()
        return cur.lastrowid

    @staticmethod
    def getAll():
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM %s ;" % (Car.TABLE_NAME))
        while True:
            car = cur.fetchone()
            if not car:
                break
            yield car
        conn.close()

    @staticmethod
    def printAll():
        for item in Car.getAll():
            print(item)

    @staticmethod
    def getAllByModel(brand,model):
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM %s WHERE BRAND='%s',MODEL='%s';" % (Car.TABLE_NAME,brand,model))
        while True:
            car = cur.fetchone()
            if not car:
                break
            yield car
        conn.close()

    @staticmethod
    def getAllByBrand(brand):
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM %s WHERE BRAND='%s';" % (Car.TABLE_NAME, brand))
        while True:
            car = cur.fetchone()
            if not car:
                break
            yield car
        conn.close()

    @staticmethod
    def getBrands():
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT BRAND FROM %s;" % (Car.TABLE_NAME))
        all = cur.fetchall()
        out= [row[0] for row in all]
        conn.close()
        return out

    @staticmethod
    def getBrandModels(brand):
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT MODEL FROM %s WHERE BRAND='%s';" % (Car.TABLE_NAME,brand))
        all = cur.fetchall()
        out = [row[0] for row in all]
        conn.close()
        return out

    @staticmethod
    def getRecordsCount():
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM %s;" % (Car.TABLE_NAME))
        out = cur.fetchone()[0]
        conn.close()
        return out

    @staticmethod
    def fetchFromSite():
        from bs4 import BeautifulSoup
        import requests
        import html

        r = requests.get("https://bama.ir/price")
        soup = BeautifulSoup(html.unescape(r.text), 'html.parser')
        Car.createTable()

        for sectionHtmlNode in soup.findAll('section', attrs={'class': 'price-list-brand-section'}):
            brand = sectionHtmlNode.find('header').find('a').text.replace('قیمت خودرو ', '').strip()
            for carHtmlNode in sectionHtmlNode.find('ul').findAll('a'):
                car = Car()
                car.brand = brand
                car.model = carHtmlNode.find('span', attrs={'class': 'sefr-model'}).text.strip()
                car.pYear = int(carHtmlNode.find('small', attrs={'class': 'sefr-trim'}).text.strip())
                car.desc = carHtmlNode.find('small', attrs={'class': 'sefr-company'}).text.replace('،', '').strip()
                car.priceDesc = carHtmlNode.find('small', attrs={'class': 'sefr-time'}).text.strip()
                car.price = int(carHtmlNode.find('small', attrs={'class': 'sefr-price'}).text.replace(',', '').strip())
                car.insert()