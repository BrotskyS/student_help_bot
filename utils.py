import re

date_pattern = re.compile(r'(?:\s+)?([0][1-9]|[12][0-9]|[3][01])[-\.\/]([0][1-9]|[1][12])(?:\s+)')

def find_date(text):
	pattern = r'([0][1-9]|[12][0-9]|[3][01])[-\.\/]([0][1-9]|[1][12])(?:\s+)?$'
	match = re.search(pattern, text)
	print(match)
	return f'{match[1]}/{match[2]}' if match else None