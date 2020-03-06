check_empty = 0

for check_empty in [1, 0]:
    for a in [0, '', None, 2]:
        try:
            assert not check_empty or a or a in [0, ''] , f'key or name is EMPTY? ({a})'
            print(check_empty, a, 'ok')
        except:
            print(check_empty, a, 'e')
