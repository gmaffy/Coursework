
def integer_mass():
    mass_dict = dict()
    with open("integer_mass_table.txt") as f:
        data = f.read().split()
        for idx, item in enumerate(data):
            if not idx % 2:
                mass_dict[item] = int(data[idx + 1])
        return mass_dict

integer_mass_table = integer_mass()

print integer_mass_table
aminoacid_masses = sorted(list(set(integer_mass_table.values())))
def mass(pep):
    return sum(pep)

def parentmass(spec):
    return max(spec)

def score(pep, spec):
    s = spectrum(subpeptides_n, pep)
    sp = list(spec)
    output = 0
    for x in s:
        if x in sp:
            output += 1
            sp.remove(x)
    return output

def cut_leads(leaderboard, N, spec):
    leaders = sorted([(p,score(p,spec)) for p in leaderboard], key=lambda k : k[1], reverse=True)   
    return [p for p,s in leaders if len(leaders) <= N or s >= leaders[N][1]]

def leaderboardsequencing(spec, N):
    leaderboard = [[]]
    leaderpeptide = []
    leaderscore = 0
    pm = parentmass(spec)
    while leaderboard:
        print 'Leader length: %s' % len(leaderboard)
        leaderboard = expand_list_pep(leaderboard)
        print 'Leader expanded: %s' % len(leaderboard)
        leaderboard = cut_leads(leaderboard, N, spec)
        print 'After cut: %s' % len(leaderboard)
        top = score(leaderboard[0], spec)
        if top > leaderscore:
            leaderpeptide = leaderboard[0]
            leaderscore = top
            lastleaderboard = list(leaderboard)
        st = 'Top: %s \nScore: %s' % ('-'.join(map(str, leaderpeptide)), leaderscore)
        m = len(st)
        print st
        print "="*m
        leaderboard = [p for p in leaderboard if mass(p) <= pm]
    return leaderpeptide, lastleaderboard

def expandPeptide(L, p, m, sp_f):
    sp = dict(L[p][0])
    sc = L[p][2]
    ma = L[p][3]
    p_list = L[p][1]
    ma += m
    if ma <= max(sp_f):
        if p == '':
            sp[m] = sp.get(m,0) + 1
            if sp[m] <= sp_f.get(m,0):
                sc += 1
        else:
            sc = modifySpectrum(p_list, m, sp, sc, sp_f)    
        newkey = newPeptideKey(p,m)
        L[newkey] = (sp, p_list + [m], sc, ma)
    
def modifySpectrum(p_list, m, sp, sc, sp_f):
    output = sc
    coming = [sum(s) for s in extension_newsubs(p_list,m)]
    for m in coming:
        sp[m] = sp.get(m,0) + 1
        if sp[m] <= sp_f.get(m,0):
            output += 1
    #going = [sum(s) for s in extension_outdatedsubs(p_list)]
    #for m in going:
    #    sp[m] -= 1
    #    if sp[m] < sp_f.get(m,0):
    #        output -= 1
    return output

def specFreq(spec):
    output = {}
    for m in spec:
        output[m] = output.get(m,0) + 1
    return output

def newPeptideKey(p,a):
    if p == '':
        return str(a)
    else:
        return p + '-' + str(a)

def extension_newsubs(oldpep, a):
    pivot = len(oldpep)
    newpep = oldpep + [a]
    newpep_extended = newpep + newpep[:pivot - 1]
    output = [[a], newpep]
    for i in range(pivot-1):
        for j in range(i+2):
            output += [newpep_extended[pivot-(i+1)+j:pivot+1+j]]
    return output

def extension_outdatedsubs(oldpep):
    pivot = len(oldpep) - 1
    oldpep_extended = oldpep + oldpep[:pivot -1]
    output = []
    for i in range(pivot-1):
        for j in range(i + 1):
            output += [oldpep_extended[pivot-i+j:pivot+1+j+1]]
    return output

def expandLeaderboard(L, sp_f):
    current = list(L.keys())
    for p in current:
        preparePep(L, p, sp_f)
        for m in aminoacid_masses:
            expandPeptide(L, p, m, sp_f)
        del L[p]

def preparePep(L, p, sp_f):
    sp = dict(L[p][0])
    p_list = L[p][1]
    sc = L[p][2]
    ma = L[p][3]
    going = [sum(s) for s in extension_outdatedsubs(p_list)]
    for m in going:
        sp[m] -= 1
        if sp[m] < sp_f.get(m,0):
            sc -= 1
    L[p] = (sp, p_list, sc, ma)

def newleaderboardsequencing(spec, N):
    LeaderBoard = {}
    LeaderBoard[''] = ({0:1}, [], 1, 0)
    leaderpeptide = ''
    leaderscore = 1
    pm = parentmass(spec)
    spec_frec = specFreq(spec)
    while LeaderBoard:
        print 'Leader length: %s' % len(LeaderBoard)        
        #print 'Leader expanded: %s' % len(LeaderBoard)
        top_scores = sorted([LeaderBoard[p][2] for p in LeaderBoard], reverse=True)
        if len(top_scores) > N:
             LeaderBoard = {p:v for p,v in LeaderBoard.items() if v[2] >= top_scores[N]}
        #print 'After cut: %s' % len(LeaderBoard)
        top = top_scores[0]
        if top > leaderscore:
            top_scorers = [p for p in LeaderBoard if LeaderBoard[p][2] == top]
            leaderpeptide = top_scorers[0]
            leaderscore = top
        st = 'Top: %s \nScore: %s' % (leaderpeptide, leaderscore)
        m = len(st)
        print st
        print "="*m
        #LeaderBoard = {p:v for p,v in LeaderBoard.items() if v[3] <= pm}
        expandLeaderboard(LeaderBoard, spec_frec)
    return leaderpeptide

spl = "329 251 479 1152 1413 1200 820 813 417 763 114 884 923 365 1240 1090 393 1304 428 1422 87 646 1441 759 1299 128 507 1270 1482 137 1142 1062 554 1368 270 379 772 332 1455 1028 1141 793 1109 756 628 620 1204 506 900 427 1432 1351 1048 541 635 555 1455 949 242 941 535 1015 369 1176 1569 683 887 521 427 682 407 131 1441 934 314 299 1014 934 113 1063 1318 877 1291 278 886 218 1383 147 515 962 1438 776 114 265 1034 749 555 806 1142 663 607 186 906 1327 256 1190 1237 303 241 685 1328 201 1135 1313 1021 1014 1441 797 635 1266 434 1456 128 1162 548 0 460 156 1255 1054 128 692 810 669".split()
spec = map(int, spl)
spec_freq = specFreq(spec)

x = newleaderboardsequencing(spec, 19)
print x
