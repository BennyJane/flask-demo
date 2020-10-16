# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash


# 返回所有 ==》 用于表单错误处理
def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)
