import re

def convert_to_numeric_representation(plaintext, blockSize, padding='A'):
    """
    params: plaintext, str
            block_size, int
            padding, string: let The length of the plaintext is equal to an integer multiple of the block size
    return int
    """
    plaintext = plaintext.upper()
    plaintext = plaintext.replace(' ', '')
    # 对 plaintext 按照 block_size 的大小进行分组，最后不足 block_size的部分补充 A
    r = len(plaintext) % blockSize
    plaintext += padding * (blockSize - r) if r != 0 else ''
    #print(plaintext, f'len = {len(plaintext)}')

    textlist = re.findall(r'.{%d}' % blockSize, plaintext)
    #print(textlist)
    
    res = []
    for text in textlist:
        ans = 0
        for index, char in enumerate(text):
            ans += (ord(char) - 65) * 26 ** (blockSize - index - 1)
        res.append(ans)

    return res
    
# 将数字转字母
def convert_to_string(numlist, blockSize):
    """
    params: numlist, list
            blockSize: int
    return: string
    """
    res = ''
    for num in numlist:
        temp = []
        while num > 0:
            r = num % 26
            num = num // 26
            temp.append(r)
        diff = blockSize - len(temp) 
        temp += [0] * diff if diff > 0 else []
        res += ''.join([chr(i + 65) for i in temp[::-1]])

    return res

