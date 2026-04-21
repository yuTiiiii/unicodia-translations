# Task: someone edited INI instead of translation files
# And I have only Python on a limited computer

import xml.etree.ElementTree as ET
import xini

# Ini file, completely translated
IN_INI = "../cn/lang.ini"

# Some translation:
#  * completely translated (no bad/untranslated),
#  * roughly the same time as Ini
#  * better the same settings as wanted (reference, pseudoloc...)
IN_TRANSL = "../ru.utran"

# Output file
OUT_FILE = "cn.utran"

# Output language
OUT_LANG = "cn"

# Start: load INI
ini = xini.Ini(IN_INI, '.')
print(f'Loaded {ini.len()} INI strings.')

xml = ET.parse(IN_TRANSL)
root = xml.getroot()

def countStringsRec(node):
    sum = 0
    for v in node.findall('group'):
        sum += countStringsRec(v);
    sum += len(node.findall('text'))
    return sum

def countStrings(node):
    hFile = node.find('file')
    if hFile is None:
        raise Exception("Cannot find <file> un UTran for some reason")
    return countStringsRec(hFile)

cnt = countStrings(root)
print(f'Loaded {cnt} XML strings.')
