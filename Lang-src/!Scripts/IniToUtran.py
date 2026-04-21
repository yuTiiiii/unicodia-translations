# Task: someone edited INI instead of translation files
# And I have only Python on a limited computer

import xini

# Ini file, completely translated
INIFILE = "../cn/lang.ini"

# Some translation, completely translated (no bad/untranslated),
# roughly the same time as Ini
TRANSLATION = "../ru.utran"

OUTFILE = "cn.utran"
WANTED_LANG = "cn"

ini = xini.Ini(INIFILE, '.')
print(f'Loaded {ini.len()} INI strings')
