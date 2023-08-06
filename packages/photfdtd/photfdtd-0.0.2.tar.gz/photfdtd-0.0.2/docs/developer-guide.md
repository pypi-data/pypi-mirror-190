# 开发者文档

## 生成 distribution 文件

在 **pyproject.toml** 的相同目录下:

```shell
# 同时构建 source and binary distribution files
python3 -m build
```

## 上传 package 到 PyPI

使用以下命令上传到 PyPI，注意你需要确保项目版本和 PyPI上已存在的项目版本不一样，否则会产生冲突，同时你需要清除 `dist` 目录下已存在的旧版 distribution 文件。

```shell
python3 -m twine upload dist/*
```