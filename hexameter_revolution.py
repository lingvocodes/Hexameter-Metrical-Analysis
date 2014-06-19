import re, codecs, hexa_types, operator, os

file_name = "marked"  #hex_text

cowboy = codecs.open("testing_issues.txt", "w", "utf-8")
avatar = codecs.open("analyzed_hexameter.csv", "w", "utf-8")


dift_dict = {u'ä': u'ae', u'ö': u'oe', u'à': u'au', u'è': u'eu', u'ù': u'uj'}
dift_two_list = [u'ae', u'oe', u'au', u'eu', u'uj']
dift_dict_stressed = {u'ä': u'áe', u'ö': u'óe', u'à': u'áu', u'è': u'éu', u'ù': u'új'}
vow_mapping = {u'a': u'ā', u'e': u'ē', u'i': u'ī', u'o': u'ō', u'y': u'ȳ', u'u': u'ū'} #to long
vow_mapping_stressed_to_long =  {u'á': u'ā', u'é': u'ē', u'í': u'ī', u'ó': u'ō', u'ú': u'ū'}
vow_mapping_mutual_to_short =  {u'a': u'ă', u'e': u'ĕ', u'i': u'ĭ', u'o': u'ŏ', u'u': u'ŭ'}

up_vowels = u"AEUIYO"

vowels = u'aeioyuēāīōūĭĕăўŭŏäöàèùáéíóú'
short_v  = u'aeioyu' #на самом деле обоюдные
shortest_v  = u'ĭĕăўŭŏ'
long_v = u'ȳūēāīōöàèù'
dift = u'äöàèù'
cons = u'qrtpsdfghjklzxcvbnm'
cv = vowels + cons
alls = cv + dift
vd = vowels + dift
all_vowels = vd + long_v + shortest_v
aux = u'#%'
prefix = u"\\W" # для проверки эффективности комментировать следующую строку
prefix = u"a|ab|abs|ad|ac|af|ag|al|an|ap|ar|as|at|aequi|alter|alti|amb|ambi|ambo|ante|bi|circum|cis|co|col|com|cor|con|contr|contra|de|di|dif|dis|е|ex|extra|il|im|ir|in|inaequi|infra|inter|intra|intro|multi|ob|oc|op|pauc|pauci|per|pluri|post|prae|pro|quadri|quin|quinque|re|semi|semper|sub|su|sue|suf|sug|sum|sup|sur|sus|super|supra|trans|tra|tri|ubi|ultra|uni"

#общая статистика
session_result = [] #array element - file, in file arrays of strings
session_results_failed = []



#функция распечатки результатов/отладки
maintenance = 0 #менять в коде, если нужно печатать 1) всё m=1, ничего m=0 2) 2 если что-то особенное! мм!
common = 1
def print_by(code, string):
    if maintenance == 1:
        print string
    elif maintenance == 0:
        pass
    elif maintenance == 2:
        if code == 1:
            print string
            
def u_v_detection(f):
    U, u, V, v = 0, 0, 0, 0
    for line in f:
        if "_processed-" in line: #пропуск заголовка файла
            continue
        if u"V" in line:
            V = 1
        if u"v" in line:
            v = 1
        if u"U" in line:
            U = 1
        if u"u" in line:
            u = 1
        if (U == 1) and (V == 1) and (u == 1) and (v == 1):
            return True
    if (U == 0) and (V == 1) and (u == 1) and (v == 0):
        return False
    else:
        return False #actually - wtf

def array_print(arr_arr):
    line = u""
    for i in arr_arr:
        line += u"["
        if (type(i) == float) or (type(i) == int):
            return str(i)
##        if isinstance(u, str):
##            return str(i)
        for j in range(len(i)):
            if j == 0:
                line += i[j] + u":"
            else:
                line += str(i[j]) + u":"
        line = line[:-1] + u"]_"
    return line[:-1]
            

def twoV_to_dift(line):
    for i in dift_dict:
        line = re.sub(dift_dict[i], i, line)
        line = re.sub(dift_dict_stressed[i], i, line)
    return line

def dift_to_twoV(line):
    for i in dift_dict:
        line = re.sub(i, dift_dict[i], line)
    return line

def shortV_to_longV(vowel):
    for i in vow_mapping:
        if i == vowel:
            return vow_mapping[i]
    return vowel

def longV_to_shortV(vowel):
    for i in vow_mapping:
        if vow_mapping[i] == vowel:
            return i
    return vowel

def mutualV_to_shortV(vowel):
    for i in vow_mapping_mutual_to_short:
        if i == vowel:
            return vow_mapping_mutual_to_short[i]
    return vowel

def mutualV_to_shortV_line(line):
    for i in vow_mapping_mutual_to_short:
        line = re.sub(i, vow_mapping_mutual_to_short[i], line)
    return line

def mutualV_to_longV_line(line):
    for i in vow_mapping:
        line = re.sub(i, vow_mapping[i], line)
    return line

def stressed_to_long(line):##
    for i in vow_mapping_stressed_to_long:
        line = re.sub(i, vow_mapping_stressed_to_long[i], line)
    return line

def equal_vowels(v1,v2):
    if (vow_mapping[v1] == v2) or (vow_mapping[v2] == v1):
        return True
    else:
        return False

