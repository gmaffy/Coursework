from collections import Counter

def integer_mass():
    mass_dict = dict()
    with open("integer_mass_table.txt") as f:
        data = f.read().split()
        for idx, item in enumerate(data):
            if not idx % 2:
                mass_dict[item] = int(data[idx + 1])
        return mass_dict

INTEGER_MASS_TABLE = integer_mass()

def subpeptides(peptide):
    subs = [peptide]
    peptide_ext = list(peptide) + list(peptide)[:len(list(peptide)) - 2]
    for idx1 in range(len(list(peptide))):
        for idx2 in range(len(list(peptide))-1):
            subs += [''.join(peptide_ext[idx1:idx1+idx2+1])]
    return subs

def mass_subpeptides(peptide):
    subs = list([peptide])
    peptide_ext = list(peptide) + list(peptide)[:len(list(peptide)) - 2]
    for idx1 in range(len(peptide)):
        for idx2 in range(len(peptide) - 1):
            subs += [peptide_ext[idx1:idx1+idx2+1]]
    return subs
            

def num_subpeptides(cyclic_size):
    return (cyclic_size - 1) * cyclic_size

def peptide_mass(peptide):
    mass_list = [INTEGER_MASS_TABLE[i] for i in list(peptide)]
    return sum(mass_list)
    

def naive_theoretical_spectrum(cyclic_peptide):
    subpeps = subpeptides(cyclic_peptide)
    mass_list = [peptide_mass(pep) for pep in subpeps]+[0]
    return sorted(mass_list)

def naive_theoretical_mass_spectrum(cyclic_peptide):
    subpeps = mass_subpeptides(cyclic_peptide)
    mass_list = [sum(pep) for pep in subpeps] + [0]
    return sorted(mass_list)

aminoacid_masses = sorted(list(set(INTEGER_MASS_TABLE.values())))

def linear_spectrum_fast(peptide, aminoacid, aminoacidmass):
    """faster alternative to linear_spectrum()"""
    prefix_mass = [0]
    for i in range(0,len(peptide)):
        for j, item in enumerate(aminoacid):
            if aminoacid[j] == peptide[i]:
                print peptide[i]
                prefix_mass.append(prefix_mass[i]+aminoacidmass[j])
    linearspectrum = [0]
    for i in range(0, len(prefix_mass)-1):
        for j in range(i+1, len(prefix_mass)):
            linearspectrum.append(prefix_mass[j] - prefix_mass[i])
    return sorted(linearspectrum)   

def peptides(n, d):
    for m in aminoacid_masses:
        if n-m in d:
            d[n] = d.get(n,0)+d[n-m]
    return d

def pep_counter(M):
    dicc = {0:1}
    mn = min(aminoacid_masses)
    for i in range(M-mn+1):
        j = i+mn
        peptides(j,dicc)
    return dicc

def num_linear_subpeptides(linear_size):
    return sum(range(linear_size+1)) + 1

def expand(peptides):
    """Peptides are treated as chains of amino acids."""
    expanded_peptides = []
    for pep in peptides:
        for aa in INTEGER_MASS_TABLE.keys():
            expanded_peptides.append(pep+aa)
    return expanded_peptides

def mass_expand(peptides, mass_list):
    """Mass-only version of expand. Peptides is a list of lists of masses (i.e. each pep is a list of masses)."""
    expanded_peptides = []
    for pep in peptides:
        for aa in mass_list:
            expanded_peptides.append(pep+[aa])
    return expanded_peptides

    
def linear_spectrum(peptide):
    mass_list = list()
    for window_size in range(1,len(peptide)):
        for possible_position in range(len(peptide)-window_size+1):
            #print peptide[possible_position:possible_position+window_size]
            mass_list.append(peptide_mass(peptide[possible_position:possible_position+window_size]))
    mass_list.append(0)
    mass_list.append(peptide_mass(peptide))
    return sorted(mass_list)

def linear_mass_spectrum(peptide):
    """Mass-based version of linear_spectrum in which peptides are treated as lists of masses."""
    mass_list = list()
    mass_list.append(0)
    mass_list.append(sum(peptide))
    for window_size in range(1,len(peptide)):
        for possible_position in range(len(peptide) - window_size+1):
            mass_list.append(sum(peptide[possible_position:possible_position+window_size]))
    return sorted(mass_list)

