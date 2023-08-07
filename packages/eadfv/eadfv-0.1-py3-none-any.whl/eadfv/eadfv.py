import unicodedata

def getreallen(input_s) :
    lo = 0
    input_k = str(input_s)
    for c in input_k:
        if unicodedata.east_asian_width(c) in ['F', 'W']:
            lo+=2
        else: 
            lo+=1
    return lo
    

def prettyprint(input_s, max_size) :
    lo = 0 
    for c in input_s:
        if unicodedata.east_asian_width(c) in ['F', 'W']:
            lo+=2
        else: 
            lo+=1
    output = str(input_s) + " "*(int(max_size+3)-lo)
    print(output, end='')

def view(df, int1, int2) :
    maxlen = []
    for j in range(len(df.columns.values.tolist())) :
        maxlen.append(0)
    for k in range(len(df.columns.values.tolist())) :
        i = str(df.columns.values.tolist()[k])
        if getreallen(i) > maxlen[k] : maxlen[k] = getreallen(i)
    for rowname in range(int1, int2) :
           for k in range(len(df.columns.values.tolist())) :
                i = df.columns.values.tolist()[k]
                if getreallen(str(df[i][rowname])) > maxlen[k] : maxlen[k] = getreallen(str(df[i][rowname]))
    for k in range(len(df.columns.values.tolist())) :
        prettyprint(df.columns.values.tolist()[k], maxlen[k])
    print("\n", end='')
    for rowname in range(int1, int2):
        for k in range(len(df.columns.values.tolist())) :
            i = df.columns.values.tolist()[k]
            prettyprint(str(df[i][rowname]), maxlen[k])
        print("\n", end='')