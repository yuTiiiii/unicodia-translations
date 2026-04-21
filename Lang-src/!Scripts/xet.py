# My work with ElementTree

import xml.etree.ElementTree as ET
import xini

def _countStringsRec(node : ET.Element) -> int:
    sum = 0
    for v in node.findall('group'):
        sum += _countStringsRec(v);
    sum += len(node.findall('text'))
    return sum

def countStrings(root : ET.Element) -> int:
    hFile = root.find('file')
    if hFile is None:
        raise Exception('Cannot find <file> in UTran for some reason')
    return _countStringsRec(hFile)

def fixupSettings(root : ET.Element, outLang : string):
    hInfo = root.find('info')
    if hInfo is None:
        raise Exception('Cannot find <info> in UTran for some reason')
    hTransl = hInfo.find('transl')
    if hTransl is None:
        raise Exception('Cannot find <info/transl> in UTran for some reason')
    hTransl.attrib['lang'] = outLang

def _unescapeSlashes(x : string, id : string) -> string:
    pos = 0
    iReplacement = 0
    xOld = x
    while True:
        pSlash = x.find('\\', pos)
        # not found / last
        if pSlash < 0:
            break
        if pSlash + 1 >= len(x):
            raise Exception(f'Strange ending escape in <{id}>')
        nextc = x[pSlash + 1]
        if nextc == '\\':
            x = x[:pSlash] + '\\' + x[(pSlash + 2):]
            pos = pSlash + 2
        elif nextc == 'n':
            x = x[:pSlash] + '\n' + x[(pSlash + 2):]
            pos = pSlash + 2
        else:
            raise Exception(f'Strange escape \\{nextc} in <{id}>')
        iReplacement = iReplacement + 1
        if iReplacement >= 30:
            raise Exception(f'Too many replacements in <{id}>, before <{xOld}>, after <{x}>')
    if len(x) + iReplacement != len(xOld):
        raise Exception(f'Escaped length mismatch in <{id}>')
    return x        

def _hackTranslation(hString : ET.Element, iniTransl : string, id : string):
    realTransl = _unescapeSlashes(iniTransl, id)

def _stickIds(prefix : string, suffix : string):
    if prefix == '':
        return suffix
    return prefix + '.' + suffix

def _retranslateRec(node : ET.Element, ini : xini.Ini, prefix : string):
    index = 0
    for v in node.findall('group'):
        index = index + 1
        if not 'id' in v.attrib:
            raise Exception(f'Cannot find id in UTransl / {prefix} / group #{index}')
        newId = v.attrib['id']
        if newId == '':
            raise Exception(f'Empty id in UTransl / {prefix} / group #{index}')
        newPrefix = _stickIds(prefix, newId)
        _retranslateRec(v, ini, newPrefix)
    index = 0
    for v in node.findall('text'):
        index = index + 1
        if not 'id' in v.attrib:
            raise Exception(f'Cannot find id in UTransl / {prefix} / string #{index}')
        newId = v.attrib['id']
        if newId == '':
            raise Exception(f'Empty id in UTransl / {prefix} / string #{index}')
        newBigId = _stickIds(prefix, newId)
        translation = ini.at(newBigId)
        if translation is None:
            raise Exception(f'Cannot translate {newPrefix}')
        _hackTranslation(v, translation, newBigId)

def retranslate(root : ET.Element, ini : xini.Ini):
    hFile = root.find('file')
    if hFile is None:
        raise Exception("Cannot find <file> in UTran for some reason")
    return _retranslateRec(hFile, ini, '')
