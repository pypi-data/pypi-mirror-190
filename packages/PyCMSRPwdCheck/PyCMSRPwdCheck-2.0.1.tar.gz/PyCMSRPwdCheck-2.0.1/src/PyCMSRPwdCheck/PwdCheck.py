#coding=utf-8
__author__ = 'yujingrong'

import importlib, sys, enum
importlib.reload(sys)

keys = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']','\\'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '','\''],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'],
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=']]

keys2 = [['1', 'q', 'a', 'z'],
        ['2', 'w', 's', 'x'],
        ['3', 'e', 'd', 'c'],
        ['4', 'r', 'f', 'v'],
        ['5', 't', 'g', 'b'],
        ['6', 'y', 'h', 'n'],
        ['7', 'u', 'j', 'm'],
        ['8', 'i', 'k', ','],
        ['9', 'o', 'l', '.'],
        ['0', 'p', '', '/'],
        ['-', '[', '\'']]

keys3 = [['a', 'w', '3'],
        ['z', 's', 'e', '4'],
        ['x', 'd', 'r', '5'],
        ['c', 'f', 't', '6'],
        ['v', 'g', 'y', '7'],
        ['b', 'h', 'u', '8'],
        ['n', 'j', 'i', '9'],
        ['m', 'k', 'o', '0'],
        [',', 'l', 'p', '-'],
        ['.', '', '[', '='],
        ['/', '\'', ']']]

