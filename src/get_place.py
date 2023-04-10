from .Haifu import Haifu

def get_place(haifu: Haifu, ban):
    '''
    Download the haifu and return the placing and rate before match
    '''
    o0, s0, o1, s1, o2, s2, o3, s3 = haifu.owari
    sp = [float(s0), float(s1), float(s2), float(s3)]
    placing = [1, 1, 1, 1]
    for i in range(4):
        for j in range(4):
            if(sp[i] < sp[j]):
                placing[i] += 1
    return placing[ban]
