import functools
from flask import request


def validator(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        frontValues = {}
        checkFields = getattr(f, "checked")
        if request.method == 'GET':
            inputField = request.args
            print(inputField)
            for key, value in checkFields.items():
                targetField = inputField.get(key, None)
                for func in value:
                    func(targetField)
                    frontValues[key] = targetField

        # f.frontValues = frontValues
        print(frontValues)
        return f(**frontValues)

    return wrapper


def frontValidator(fields):
    frontValues = {}
    inputField = {}
    if request.method == 'GET':
        inputField = getParams()
    elif request.method == 'POST':
        inputField = postParams()
    for key, methods in fields.items():
        targetField = inputField.get(key, None)
        for method in methods:
            res = method(targetField)
            if res is not None:
                # 添加默认值
                targetField = res
        frontValues[key] = targetField
    return frontValues


def getParams():
    params = {}
    argsDict = request.args.to_dict(flat=True)
    params.update(argsDict)
    return params


def postParams():
    """获取post请求"""
    params = {}
    argsDict = request.args.to_dict(flat=True) or {}
    params.update(argsDict)
    jsonDict = request.get_json(force=True, silent=True) or {}
    params.update(jsonDict)
    formDict = request.form.to_dict(flat=True) or {}
    params.update(formDict)
    return params
