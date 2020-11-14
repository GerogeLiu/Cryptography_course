# 凯撒加密
def caesarCipher(shift, plaintext):
    plaintext = plaintext.upper()
    plainText = plaintext.replace(" ", "")
    cipherText = ''
    def caesarEncrypt(letter):
        return chr(65 + (ord(letter) % 65 + shift) % 26)
    for char in plainText:
        cipherText += caesarEncrypt(char)
    return cipherText

# 矩阵置换加密
def permutationCipher(keyword, plainText):
    """
    加密方法：
    1. 根据keyword的长度将plainText划分为若干rows
    最后不足的补充'x‘；
    2. 根据keyword中单词排列顺序得到对每个row进行打乱的方法
    """
    keyword = keyword.upper()
    cipher_length = len(keyword)
    cipher_list = []
    # keyword中字符在子母表中出现的顺序进行排序，放入cipher_list
    temp_list = list(map(ord, list(keyword)))
    sorte_temp = sorted(temp_list)
    d = dict(zip(sorte_temp, [i for i in range(len(temp_list))]))
    for temp in temp_list:
        cipher_list.append(d[temp])
    
    # 给plainText按照 cipher_length进行切割，不足补充'x'
    plainText = plainText.upper()
    need_add_x = cipher_length - len(plainText) % cipher_length
    newPlainText = plainText + 'X' * need_add_x
    # 按照cipher_length进行切割
    plain_text_list = re.findall(r'.{%d}' % cipher_length, newPlainText)
    #print(plain_text_list)
    def permutationEncrypt(cipher_list, text):
        res = ''
        for i in cipher_list:
            res += text[i]
        return res
    
    cipherText = ''
    for text_row in plain_text_list:
        cipherText += permutationEncrypt(cipher_list, text_row)

    return cipherText


def playFairCipher(keyword, plainText):
    """
    加密分为三步：
    1. 通过keyword 获得5*5的密码表(字母从左往右排列)
    2. 对明文进行两个字母一组的分组
    3. 分组后的明文通过密码表获得对应密文
    """
    keyword = keyword.upper()
    plainText = plainText.upper()
    cipherText = ''
    def getCipherTable(keyword):
        temp_list = []
        # 将 keyword 中的"J" 换成 "I"
        for char in keyword:
            if char not in temp_list:
                if char == 'J':
                    temp_list.append('I')
                else:
                    temp_list.append(char)
        # 找出25个(不包括"J"")不在temp_list中的大写字母，并将其排好序
        temp = sorted(list(set([chr(i) for i in range(65, 91) if i != 74]) - set(temp_list)))
        cipherTable = np.array(temp_list + temp).reshape(5, 5)
        return cipherTable
        #print(cipherTable)

    # step 2: 对 plainText 进行分组
    # 两个一组，如果为奇数个最后补 'X'；
    # 如果一组的两个字母相同，则需要将其拆开，前一个字母后添加"X"
    def cutPlainText(text):
        i = 0
        while i < len(text) - 1:
            if text[i] == text[i + 1]:
                text = text[:i+1] + 'X' + text[i+1:]
            i += 2
        if i < len(text):
            text += 'X'
        plain_text_list = re.findall(r'.{2}', text)
        return plain_text_list

    # step 3: 获取两个单词一组密文
    def playFairEncrypt(cipherTable, words):
        # 分别获得words中字母在 密码不能中的索引位置
        pos_x, pos_y = list(map(lambda x: tuple(np.argwhere(cipherTable == x)[0]), list(words)))
        # 如果在同一行, 同一列，以及其他情况时
        if pos_x[0] == pos_y[0]:
            cipher_x = cipherTable[pos_x[0]][(pos_x[1] + 1) % 5]
            cipher_y = cipherTable[pos_y[0]][(pos_y[1] + 1) % 5]
        elif pos_x[1] == pos_y[1]:
            cipher_x = cipherTable[(pos_x[0] + 1) % 5][pos_x[1]]
            cipher_y = cipherTable[(pos_y[0] + 1) % 5][pos_y[1]]
        else:
            cipher_x = cipherTable[pos_x[0]][pos_y[1]]
            cipher_y = cipherTable[pos_y[0]][pos_x[1]]
        return cipher_x + cipher_y

    cipherTable = getCipherTable(keyword)
    plain_text_list = cutPlainText(plainText)
    for words in plain_text_list:
        cipherText += playFairEncrypt(cipherTable, words)

    return cipherText