def cyclospectrum_equality(peptide, spectrum):
    return all([bool(s in spectrum) for s in linear_spectrum(peptide)])

def cyclospectrum_mass_equality(peptide, spectrum):
    return all([bool(s in spectrum) for s in peptide])

def mass_list(peptide):
    """Helper function to turn output of cyclopeptide_sequencing into the format preferred by course: string of masses separated by dashes"""
    return '-'.join([str(peptide_mass(p)) for p in peptide])

def cyclopeptide_sequencing(spectrum):
    """Determines which linear spectra are consistent with a given cyclospectrum"""
    peptides = [""]
    solution = []
    while len(peptides)!=0:
        print len(peptides[-1])
        peptides = expand(peptides)
        pep_copy = list(peptides)
        for pep in peptides:
            if peptide_mass(pep) == max(spectrum):
                if cyclospectrum_equality(pep, spectrum):
                    if not mass_list(pep) in solution:
                        solution.append(mass_list(pep))
                pep_copy.remove(pep)
            
            elif not cyclospectrum_equality(pep, spectrum):
                pep_copy.remove(pep)
        peptides = list(pep_copy)
        print len(peptides)
    return solution
        

def score(peptide, spectrum):
    """Determine number of mismatches between a theoretical cyclospectrum and an experimental one"""
    pep_spectrum = naive_theoretical_spectrum(peptide)
    score = 0
    for mass in spectrum:
        if not mass in pep_spectrum:
            pass
        else:
            score += 1
            pep_spectrum.remove(mass)
    return score

def linear_score(peptide, spectrum):
    pep_spectrum = linear_spectrum(peptide)
    score = 0
    for mass in spectrum:
        if not mass in pep_spectrum:
            pass
        else:
            score += 1
            pep_spectrum.remove(mass)
    return score    

def mass_score(peptide, spectrum):
    pep_spectrum = naive_theoretical_mass_spectrum(peptide)
    score = 0
    for mass in spectrum:
        if not mass in pep_spectrum:
            pass
        else:
            score += 1
            pep_spectrum.remove(mass)
    return score

def linear_mass_score(peptide, spectrum):
    pep_spectrum = linear_mass_spectrum(peptide)
    score = 0
    for mass in spectrum:
        if not mass in pep_spectrum:
            pass
        else:
            score += 1
            pep_spectrum.remove(mass)
    return score

def trim(leaderboard, spectrum, n):
    score_dict = dict()
    new_leaders = list()
    for pep in leaderboard:
        score = linear_score(pep, spectrum)
        if score in score_dict.keys():
            score_dict[score].append(pep)
        else:
            score_dict[score] = [pep]
    allowed_scores = sorted(score_dict.keys())
    while len(new_leaders) < n:
        try:
            score = allowed_scores.pop()
            new_leaders.extend(score_dict[score])
        except IndexError:
            break
    return new_leaders

def trim2(leaderboard, spectrum, n):
    scores = [linear_score(pep, spectrum) for pep in leaderboard]
    scores_leaders = zip(scores, leaderboard)
    scores_leaders = sorted(scores_leaders)
    sorted_scores = [i[0] for i in reversed(scores_leaders)]
    sorted_leaders = [i[1] for i in reversed(scores_leaders)]
    for j in range(n-1, len(leaderboard)):
        if sorted_scores[j] < sorted_scores[n-1]:
            return sorted_leaders[0:j]
    return sorted_leaders

def mass_trim(leaderboard, spectrum, n):
    scores = [linear_mass_score(pep, spectrum) for pep in leaderboard]
    scores_leaders = zip(scores, leaderboard)
    scores_leaders = sorted(scores_leaders)
    sorted_scores = [i[0] for i in reversed(scores_leaders)]
    sorted_leaders = [i[1] for i in reversed(scores_leaders)]
    for j in range(n-1, len(leaderboard)):
        if sorted_scores[j] < sorted_scores[n-1]:
            return sorted_leaders[0:j]
    return sorted_leaders
    