def equal_vowels_dift(v1,v2): #обычно v2 - дифтонг
    if (v1 not in dift_two_list) and (v2 not in dift_two_list):
        return False
    if v2 in dift_two_list:
        if v1 in dift_dict:
            if (dift_dict[v1] == v2):
                return True
            else:
                return False
        else:
            return False
    if v1 in dift_two_list:
        if v2 in dift_dict:
            if (dift_dict[v2] == v1):
                return True
            else:
                return False
        else:
            return False

def shortV_to_longV_line(line):
    _v_ = re.search(u"(\\W|^)([aeiuoy])(\\W|^)", line)
    if _v_ != None:
        line = re.sub("(\\W|^)" + _v_.group(2) + "(\\W|^)", "\\1" + shortV_to_longV(_v_.group(2)) + "\\2", line)
    return line

# muta cum liquida и не только
def mcl(line):
    line = re.sub(u'([bpdtgc])([rl])', u'\\1%\\2', line)
    line = re.sub(u'([' + cons + '])(h)', u'\\1%\\2', line)
    line = re.sub(u'(^| )i' + '([' + all_vowels + '])', u'\\1j\\2', line)
    line = re.sub(u'qu', 'q', line) #'q%v', line)
    
    
    
    return line

# i -> j старая версия, не используется
def i_to_j(line):
    line = re.sub('(^| )i' + '([' + all_vowels + '])', '\\1j\\2', line) #// #iV > #jV
    line = re.sub('([' + all_vowels + '])' + 'i' + '([' + all_vowels + '])', '\\1j\\2', line) #// ViV > VjV
    return line


def main_dividers(line):
    #три согласные
    line = re.sub('([^^][' + cons + '])([' + cons + '])([' + cons + '][' + alls + '])', '\\1#\\2-\\3', line)
    line = re.sub('([^^][' + cons + '])([' + cons + '])([' + cons + '][' + alls + '])', '\\1#\\2-\\3', line)
    
    #две согласные
    line = re.sub('([^^][' + cons + '])([' + cons + '][' + alls + aux + '])', '\\1-\\2', line)
    line = re.sub('([^^][' + cons + '])([' + cons + '][' + alls + aux + '])', '\\1-\\2', line)
    #гласная-согласная
    line = re.sub('([' + vd + '])([' + cons + '][' + vowels + '%])', '\\1-\\2', line)
    line = re.sub('([' + vd + '])([' + cons + '][' + vowels + '%])', '\\1-\\2', line)
    
    #гласная-гласная
    line = re.sub('([' + vowels + '])([' + vd + '])', '\\1-\\2', line)
    return line

##line = u'tenebrae doctrina fortūna sanctum lectio patria deus lupus aratrum tenetnetnautreunio'

#собирающая функция для деления на слоги. принимает строку
def dis(line):
    line = line.lower()

    
    line = mcl(line) # muta cum liquida
    
    
##    line = twoV_to_dift(line)
##    line = i_to_j(line)
    line = main_dividers(line)

    
    
    #отчистка от служебных символов
    line = re.sub('[' + aux + ']', '', line)
    line = re.sub('([' + vowels + '])(-[' + vowels + '])', '\\1@\\2', line)
##    print line

    return line

#принимает слог, возвращает его длину в виде символов: — и v : долгий и короткий соответственно
def syl_amount(syl, next_syl):
    if re.search('[' + dift + ']', syl) != None:
        case = 'dift'
        s_a = u'—'
    elif re.search('[' + long_v + ']', syl) != None:
        case = 'long vowel'
        s_a = u'—'
    elif re.search('[' + shortest_v + ']', syl) != None:
        case = 'short vowel'
        s_a = u'v'
    elif re.search ('.+[' + cons + ']$', syl) != None:
        case = 'close syl'
        s_a =u'—'
    elif re.search ('@', syl) != None:
        syl = re.sub('@', '', syl)
        case = 'vowel after vowel syl'
        s_a =u'v'
##    elif (re.search('[' + short_v + ']$', syl) != None) and (re.search('^[bpdtgc][rl]', next_syl) != None): 
##        case = 'vowel before mcl'
##        s_a =u'v'
    else:
        case = 'unknown'
        s_a = u'x'
        
##    print syl + ' - ' + case + ' = ' + s_a
    return s_a


#принимает строку, поделенную на слоги, возвращает слоговую схему
##def syl_scheme(line):
##    line = re.sub(' ', '-', line)
##    s_s = ''
##    syls = line.split('-')
##    for syl in syls:
##        s_s += syl_amount(syl) + ' '
##    return s_s

#вспомогательная функция, используется дял тестирования. печатает все
#символы, не являющиеся обычными символами латинского алфавита, то есть
#с диакритиками, знаки препиания и т.д. по одному разу каждый.
def aux_symbols(line):
    sym = ['']
    for i in line:
        if re.search('[a-zA-Z]', i) == None:
            i = i.lower()
            if i not in sym:
                sym.append(i)
    for i in sym:
        print i, 

#возвращает "красивую схему"
def print_syl_input(i_s):
    s = re.sub('([^ ])([^ ])','\\1 \\2',i_s)
    s = re.sub('([^ ])([^ ])','\\1 \\2',s)
    return s

def replace_vowel(match): # для i_j_analyzer 
    return match.group(1).replace(match.group(1), shortV_to_longV(match.group(1)) + u"j" + match.group(2))

