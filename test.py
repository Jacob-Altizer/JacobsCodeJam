
import re

data = 'preview_program.php?catoid=30&poid=1203&returnto=2019'

split_data = re.split('&|=', data)

print(split_data[-3])
