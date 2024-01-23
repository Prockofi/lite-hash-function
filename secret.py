from time import time

class Secret:
    def __init__(self) -> None:
        self.alfabet = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzАаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ђѓєѕіїјљњћќѝўџѠѡѢѤѥѦѧѨѩѪѫѬѭѮѯѰѱѲѳѴѵѶѷѸѹѺѻѼѽѾѿҀҋҌҍҎҏҐґҒғҔҕҖҗҘҙҚқҜҝҞҟҠҡҢңҤҥҦҧҨҩҪҫҬҭҮүҲҳҴҵҶҷҸҹҺһҼҽҾꚗ'

    def hash(self, data: str, step: int=128, ln: int=16) -> str:
        res = [bin(self.alfabet.index(char))[2:].zfill(8) for char in data]
        for iteration in range(step):
            for i1 in range(len(res)):
                for i2 in range(len(res)):
                    if i1 != i2:
                        res[i2] = self.matching(res[i1], res[i2])
            num = int(''.join([str(int(el, 2)) for el in res]))
            num = str(num**3)
            result = ''
            for i in range(len(num)):
                try:
                    line = int(num[i] + num[i+1] + num[i+2])
                    if line >= 256:
                        line = int(num[i] + num[i+1])
                except:
                    line = int(num[i])
                result += self.alfabet[line]
            result = result[:ln]
            res = [(bin(self.alfabet.index(x))[2:]).zfill(8) for x in result]
        res_hash = ''
        for el in res:
            res_hash += self.alfabet[int(el, 2)]
        return res_hash

    def gen(self, salt: int=round(time()), ln: int=16)  -> str:
        result = []
        salt = str(salt)
        while len(salt) < ln*3:
            salt = str(int(salt[:round((len(salt)/2))]) * int(salt[round(len(salt)/2):])**2)
            salt = salt.replace('0', '2', salt.count('0'))
        salt = salt[:ln]
        for i in range(len(salt)):
            try:
                index = int(salt[i] + salt[i+1] + salt[i+2])
                if index >= 256:
                    index = int(salt[i] + salt[i+1])
            except:
                index = int(salt[i])
            result.append(self.alfabet[index])
        return ''.join(result)

    def matching(self, mask: str, val: str) -> str:
        result = ''
        for i in range(8):
            if mask[i] == '1':
                if val[i] == '1':
                    result += '0'
                else:
                    result += '1'
            else:
                result += val[i]
        return result

    def key(self, key: str):
        self.key = key

    def cripto(self, data: str) -> str:
        if len(self.key) > len(data):
            key = self.key[:len(data)]
        if len(self.key) < len(data):
            key = (self.key*((len(data)-len(self.key))))[:len(data)]
            if key == '':
                key = self.key

        res = ''
        for i in range(len(key)):
            el = bin(self.alfabet.index(data[i]))[2:].zfill(8)
            el2 = bin(self.alfabet.index(key[i]))[2:].zfill(8)
            line = self.matching(el, el2)
            res += self.alfabet[int(line, 2)]
        return res