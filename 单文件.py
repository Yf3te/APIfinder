import re

# 从文件读取样本1.txt的内容，指定编码为utf-8-sig以兼容大部分情况
with open('单文件.txt', 'r', encoding='utf-8-sig') as file:
    content = file.read()

# 用于存储最终的结果
api_paths = set()

# 匹配包含/的路径 (例如 "/fre"、"/gtr/gfr" 等)
regex1 = r'["\'](\/[^"\']+)(?=["\'])'
matches = re.findall(regex1, content)
api_paths.update(matches)

# 匹配加号拼接的路径 (例如 + 'frew'、+"bytv" 等)
regex2 = r'\+\s*["\']\s*([^"\']+)\s*["\']'
matches = re.findall(regex2, content)
api_paths.update(matches)

# 匹配变量定义（提取类似 BASE_ZUUL_URL="/aop_web/" 的形式）
variable_regex = r'(\w+)\s*[:=]\s*["\']([^"\']+)["\']'
variables = {}
matches = re.findall(variable_regex, content)
for var, value in matches:
    variables[var] = value

# 匹配变量拼接路径 (例如 BASE_ZUUL_URL+"zuul/filesystem")
regex3 = r'(\w+)\s*\+\s*["\']([^"\']+)["\']'
matches = re.findall(regex3, content)

# 根据提取到的变量和值进行路径拼接
for var, path in matches:
    if var in variables:
        full_path = variables[var] + path
        # 确保拼接路径以/开头
        if not full_path.startswith('/'):
            full_path = '/' + full_path
        api_paths.add(full_path)

# 匹配包含加号拼接路径的具体子路径（例如 BASE_ZUUL_URL+"openapp/filesystem"）
regex4 = r'(\w+)\s*\+\s*["\'](\/[^"\']+)["\']'
matches = re.findall(regex4, content)

# 将匹配到的拼接路径加入结果中，并显示拼接过程
for var, sub_path in matches:
    if var in variables:
        full_path = variables[var] + sub_path
        if not full_path.startswith('/'):
            full_path = '/' + full_path
        api_paths.add(full_path)

# 处理路径，确保每个路径都以/开头
final_paths = set()
for path in api_paths:
    # 删除包含非法字符（:）的路径
    if any(char in path for char in ":;-.[]()*, +#$%&=<>!\\{}|?"):
        continue
    # 替换//为/
    path = path.replace('//', '/')
    # 确保路径以/开头
    if not path.startswith('/'):
        path = '/' + path
    final_paths.add(path)

# 输出结果到2.txt，指定编码为utf-8-sig以确保兼容
with open('单文件输出.txt', 'w', encoding='utf-8-sig') as f:
    for path in sorted(final_paths):
        f.write(path + "\n")

print("匹配的路径已保存到 单文件输出.txt")