def leaderboard_cyclopedptide_sequencing(spectrum, n):
    """Heuristic algorithm to find best candidate linear spectrum consistent with a given cyclospectrum when there are mismatches and errors""" 
    leaderboard = [""]
    leaderpeptide = [""]
    while len(leaderboard) != 0:
        leaderboard = expand(leaderboard)
        leaderboard_copy = list(leaderboard)
        for pep in leaderboard:
            if peptide_mass(pep) == max(spectrum):
                if score(pep, spectrum) > score(leaderpeptide[0], spectrum):
                    leaderpeptide = [pep]
                elif score(pep, spectrum) == score(leaderpeptide[0], spectrum):
                    leaderpeptide.append(pep)
                    #print score(pep, spectrum)
            elif peptide_mass(pep) > max(spectrum):
                leaderboard_copy.remove(pep)
        leaderboard = trim2(leaderboard_copy, spectrum, n)
    if leaderpeptide == type("a"):
        return leaderpeptide, mass_list(leaderpeptide)
    else:
        return leaderpeptide, [mass_list(leaderpep) for leaderpep in leaderpeptide]

def spectral_convolution(spectrum):
    convolution = list()
    for idx1, obj1 in enumerate(spectrum):
        for idx2, obj2 in enumerate(spectrum):
            if not idx1 == idx2:
                if 57 <= (obj2 - obj1) <= 200:
                    convolution.append(obj2 - obj1)
    return convolution

def spectral_convolution_winners(spectrum, m):
    """Pick M most popular masses in spectral convolution, with ties."""
    multiplicity = dict()
    masses = list()
    cnt = Counter(spectral_convolution(spectrum))
    for key in cnt.keys():
        if cnt[key] in multiplicity.keys():
            multiplicity[cnt[key]].append(key)
        else:
            multiplicity[cnt[key]] = [key]
    for key in reversed(sorted(multiplicity.keys())):
        if len(masses) < m:
            masses.extend(multiplicity[key])
        else:
            return masses
    return masses


def convolution_cyclopeptide_sequencing(spectrum, n, m):
    """Use spectral convolution to restrict AA alphabet to top m AAs in convolution.
    Then implement leaderboard cyclopeptide sequencing with a leaderboard of size n."""
    mass_winners = spectral_convolution_winners(spectrum, m)
    print len(spectral_convolution(spectrum))
    print len(mass_winners)
    leaderboard = [[]]
    leaderpeptide = [[]]
    while len(leaderboard) != 0:
        leaderboard = mass_expand(leaderboard, mass_winners)
        leaderboard_copy = list(leaderboard)
        for pep in leaderboard:
            if sum(pep) == max(spectrum):
                if mass_score(pep, spectrum) > mass_score(leaderpeptide[0], spectrum):
                    leaderpeptide = [pep]
                elif mass_score(pep, spectrum) == mass_score(leaderpeptide[0], spectrum):
                    leaderpeptide.append(pep)
                    #print score(pep, spectrum)
            elif sum(pep) > max(spectrum):
                leaderboard_copy.remove(pep)
        leaderboard = mass_trim(leaderboard_copy, spectrum, n)
    for i in leaderpeptide:
        print i, mass_score(i, spectrum)
    return leaderpeptide

def format_convolution(convolution_cyclopep_seq_output):
    for i in convolution_cyclopep_seq_output:
        print "-".join([str(j) for j in i])
    