def i_j_analyzer(line, marker):
##    marker = 1 #для проверки эффективности
    if marker == 1:
        return line
    #   #iV > #jV то есть на границе слова или после приставкой (исключения - формы глагола eo и другие)
    line = re.sub(u"(\\W|^)(" + prefix + "|)?i([" + all_vowels + "])", u"\\1\\2j\\3", line)
    #   ViV > VjV, причем гласный перед j долгий.
    line = re.sub(u"([" + all_vowels + "])i([" + all_vowels + "])", replace_vowel, line)
    return line

def u_super_changer(line):
    new_line = u""
    line_array = line.split()
    for word in line_array:
        if re.search(u"<[uVv]>",word) != None:
            word2 = re.sub(u"<u>",u"v", word)
            word2 = re.sub(u"<v>",u"u", word2)
            if word2 in dictionary_full:
                new_line += word2 + u" "
            else:
                new_line += word + u" "
        else:
            new_line += word + u" "
            
    return new_line[:-1]

def u_v_analyzer(line, uv_mark, j_marker):
    if uv_mark == True:
        return line, j_marker
    line = re.sub(u"([uVv])", u"<\\1>", line) # <[uVv]>
    line = i_j_analyzer(line, j_marker)
    line = re.sub(u"<[uVv]>([" + cons + u"])", u"u\\1", line) # *+СОГЛ (в любом месте) > u+СОГЛ
    line = re.sub(u"(\\W|^)<[uVv]>([" + all_vowels + u"])", u"\\1v\\2", line) #*+ГЛ (в начале слова) > v+ГЛ
    line = re.sub(u"<[uVv]>(\\W|$)", u"u\\1", line)

    if re.search(u"<[uVv]>",line) != None:
        line = u_super_changer(line)

    line = re.sub(u"<([uVv])>", u"\\1", line)
    return line, 0


def caes_cut_scheme(sorted_schemes, caes_scheme):
    result = []
    caes_dict = {} #словарь из схем  с цезурами
    for i in caes_scheme:
        caes_dict[(re.sub(u"\\|", u" ", i[0]))] = i[1]
    for i in range(len(sorted_schemes)):
        if sorted_schemes[i][0] in caes_dict:
            result.append((sorted_schemes[i][0],sorted_schemes[i][1], caes_dict[sorted_schemes[i][0]]))
    return result

def clarify_caesura(detected):
    #если одинаковые цезуры везде 
    equality = True     
    for i in detected:
        for j in detected:
            if i[1] != j[1]:
                equality = False
        if equality == False:
            break
        
    if equality == True:
        return False, 1

    #если не одинаковые

    #если нашли точную схему, то возвращать True
    return False, detected
    

def caesura_types(caes_scheme):
    types = []
##    "^—.(v.v|—).—.(v.v|—).—.(v.v|—)"
    if re.search(u"^—.(v.v|—).—\\|(v.v|—).—.(v.v|—)", caes_scheme) != None:
        types.append(3)
    if re.search(u"^—.(v.v|—).—.(v v|—).-\\|(v.v|-)", caes_scheme) != None:
        types.append(5)
    if re.search(u"^—.(v.v|—).—.(v v|—).—.v\\|v", caes_scheme) != None:
        types.append(5.5)
    if re.search(u"^—.(v.v|—).—.(v.v|—).—.(v.v|—).—\\|(v.v|—)", caes_scheme) != None:
        types.append(7)
##    if types:
##        print caes_scheme
    return types

def caesura(line, syllables, schemes):
    right = u""
    line = re.sub(u"([.,;!:?-]|\'|\")", u'', line).lower()
    
    syls_new = u""
    for i in syllables:
        syls_new += longV_to_shortV(i)
    
    
    syllables = syls_new
##    syllables_spaces = return_qu_with_spaces(line, syllables)
    syls_new = dift_to_twoV(syllables)
    
    w_ww = re.findall(u"\\w\\w \\w\\w", line)
##    print line
    for i in w_ww:
        i = re.sub(u" ",u"-", i)
        syls_new = re.sub(u"(" + i[0] + "(" + i[1] + ")?)-(" + i[3] + "|j)(" + i[4] + ")",u"\\1_-\\3\\4", syls_new)
##    print syls_new
##    print syllables_spaces
    syls_new_split = syls_new.split(u"-")
##
    caesuras_array = [] 
##    print line
##    print syls_new
    for scheme in range (len(schemes)):
        sch_caesura = u""
        sch = schemes[scheme][0].split(u" ")
        
        #составление строки из массива с символами (строка с цезурами)
        for i in range(len(sch)):
            if u"_" in syls_new_split[i]:
                sch_caesura += sch[i] + u"|"
            else:
                sch_caesura += sch[i] + u" "
        sch_caesura = re.sub(u"\\n", u"", sch_caesura.strip(u" "))
        caesuras_array.append([sch_caesura, caesura_types(sch_caesura)])
    #определение наиболее вероятной схемы по цезуре. черточки означают не только цезуры, но паузы в целом
    print_by(1, u"Цезуры:")##################################################
    detected = [] #список схем с максимальным количеством цезур
    d_max = 0
##    print line
    cowboy.write(line + u"\r\n")
    cowboy.write(syllables + u"\r\n")
    for i in caesuras_array:
