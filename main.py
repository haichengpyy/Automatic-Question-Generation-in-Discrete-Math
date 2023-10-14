from Node import Node
import Generator, generation

def generate_questons(question_num, rule_num):
    questions = []
    i = 0
    while i < question_num :
        test = Node('E',-1 )
        test1 = Node('E',-1 )
        generation.generate_two(test,test1)
        generation.update(test)
        generation.update(test1)
        print(test.attri + '  =  ' + test1.attri)
        flag = generation.reset_counter(rule_num)
        if not flag:
            print('not qualified')
        else:
            i += 1
            questions.append(test.attri + '  =  ' + test1.attri)
    print('Here are the ' + str(question_num) + ' questions we generated which need to use at least ' + str(rule_num) + ' rules:')
    for j in questions:
        print( j )


generate_questons(5,3)