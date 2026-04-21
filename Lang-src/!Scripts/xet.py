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
        newPrefix = _stickIds(prefix, newId)
        translation = ini.at(newPrefix)
        if translation is None:
            raise Exception(f'Cannot translate {newPrefix}')

def retranslate(root : ET.Element, ini : xini.Ini):
    hFile = root.find('file')
    if hFile is None:
        raise Exception("Cannot find <file> in UTran for some reason")
    return _retranslateRec(hFile, ini, '')
