# Simple INI support

def stripEol(x : string) -> string:
    if x.endswith('\r'):
        x = x[:len(x) - 1]
    if x.endswith('\n'):
        x = x[:len(x) - 1]
    return x

class Ini:
    def __init__(self, fname : string = '', separator : string = '.'):
        self.load(fname, separator)

    def load(self, fname : string, separator : string = '.'):
        self.data = dict()
        self.merge(fname, separator)

    def merge(self, fname : string, separator : string = '.'):
        currPrefix = ''
        if fname == '':
            return
        with open(fname, 'r', encoding='UTF-8') as file:
            for lno, line in enumerate(file, start=1):
                line = stripEol(line).lstrip()
                if (line == '') or line.startswith(';') \
                       or line.startswith('#'):
                    continue
                if line.startswith('['):
                    line = line[1:].rstrip()
                    if not line.endswith(']'):
                        raise Exception(f'Line {lno}: does not end with ]')
                    line = line[:len(line) - 1].strip()
                    if line == '':
                        currPrefix = ''
                    else:
                        currPrefix = line + separator
                else:
                    whereEq = line.find('=')
                    if whereEq < 0:
                        raise Exception(f'Line {lno}: equals = not found')
                    key = line[:whereEq].strip()
                    if key == '':
                        raise Exception(f'Line {lno}: empty key')
                    value = line[(whereEq + 1):]
                    if value.startswith('"'):
                        raise Exception(f'Line {lno}: starts with quote, unsupported')
                    self.data[currPrefix + key] = value

    def len(self):
        return len(self.data)

    def at(self, key : string):
        if key in self.data:
            return self.data[key]
        else:
            return None

