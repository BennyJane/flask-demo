def string_to_num(s, error_return=None):
    """
    :param s: 待转换的字符串
    :param error_return: 非数值的最终返回结果
    :return:
    >>> string_to_num('5')
    5
    >>> string_to_num('5.2')
    5.2
    >>> string_to_num(10)
    10
    >>> string_to_num(10.1)
    10.1
    >>> string_to_num('this is not a string') is None
    """
    if isinstance(s, (int, float)):
        return s
    if s.isdigit():
        return int(s)
    try:
        return float(s)
    except ValueError:
        return error_return


def js_string_to_python(item):
    return None if item in ('null', 'undefined') else item
