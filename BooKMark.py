#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string

class BookMark():

    def __init__(self):
	self.directory = os.path.join(os.getcwd(), "kindle_hls")
	self.input_file_path = os.path.join(os.getcwd(), "My Clippings.txt")

    def readTitleAndContent(self):
	with open(self.input_file_path, "r", encoding = "utf8") as f:
	    file_details = f.read()
	    test = file_details.split("==========")
	    del test[len(test) - 1]
	    title_update = ""
	    content_update = {}

	    for i in range(len(test)):
		line = test[i].split("\n")
		if line[0]:
		    title = line[0]
		    content = line[3]
		else:
		    title = line[1]
		    content = line[4]

		if title in content_update.keys():
		    content_update.get(title).append(content)
		else:
		    content_update[title] = []
		    content_update.get(title).append(content)
	return content_update


    def writeAllBooks(self, content_update):
	for title in content_update.keys():
	    self.writeSingleBookToFile(title, content_update)

    def writeSingleBookToFile(self, title, content_update):
        title_update = title
	if(title_update.find(":") >= 0):
	    title_update = title_update.replace(":","：")
	output_file_path = os.path.join(self.directory, u"%s.txt" % title_update.strip())

	with open(output_file_path, 'w', encoding = "utf8") as wf:
	    writerBufferList = []
	    for i in range(len(content_update.get(title))):
		writerBufferList.append(str(i + 1) + ":  " + content_update.get(title)[i].strip())
	    wf.write("\n\n" + "\n\n\n".join(writerBufferList))

    def directoryCheck(self):
	if not os.path.exists(self.directory):
	    os.makedirs(self.directory)
	return

    def main(self):
	self.directoryCheck()
	content_update = self.readTitleAndContent()
	self.writeAllBooks(content_update)

if __name__ == '__main__':
	print("Processing...")
	s = BookMark()
	s.main()
	print("Done...")