keys4 = [['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],]

R0_DEFAULT_SUCCESS = ("00000","口令满足安全要求")
R0_DEFAULT_ERROR = ("00C00","口令不满足安全要求")
R1_RANGE_ERROR = ("01C01","口令长度应至少8位")
R2_DIGIT_ERROR = ("02C01","口令应包括数字")
R2_LOWER_CASE_ERROR = ("02C02","口令应包括小写字母")
R2_UPPER_CASE_ERROR = ("02C03","口令应包括大写字母")
R2_SPECIAL_CHAR_ERROR = ("02C04","口令应包括特殊字符")
R2_GROUP_CHECK_ERROR = ("02C05","口令应包括数字、小写字母、大写字母、特殊符号4类中至少3类")
R3_COMPLETE_NAME_CHECK_ERROR = ("03C04","口令中不得包含用户名的完整或连续五位字符串（包括大小写变位或形似变换）")
R4_THREE_CHARS_DUPLICATE_ERROR = ("04C01","口令中不能出现3位以上（含三位）重复字母、数字、特殊字符")
R5_CHAR_SERIAL_ERROR = ("05C01","禁止键盘排序口令")

class PwdCheck:
    def __init__(self):
        self.__code = R0_DEFAULT_ERROR[0]
        self.__msg = R0_DEFAULT_ERROR[1]

    def setCode(self, code):
        self.__code = code

    def getCode(self):
        return self.__code

    def setMsg(self, msg):
        self.__msg = msg

    def getMsg(self):
        return self.__msg

    # 键盘连续性
    def isKeyboardContinuous(self, pwd):
        try:
            res = self.keyS(self.keyVariation(pwd, keys), self.keyVariation(pwd, keys2), self.keyVariation(pwd, keys3), self.keyVariation(pwd, keys4))
            if res:
                self.setCode(R5_CHAR_SERIAL_ERROR[0])
                self.setMsg(R5_CHAR_SERIAL_ERROR[1])
                return True
            else:
                return False
        except:
            self.setCode(R0_DEFAULT_ERROR[0])
            self.setMsg(R0_DEFAULT_ERROR[1])
            return True

    def keyS(self, b1, b2, b3, b4):
        if (1-b1) and (1-b2) and (1-b3) and (1-b4):
            return False
        return True

    def keyVariation(self, pwd, keys):
        isTrue = False
        pwdChars = self.getChars(pwd)
        list = []
        for k in range(len(pwdChars)):
            for i in range(len(keys)):
                for j in range(len(keys[i])):
                    if keys[i][j] == pwdChars[k]:
                        list.append(str(i) + "," + str(j))
        if list == []:
            return False
        index = 1
        tmpY = int(list[0].split(',')[0])
        tmpX = int(list[0].split(',')[1])
        for i in range(1, len(list)):
            y = int(list[i].split(",")[0])
            x = int(list[i].split(",")[1])
            if tmpY == y:
                if tmpX - x == -1:
                    tmpX = x
                    index += 1
                    if index > 2:
                        break
                    continue
                else:
                    tmpY = y
                    tmpX = x
                    index = 1
                    continue
            else:
                index = 1
                tmpX = x
                tmpY = y
        if index < 3:
            tmpY = int(list[0].split(",")[0])
            tmpX = int(list[0].split(",")[1])
            for i in range(1, len(list)):
                y = int(list[i].split(",")[0])
                x = int(list[i].split(",")[1])
                if tmpY == y:
                    if tmpX - x == 1:
                        tmpX = x
                        index += 1
                        if index > 2:
                            break
                        continue
                    else:
                        tmpY = y
                        tmpX = x
                        index = 1
                        continue
                else:
                    index = 1
                    tmpX = x
                    tmpY = y
        if index > 2:
            isTrue = True
        return isTrue


    # 特殊字符转换
    def getChars(self, pwd):
        pwdChars = pwd.lower()
        if "!" in pwdChars:
            pwdChars = pwdChars.replace("!", "1")
        if "@" in pwdChars:
            pwdChars = pwdChars.replace("@", "2")
        if "#" in pwdChars:
            pwdChars = pwdChars.replace("#", "3")
        if "$" in pwdChars:
            pwdChars = pwdChars.replace("$", "4")
        if "￥" in pwdChars:
            pwdChars = pwdChars.replace("￥", "4")
        if "%" in pwdChars:
            pwdChars = pwdChars.replace("%", "5")
        if "^" in pwdChars:
            pwdChars = pwdChars.replace("^", "6")
        if "&" in pwdChars:
            pwdChars = pwdChars.replace("&", "7")
        if "*" in pwdChars:
            pwdChars = pwdChars.replace("*", "8")
        if "(" in pwdChars:
            pwdChars = pwdChars.replace("(", "9")
        if ")" in pwdChars:
            pwdChars = pwdChars.replace("*", "0")
        if "_" in pwdChars:
            pwdChars = pwdChars.replace("_", "-")
        if "+" in pwdChars:
            pwdChars = pwdChars.replace("+", "=")
        if "{" in pwdChars:
            pwdChars = pwdChars.replace("{", "[")
        if "}" in pwdChars:
            pwdChars = pwdChars.replace("}", "]")
        if "|" in pwdChars:
            pwdChars = pwdChars.replace("|", "\\")
        if ":" in pwdChars:
            pwdChars = pwdChars.replace(":", "")
        if "\"" in pwdChars:
            pwdChars = pwdChars.replace("\"", "\'")
        if "<" in pwdChars:
            pwdChars = pwdChars.replace("<", ",")
        if ">" in pwdChars:
            pwdChars = pwdChars.replace(">", ".")
        if "?" in pwdChars:
            pwdChars = pwdChars.replace("?", "/")
        return pwdChars

    # 用户无关性校验
    def isUserContact(self, pwd, name):
        try:
            if name is None:
                self.setCode(R0_DEFAULT_ERROR[0])
                self.setMsg(R0_DEFAULT_ERROR[1])
                return True
            newName = self.toChangeCharSimilar(name)
            newPwd = self.toChangeCharSimilar(pwd)
            if newName in newPwd:
                self.setCode(R3_COMPLETE_NAME_CHECK_ERROR[0])
                self.setMsg(R3_COMPLETE_NAME_CHECK_ERROR[1])
                return True
            if len(newName) > 5:
                for i in range(len(newName) - 4):
                    substring = newName[i:(i+5)]
                    if substring in newPwd:
                        self.setCode(R3_COMPLETE_NAME_CHECK_ERROR[0])
                        self.setMsg(R3_COMPLETE_NAME_CHECK_ERROR[1])
                        return True
                return False
            return False
        except:
            self.setCode(R0_DEFAULT_ERROR[0])
            self.setMsg(R0_DEFAULT_ERROR[1])
            return True

    # 判断连续三次重复字符
    def threeTimesChar(self, pwd):
        try:
            chars = self.getChars(pwd)
            for i in range(len(chars)-2):
                if chars[i] == chars[i+1]:
                    if chars[i] == chars[i+2]:
                        self.setCode(R4_THREE_CHARS_DUPLICATE_ERROR[0])
                        self.setMsg(R4_THREE_CHARS_DUPLICATE_ERROR[1])
                        return True
            return False
        except:
            self.setCode(R0_DEFAULT_ERROR[0])
            self.setMsg(R0_DEFAULT_ERROR[1])
            return True

    # 形相似字符串转换
    def toChangeCharSimilar(self, name):
        pwdLower = name.lower()
        if "!" in pwdLower:
            pwdLower = pwdLower.replace("!", "1")
        if "o" in pwdLower:
            pwdLower = pwdLower.replace("o", "0")
        if "i" in pwdLower:
            pwdLower = pwdLower.replace("i", "1")
        if "z" in pwdLower:
            pwdLower = pwdLower.replace("z", "2")
        if "@" in pwdLower:
            pwdLower = pwdLower.replace("@", "a")
        if "$" in pwdLower:
            pwdLower = pwdLower.replace("$", "s")
        if "l" in pwdLower:
            pwdLower = pwdLower.replace("l", "1")
        if "|" in pwdLower:
            pwdLower = pwdLower.replace("|", "1")
        if "&" in pwdLower:
            pwdLower = pwdLower.replace("&", "8")
        if "s" in pwdLower:
            pwdLower = pwdLower.replace("s", "5")
        if "@" in pwdLower:
            pwdLower = pwdLower.replace("@", "a")
        if "q" in pwdLower:
            pwdLower = pwdLower.replace("q", "9")
        return pwdLower

    # 全角字符串转半角字符串
    def ToDBc(self, input):
        rstring = ""
        for uchar in input:
            inside_code = ord(uchar)
            if inside_code == 12288:                            # 全角空格直接转换
                inside_code = 32
            elif 65281 <= inside_code <= 65374:   				# 全角字符（除空格）根据关系转化
                inside_code -= 65248
            rstring += chr(inside_code)
        return rstring

    # 判断字符串中是否含有中文或者中文字符
    def isChinese(self, str):
        for ch in str.encode("utf-8").decode("utf-8"):
            if u'\u4e00' <= ch <= u'\u9fff':
                self.setCode(R2_GROUP_CHECK_ERROR[0])
                self.setMsg(R2_GROUP_CHECK_ERROR[1])
                return True
        return False

    # 判断是否包含空格
    def isIncludeEmpty(self, str):
        try:
            if " " in str:
                return True
        except:
            return False

    # 特殊字符、数字、大写字母、小写字母 4选3
    def isLetterDigit(self, s):
        if (len(s) > 16) or (len(s) < 8):
            self.setCode(R1_RANGE_ERROR[0])
            self.setMsg(R1_RANGE_ERROR[1])
            return False
        isDigit = 0
        isUpper = 0
        islower = 0
        isSpecial = 0
        symbol= ['.','`','~', '!','$', '@', '#', '%', '^', '&', '*','{', '}',
                 '(', ')', '+','-', '=', '"', ',', '.', '?', '[', ']',
                 '\\','\'',':',';','|','/','<','>','?','_','.']
        for i in range(len(s)):
            if s[i].isupper():
                isUpper = 1
            if s[i].islower():
                islower = 1
            if s[i].isdigit:
                isDigit = 1
            if s[i] in symbol:
                isSpecial = 1
        isRight = isUpper + islower +isDigit + isSpecial
        if isRight >= 3:
            return True
        else:
            self.setCode(R2_GROUP_CHECK_ERROR[0])
            self.setMsg(R2_GROUP_CHECK_ERROR[1])
            return False

    #  弱口令校验的主方法，返回True表示是弱密码
    def checkPw(self, password, name):
        if password is None:
            self.setCode(R0_DEFAULT_ERROR[0])
            self.setMsg(R0_DEFAULT_ERROR[1])
            return True
        if self.isChinese(password):
            return True
        password = self.ToDBc(password)
        if int(self.isLetterDigit(password)) == 0:
            return True
        if self.isKeyboardContinuous(password):
            return True
        if self.threeTimesChar(password):
            return True
        if self.isUserContact(password, name):
            return True
        self.setCode(R0_DEFAULT_SUCCESS[0])
        self.setMsg(R0_DEFAULT_SUCCESS[1])
        return False
