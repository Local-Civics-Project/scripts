import re
import os
import subprocess
import PyPDF2

class App:
  def __init__(self, filename):
    self.filename = filename
    self.content = ""
    self.blacklist = [
      "Incumbency",
      "Chart",
      "From",
      "To",
      "Period",
      "No.",
    ]

  def extractText(self):
    file = open("list.pdf", "rb")

    fileReader = PyPDF2.PdfFileReader(file)


    for page_no in range(fileReader.numPages):
      self.content += fileReader.getPage(page_no).extractText()

    return self.parseNames()

  def parseNames(self):
    arr = self.content.split()
    authorities = []

    for item in arr:
      if re.match("\d{2}/\d{2}/\d{4}", item):
        continue

      elif re.match("\d+\.", item) or item == "Sr.":
        authorities.append("")
        continue

      elif item in self.blacklist:
        continue

      else:
        authorities[-1] = (authorities[-1] + " " + item).strip()

    return authorities

if not os.path.isfile('./list.pdf'):
  subprocess.call(["wget", "-4", "-O", "list.pdf", "https://vmc.gov.in/pdf/Incumbency%20Chart%20(2018).pdf"])

app = App("list.pdf")

for name in app.extractText():
  print(name)
