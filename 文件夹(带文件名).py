import re
import os

# 用于存储最终的路径和文件名对应关系
api_paths = {}

# 原代码中的正则表达式
original_pattern_raw = r"""
  (?:"|')                               # Start newline delimiter
  (
    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
    |
    ((?:/|\.\./|\./)                    # Start with /,../,./
    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
    [^"'><,;|()]{1,})                   # Rest of the characters can't be
    |
    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
    [a-zA-Z0-9_\-/]{1,}                 # Resource name
    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
    (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
    |
    ([a-zA-Z0-9_\-]{1,}                 # filename
    \.(?:php|asp|aspx|jsp|json|
         action|html|js|txt|xml)             # . + extension
    (?:\?[^"|']{0,}|))                  # ? mark with parameters
  )
  (?:"|')                               # End newline delimiter
"""
original_pattern = re.compile(original_pattern_raw, re.VERBOSE)

# 定义API文件夹路径
api_folder = 'API'

# 遍历API文件夹及其所有子文件
for root, dirs, files in os.walk(api_folder):
    for file in files:
        file_path = os.path.join(root, file)

        # 读取所有文件（不限制文件类型），捕获解码错误
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()

            # 使用原正则表达式匹配路径
            original_matches = original_pattern.finditer(content)
            for match in original_matches:
                url = match.group().strip('"').strip("'")
                if url not in api_paths:
                    api_paths[url] = []
                api_paths[url].append(file_path)

            # 匹配包含/的路径 (例如 "/fre"、"/gtr/gfr" 等)
            regex1 = r'["\'](\/[^"\']+)(?=["\'])'
            matches = re.findall(regex1, content)
            for match in matches:
                if match not in api_paths:
                    api_paths[match] = []
                api_paths[match].append(file_path)

            # 匹配加号拼接的路径 (例如 + 'frew'、+"bytv" 等)
            regex2 = r'\+\s*["\']\s*([^"\']+)\s*["\']'
            matches = re.findall(regex2, content)
            for match in matches:
                if match not in api_paths:
                    api_paths[match] = []
                api_paths[match].append(file_path)

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
                    if full_path not in api_paths:
                        api_paths[full_path] = []
                    api_paths[full_path].append(file_path)

            # 匹配包含加号拼接路径的具体子路径（例如 BASE_ZUUL_URL+"openapp/filesystem"）
            regex4 = r'(\w+)\s*\+\s*["\'](\/[^"\']+)["\']'
            matches = re.findall(regex4, content)

            # 将匹配到的拼接路径加入结果中，并显示拼接过程
            for var, sub_path in matches:
                if var in variables:
                    full_path = variables[var] + sub_path
                    if not full_path.startswith('/'):
                        full_path = '/' + full_path
                    if full_path not in api_paths:
                        api_paths[full_path] = []
                    api_paths[full_path].append(file_path)

        except UnicodeDecodeError:
            print(f"无法读取文件 {file_path}: 文件编码不支持，已跳过。")
            continue
        except Exception as e:
            print(f"无法处理文件 {file_path}: {e}")
            continue

# 处理路径，确保每个路径都以/开头，结果去重
final_results = set()  # 使用集合存储最终的路径和文件名，自动去重
for path, file_names in api_paths.items():
    try:
        # 删除包含非法字符（:）的路径
        if any(char in path for char in ":;[]()*, +#$%&=<>!\\{}|?"):
            continue
        # 确保路径以/开头
        if not path.startswith('/'):
            path = '/' + path
        if re.match('//', path):
            # 替换//为/
            path = path.replace('//', '/')
        # 替换/./为/
        if re.match('/\./', path):
            path = path.replace('/./', '/')
        # 过滤包含 /@、/. 或 // 的路径
        if re.search(r'/@|/\.|//|/_|/-', path):
            continue  # 如果路径包含/@、/.或//，则跳过
        # 过滤不符合原始正则表达式的路径（可选，根据您的需求决定是否保留）
        if re.match('^/[a-zA-Z0-9]$', path):
            continue
        if path == '/':
            continue
        # 将路径和文件名组合加入结果集合
        for file_name in file_names:
            final_results.add((path, file_name))
    except Exception as e:
        print(f"处理路径 {path} 时出错: {e}")


# 定义排序函数
def custom_sort_key(item):
    path = item[0]
    # 检查路径是否包含文件后缀
    if '.' in path.rsplit('/', 1)[-1]:
        return (1, path)
    return (0, path)


# 对最终结果进行排序
sorted_results = sorted(final_results, key=custom_sort_key)

# 输出结果到文件夹(带文件名).txt，指定编码为utf-8-sig以确保兼容
with open('文件夹(带文件名).txt', 'w', encoding='utf-8-sig') as f:
    for path, file_name in sorted_results:
        f.write(f"{path} -------------- {file_name}\n")

print("匹配的路径和文件名已保存到 文件夹(带文件名).txt")
