import random


class Node(object):
    def __init__(self, id, element="exp", left=None, right=None):
        self.element = element
        self.left = left
        self.right = right
        self.attri = ""
        self.id = id


# 全局变量
node_id = 0  # 记录每个node的id方便后续在随机池中检索
# 两种操作的次数控制在都不超过十次
bop = 0  # 在generate过程中记录bop的次数
uop = 0  # 在generate过程中记录uop的次数
operators = ["∨", "→", "∧"]
cv = ["p", "q", "r", "s", "T", "F"]
equRules = [
    '┐(p∧q) = ┐p∨┐q',  # 0
    '┐(p∨q) = ┐p∧┐q',  # 1
    'p∨(q∧r) = (p∨q)∧(p∨r)',  # 2
    '(q∧r)∨p = (p∨q)∧(p∨r)',  # 3 顺序可以调换
    'p∧(q∨r) = (p∧q)∨(p∧r)',  # 4
    '(q∨r)∧p = (p∧q)∨(p∧r)',  # 5
    'p→q = ┐p∨q',  # 6
    'p→q = ┐q→┐p',  # 7
    '(p→q)∨(p→r) = p→(q∨r)',  # 8
    '(p→r)∨(q→r) = (p∧q)→r)',  # 9
    '(p→q)∧(p→r) = p→(q∧r)',  # 10
    '(p→r)∧(q→r) = (p∨q)→r)',  # 11
    '┐(┐q) = q',  # 12
]
pool = []  # 随机池


def generate(node):
    global node_id
    global operators
    global cv
    global bop, uop
    option = random.randint(1, 3)  # 随机选取一种操作 1：bop 2：uop 3：exp赋值
    if option == 1 and bop < 10:
        operator = random.choice(operators)
        node_id += 1
        node_left = Node(node_id)
        node_id += 1
        node_right = Node(node_id)
        node.element = operator
        node.left = node_left
        node.right = node_right
        bop += 1
        generate(node_left)
        generate(node_right)
    elif option == 2 and uop < 10:
        node.element = "┐"
        node_id += 1
        child = Node(node_id)
        node.left = child
        uop += 1
        generate(child)
    else:
        val = random.choice(cv)
        node.element = val
    return

def update(root):
    # 从底部依次update每个node的attri，检查整棵树的attri只需要root的attri即可
    if root.left == None and root.right == None:
        root.attri = root.element
        return
    elif root.left != None and root.right == None:
        update(root.left)
        root.attri = "(" + root.element + root.left.attri + ")"
        return
    else:
        update(root.left)
        update(root.right)
        root.attri = "(" + root.left.attri + root.element + root.right.attri + ")"
        return

# ∨
# →
# ∧
# ┐

def check(root):
    # 找到能使用equivalent rule进行变换的tree structure，并将其node的id及其对应的equivalent rule加入随机池
    if root.left == None and root.right == None:
        return
    if root.element == '┐':
        if root.left.element == '∧':
            tmp = [root.id, 0]  # tmp[nodeID, equRules]
            pool.append(tmp)
        if root.left.element == '∨':
            tmp = [root.id, 1]
            pool.append(tmp)
        if root.left.element == '┐':
            tmp = [root.id, 12]
            pool.append(tmp)
        check(root.left)
    elif root.element == '∨':
        if root.right.element == '∧':
            tmp = [root.id, 2]
            pool.append(tmp)
        elif root.left.element == '∧':
            tmp = [root.id, 3]
            pool.append(tmp)
        elif root.left.element == '→' and root.right.element == '→':
            if root.left.left.attri == root.right.left.attri:
                tmp = [root.id, 8]
                pool.append(tmp)
            if root.left.right.attri == root.right.right.attri:
                tmp = [root.id, 9]
                pool.append(tmp)
        check(root.left)
        check(root.right)
    elif root.element == '∧':
        if root.right.element == '∨':
            tmp = [root.id, 4]
            pool.append(tmp)
        elif root.left.element == '∨':
            tmp = [root.id, 5]
            pool.append(tmp)
        elif root.left.element == '→' and root.right.element == '→':
            if root.left.left.attri == root.right.left.attri:
                tmp = [root.id, 10]
                pool.append(tmp)
            if root.left.right.attri == root.right.right.attri:
                tmp = [root.id, 11]
                pool.append(tmp)
        check(root.left)
        check(root.right)
    elif root.element == '→':
        tmp1 = [root.id, 6]
        pool.append(tmp1)
        tmp2 = [root.id, 7]
        pool.append(tmp2)
        check(root.left)
        check(root.right)

