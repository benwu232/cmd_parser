import sys
import pprint

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


def parse_cmd(cmd_list, blank_space_pattern='\\_',
              dict_flag=':', dict_start='{', dict_end='}',
              list_start = '[', list_end = ']'):
    '''
    Parse command line to python directory
    The gramma is similar to python
    { } contains directory
    [ ] contains list
    \_  means blank space. Because blank spaces are used to split command line, use '\_' to replace a blank space in
    the parameters. it will be replaced by a blank space in the final output.

    example
    n: 100 dict1: { m: 3 ar: [ 10 11 12 { x: 1 y: 2 seq: [ 7 8 [ 9 ] ] } 13 ] a: 1 c: 2 dict3: { f: 3 h: i } j: k }
    out_dict {'n': '100', 'dict1': {'m': '3', 'ar': ['10', '11', '12', {'x': '1', 'y': '2', 'seq': ['7', '8', ['9']]}, '13'], 'a': '1', 'c': '2', 'dict3': {'f': '3', 'h': 'i'}, 'j': 'k'}}

    spark: { } kafka: { brokers: local.1:10001,local.2:10002,local.3:10003 err_topic: err_log period: 2 } err_db: { host: 127.0.0.1 port: 3306 username: abc password: 123456 db_name: gh charset: utf8mb4 } err_table: { table_name: err_log  schema: { error_type: VCHAR(50) err_gen_at: BIGINT\_NOT\_NULL app_name: VCHAR(50)  } }
    out_dict {'spark': {}, 'kafka': {'err_topic': 'err_log', 'period': '2'}, 'err_db': {'host': '127.0.0.1', 'port': '3306', 'username': 'abc', 'password': '123456', 'db_name': 'gh', 'charset': 'utf8mb4'}, 'err_table': {'table_name': 'err_log', 'schema': {'error_type': 'VCHAR(50)', 'err_gen_at': 'BIGINT NOT NULL', 'app_name': 'VCHAR(50)'}}}

    :param cmd_list: list of commands, generally sys.argv[1:]
           blank_space_pattern: pattern of blank spaces in comments
           dict_flag: flag of dict, the part of string before it is parsed as the name of the dict
           dict_start: default value '{'
           dict_end: default value '}'
           list_start: default value '['
           list_end: default value ']'
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
        s = s.replace(blank_space_pattern, ' ')      #process of blank spaces in parameters
        item = s
        if dict_flag in s:
            cur_key = s.split(dict_flag)[0]

        elif item == dict_start:
            seg = {}
            pro(seg)
            cmd_stacks.append(seg)

        elif item == list_start:
            seg = []
            pro(seg)
            cmd_stacks.append(seg)

        elif list_end in item or dict_end in item:
            cmd_stacks.pop()

        else:
            pro(item)

    return cmd_dict

def print_parse_cmd(args):
    print('input', args)
    out_dict = parse_cmd(args)
    print('out_dict', out_dict)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(out_dict)
    print('bingo')


if __name__ in '__main__':
    args = sys.argv[1:]
    print_parse_cmd(args)


