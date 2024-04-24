
from yggdrasil.utils.string import normalize_string

print(normalize_string("Hello, World!") == "hello, world!")
print(normalize_string("Héllo, Wòrld!") == "hello, world!")