# 解密
def decryptCaesarCipher(shift, text):
    text = text.upper()
    text = text.replace(" ", "")
    decrypted_text = ''
    for char in text:
        decrypted_text += chr(65 + (ord(char) % 65 - shift) % 26)

    return decrypted_text


def decryptPermutationCipher(keyword, text):
    keyword = keyword.upper()
    cipher_length = len(keyword)
    # 检查text长度，如果不是cipher_length的整数倍则报错
    assert len(text) % cipher_length == 0, '待解密字符串长度与keyword长度不匹配'
    cipher_list = []
    # keyword中字符在子母表中出现的顺序进行排序，放入cipher_list
    temp_list = list(map(ord, list(keyword)))
    sorte_temp = sorted(temp_list)
    d = dict(zip(sorte_temp, [i for i in range(len(temp_list))]))
    for temp in temp_list:
        cipher_list.append(d[temp])
    cipherText_list = re.findall(r'.{%d}' % cipher_length, text)
    decrypted_text = '' 
    for cipherText_row in cipherText_list:
        temp = ['' for _ in cipherText_row]
        for i, j in zip(cipher_list, cipherText_row):
            temp[i] = j
        decrypted_text += ''.join(temp)
    return decrypted_text
         

def decryptPlayfairCipher(keyword, text):
    keyword = keyword.upper()
    text = text.upper()
    decryptText = ''
    def getCipherTable(keyword):
        temp_list = []
        # 将 keyword 中的"J" 换成 "I"
        for char in keyword:
            if char not in temp_list:
                if char == 'J':
                    temp_list.append('I')
                else:
                    temp_list.append(char)
        # 找出25个(不包括"J"")不在temp_list中的大写字母，并将其排好序
        temp = sorted(list(set([chr(i) for i in range(65, 91) if i != 74]) - set(temp_list)))
        cipherTable = np.array(temp_list + temp).reshape(5, 5)
        return cipherTable
        #print(cipherTable)

    # step 2: 判断text是否与keyword匹配
    def cutPlainText(text):
        plain_text_list = re.findall(r'.{2}', text)
        return plain_text_list

    # step 3: 获取两个单词一组密文
    def playFairEncrypt(cipherTable, words):
        # 分别获得words中字母在 密码不能中的索引位置
        pos_x, pos_y = list(map(lambda x: tuple(np.argwhere(cipherTable == x)[0]), list(words)))
        # 如果在同一行, 同一列，以及其他情况时
        if pos_x[0] == pos_y[0]:
            cipher_x = cipherTable[pos_x[0]][(pos_x[1] - 1) % 5]
            cipher_y = cipherTable[pos_y[0]][(pos_y[1] - 1) % 5]
        elif pos_x[1] == pos_y[1]:
            cipher_x = cipherTable[(pos_x[0] - 1) % 5][pos_x[1]]
            cipher_y = cipherTable[(pos_y[0] - 1) % 5][pos_y[1]]
        else:
            cipher_x = cipherTable[pos_x[0]][pos_y[1]]
            cipher_y = cipherTable[pos_y[0]][pos_x[1]]
        return cipher_x + cipher_y

    cipherTable = getCipherTable(keyword)
    assert len(text) % 2 == 0, '待解密字符串长度不符合解密条件'
    plain_text_list = cutPlainText(text)
    for words in plain_text_list:
        decryptText += playFairEncrypt(cipherTable, words)

    return decryptText
