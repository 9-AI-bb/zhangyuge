import os
import sys

home_path = []
m_size = 0
for home, _, _ in os.walk('D:/'):
    home_path.append(home)
    m_size += sys.getsizeof(home)
print(sys.getsizeof(home_path))
print(m_size)