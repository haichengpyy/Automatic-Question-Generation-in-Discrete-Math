import random
import numpy as np


class Node(object):
    def __init__(self, id, element, left=None, mid=None, right=None):
        self.element = element
        self.left = left
        self.mid = mid
        self.right = right
        self.attri = ""
        self.id = id


# 全局变量
node_id = 0  # 记录每个node的id方便后续在随机池中检索
# 两种操作的次数控制在都不超过十次
counter_e = 0
counter_t = 0
counter_u = 0
counter_r = 0
operators = ["∨", "→", "∧"]
cv = ["p", "q", "r", "s", "T", "F"]
equRules = [
    '┐(p∧q) = ┐p∨┐q',  # 0-
    '┐(p∨q) = ┐p∧┐q',  # 1-
    'p∨(q∧r) = (p∨q)∧(p∨r)',  # 2-
    '(q∧r)∨p = (p∨q)∧(p∨r)',  # 3 -顺序可以调换
    'p∧(q∨r) = (p∧q)∨(p∧r)',  # 4-
    '(q∨r)∧p = (p∧q)∨(p∧r)',  # 5-
    'p→q = ┐p∨q',  # 6
    'p→q = ┐q→┐p',  # 7zz
    '(p→q)∨(p→r) = p→(q∨r)',  # 8
    '(p→r)∨(q→r) = (p∧q)→r)',  # 9
    '(p→q)∧(p→r) = p→(q∧r)',  # 10
    '(p→r)∧(q→r) = (p∨q)→r)',  # 11
    '┐(┐q) = q',  # 12
]
pool = []  # 随机池
level = 0
probability = np.array([0.6, 0.4, 0.0])


def generate_nodes(elements):
    global node_id
    res = []
    for i in elements:
        new = Node(node_id, i)
        node_id += 1
        res.append(new)
    return res


def generate(node):
    global node_id
    global operators
    global cv
    global bop, uop
    global level
    global probability
    global counter_e, counter_t, counter_u, counter_r
    level += 1
    if level > 8:
        probability = np.array([0.05, 0.05, 0.9])
    option = np.random.choice([1, 2, 3], p=probability.ravel())  # 随机选取一种操作 1：bop 2：uop 3：exp赋值

    if node.element == 'E':
        if counter_e < 3:
            if option == 1:
                nodes = generate_nodes(['E', '→', 'T'])
                counter_e += 1
                node.left = nodes[0]
                node.mid = nodes[1]
                node.right = nodes[2]
                generate(node.left)
                generate(node.right)
            else:
                node_left = Node(node_id, 'T')
                node_id += 1
                node.left = node_left
                generate(node.left)
        else:
            node_left = Node(node_id, 'T')
            node_id += 1
            node.left = node_left
            generate(node.left)

    if node.element == 'T':
        if counter_t < 3:
            if option == 1:
                nodes = generate_nodes(['T', '∨', 'U'])
                counter_t += 1
                node.left = nodes[0]
                node.mid = nodes[1]
                node.right = nodes[2]
                generate(node.left)
                generate(node.right)
            else:
                node_left = Node(node_id, 'U')
                node_id += 1
                node.left = node_left
                generate(node.left)
        else:
            node_left = Node(node_id, 'U')
            node_id += 1
            node.left = node_left
            generate(node.left)

    if node.element == 'U':
        if counter_t < 3:
            if option == 1:
                nodes = generate_nodes(['U', '∧', 'R'])
                counter_u += 1
                node.left = nodes[0]
                node.mid = nodes[1]
                node.right = nodes[2]
                generate(node.left)
                generate(node.right)
            else:
                node_left = Node(node_id, 'R')
                node_id += 1
                node.left = node_left
                generate(node.left)
        else:
            node_left = Node(node_id, 'R')
            node_id += 1
            node.left = node_left
            generate(node.left)

    if node.element == 'R':
        if counter_r < 3:
            if option == 1:
                nodes = generate_nodes(['┐', 'R'])
                counter_r += 1
                node.left = nodes[0]
                node.right = nodes[1]
                generate(node.right)
            elif option == 2:
                nodes = generate_nodes(['(', 'E', ')'])
                node.left = nodes[0]
                node.mid = nodes[1]
                node.right = nodes[2]
                generate(node.mid)
            else:
                val = random.choice(cv)
                node_left = Node(node_id, val)
                node_id += 1
                node.left = node_left
        else:
            if option == 1:
                nodes = generate_nodes(['(', 'E', ')'])
                node.left = nodes[0]
                node.mid = nodes[1]
                node.right = nodes[2]
                generate(node.mid)
            else:
                val = random.choice(cv)
                node_left = Node(node_id, val)
                node_id += 1
                node.left = node_left
    return
    # if option == 1 and bop < 5:
    #     operator = random.choice(operators)
    #     # node_id += 1
    #     node_left = Node(node_id)
    #     node_id += 1
    #     # print("node id:",node_left.id,"  element:",node_left.element)
    #     node_right = Node(node_id)
    #     node_id += 1
    #     # print("node id:",node_right.id,"  element:",node_right.element)
    #     node.element = operator
    #     node.left = node_left
    #     node.right = node_right
    #     bop += 1
    #     generate(node_left)
    #     generate(node_right)
    # elif option == 2 and uop < 5:
    #     node.element = "┐"
    #
    #     child = Node(node_id)
    #     node_id += 1
    #     node.left = child
    #     uop += 1
    #     generate(child)
    # else:
    #     val = random.choice(cv)
    #     node.element = val