#test_spec = [int(m) for m in list("0 71 101 114 115 147 147 172 185 186 186 248 262 286 294 300 301 319 371 372 395 409 433 448 466 472 486 487 510 557 580 581 595 601 619 634 658 672 695 696 748 766 767 773 781 805 819 881 881 882 895 920 920 952 953 966 996 1067"
#.split())]
#x = cyclopeptide_sequencing(test_spec)
##leaders = "GFAQHVMEGIGLDVKFTNIISCFFDHEWSTCHCKHHNSINHTMSMVF LIGDDDEADNCMMMVQSIKWKTLLRYGAFFTFPFYSYAILHVFYVLW KPMWWAFIFGFCDMKNCFDAPFWMHNSVQWEQHYRCNDVKMMSQLCW MAPRDIRMYFDKYHETAALDSQWIIQQIYHLMNVRKLNRTNRFTSVG FEKYHQQQILIDAQRVRLVHTVARAGPGWVQTGGWQQTCPRYKPYAW NVNPCERSSPPNFSWFMSFWADNSDYGDVIFCCPSVLRTMEMQSKKG WDTDTFFQKAMLKKDETADQIFNLRPYSLTCHNENILGNDNQEKQAG TLGSGENDKGHTVGAGHKGHPEREFEAPIERHEHPRVMMTKVGCYWI VCGHHHEQTVIMKAFDAWKVGFLGPIVAWVIFPAVYLWGKSLCPWTN YDSPTTYLSTHCHRLTNRMVHENPVICPPQDFAKYLIQSGWEFPLVA KDPINQTGDTNVRNFNVGCFCGCYFQWERHDGTPMHFWFSQKLSLTW HMKKLFWGIMKHHILFDFVNQPAFTNKAKGPTPHKAEELIRNLGQEK FNDRQRLVCHTNQCCAYKNKVVCSGGGSEISTNAHTYHFLALGHQVG MYYSAWTEPYYPPTLQIWWWYWKYGCTACQTGPHTMVFVQPTCKCVH YYGYRQCSWCQRWTVRRMLCWIDVLHKALHWHVCLLFHQALYGFSHE WASIGAIMRSAKDMYESLEFHKTHCTYFVYMVCKEARPGWTFFIEWV".split()
##spect = [int(m) for m in "0 71 87 97 97 99 101 101 101 101 101 103 103 113 113 113 113 113 113 113 113 114 114 115 115 128 128 129 129 129 129 129 129 131 131 131 137 137 147 147 156 156 156 163 163 163 186 186 198 200 200 202 202 204 214 214 216 216 216 226 228 230 234 242 242 242 242 242 242 244 245 253 257 257 257 259 260 266 266 268 269 271 276 276 276 276 278 283 284 285 287 293 294 299 301 303 313 317 317 317 327 329 331 343 343 347 354 355 355 356 359 363 363 370 370 371 371 372 379 382 384 388 389 397 397 400 405 407 408 408 413 413 415 415 416 418 418 420 422 428 430 430 432 434 439 444 455 456 458 459 473 476 484 484 485 485 487 499 500 501 506 507 510 510 511 513 515 518 522 526 527 528 529 529 531 533 533 537 540 541 544 544 545 547 558 559 562 568 569 571 572 574 585 586 588 597 598 607 610 612 616 619 620 624 624 625 626 631 636 641 644 646 650 657 657 660 662 663 669 669 670 671 672 674 675 678 681 684 685 689 691 692 696 698 699 700 700 701 711 733 733 735 738 738 739 741 753 771 772 772 773 775 775 775 778 779 782 783 783 786 788 789 794 794 797 798 798 800 801 802 804 805 806 808 810 813 815 828 837 840 846 854 862 864 864 866 869 882 884 885 886 888 889 899 901 902 902 903 904 907 908 911 911 914 914 924 925 926 928 935 935 937 937 941 941 945 952 955 961 961 975 975 977 984 987 988 992 995 999 1002 1013 1015 1016 1017 1017 1017 1022 1025 1032 1032 1038 1039 1039 1040 1044 1051 1055 1058 1058 1059 1062 1065 1066 1070 1070 1072 1074 1084 1088 1097 1099 1100 1101 1103 1104 1105 1106 1118 1118 1121 1130 1133 1135 1142 1150 1151 1153 1153 1154 1154 1156 1165 1171 1172 1186 1187 1194 1196 1198 1200 1201 1201 1202 1207 1212 1213 1214 1215 1216 1217 1217 1218 1218 1219 1231 1233 1234 1234 1236 1248 1255 1259 1264 1267 1272 1279 1281 1285 1298 1300 1301 1309 1311 1315 1315 1315 1316 1318 1319 1319 1321 1325 1330 1331 1334 1335 1338 1341 1343 1344 1346 1347 1348 1352 1363 1363 1372 1379 1395 1396 1398 1402 1410 1414 1414 1422 1422 1428 1429 1429 1430 1431 1432 1433 1434 1435 1435 1438 1447 1448 1450 1452 1460 1461 1471 1472 1472 1476 1476 1478 1481 1494 1499 1509 1515 1517 1521 1525 1532 1534 1535 1535 1535 1543 1546 1548 1551 1557 1557 1561 1561 1561 1562 1566 1566 1573 1577 1581 1585 1585 1589 1603 1605 1606 1608 1609 1609 1612 1618 1628 1634 1635 1636 1638 1647 1663 1664 1664 1664 1672 1672 1674 1674 1677 1680 1682 1686 1690 1694 1699 1702 1708 1713 1715 1716 1718 1718 1722 1723 1724 1740 1741 1743 1748 1749 1756 1763 1777 1777 1778 1781 1785 1792 1801 1803 1803 1805 1810 1811 1811 1815 1819 1819 1822 1823 1827 1830 1837 1837 1842 1844 1849 1850 1853 1869 1872 1876 1878 1878 1879 1887 1905 1906 1906 1912 1916 1916 1916 1924 1925 1929 1934 1936 1939 1940 1940 1940 1948 1948 1950 1965 1972 1979 1979 1991 1993 1996 2000 2000 2005 2007 2007 2009 2017 2019 2019 2026 2031 2034 2035 2039 2042 2053 2053 2058 2061 2064 2076 2079 2079 2087 2087 2094 2096 2097 2103 2113 2118 2120 2120 2123 2125 2132 2132 2135 2135 2136 2138 2140 2147 2150 2167 2171 2171 2192 2193 2200 2200 2200 2205 2209 2216 2216 2219 2224 2226 2226 2232 2233 2233 2233 2235 2237 2250 2252 2262 2266 2266 2268 2276 2284 2287 2296 2300 2303 2313 2318 2334 2334 2334 2336 2336 2337 2339 2347 2349 2355 2355 2356 2363 2363 2365 2366 2379 2380 2389 2397 2397 2413 2413 2416 2418 2434 2435 2437 2446 2447 2449 2449 2452 2466 2468 2468 2473 2476 2490 2492 2493 2494 2494 2494 2502 2510 2511 2519 2526 2533 2536 2542 2547 2549 2550 2553 2560 2578 2579 2579 2586 2597 2605 2605 2615 2620 2622 2623 2624 2624 2625 2627 2631 2632 2634 2648 2650 2650 2650 2651 2655 2689 2691 2706 2710 2711 2715 2733 2733 2733 2735 2738 2742 2742 2744 2747 2751 2753 2756 2761 2763 2768 2771 2779 2802 2807 2813 2820 2824 2825 2828 2836 2836 2836 2843 2846 2862 2862 2866 2871 2873 2876 2876 2881 2882 2900 2903 2907 2924 2933 2933 2937 2938 2944 2944 2949 2953 2957 2965 2972 2975 2975 2975 2987 2995 2999 3004 3018 3034 3034 3037 3037 3038 3039 3058 3062 3066 3066 3070 3073 3078 3078 3082 3088 3101 3104 3112 3119 3130 3135 3138 3149 3151 3152 3163 3163 3171 3172 3179 3190 3191 3193 3195 3217 3217 3220 3229 3238 3241 3241 3243 3244 3248 3250 3251 3276 3286 3291 3292 3300 3308 3318 3320 3321 3330 3335 3342 3351 3351 3354 3354 3357 3358 3358 3372 3387 3405 3407 3420 3422 3429 3431 3433 3433 3434 3439 3448 3455 3471 3483 3485 3486 3486 3488 3510 3514 3521 3533 3534 3534 3535 3546 3551 3552 3568 3585 3596 3599 3599 3600 3611 3611 3614 3615 3622 3634 3635 3647 3649 3664 3664 3681 3682 3696 3697 3708 3713 3727 3728 3728 3728 3735 3748 3750 3751 3771 3777 3797 3809 3812 3827 3828 3837 3841 3841 3842 3851 3857 3864 3864 3868 3868 3884 3898 3913 3940 3940 3942 3943 3955 3965 3969 3970 3970 3977 3981 4013 4014 4027 4027 4044 4053 4054 4056 4057 4083 4096 4098 4099 4110 4126 4140 4140 4140 4145 4155 4158 4167 4171 4184 4209 4211 4212 4223 4253 4255 4259 4268 4272 4284 4296 4296 4299 4303 4313 4352 4368 4373 4374 4397 4397 4397 4400 4409 4409 4416 4428 4465 4469 4487 4501 4510 4510 4526 4529 4538 4560 4566 4572 4584 4630 4639 4639 4639 4643 4651 4673 4673 4681 4685 4752 4752 4752 4768 4782 4786 4786 4802 4829 4853 4867 4881 4881 4883 4915 4915 4942 4968 4968 4982 4994 5028 5044 5069 5069 5071 5095 5097 5157 5157 5170 5184 5198 5210 5258 5270 5299 5311 5313 5371 5373 5412 5426 5474 5486 5527 5575 5587 5642 5688 5743 5844".split()]
#leaders = "LAST ALST TLLT TQAS".split()
#spect = [int(m) for m in "0 71 87 101 113 158 184 188 259 271 372".split()]
#print trim2(leaders, spect, 5)
#spect = [int(m) for m in "0 97 99 114 128 147 147 163 186 227 241 242 244 260 261 262 283 291 333 340 357 385 389 390 390 405 430 430 447 485 487 503 504 518 543 544 552 575 577 584 632 650 651 671 672 690 691 738 745 747 770 778 779 804 818 819 820 835 837 875 892 917 932 932 933 934 965 982 989 1030 1039 1060 1061 1062 1078 1080 1081 1095 1136 1159 1175 1175 1194 1194 1208 1209 1223 1225 1322".split()]
#spect = [int(m) for m in "0 97 99 113 114 115 128 128 147 147 163 186 227 241 242 244 244 256 260 261 262 283 291 309 330 333 340 347 385 388 389 390 390 405 435 447 485 487 503 504 518 544 552 575 577 584 599 608 631 632 650 651 653 672 690 691 717 738 745 770 779 804 818 819 827 835 837 875 892 892 917 932 932 933 934 965 982 989 1039 1060 1062 1078 1080 1081 1095 1136 1159 1175 1175 1194 1194 1208 1209 1223 1322".split()]
#spect = [int(m) for m in "0 97 99 113 114 115 128 128 147 147 163 186 227 241 242 244 244 256 260 261 262 283 291 309 330 333 340 347 385 388 389 390 390 405 435 447 485 487 503 504 518 544 552 575 577 584 599 608 631 632 650 651 653 672 690 691 717 738 745 770 779 804 818 819 827 835 837 875 892 892 917 932 932 933 934 965 982 989 1039 1060 1062 1078 1080 1081 1095 1136 1159 1175 1175 1194 1194 1208 1209 1223 1322".split()]
##spect = [int(m) for m in "0 97 99 113 114 115 128 128 147 147 163 186 227 241 242 244 244 256 260 261 262 283 291 309 330 333 340 347 385 388 389 390 390 405 435 447 485 487 503 504 518 544 552 575 577 584 599 608 631 632 650 651 653 672 690 691 717 738 745 770 779 804 818 819 827 835 837 875 892 892 917 932 932 933 934 965 982 989 1039 1060 1062 1078 1080 1081 1095 1136 1159 1175 1175 1194 1194 1208 1209 1223 1322".split()]
##x = leaderboard_cyclopedptide_sequencing(spect, 1000)
##for i in x[1]:
        
