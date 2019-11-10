import sys

# dict1=-ds ar=-ls 10 11 12 dict2=-ds x=1 y=2 seq=-ls 7 8 seq2=-ls 9 -le -le -de 13 -le a=1 c=2 dict3=-ds f=3 h=i -de j=k -de

#example
# n: 100 dict1: { m: 3 ar: [ 10 11 12 { x: 1 y: 2 seq: [ 7 8 [ 9 ] ] } 13 ] a: 1 c: 2 dict3: { f: 3 h: i } j: k }
# The gramma is similar to python
# { } contains directory
# [ ] contains list

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


def parse_cmd(cmd_list):
    cmd_dict = {}
    layers = [cmd_dict]
    cur_key = None

    def pro(section):
        if type(layers[-1]) == list:
            layers[-1].append(section)
        elif type(layers[-1]) == dict:
            layers[-1][cur_key] = section

    for s in cmd_list:
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