def update(root):
    # 从底部依次update每个node的attri，检查整棵树的attri只需要root的attri即可
    if root.left == None and root.right == None and root.mid == None:
        root.attri = root.element
        return
    elif root.left != None and root.right == None and root.mid == None:
        update(root.left)
        root.attri = root.left.attri
        return
    elif root.left != None and root.right != None and root.mid == None:
        update(root.right)
        root.attri = "┐" + root.right.attri
        return
    elif root.left.element == '(' and root.right.element == ')' and root.mid != None:
        update(root.mid)
        root.attri = '(' + root.mid.attri + ')'
        return
    else:
        update(root.left)
        update(root.right)
        root.attri = root.left.attri + root.mid.element + root.right.attri
        return


# ∨
# →
# ∧
# ┐

def check(root):
    global pool
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


def transform_6(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '∨'
        p = root.left
        q = root.right
        node_left = Node(node_id, '┐')
        node_id += 1
        node_left.left = p
        root.left = node_left
        root.right = q
        return
    else:
        transform_6(root.left, id)
    if root.right is not None:
        transform_6(root.right, id)


def transform_7(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        # root.element = '∨'
        p = root.left
        q = root.right
        node_left = Node(node_id, '┐')
        node_id += 1
        node_right = Node(node_id, '┐')
        node_id += 1
        node_left.left = q
        node_right.left = p
        root.left = node_left
        root.right = node_right
        return
    else:
        transform_7(root.left, id)
    if root.right is not None:
        transform_7(root.right, id)


def transform_8(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '→'
        p = root.left.left
        q = root.left.right
        r = root.right.right

        node_right = Node(node_id, '∨')
        node_id += 1

        node_right.left = q
        node_right.right = r
        root.left = p
        root.right = node_right
        return
    else:
        transform_8(root.left, id)
    if root.right is not None:
        transform_8(root.right, id)


def transform_9(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '→'
        p = root.left.left
        r = root.left.right
        q = root.right.left

        node_left = Node(node_id, '∧')
        node_id += 1

        node_left.left = p
        node_left.right = q
        root.right = r
        root.left = node_left
        return
    else:
        transform_9(root.left, id)
    if root.right is not None:
        transform_9(root.right, id)


def transform_10(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '→'
        p = root.left.left
        q = root.left.right
        r = root.right.right

        node_right = Node(node_id, '∧')
        node_id += 1

        node_right.left = q
        node_right.right = r
        root.left = p
        root.right = node_right
        return
    else:
        transform_10(root.left, id)
    if root.right is not None:
        transform_10(root.right, id)


def transform_11(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '→'
        p = root.left.left
        r = root.left.right
        q = root.right.left

        node_left = Node(node_id, '∨')
        node_id += 1

        node_left.left = p
        node_left.right = q
        root.right = r
        root.left = node_left
        return
    else:
        transform_11(root.left, id)
    if root.right is not None:
        transform_11(root.right, id)


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


def transform(root, times):
    global pool
    if times >= 5:
        print("enough times transform!!")
        return
    if pool == []:
        print("no longer trzansform!!")
        return
    index = random.randint(0, len(pool) - 1)
    rule = pool[index]
    print("use rule:", rule)
    if rule[1] == 0:
        transform_0(root, rule[0])

    elif rule[1] == 1:
        transform_1(root, rule[0])

    elif rule[1] == 2:
        transform_2(root, rule[0])

    elif rule[1] == 3:
        transform_3(root, rule[0])

    elif rule[1] == 4:
        transform_4(root, rule[0])

    elif rule[1] == 5:
        transform_5(root, rule[0])

    elif rule[1] == 6:
        transform_6(root, rule[0])

    elif rule[1] == 7:
        transform_7(root, rule[0])

    elif rule[1] == 8:
        transform_8(root, rule[0])

    elif rule[1] == 9:
        transform_9(root, rule[0])
    elif rule[1] == 10:
        transform_10(root, rule[0])
    elif rule[1] == 11:
        transform_11(root, rule[0])
    elif rule[1] == 12:
        transform_12(root, rule[0])
    update(root)
    pool.clear()
    check(root)
    print(test.attri)
    print("随机池：", pool)
    times += 1
    transform(root, times)


def printnodecheck(root):
    print("node id:", root.id, "  element:", root.element)
    if root.left == None and root.right == None:
        return

    else:
        printnodecheck(root.left)
    if root.right is not None:
        printnodecheck(root.right)


test = Node(-1, 'E')
generate(test)
# printnodecheck(test)
update(test)
# leftrule = test.attri
print(test.attri)
# check(test)
#
# print("随机池:", pool)
# transform(test, 0)
# print("hi, please do the transform:", leftrule, "=", test.attri)
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