##    print i
M = 390
N = 19
spec = [int(m) for m in "329 251 479 1152 1413 1200 820 813 417 763 114 884 923 365 1240 1090 393 1304 428 1422 87 646 1441 759 1299 128 507 1270 1482 137 1142 1062 554 1368 270 379 772 332 1455 1028 1141 793 1109 756 628 620 1204 506 900 427 1432 1351 1048 541 635 555 1455 949 242 941 535 1015 369 1176 1569 683 887 521 427 682 407 131 1441 934 314 299 1014 934 113 1063 1318 877 1291 278 886 218 1383 147 515 962 1438 776 114 265 1034 749 555 806 1142 663 607 186 906 1327 256 1190 1237 303 241 685 1328 201 1135 1313 1021 1014 1441 797 635 1266 434 1456 128 1162 548 0 460 156 1255 1054 128 692 810 669".split()]
#format_convolution(convolution_cyclopeptide_sequencing(spec, N, M))


#156-147-131-87-114-128-186-113-128-128-137-114, score 134
#formatted [156, 147, 131, 87, 114, 128, 186, 113, 128, 128, 137, 114]
#wrong answers:
#[114, 128, 186, 113, 128, 128, 137, 114, 156, 147, 131, 87] 134
#[114, 87, 131, 147, 156, 114, 137, 128, 128, 113, 186, 128] 134
#[113, 186, 128, 114, 87, 131, 147, 156, 114, 137, 128, 128] 134
#[113, 128, 128, 137, 114, 156, 147, 131, 87, 114, 128, 186] 134
#[87, 131, 147, 156, 114, 137, 128, 128, 113, 186, 128, 114] 134
#[87, 114, 128, 186, 113, 128, 128, 137, 114, 156, 147, 131]
