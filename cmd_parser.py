import ast
import sys
#test_string = '{"Nikhil" : 1, "Akshat" : 2, "Akash" : 3}'


in_str = "dict1=-ds ar=-ls 10 11 12 dict2=-ds x=1 y=2 seq=-ls 7 8 -le -de 13 -le a=1 c=2 dict2=-ds f=3 h=i -de j=k -de"
# dict1=-ds1 a=1 c=2 dict2=-ds2 f=3 h=i -de2 j=k -de2
# dict1=-ds ar=-ls 10 11 12 dict2=-ds x=1 y=2 seq=-ls 7 8 seq2=-ls 9 -le -le -de 13 -le a=1 c=2 dict3=-ds f=3 h=i -de j=k -de
# dict1={ ar=[ 10 11 12 dict2={ x=1 y=2 seq=[ 7 8 seq2=[ 9 ] ] } 13 ] a=1 c=2 dict3={ f=3 h=i } j=k }
# dict1:{ ar:[ 10 11 12 dict2:{ x:1 y:2 seq:[ 7 8 seq2:[ 9 ] ] } 13 ] a:1 c:2 dict3:{ f:3 h:i } j:k }
# dict1:{ ar:[ 10 11 12 { x:1 y:2 seq:[ 7 8 [ 9 ] ] } 13 ] a:1 c:2 dict3:{ f:3 h:i } j:k }
# n: 100 dict1: { m: 3 ar: [ 10 11 12 { x: 1 y: 2 seq: [ 7 8 [ 9 ] ] } 13 ] a: 1 c: 2 dict3: { f: 3 h: i } j: k }

def parse_dict(str_in):
    dic = {}
    cur_dict = dic
    layer = [dic]
    for item in str_in:
        slist = item.split('=')
        if len(slist) == 2:     #key-value
            if '-ds' in slist[1]:
                cur_dict[slist[0]] = {}
                cur_dict = cur_dict[slist[0]]
                layer.append(cur_dict)
            else:
                cur_dict[slist[0]] = slist[1]
        elif len(slist) == 1 and '-de' in slist[0]:    #end of key-value
            layer.pop()
            cur_dict = layer[-1]
    return dic

def parse_cmd1(str_in):
    cmd_dict = {}
    layers = [cmd_dict]

    for s in str_in:
        items = s.split('=')

        if type(layers[-1]) == list:
            if len(items) == 2:
                if '-ds' in items[1]:  # start of dict
                    d = {}
                    layers[-1].append(d)
                    layers.append(d)
                elif '-ls' in items[1]:  # start of list
                    l = []
                    layers[-1].append(l)
                    layers.append(l)
            else:
                assert len(items) == 1
                if '-le' in items[0]:
                    layers.pop()
                else:
                    layers[-1].append(items[0])

        elif type(layers[-1]) == dict:
            if len(items) == 2:
                if '-ds' in items[1]:  # start of dict
                    layers[-1][items[0]] = {}
                    layers.append(layers[-1][items[0]])
                elif '-ls' in items[1]:  # start of list
                    layers[-1][items[0]] = []
                    layers.append(layers[-1][items[0]])
                else:
                    layers[-1][items[0]] = items[1]
            else:
                assert len(items) == 1
                if '-de' in items[0]:
                    layers.pop()

    return cmd_dict

def parse_cmd2(str_in):
    cmd_dict = {}
    layers = [cmd_dict]

    for s in str_in:
        items = s.split(':')

        if type(layers[-1]) == list:
            if len(items) == 2:
                if '{' in items[1]:  # start of dict
                    d = {}
                    layers[-1].append(d)
                    layers.append(d)
                elif '[' in items[1]:  # start of list
                    l = []
                    layers[-1].append(l)
                    layers.append(l)
            else:
                assert len(items) == 1
                if '{' in items[0]:  # start of dict
                    d = {}
                    layers[-1].append(d)
                    layers.append(d)
                elif '[' in items[0]:  # start of list
                    l = []
                    layers[-1].append(l)
                    layers.append(l)
                elif ']' in items[0] or '}' in items[0]:
                    layers.pop()
                else:
                    layers[-1].append(items[0])

        elif type(layers[-1]) == dict:
            if len(items) == 2:
                if '{' in items[1]:  # start of dict
                    layers[-1][items[0]] = {}
                    layers.append(layers[-1][items[0]])
                elif '[' in items[1]:  # start of list
                    layers[-1][items[0]] = []
                    layers.append(layers[-1][items[0]])
                else:
                    layers[-1][items[0]] = items[1]
            else:
                assert len(items) == 1
                if '}' in items[0]:
                    layers.pop()

    return cmd_dict



def parse_cmd(str_in):
    cmd_dict = {}
    layers = [cmd_dict]
    cur_key = None

    def pro(d):
        if type(layers[-1]) == list:
            layers[-1].append(d)
        elif type(layers[-1]) == dict:
            layers[-1][cur_key] = d

    for s in str_in:
        item = s
        if ':' in s:
            cur_key = s.split(':')[0]

        elif item == '{':
            d = {}
            pro(d)
            layers.append(d)

        elif item == '[':
            d = []
            pro(d)
            layers.append(d)

        elif ']' in item or '}' in item:
            layers.pop()

        else:
            pro(item)

    return cmd_dict


if __name__ in '__main__':
    args = sys.argv[1:]
    #args = in_str
    print('input', args)
    out_dict = parse_cmd(args)
    print('out_dict', out_dict)
    print('bingo')
