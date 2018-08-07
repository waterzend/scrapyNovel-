# -*- coding: utf-8 -*-
import pymysql
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.shared import Inches
import re


def clear(html):
    pattern = re.compile('<div id="content[\s|\S]*script></div>')
    list_html = pattern.split(html)
    fileter_html = filter(None, list_html)
    pattern_other = re.compile('[<br>|</div>]')
    clear = pattern_other.split(fileter_html[0])
    return "".join(clear)


db = pymysql.connect("127.0.0.1", "root", "root", "yunxizhuan", charset='utf8')
cursor = db.cursor()
sql = "select * from content "
document = Document()
document.add_heading(u'芸汐传', 0)
try:
    cursor.execute(sql)
    print(cursor.rownumber)
    result = cursor.fetchone()
    while result != None:
        title = result[1]
        document.add_heading(title, 1)
        content = clear(result[2])
        paragraph = document.add_paragraph(content)
        result = cursor.fetchone()

except:
    print("error")
document.save('demoyunxi.docx')
db.close()
