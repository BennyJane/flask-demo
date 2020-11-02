from datetime import date, datetime, time, timedelta


def json_iso_dttm_ser(obj):
    if isinstance(obj, (datetime, time, date)):
        obj = obj.isoformat()
    else:
        raise TypeError("类型{}:{} 不能正常序列化".format(type(obj), obj))
    return obj
