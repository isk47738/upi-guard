import re

with open(r'd:\web devlopment baba\fake_upi_detector\fast_scanner.html', 'r', encoding='utf-8') as f:
    text = f.read()

get_ids = set(re.findall(r"document\.getElementById\(['\"]([a-zA-Z0-9_-]+)['\"]", text))
html_ids = set(re.findall(r"id=['\"]([a-zA-Z0-9_-]+)['\"]", text))

missing = get_ids - html_ids
print('IDs referenced in JS but missing in HTML:', missing)
