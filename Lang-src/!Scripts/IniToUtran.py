# Task: someone edited INI instead of translation files
# And I have only Python on a limited computer

import xml.etree.ElementTree as ET
import xini
import xet

# Ini file, completely translated
IN_INI = "../cn/lang.ini"

# Some translation:
#  * completely translated (no bad/untranslated),
#  * roughly the same time as Ini (we do not track baddies)
#  * better the same settings as wanted (reference, pseudoloc...)
IN_TRANSL = "../ru.utran"

# Output file
OUT_FILE = "~cn.utran"

# Output language
OUT_LANG = "cn"

# Start: load INI
ini = xini.Ini(IN_INI, '.')
print(f'Loaded {ini.len()} INI strings.')

# Load XML
xml = ET.parse(IN_TRANSL)
root = xml.getroot()
cnt = xet.countStrings(root)
print(f'Loaded {cnt} XML strings.')

# Work
xet.fixupSettings(root, OUT_LANG)
nRet = xet.retranslate(root, ini)
print(f'Retranslated {nRet} strings.')

# Save
xml.write(OUT_FILE, 'utf-8')
