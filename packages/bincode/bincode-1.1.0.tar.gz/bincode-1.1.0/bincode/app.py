import json
import os


def search(number: int) -> dict:
    
    def luhn(s: str) -> bool:
        a, b = 0, [*map(int, s)]
        for i, j in enumerate(b[:-1][::-1]):
            if i % 2 == 0:
                a += sum(map(int, str(j * 2)))
            else:
                a += j
        if b[-1] == 10 - (a % 10):
            return True
        return False
    
    path = os.path.dirname(__file__)
    with open(f'{path}/static/data.json', 'r') as f:
        data = json.load(f)
    
    number = str(number)
    
    for d in data:
        for p in d['prefix']:
            if p[0] <= int(number[:8].ljust(8, '0')) <= p[1]:
                if luhn(number) and len(number) in d['length']:
                    valid = True
                else:
                    valid = False
                return {'id': d['id'], 'valid': valid}
    return {'id': None, 'valid': False}
