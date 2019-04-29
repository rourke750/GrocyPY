import sqlite3

from . import utils

receipt_table = (
    '''
    CREATE TABLE IF NOT EXISTS ReceiptTransactions(
        userId VARCHAR(255) NOT NULL,
        divisionNumber INT NOT NULL,
        storeNumber INT NOT NULL,
        transactionDate VARCHAR(255) NOT NULL,
        terminalNumber INT NOT NULL,
        transactionId INT NOT NULL,
        PRIMARY KEY (userId, storeNumber, transactionId)
    );
    '''
)

dbname = utils.resource_path('sqldb.db')

sqlite_insert_receipt = 'INSERT INTO ReceiptTransactions(userId, divisionNumber, storeNumber, transactionDate, terminalNumber, transactionId) VALUES(?, ?, ?, ?, ?, ?);'
sqlite_check_exists = 'SELECT COUNT(*) FROM ReceiptTransactions WHERE userId=? AND storeNumber=? AND transactionId=?;'

conn = None
r = None

def check_sqllite_connection():
    try:
        global conn
        conn = sqlite3.connect(dbname, check_same_thread=False)
        return True
    except sqlite3.DatabaseError as err:
        utils.log('Sqlite connection could not be established', logging.ERROR)
        utils.log(str(err), logging.ERROR)
        return False
        
def is_receipt_generated(userId, storeNumber, transactionId):
    try:
        cursor = conn.cursor()
        cursor.execute(sqlite_check_exists, (userId, storeNumber, transactionId))
        row = cursor.fetchone()
        return row[0] > 0
    except sqlite3.DatabaseError as err:
        utils.log(str(err), logging.ERROR)
    finally:
        cursor.close()
    return False
    
def generate_receipt(userId, divisionNumber, storeNumber, transactionDate, terminalNumber, transactionId):
    try:
        cursor = conn.cursor()
        cursor.execute(sqlite_insert_receipt, (userId, divisionNumber, storeNumber, transactionDate, terminalNumber, transactionId))
        conn.commit()
    except sqlite3.DatabaseError as err:
        utils.log(str(err), logging.ERROR)
    finally:
        cursor.close()
        
if not check_sqllite_connection():
    sys.exit(0)
try:
    cursor = conn.cursor()
    cursor.execute(receipt_table)
except sqlite3.Error as err:
    utils.log("Sqlite error with generating tables." + str(err), logging.ERROR)
finally:
    conn.commit()
    cursor.close()