import chatbot.DBClass as mdb
from time import time
from chatbot.credentials.credentials_ftp import ftp_config
from io import BytesIO
import ftplib
import requests
import json
from pyzbar.pyzbar import decode
from PIL import Image

class ImageCl():
    def __init__(self, ImageBefore):
        self.ImageBefore = ImageBefore #get link to image for recognition and detection
        self.db = mdb.DBrunner()
        self.start_time = time()

    def Runner(self):
        'run all functions to detect and recognize waste and add all data to db'
        wasteResult = self.imageRecognition()
        imgBefore = requests.get(self.ImageBefore).content
        img = self.imageAfter.split('/')
        image_path = img[-1]
        'add photo to FTP server'
        connection = ftplib.FTP(ftp_config['host'], ftp_config['username'], ftp_config['password'])
        r = BytesIO()
        connection.retrbinary('RETR path' + image_path, r.write) # TODO: set FTP path
        r.seek(0)
        'add data to DB'
        self.row = self.db.insertBlob(f'INSERT INTO imagelogs (imageBefore,imageAfter) VALUES (%s,%s)',
                                      (imgBefore, r.getvalue()))
        self.addWasteTypes()
        productInfo = self.barcodeRecognition()
        self.db.insert(f'UPDATE imagelogs SET time={time() - self.start_time} WHERE imageId = {self.row}')
        return wasteResult , productInfo


    def imageRecognition(self):
        'connect to detection server, and receive link to recognized image'
        self.imageDetect = requests.get('url' + self.ImageBefore) # TODO: set API
        self.wasteDetect = json.loads(self.imageDetect.text)
        self.imageAfter = self.wasteDetect[0]['url'] #link to recognized image
        return self.wasteDetect #return all data (text + link to recognized image)

    def barcodeRecognition(self):
        'func to recognize barcode, if it is on the wastepic'
        response = requests.get(self.ImageBefore, stream=True)
        img = Image.open(response.raw)
        decoded_objects = decode(img)
        for obj in decoded_objects:
            barcodeData = obj.data.decode("utf-8")
            if barcodeData is not None:
                rows = self.db.select(f'SELECT * FROM Products WHERE ProductCode = {barcodeData}')
                if rows != []:
                    self.db.insert(f'UPDATE imagelogs SET barcode={barcodeData},barid={rows[0][0]} WHERE imageId = {self.row}')
                    return rows
                else:
                    addedRow = self.db.insert(f'INSERT INTO Products (ProductCode) VALUES ({barcodeData})')
                    self.db.insert(f'UPDATE imagelogs SET barcode={barcodeData},barid={addedRow} WHERE imageId = {self.row}')
                    return None
            else:
                return None

    def addWasteTypes(self):
        for i in range(1, len(self.wasteDetect)):
            name = self.wasteDetect[i]['name']
            score = self.wasteDetect[i]['score']
            self.db.insert(f"INSERT INTO wastelogs (imageId,type,percent) VALUES ({self.row}, '{name}', '{score}')")

