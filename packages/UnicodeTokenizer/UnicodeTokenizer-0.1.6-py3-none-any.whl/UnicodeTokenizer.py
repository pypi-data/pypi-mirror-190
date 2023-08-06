# -*- coding: utf-8 -*-

import unicodedata


class UnicodeTokenizer:
    def __init__(self,  do_lower_case=True, never_split=[], high_UnicodePoint=10000, remove_blank=True):
        self.do_lower_case = do_lower_case
        self.high_UnicodePoint = high_UnicodePoint
        self.never_split = set(x for x in never_split)
        self.remove_blank=remove_blank

    def is_blank(self,x):
        return not bool(x.strip())
    
    def split_blank(self,line):
        if not line:
            return []
        marks = [self.is_blank(x) for x in line]
        return self.split_marks(line,marks)

    # def split_marks1(self,line,marks):
    #     # slow
    #     starts=[i for i in range(len(marks) ) if i==0 or marks[i]!=marks[i-1] or marks[i] == None]
    #     tokens=[  line[x:starts[i+1]]  if i+1<len(starts) else line[i:]  for i,x in enumerate(starts) ]
    #     return tokens

    def split_marks(self,line,marks):
        tokens = []
        for i, x in enumerate(line):
            if i == 0:
                tokens.append(x)
            elif marks[i] or marks[i-1]:
                tokens.append(x)
            else:
                tokens[-1] += x
        return tokens
        
    def normalize(self, line,  normal_type="NFD"):
        l = unicodedata.normalize(normal_type, line)
        return l
    
    def split_high_UnicodePoint(self,line):
        if len(line) == 1:
            return [line]
        elif len(line) == 0:
            return []
        marks = [ord(x) >= self.high_UnicodePoint for x in line]
        return self.split_marks(line, marks)

    def split_category(self,line):
        if len(line) == 1:
            return [line]
        elif len(line) == 0:
            return []
        categorys = [unicodedata.category(x)[0] for x in line]
        names = [unicodedata.name(x).split(' ')[0] if categorys[i] in 'LN' else None for i, x in enumerate(line)]
        # marks=names  # not fast
        # starts=[i for i in range(len(marks) ) if i==0 or marks[i]!=marks[i-1] or marks[i] is None]
        # tokens=[  line[x:starts[i+1]]  if i+1<len(starts) else line[i:]  for i,x in enumerate(starts) ]
        # return tokens
        tokens = []
        for i, x in enumerate(line):
            if i == 0:
                tokens.append(x)
                continue
            if categorys[i] == categorys[i-1] == 'L':
                if names[i]==names[i-1]:
                    tokens[-1] += x
                else:
                    tokens.append(x)
                continue
            elif categorys[i] == categorys[i-1] == 'N':
                if names[i] == names[i-1]:
                    tokens[-1] += x
                else:
                    tokens.append(x)
                continue
            else:
                tokens.append(x)
        return tokens

    def split_line(self, line):
        words = self.split_blank(line)
        tokens = []
        for x in words:
            if x in self.never_split:
                tokens.append(x)
            else:
                if self.do_lower_case:
                    x = self.normalize(x.lower())
                us = self.split_blank(x)
                for u in us:
                    vs = self.split_high_UnicodePoint(u)
                    for v in vs:
                        w = self.split_category(v)
                        tokens += w
        return tokens

    def tokenize(self, line):
        if self.remove_blank:
            tokens=[]
            for word in line.split():
                tokens+=[x.strip() for x in  self.split_line(word) if x.strip()]  
        else:
            tokens=self.split_line(line)
        return tokens


if __name__ == "__main__":
    from logzero import logger


    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏２０１９\U0010ffff"
    # line = "art_new_word=True"
    tokenizer=UnicodeTokenizer()
    logger.info((tokenizer.split_blank(line)))
    # line = "=True"

    tokenizer = UnicodeTokenizer()
    logger.info(tokenizer.tokenize(line))
    import timeit
    # re=timeit.timeit("''.join(chr(x) for x in range(int(1e6))) ")
    # logger.info(re)

    import time
    t0 = time.time()
    for i in range(10000):
        # chr(i)  # ValueError: chr() arg not in range(0x110000)
        tokenizer.tokenize(line)
    t1 = time.time()
    logger.info(t1-t0)