##        print i[0]
##        print i[1]
        cowboy.write(i[0] + u"\r\n Цезуры: \r\n")
        for k in i[1]:
            cowboy.write(u" [" +str(k) + u" половинная] ")
        cowboy.write(u"\r\n")
        if len(i[1]) > d_max:
            detected = []
            d_max = len(i[1])
            detected.append(i)
        elif len(i[1]) == d_max:
            detected.append(i)
##    print ''
    cowboy.write(u"\r\n\r\n")

    for d in detected:
        print_by(1, d[0])########################################
        print_by(1, d[1])
##    for s in schemes: #schemes это кортеж где s[0] - схема
##        print s[0]
##    print ""

    if len(detected) == 1:
        return detected, True
    elif len(detected) > 1:
        is_one, varified = clarify_caesura(detected)
        if is_one == True:
            return varified, True
        else:
            return detected, False
    else:
        return detected, False # no yet ready!!!


#составление словаря из текстов
##print u"Составление динамичного словаря..."
dictionary_full = {}
for root, dirs, files in os.walk('thes_lat'):
    for file_n in files:
        if u"processed"  in file_n:
##            print file_name
            f_n_2 = file_n[:-4]
            text = codecs.open(u'thes_lat//' + f_n_2 + u".txt", "r", "utf-8")
            u_v_d = u_v_detection(text)
            if u_v_d == False:
                text.close()
                continue
            elif u_v_d == True:
                text.close()
                text = codecs.open(u'thes_lat//' + f_n_2 + u".txt", "r", "utf-8")
                for line in text:
                    line = line.lower().split()
                    for w in line:
                        w = w.strip(u'!?.,/{}[]()-:;')
                        if w not in dictionary_full:
                            dictionary_full[w] = 1
                        else:
                            dictionary_full[w] += 1
            else:
                text.close()
            text.close()

##sas = u"vis animae flammaeue; ruit qUa proxima cedunt"
##
##print u_v_analyzer(sas, True, 0)
##for i in dictionary_full:
##    if u"vol" in i:
##        print i
def find_vowels(line):
    return re.findall(u"[" + all_vowels + "]{1,2}", line)

def split_two_vowels(line_array, rang):
##    print line_array,
##    print "<<<<<<<<<<<<<<<<<<<<<<<"
    new_ar = []
    if rang != 0:
        for i in range(rang):
            new_ar.append(line_array[i])
##    print (rang+1)
##    print len(line_array)
    

    two_vow = re.sub(u"([" + all_vowels + "])", u"\\1%", line_array[rang]).strip(u"%").split(u"%")
##    print two_vow,
##    print " - two_vow"
    for i in two_vow:
        new_ar.append(i)

    if (rang+1) <= len(line_array):
        for i in range(rang+1,len(line_array)):
            new_ar.append(line_array[i])
##    print new_ar,
##    print " - -- - new ar"
    return new_ar
                     

def qu_eliz_aferez_factor(line):
    line = re.sub(u"qU", u"qu", line)
    line = re.sub(u'([' + all_vowels + all_vowels.upper() + ']m?\\W?) \\W?(Ee)(st?)', u"\\1\\3", line)
    line = re.sub(u'([' + all_vowels + all_vowels.upper() + '])(m?\\W? \\W?h?[' + all_vowels + all_vowels.upper() + '])',u"\\2" , line)
    return line
##def equal_vowels_dift(line_vowel, syllable_vowel):

def elision_aux(match):
    return match.group(1).replace(match.group(1), match.group(1).upper() + match.group(2))

def afereza_aux(match):
    return match.group(2).replace(match.group(2), match.group(1) + match.group(2).upper() + match.group(3))

def elision_factor(line):
    line = re.sub(u"qu", u"qU", line)
    line = re.sub(u'([' + all_vowels + ']m?\\W? \\W?)(e)(st?)', afereza_aux, line)
    line = re.sub(u'([' + all_vowels + '])(m?\\W? \\W?h?[' + all_vowels + '])', elision_aux, line)
    return line

def glue(array): #склеивает все элементы массива в  одну строку
    line = u""
    for i in array:
        line += i
    return line

def low_array_text(array):
    for i in range (len(array)):
        array[i] = array[i].lower()
    return array

def phonetic_marker(line, syllables, scheme, j_detect, u_v_detect):
    print syllables
    line = line.lower()
    marked_line = u""
    line, j_detect = u_v_analyzer(line, u_v_detect, j_detect)
    line = i_j_analyzer(line, j_detect)
    #1
    line = elision_factor(line)
    line_vowel_split = re.sub(u"([" + all_vowels + "]{1,2})", u"\\1%", line).split(u"%")
##    line_vowel_split = low_array_text(line_vowel_split)
    if re.search(u"[" + all_vowels + "]",line_vowel_split[-1]) == None:
        line_vowel_split[-2] = line_vowel_split[-2] + line_vowel_split[-1]
        line_vowel_split.pop(-1)
