# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier

from webApp import create_app

app = create_app()
config = app.config
if __name__ == '__main__':
    app.run(debug=config.get("DEBUG"), host=config.get("HOST"), port=config.get("PORT"))
