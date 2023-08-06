import re
import math

def sort_file(data,reverse = False):
    Kanjiwithnumberonly = []
    kanjistartwithnumber = []
    kanjistartwithcharacter =[]
    kanjiwithcharacteronly = []
    numerals = '一二三四五六七八九十百千万億兆京'
    kanji_character = '^一二三四五六七八九十百千万億兆京'
    numerals_pattern = "|".join(numerals)
    for item in data:
        kanji_numbers = re.findall(f'[{numerals_pattern}]+',item)
        kanji = re.findall(f'[{kanji_character}]+',item)
        if item[0] in numerals:#(starting with kanjinumberonly or kanjinumber + kanji)
            if not kanji:
                Kanjiwithnumberonly.append((item,kanji_numbers,kanji_numbers))
            else:
                kanjistartwithnumber.append((item,kanji_numbers,kanji))
        else:
            if not kanji_numbers:
                kanjiwithcharacteronly.append((item))
            else:
                kanjistartwithcharacter.append((item,kanji_numbers,kanji))
    Kanjiwithnumberonly = [(x[0], ''.join(x[1]),''.join(x[2])) for x in Kanjiwithnumberonly]
    kanjistartwithnumber = [(x[0], ''.join(x[1]),''.join(x[2])) for x in kanjistartwithnumber]
    kanjistartwithcharacter = [(x[0], ''.join(x[1]),''.join(x[2])) for x in kanjistartwithcharacter]
    Kanjiwithnumberonly = sort_kanji(Kanjiwithnumberonly)
    kanjistartwithnumber = sort_kanji(kanjistartwithnumber)
    kanjistartwithcharacter = sort_kanji(kanjistartwithcharacter,1)
    kanji = sorted(kanjiwithcharacteronly)
    sorted_data = Kanjiwithnumberonly + kanjistartwithnumber + kanjistartwithcharacter
    sorted_data =[data[0] for data in sorted_data] + kanji
    if reverse:sorted_data.reverse()
    return sorted_data

def sort_kanji(string,flag = 0):
    data = []
    for item in string:
        result = item[1].translate(str.maketrans("零一二三四五六七八九拾", "0123456789十", ""))
        convert_table = {"十": "0", "百": "00", "千": "000", "万": "0000", "億": "00000000", "兆": "000000000000", "京": "0000000000000000"}
        unit_list = "|".join(convert_table.keys())
        while re.search(unit_list,result):
            for unit in convert_table.keys():
                zeros = convert_table[unit]
                for numbers in re.findall(f"(\d+){unit}(\d+)", result):
                    result = result.replace(numbers[0] + unit + numbers[1], numbers[0] + zeros[len(numbers[1]):len(zeros)] + numbers[1])
                for number in re.findall(f"(\d+){unit}", result):
                    result = result.replace(number + unit, number + zeros)
                for number in re.findall(f"{unit}(\d+)", result):
                    result = result.replace(unit + number, "1" + zeros[len(number):len(zeros)] + number)
                result = result.replace(unit, "1" + zeros)
        data.append((item[0],int(result),item[2]))
    if flag == 0:
        sorted_data = sorted(data,key=lambda x:(x[1],x[2]))
    else:
        sorted_data = sorted(data,key=lambda x:(x[2],x[1]))
    output_data = number2kanji(sorted_data)
   
    return output_data
       
def number2kanji(number,style = "all"):
    kanji = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}
    digits = (
        '', '万', '億', '兆', '京', '垓', '𥝱', '穣', '溝', '澗', '正', '載', '極', '恒河沙', '阿僧祇', '那由多',
        '不可思議',
        '無量大数')
    output = []
    for item in number:
        number = item[1]
        if style == "all":
            result = ""  # all letters will be added to this
            for i in range(math.ceil(math.log(number, 1000)), -1, -1):
                c_num = str((number % (10 ** ((i + 1) * 4))) // (10 ** (i * 4))).zfill(4)  # remainder
                c_str = ""
                if c_num == "0000":
                    continue
                if c_num[0] > "0":  # 1st digit
                    if c_num[0] != "1":
                        c_str += kanji[int(c_num[0])]
                    c_str += "千"
                if c_num[1] > "0":  # 2nd digit
                    if c_num[1] != "1":
                        c_str += kanji[int(c_num[1])]
                    c_str += "百"
                if c_num[2] > "0":  # 3rd digit
                    if c_num[2] != "1":
                        c_str += kanji[int(c_num[2])]
                    c_str += "十"
                if c_num[3] > "0":  # 4th digit
                    c_str += kanji[int(c_num[3])]
                if c_str:
                    result += c_str + digits[i]
            output.append((item[0],result))
    return output