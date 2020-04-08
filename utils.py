import re

def find_date(text):
	date_pattern = re.compile(r'([0-2][1-9]|[3][01])[-\/.]([0][1-9]|[1][12])(?:\s+)?$')
	match = date_pattern.search(text)
	return f'{match[1]}/{match[2]}' if match else None