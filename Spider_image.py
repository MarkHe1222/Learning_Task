import urllib.request
import urllib.error
import re
import time
import os
import zipfile
import smtplib

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool

class bugGetImg():
	def __init__(self):
		self.timeOut = 1000
		self.user_Agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
		self.headers = {'User-Agent': self.user_Agent}
		self.t = time.localtime()
		self.folderName = str(self.t.__getattribute__("tm_year"))+'-'+\
		str(self.t.__getattribute__("tm_mon"))+'-'+str(self.t.__getattribute__("tm_mday"))
		self.localImgPath = r'C:\Users\hem4\Desktop\%s' %(self.folderName)

	def getHtml(self, pageStart, pageEnd):
		imgSrc = []
		for pageIndex in range(pageStart, pageEnd + 1):
			url = 'http://www.dbmeinv.com/dbgroup/show.htm?pager_offset=' + str(pageIndex)
			try:
				req = urllib.request.Request(url = url, headers = self.headers)
				webPage = urllib.request.urlopen(req, timeout = self.timeOut)
				data = webPage.read()
				data = data.decode('UTF-8')
				soup = BeautifulSoup(data, 'html.parser')
				imgContent= soup.findAll(['img'])
				for i in imgContent:
					imgSrc.append(i.get('src'))
			except urllib.error.HTTPError as e:
				print('The server could\'t fulfill the request.'+ str(pageIndex))
				print('Error code: ', e.code)
				continue
			except urllib.error.URLError as e:
				print('We failed to reach a server.')
				print('Reason: ', e.reason)
				continue
		print(imgSrc)
		if not os.path.exists(self.localImgPath):
			os.makedirs(self.localImgPath)
		return imgSrc

	def downloadImg(self, imgPath):
		target = self.localImgPath + '\\' + imgPath.split('/')[-1]
		print('localPath: ' + target + '\nimgPath: ' + imgPath + '\n')

		try:
			download_Image = urllib.request.urlretrieve(imgPath, target)
		    # download_Image = os.system('wget ' + imgPath + '-P' + target)
		except urllib.error.URLError as e:
			print('Can\'t download: ' + imgPath.split('/')[-1])
			print('Reason: ', e.reason)

	def zipImg(self):
		os.chdir(self.localImgPath)
		myZip = zipfile.ZipFile(self.localImgPath+'.zip','w')
		for image in os.listdir(self.localImgPath):
			print(image)
			myZip.write(image)
		myZip.close()
		print('zip already created!')

	def _format_addr(self, s):
	    name, addr = parseaddr(s)
	    return formataddr((Header(name, 'utf-8').encode(), addr))
	def sendEmail(self):
		from_addr = '609571515@qq.com'
		password = '@HE18800230976'
		to_addr = ['582565501@qq.com','1274527513@qq.com','171244336@qq.com','506598255@qq.com','905375751@qq.com','3047524460@qq.com','517497696@qq.com']
		smtp_server = 'smtp.qq.com'

		msg = MIMEMultipart()
		msg.attach(MIMEText('都是你喜欢的胸和腿。 send by Python. edit by Mark.', 'plain', 'utf-8'))
		msg['From'] = self._format_addr('Python爱好者 <%s>' % from_addr)
		msg['To'] = self._format_addr('管理员 <%s>' % to_addr)
		msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()

		# with open(r'C:\Users\hem4\Desktop\2016-8-25.zip', 'rb') as f:
		with open(self.localImgPath+'.zip', 'rb') as f:
			mime = MIMEBase('image', 'jpg', filename = '2016-8-25.zip')
			mime.add_header('Content-Disposition', 'attachment', filename='2016-8-25.zip')
			mime.add_header('Content-ID', '<0>')
			mime.add_header('X-Attachment-Id', '0')
			mime.set_payload(f.read())
			encoders.encode_base64(mime)
			msg.attach(mime)
		try:
			server = smtplib.SMTP(smtp_server, 587)
			server.starttls()
			server.set_debuglevel(1)
			server.login(from_addr, password)
			server.sendmail(from_addr, to_addr, msg.as_string())
			server.quit()
			print('File send successful!!!')
		except Exception as e:
			print(str(e))


if __name__ == '__main__':
	getimage = bugGetImg()
	pageUlr = getimage.getHtml(1,10)
	pool = ThreadPool(13)
	result = pool.map(getimage.downloadImg, pageUlr)
	pool.close()
	print("Download has finished.")
	# pool.join()
	getimage.zipImg()
	getimage.sendEmail()