##    print line_vowel_split
##    print len(line_vowel_split)
##    print syllables
##    print len(find_vowels(syllables))
##    print scheme
##    print glue(line_vowel_split)
    scheme_split = scheme.split()
    if len(line_vowel_split) == len(scheme.split()):
        for i in range (len(line_vowel_split)):
            if scheme_split[i] == u"—":
                line_vowel_split[i] = mutualV_to_longV_line(line_vowel_split[i])
            elif scheme_split[i] == u"v":
                line_vowel_split[i] = mutualV_to_shortV_line(line_vowel_split[i])
        return glue(line_vowel_split).lower()
    #2
    else:
        line_vowels = find_vowels(line)
        syllable_vowels = find_vowels(syllables)
        if len(line_vowels) < len(syllable_vowels):
            min_vow = len(line_vowels)
            max_vow = len(syllable_vowels)
        else:
            min_vow = len(syllable_vowels)
            max_vow = len(line_vowels)
        j = 0
##        print line_vowels
##        print syllable_vowels
        for i in range(min_vow):
##            print line_vowels[i],
##            print syllable_vowels[j]
##            print len(line_vowels),
##            print "line"
##            print len(syllable_vowels),
##            print "syll_vow"

            if (i+1) < len(line_vowel_split):
                if (line_vowels[i] == u"e") and (u"est" in line_vowel_split[i+1]):
                    line_vowel_split = split_two_vowels(line_vowel_split, i)
                    j += 2
##                    print line_vowel_split[i]
                    continue
            if j < min_vow:
                if line_vowels[i] == syllable_vowels[j]:
                    j+=1
                    continue
                if equal_vowels_dift(line_vowels[i], syllable_vowels[j]) == True:
                    j+=1
                    continue
                if syllable_vowels[j] in u'ēāīōȳū':
                    if line_vowels[i] in u"eaiuyo":
                        if vow_mapping[line_vowels[i]] == syllable_vowels[j]:
                            j += 1
                            continue
##            print j + 1,
##            print "j + 1"
##            print max_vow,
##            print "max_vow"
            if (j) < min_vow-1:
##                print line_vowels[i],
##                print syllable_vowels[j] + syllable_vowels[j+1]
##                print syllable_vowels[j] + line_vowel_split[j+1][0]
                if (line_vowels[i] == (syllable_vowels[j] + syllable_vowels[j+1])): #up_vowels
                    qu_eliz_aferez = qu_eliz_aferez_factor(line_vowel_split[j])
                    if len(set(qu_eliz_aferez)&set(up_vowels)) != 0:
                        continue
##                    print line_vowels[i]
##                    print syllable_vowels[j] + syllable_vowels[j+1]
##                    print line
##                    print syllables
##                    print line_vowel_split
                    line_vowel_split = split_two_vowels(line_vowel_split, j)
                    j += 2
                    continue
                elif (line_vowels[j] + line_vowel_split[j+1][0] in dift_two_list):
                    if equal_vowels_dift(line_vowels[j] + line_vowel_split[j+1][0], syllable_vowels[j]) == True:
                        line_vowel_split[j] += line_vowel_split[j+1][0]
                        line_vowel_split[j+1] = line_vowel_split[j+1][1:]
                        j+=2
                        continue
                elif (line_vowel_split[j][-1] + line_vowel_split[j+1][0] in dift_two_list):
                    if equal_vowels_dift(line_vowel_split[j][-1] + line_vowel_split[j+1][0], syllable_vowels[j+1]) == True:
                        line_vowel_split[j+1] = line_vowel_split[j][-1] + line_vowel_split[j+1]
                        line_vowel_split[j] = line_vowel_split[j][:-1]
                        j+=2
                        continue
##                    print j
        if len(line_vowel_split) == len(scheme_split):
            for i in range (len(line_vowel_split)):
                if scheme_split[i] == u"—":
                    line_vowel_split[i] = mutualV_to_longV_line(line_vowel_split[i])
                elif scheme_split[i] == u"v":
                    line_vowel_split[i] = mutualV_to_shortV_line(line_vowel_split[i])
            return glue(line_vowel_split).lower()
        else:
            return u"marking_failed"
##            print line_vowel_split
##            print len(line_vowel_split)
##            print glue(line_vowel_split)
##            print scheme
##            print len(scheme_split)
##            print syllables
                


        
        
##        print ""

##line = u"latonae magniqUe jouis decus, aurea proles,"
##syllables = u"la-to-nä-mag-ni-qe-jo-uis-de-cu-sà-re-a-pro-les"
##scheme = u"— — — — — v v — v v — v v — x"
##phonetic_marker(line, syllables, scheme, 0, False)
##asd = raw_input("kkkk")

#основная часть программы с обработкой файла <<<<<<<<<<<<<
def analyze(file_name):
    hex_txt_file = codecs.open('thes_lat//' + file_name +'.txt', 'r', 'utf-8')
    eagle = codecs.open('thes_lat//statistics//accuracy_stat_' + file_name[:-10] + '.txt', 'w', 'utf-8')
    
    #статистические, вспомогательные и общие переменные
    hex_lines = 0
    definite = {} #словарь определенных
    definite_count = 0 #сколько определенных
    results = [] #первичная база с определенными и неопределенными строками
    arr_results = [] #массив массивов(инфы о строках)


    
    dif_80 = 0
    dif_30_to_80 = 0
    dif_30 = 0

    #caes
    caes_stats = 0
    caes3 = 0
    caes5 = 0
    caes55 = 0
    caes7 = 0

    #анализ на различение j и i
    for line in hex_txt_file:
        if "_processed-" in line: #пропуск заголовка файла
            continue
        if u'j' not in line:
            j_detect = 0
        else:
            j_detect = 1
            break
    hex_txt_file.close()

    if j_detect == 0:
        print_by(1, u"Различение i и j: Нет") ##################
    else:
        print_by(1, u"Различение i и j: Да")

    #анализ на различение u и v
    hex_txt_file = codecs.open('thes_lat//' + file_name +'.txt', 'r', 'utf-8')
    u_v_detect = u_v_detection(hex_txt_file)

    hex_txt_file.close()

    
    hex_txt_file = codecs.open('thes_lat//' + file_name +'.txt', 'r', 'utf-8')
    #основная обработка
    for line in hex_txt_file:
        line = line.lower()
        line = line.strip(u" ")
        
