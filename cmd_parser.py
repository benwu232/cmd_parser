import sys

# dict1=-ds ar=-ls 10 11 12 dict2=-ds x=1 y=2 seq=-ls 7 8 seq2=-ls 9 -le -le -de 13 -le a=1 c=2 dict3=-ds f=3 h=i -de j=k -de


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
    '''
    Parse command line to python directory
    The gramma is similar to python
    { } contains directory
    [ ] contains list

    example
    n: 100 dict1: { m: 3 ar: [ 10 11 12 { x: 1 y: 2 seq: [ 7 8 [ 9 ] ] } 13 ] a: 1 c: 2 dict3: { f: 3 h: i } j: k }
    out_dict {'n': '100', 'dict1': {'m': '3', 'ar': ['10', '11', '12', {'x': '1', 'y': '2', 'seq': ['7', '8', ['9']]}, '13'], 'a': '1', 'c': '2', 'dict3': {'f': '3', 'h': 'i'}, 'j': 'k'}}

    :param cmd_list:
    :return: python directory which contains command list
    '''
    cmd_dict = {}
    cmd_stacks = [cmd_dict]
    cur_key = None

    def pro(seg):
        if type(cmd_stacks[-1]) == list:
            cmd_stacks[-1].append(seg)
        elif type(cmd_stacks[-1]) == dict:
            cmd_stacks[-1][cur_key] = seg

    for s in cmd_list:
        item = s
        if ':' in s:
            cur_key = s.split(':')[0]

        elif item == '{':
            seg = {}
            pro(seg)
            cmd_stacks.append(seg)

        elif item == '[':
            seg = []
            pro(seg)
            cmd_stacks.append(seg)

        elif ']' in item or '}' in item:
            cmd_stacks.pop()

        else:
            pro(item)

    return cmd_dict


if __name__ in '__main__':
    args = sys.argv[1:]
    print('input', args)
    out_dict = parse_cmd(args)
    print('out_dict', out_dict)
    print('bingo')


