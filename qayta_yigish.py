"""bank.json va sayt fayllaridan offline nusxani qayta yig‘ish. Python 3."""
from pathlib import Path
import base64
import json
import re

root = Path(__file__).resolve().parent
site = root / 'sayt'
bank = json.loads((site / 'bank.json').read_text(encoding='utf-8'))
assert len({q['id'] for q in bank}) == len(bank), 'Savol ID takrorlangan'
encoded = []
for q in bank:
    image = site / q['image']
    data = image.read_bytes()
    if not data:
        raise ValueError(f'Rasm bo‘sh: {image}')
    mime = {'.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg'}[image.suffix.lower()]
    encoded.append({**q, 'image': f'data:{mime};base64,' + base64.b64encode(data).decode('ascii')})
(site / 'bank.js').write_text('window.QUESTION_BANK=' + json.dumps(bank, ensure_ascii=False, separators=(',', ':')) + ';', encoding='utf-8')
html = (site / 'index.html').read_text(encoding='utf-8')
css = (site / 'style.css').read_text(encoding='utf-8')
html, n = re.subn(r'<link rel="stylesheet" href="style\.css[^"<>]*">', lambda _: '<style>' + css + '</style>', html)
assert n == 1, 'CSS havolasi topilmadi'
html, n = re.subn(r'<script src="(?:bank|app)\.js[^"<>]*" defer></script>', '', html)
assert n == 2, 'JavaScript havolalari topilmadi'
js = 'window.QUESTION_BANK=' + json.dumps(encoded, ensure_ascii=False, separators=(',', ':')) + ';\n' + (site / 'app.js').read_text(encoding='utf-8')
js = re.sub(r'</script', lambda _: '<' + chr(92) + '/script', js, flags=re.I)
html = html.replace('</body>', '<script>' + js + '</script></body>')
(root / 'Informatika-30-test.html').write_text(html, encoding='utf-8')
print(f'Tayyor: {len(bank)} ta savol. Informatika-30-test.html yangilandi.')