def transform_0(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '∨'
        p = root.left.left
        q = root.left.right
        node_left = Node(node_id, '┐')
        node_left.left = p
        node_id += 1
        node_right = Node(node_id, '┐')
        node_right.left = q
        node_id += 1
        root.left = node_left
        root.right = node_right
        return
    transform_0(root.left, id)
    if root.right is not None:
        transform_0(root.right, id)


def transform_1(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '∧'
        p = root.left.left
        q = root.left.right
        node_left = Node(node_id, '┐', p)
        node_id += 1
        node_right = Node(node_id, '┐', q)
        node_id += 1
        root.left = node_left
        root.right = node_right
        return
    transform_1(root.left, id)
    if root.right is not None:
        transform_1(root.right, id)

def transform_2(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '∧'
        p = root.left
        q = root.right.left
        r = root.right.right
        node_left = Node(node_id, '∨')
        node_left.left = p
        node_left.right = q
        node_id += 1
        node_right = Node(node_id, '∨')
        node_right.left = p
        node_right.right = r
        node_id += 1
        root.left = node_left
        root.right = node_right
        return
    else:
        transform_2(root.left, id)
    if root.right is not None:
        transform_2(root.right, id)

def transform_3(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '∧'
        p = root.left.left
        r = root.left.right
        q = root.right
        node_left = Node(node_id, '∨')
        node_left.left = p
        node_left.right = q
        node_id += 1
        node_right = Node(node_id, '∨')
        node_right.left = p
        node_right.right = r
        node_id += 1
        root.left = node_left
        root.right = node_right
        return
    else:
        transform_3(root.left, id)
    if root.right is not None:
        transform_3(root.right, id)

def transform_4(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '∨'
        p = root.left
        q = root.left.left
        r = root.right.right
        node_left = Node(node_id, '∧')
        node_left = p
        node_id += 1
        node_right = Node(node_id, '∧')
        node_right.left = q
        node_right.right = r
        node_id += 1
        root.left = node_left
        root.right = node_right
        return
    else:
        transform_4(root.left, id)
    if root.right is not None:
        transform_4(root.right, id)

def transform_5(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '∨'
        p = root.right
        q = root.left.left
        r = root.left.right
        node_left = Node(node_id, '∧')
        node_id += 1
        node_right = Node(node_id, '∧')
        node_id += 1
        node_left.left = q
        node_left.right = r
        node_right.left = p
        node_right.right = r
        root.left = node_left
        root.right = node_right
        return
    else:
        transform_5(root.left, id)
    if root.right is not None:
        transform_5(root.right, id)

def transform_12(root, id):
    if root.left == None and root.right == None:
        return
    if root.id == id:
        temp = root.left.left
        root.id = temp.id
        root.element = temp.element
        root.left = temp.left
        root.right = temp.right
        return
    transform_12(root.left, id)
    if root.right is not None:
        transform_12(root.right, id)


test = Node(node_id)
generate(test)
update(test)
print(test.attri)
check(test)
print("随机池:", pool)
for i in pool:
    if i[1] == 0:
        transform_0(test, i[0])
        update(test)
        pool = []
        check(test)
        print(test.attri)
        print("随机池：", pool)
    elif i[1] == 1:
        transform_1(test, i[0])
        update(test)
        pool = []
        check(test)
        print(test.attri)
        print("随机池：", pool)
    elif i[1] == 2:
        transform_2(test, i[0])
        update(test)
        pool = []
        check(test)
        print(test.attri)
        print("随机池：", pool)
    elif i[1] == 3:
        transform_3(test, i[0])
        update(test)
        pool = []
        check(test)
        print(test.attri)
        print("随机池：", pool)
    elif i[1] == 4:
        transform_4(test, i[0])
        update(test)
        pool = []
        check(test)
        print(test.attri)
        print("随机池：", pool)
    elif i[1] == 5:
        transform_5(test, i[0])
        update(test)
        pool = []
        check(test)
        print(test.attri)
        print("随机池：", pool)
    elif i[1] == 12:
        transform_12(test, i[0])
        update(test)
        pool = []
        check(test)
        print(test.attri)
        print("随机池：", pool)
#print(test.attri)
'''
newNode = Node(node_id)
newNode.element = '∧'
node_id += 1
nodeLeft = Node(node_id)
node_id += 1
nodeLeft.element = '∨'
nodeRight = Node(node_id)
node_id += 1
nodeRight.element = 'p'
newNode.left = nodeLeft
newNode.right = nodeRight
nodeLL = Node(node_id)
node_id += 1
nodeLR = Node(node_id)
node_id += 1
nodeLL.element = 'q'
nodeLR.element = 'r'
nodeLeft.left = nodeLL
nodeLeft.right = nodeLR
update(newNode)
print(newNode.attri)
transform_5(newNode, newNode.id)
update(newNode)
print(newNode.attri)
'''