##        print line
        if "_processed-" in line: #пропуск заголовка файла
            continue
        if (len(line) < 4) or (re.search("\\w", line) == None):
            continue

        
        RESULT_CHECK = "" #для вывода на экран и второго анализа. старая версия
        line_array = []   #то же самое, что result_check, только
                            #в массивах и без надписей типа "Строка: "

        h0_line = line.strip("\n")
        RESULT_CHECK += u"Строка:\t\t" + line # 0 -------Строка------------
        line_array.append(h0_line)
        


        #if re.search('([' + all_vowels + ']) ([' + all_vowels + '])',line) != None:
        #if re.search('([' + all_vowels + ']m) (h[' + all_vowels + '])',line) != None:
        #if re.search('([' + vd + '])([' + cons + '][' + vowels + '%])',line) != None:
        #    print line
        
        line = re.sub("[,.;]", '', line) #убираем запятые, точки и двоеточия
        line = re.sub("\[.*]?", '', line) #убираем текст в квадратных скобках

        
        #ВНИМАНИЕ всякие разные штучки ЗДЕСЯ!!!!!!!!!!!!!!!!!!!!!!!!!!!!



        #афереза
        line = re.sub('([' + all_vowels + ']m? )e(st?)', '\\1\\2', line)
        line, j_detect = u_v_analyzer(line, u_v_detect, j_detect)
        line = i_j_analyzer(line, j_detect)
##        line = u"castorea eliadum palmas epiros equarum"
##        print line
        #элизия - это весело
        line = re.sub('([' + all_vowels + '])([' + all_vowels + ']m?) (h?[' + all_vowels + '])', '\\1% \\3', line)
        line = re.sub('([' + all_vowels + ']m?) (h?[' + all_vowels + '])', ' \\2', line)
        line = re.sub('%', ' ', line)
        #line = re.sub(u'([' + all_vowels + ']m\\s) ' + '([' + all_vowels + '])', u' \\2', line) #элизия    Vm+ v

        #i и j

    
##        print line
##        f = raw_input("f")

        
        #замена стоящей отдельно гласной
        line = shortV_to_longV_line(line)

        #дифтонги теперь И здесь. другая в dis. чтобы не преобразовывала гласные на сытке которые элизируются
         #преобразует дифтонги. 
        
        line = line.strip('\r\n;,. ')
        line = twoV_to_dift(line)
        line = stressed_to_long(line)
        p = re.sub("([, ;:?!-]|\'|\")", '', line)
        #p = re.sub('-+', '', p)
        p = dis(p)

        #строка, поделенная на слоги
            
        #работа со сторокой поделенной на слоги (с дефисами)
        p = re.sub("-([" + cons + "])-", "-\\1",p) #убирает отдельно стоящую согласную, принятую за слог

    ##    if (re.search("-[" + cons + "]-", p) != None):
    ##        print p
        
        h1_syllables = re.sub(u'@', u'', p)

        RESULT_CHECK += u"Слоги:\t\t" + h1_syllables + '\n' # 1 -------Слоги------------
        line_array.append(h1_syllables)
        #print h1_syllables
        
        syls = p.strip('-').split('-')
        # len(syls)
            
        input_syls = ''
        for i in range(len(syls)):
            if i < len(syls)-1:
                input_syls += syl_amount(syls[i], syls[i+1])
            else:
                input_syls += syl_amount(syls[i], u".")


        h2_syl_number = len(syls)
        RESULT_CHECK += u"Число слогов:\t" + str(h2_syl_number) + '\n' # 2 -------число слогов------------
        line_array.append(h2_syl_number)
           
        #схема строки---------------------------
        h3_task = print_syl_input(input_syls)

        RESULT_CHECK += u'Задание:\t' + h3_task + '\n'
        line_array.append(h3_task)

        
        #вывод результата
        if len(syls) > 17:
            line_array.append(u"_no scheme_")
            line_array.append(u'syllables_more_then_17')
            RESULT_CHECK += u'Результат:\tНЕТ. Количество слогов больше 17-ти.' + '\n'
            session_results_failed.append(line_array)
##            arr_results.append(line_array)
            print_by(1, RESULT_CHECK)
        elif len(syls) < 12:
            line_array.append(u"_no scheme_")
