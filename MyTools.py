import os

#数据相关
def list_of_groups(_list, children_list_len):
    """
    按数量分割list为多个list
    """
    list_of_groups = zip(*(iter(_list),) *children_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(_list) % children_list_len
    end_list.append(_list[-count:]) if count !=0 else end_list
    return end_list

def list_to_str(_list,splitsign):
    """
    list转化安装splitsign分隔的字符串
    """
    _str =""
    for ele in _list:
            _str += ele+splitsign
    return _str

def merge_dicts(*dict_args):
    """
    合并多个dict为一个dict
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def list_deduplication(_list):
    """
    列表去重
    """
    return list(set(_list))

def split_liststr_to_list(_list,splitsign,index=0):
    """
    按符号分隔list中的字符，然后返回分隔号的第index项为list
    """
    new_list =[]
    for s in _list:
        new_list.append(str(s).split(splitsign)[index])
    return new_list

#文件相关
def get_file_to_list(fliepath,name):
    """
    读取对应路径的文件，如果没有则创建
    返回list
    """
    if os.path.exists(fliepath+name+'.txt'):
        with open(fliepath+name+'.txt',mode='r',encoding='utf-8') as ff:
            try:
                list = ff.read().splitlines()
            except:
                list = [""]
        ff.close()
    else:
        with open(fliepath+name+'.txt', mode='w', encoding='utf-8') as ff:
            list = [""]
            ff.close()
    return list

def get_file_to_dict(fliepath,splitsign,name):
    """
    读取对应路径的文件，如果没有则创建
    返回dict,splitsign为分隔符
    """
    if os.path.exists(fliepath+name+'.txt'):
        dict = {}
        with open(fliepath+name+'.txt',mode='r',encoding='utf-8') as ff:
            try:
                list = ff.read().splitlines()
                for l in list:
                    s = str(l).split(splitsign,1)
                    dict[s[0].strip()] = s[1].strip()
            except:
                dict = {}
        ff.close()
    else:
        with open(fliepath+name+'.txt', mode='w', encoding='utf-8') as ff:
            dict = {}
            ff.close()
    return dict