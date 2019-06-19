import getpass  # 隐藏输入
import hashlib  # 转换加密

# 输入隐藏
pwd = getpass.getpass()
print(pwd)

# 生成hash对象
# hash = hashlib.md5()


# 算法加盐
hash = hashlib.md5("*#06l_".encode())

# 算法对密码加密,对字节码
hash.update(pwd.encode())
# 提取加密后的密码
pwd = hash.hexdigest()
print(pwd)