##            line_array.append(u'syllables_less_then_12')
            RESULT_CHECK += u'Результат:\tНЕТ. Количество слогов меньше 12-ти.' + '\n'
            session_results_failed.append(line_array)
            print_by(1, RESULT_CHECK)
        else:
            h4_result = hexa_types.ind_type(input_syls)
            if u"Не подходит" in h4_result:
                line_array.append(u"_no scheme_")
                line_array.append(u"not_defined")
            RESULT_CHECK += u'Результат:\t' + h4_result + '\n'

            #
    ##        if (re.search('[' + short_v + ']-[bpdtgc][rl]', p) != None):
    ##            print RESULT_CHECK
            #
            
            results.append(RESULT_CHECK) #добавление в первичную базу
##            print line_array
            arr_results.append(line_array) #добавление в массив массивов инфы о строке
            print_by(0, RESULT_CHECK)
        print_by(0, "")


        #statistics1 подсчет точно определенных схем
        statistics_1 = re.search(u"(Результат:.*)", RESULT_CHECK)
        if statistics_1 != None:
            hex_lines += 1
            scheme_what = statistics_1.group(1) #строка с результатом
            if u"нет" not in scheme_what.lower(): #есть ли в строке с результатом слово нет
                definite_count += 1
                scheme_what = re.sub(u"Результат:\\s*", u"", scheme_what)
                if scheme_what not in definite:
                    definite[scheme_what] = 1
                else:
                    definite[scheme_what] += 1



    #2-ой проход с учетом полученных при первом проходе данных <<<<<<<<<<<<<<<<<<<<<<<<<<<<<2<<<<<<<<<<<<<<<2<<<<<<<<<2
    for i in range(len(results)):
        not1_solution = re.search(u"решение не единственно\\):(.*(\n?.*)*)", results[i])
        no_solution = re.search(u"Не подходит ни к одному", results[i])
##        results[i] += u"Точность схемы:\t"
        if not1_solution == None:
            if no_solution == None:
                solution = re.search(u"Результат:\\t*(.*)", results[i])
                arr_results[i].append(solution.group(1))
                arr_results[i].append(u"primary")
                arr_results[i].append(u"no_additional_schemes_or_info")
##                for j in arr_results[i]:
##                    print j

            else:
                pass ##ни один из вариантов/слогов меньше 
        else:
            cur_dict = {} #словарь с текующими вариантами
            sols = not1_solution.group(1).split(u"или")
    ##        print "\nnext" #составления частотного словаря для этих схем
            for s in sols:
                if len(s) < 4:
                    continue
                s = re.sub(u"(\\n|\\t)", u"", s).strip("\s")
                for d in definite:
                    match_found = 0
                    if s == d:
                        s_fr = definite[d]
                        match_found = 1
                        break
                if match_found == 1:
                    cur_dict[s] = s_fr
                else:
                    cur_dict[s] = 0

            #выбор наиболее вероятной схемы и проставление метки _______
            sorted_cur_dict = sorted(cur_dict.iteritems(), key=operator.itemgetter(1), reverse=True)

            #выбор по цезуре
            caes_scheme, caes_detected = caesura(arr_results[i][0], arr_results[i][1], sorted_cur_dict)
            
            if caes_detected == True:
                if len(caes_scheme) == 1:
                    arr_results[i].append(re.sub(u"\\|", u" ", caes_scheme[0][0]))
                    arr_results[i].append(u"caesura")
                    arr_results[i].append(caes_scheme[0][1])
                    caes_stats += 1
                    if caes_scheme[0][1][0] == 7:
                        caes7 += 1
                    if 5.5 in caes_scheme[0][1]:
                        caes55 += 1
##                        print arr_results[i][0]
##                        print arr_results[i][1]
##                        print arr_results[i][4]
##                        print caes_scheme[0][0]
##                        print caes_scheme[0][1]
##                    for j in arr_results[i]:
##                        print j
##                    print ""
##                else 
            else:
                #по частотности
                if len(sorted_cur_dict) == len(caes_scheme):
                    caes_cutted = False
                else:
                    caes_cutted = True
                    sorted_cur_dict = caes_cut_scheme(sorted_cur_dict, caes_scheme)




                sum_freq = 0
                for s_d in sorted_cur_dict:
                    sum_freq += s_d[1]
                difference = int((float(sorted_cur_dict[0][1])/float(sum_freq) * 100))

                if difference > 80:
                    dif_80 += 1
                elif (difference > 30) and (difference <= 80):
                    dif_30_to_80 += 1
                else:
                    dif_30 += 1

                #добавляем определившуюся схему, способ определения, все варианты
                arr_results[i].append(sorted_cur_dict[0][0]) #схема
                other_accuracy = u""
                if caes_cutted == True: #способ
                    caesura_accuracy = u"caesura|"
                    other_accuracy += caesura_accuracy
                arr_results[i].append(other_accuracy + u"byFrequency%=" + str(difference))
                arr_results[i].append(sorted_cur_dict)
                    
##                for h in arr_results[i]:
##                    print h
####                    if u"caesura|" in h[5]:
####                        print h
##                print ""

    
    count_succes = 0
    for ind in range(len(arr_results)):
        hex_array = arr_results[ind]
        #print hex_array #hex_array[1] - дифтонг есть
        if hex_array[5] != u"not_defined": #если схема определилась
            arr_results[ind].append(phonetic_marker(hex_array[0],hex_array[1],hex_array[4], j_detect, u_v_detect)) #добавляем размеченную строк
        if arr_results[ind][-1] != u"marking_failed":
            count_succes += 1
