from pr_properties.pr_properties import Properties


def test_01():
    p = Properties()
    p.read(r"./pool.properties")
    # 新增
    p['2'] = 2
    p['3'] = 3
    # 写入新增的内容
    p.write()


def test_02():
    text = """# comment
kk=123
ks.1=222
ks.1=222==333"""
    p = Properties()
    p.loads(text)
    # 修改删除
    p['kk'] = 3
    del p['ks.1']
    print('\n' + p.__str__())
