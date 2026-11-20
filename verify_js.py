import re

with open(r'd:\web devlopment baba\fake_upi_detector\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

scripts = re.findall(r'<script>([\s\S]*?)</script>', text)
print('Number of scripts:', len(scripts))
if scripts:
    s = scripts[0]
    print('Script length:', len(s))
    lines = s.split('\n')
    print('Script total lines:', len(lines))
    # Check end lines
    for i in range(len(lines) - 20, len(lines)):
        print(f'{i+1}: {lines[i]}')
