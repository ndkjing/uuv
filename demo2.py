# 检验是否包含中文字符
def is_contain_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

print(is_contain_chinese('xxl'))
print(is_contain_chinese('大萨达撒'))