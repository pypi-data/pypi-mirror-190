该脚本仅用于口碑项目（或其他按需）。

更新使用：
python setup.py sdist build
之后在dist中删除上一版本的gz文件
twine upload dist/*
