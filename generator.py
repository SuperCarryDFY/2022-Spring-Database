# 自动生成车架号和车牌号
import random

def car_number():
    font = ['京', '津', '冀', '晋', '蒙', '辽', '吉', '黑',
            '沪', '苏', '浙', '皖', '闽', '赣', '鲁', '豫', '鄂', '湘', '粤', '桂', '琼', '渝', '川', '贵', '云', '藏', '陕', '甘', '青', '宁', '新']
    alph = ["A","B",'C','D','E','F']
    alph2 = ["A","B",'C','D','E','F','G','H','I','J']
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    for _ in range(10):
        p1 = random.choice(font)
        p2 = random.choice(alph)
        p3 = random.choice(alph2)
        p4 = random.choice(numbers)
        p5 = random.choice(numbers)
        p6 = random.choice(numbers)
        p7 = random.choice(numbers)
        print(p1+p2+p3+p4+p5+p6+p7)

# car_number()

def VLN():
    Cset = '0123456789ABCDEFGHJKLMPRSTUVWXYZ'
    Clist = list(Cset)
    for _ in range(10):
        s = ''
        for index in range(17):
            s += random.choice(Clist)
        print(s)

VLN()