##    for i in arr_results:
##        for j in i:
##            print j
##    print ""
##    for line in arr_results:
##        original = re.sub(u"(\n|\r)", u"", line[0])
##        if line[5] == u"primary":
##            avatar.write(original + u"+" + re.sub(u"(\n|\r)", u"", line[7]) + u"+" + re.sub(u"(\n|\r)", u"", line[4]) +  u"+" + u"первичный" + u"\r\n")
##        elif line[5] == u"caesura":
##            avatar.write(original + u"+" + re.sub(u"(\n|\r)", u"", line[7]) + u"+" + re.sub(u"(\n|\r)", u"", line[4]) +  u"+" + u"по цезуре" + array_print(line[6]) + u"\r\n")
##        elif u"caesura" in line[5]:
##            avatar.write(original + u"+" + re.sub(u"(\n|\r)", u"", line[7]) + u"+" + re.sub(u"(\n|\r)", u"", line[4]) +  u"+" + u"по цезуре и частоте" + array_print(line[6]) + u"\r\n")
##        elif u"Frequency" in line[5]:
##            avatar.write(original + u"+" + re.sub(u"(\n|\r)", u"", line[7]) + u"+" + re.sub(u"(\n|\r)", u"", line[4]) +  u"+" + u"по частоте" + array_print(line[6]) + u"\r\n")
##        else:
##            avatar.write(original + u"+" + re.sub(u"(\n|\r)", u"",line[4]) + u"+" + re.sub(u"(\n|\r)", u"",line[5]) + u"\r\n")
##    print ""
##    print u"Успешно размечено",
##    print count_succes,
##    print u"строк из ",
##    print len(arr_results)
    session_result.append(arr_results)
    

        
#здесь пробег по результатам всего файла
##first_file = session_result[0]
##for i in first_file:
##    print i

    
    eagle.write(str(difference) + u"\r\n")
##            print results[i],
##            print difference
    ##        
    ##        print "-------"

#всегда выводить
    print file_name + u"; ",
    print hex_lines
    print u"первый проход",
    print u";",
    print definite_count,
    print u";" + str(u"%.2f" % ((definite_count + 0.0)/float(hex_lines) * 100.0 )) + u"; %"
##    print u"Дополнительно:"
    print  u"распознано с помощью цезур;: " + str(caes_stats) +  str(";%.2f" % ((caes_stats + 0.0)/float(hex_lines) * 100.0 )) + "; %"
    print u"группа с точностью более 80%:;" + str(dif_80) + str(";%.2f" % ((dif_80 + 0.0)/float(hex_lines) * 100.0 )) + "; %"
    print u"группа с точностью от 30% до 80%:;" + str(dif_30_to_80) + str(";%.2f" % ((dif_30_to_80 + 0.0)/float(hex_lines) * 100.0 )) + "; %"
    print  u"группа с точностью менее 30%:;"+ str(dif_30) + str(";%.2f" % ((dif_30 + 0.0)/float(hex_lines) * 100.0 )) + "; %"
##    print caes55
##    print caes7

    print ""


##    for i in range(len(results)):
##        stroka = re.search(u"(Строка:\\s*.*)",results[i]).group(1)
##        if i > 130:
##        if arr_results[i][0] not in stroka:
##            print i
##            print re.search(u"(Строка:\\s*.*)",results[i]).group(1)
##            print arr_results[i][0]
##        print arr_results[i][1]
##        print ""
        

    hex_txt_file.close()
    eagle.close()

##проверка одного файла
##analyze(file_name)

#все файлы
for root, dirs, files in os.walk('thes_lat'):
    for file_n in files:
        if u"processed" in file_n:
            f_n = file_n[:-4]
            analyze(f_n)
            
avatar.write(u"Строка+Разметка+Схема+Точность+Дополнительно\r\n")
for filehex in session_result:
    for line in filehex:
        original = re.sub(u"(\n|\r)", u"", line[0])
        if line[5] == u"primary":
            avatar.write(original + u"+" + re.sub(u"(\n|\r)", u"", line[7]) + u"+" + re.sub(u"(\n|\r)", u"", line[4]) +  u"+" + u"первичный" + u"\r\n")
        elif line[5] == u"caesura":
            avatar.write(original + u"+" + re.sub(u"(\n|\r)", u"", line[7]) + u"+" + re.sub(u"(\n|\r)", u"", line[4]) +  u"+" + u"по цезуре" + array_print(line[6]) + u"\r\n")
        elif u"caesura" in line[5]:
            avatar.write(original + u"+" + re.sub(u"(\n|\r)", u"", line[7]) + u"+" + re.sub(u"(\n|\r)", u"", line[4]) +  u"+" + u"по цезуре и частоте" + array_print(line[6]) + u"\r\n")
        elif u"Frequency" in line[5]:
            avatar.write(original + u"+" + re.sub(u"(\n|\r)", u"", line[7]) + u"+" + re.sub(u"(\n|\r)", u"", array_print(line[6])) +  u"+" + u"не определено\r\n")
        else:
            avatar.write(original + u"+" + re.sub(u"(\n|\r)", u"",line[4]) + u"+" + re.sub(u"(\n|\r)", u"",line[5]) + u"\r\n")
        
cowboy.close()
avatar.close()
