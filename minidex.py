#!/usr/bin/python3
#A miniature pokedex by Oscar D'amico - Last updated Jan 7, 2020
import requests, time, os.path, hashlib, sys
import lxml.html as lh
import pandas

#Takes the user-provided search string and returns a copy of said
#string with only legal characters. 
def sanitize(input_string):
    input_allowed='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&1234567890-'
    output_string = ''
    for i in input_string:
        if i not in input_allowed:
            outchar = ''
        else:
            outchar = i
        output_string += outchar
    return output_string

#Check if user supplied the '+' flag, which is used to print more results than
#usual later on in the code
def extend(input_string):
    if '+' in input_string:
        return True
    else:
        return False
    

#Takes the data file name, the hashfile, and a verbosity boolean value
#Opens the data file and calculates an md5 hash for it. If the hashes match
#true is returned. If not, False is returned and we let the user know that
#the file is corrupt. 
def is_corrupt(filename, hashfile, verb):
    hasher = hashlib.md5()
    with open(filename, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    if verbose:
        print("Calculated hash for", filename, " --> "+hasher.hexdigest())
    afile.close()
    hashfile.seek(0)
    if hasher.hexdigest() == hashfile.read():
        return True
    else:
        print("[-] Critical file",filename, "corrupted...")
        return False

#Takes the url of a page containing tables, and returns
#a pandas data frame with the table contents. 
def urlToFrame(url):
    page=requests.get(url)
    doc=lh.fromstring(page.content)
    elements = doc.xpath("//tr")
    column = []
    n = 0
    for field in elements[0]: #This for loop creates an empty frame with necessary fields
        n+=1
        name=field.text_content()
        column.append((name,[]))
    for j in range(1,len(elements)):
        T=elements[j] 
        i=0

        for t in T.iterchildren():
            data=t.text_content() 
            if i>0:
                try:
                    data=int(data)
                except:
                    pass
            column[i][1].append(data)
            i+=1
    Dict={title:column for (title,column) in column}
    df=pandas.DataFrame(Dict)
    return df

#Takes a data filename and an open hash file. Replaces the open hash
#file's contents with the calculated hash,
def save_hash(filename, hashname):
    hasher = hashlib.md5()
    with open(filename, 'rb') as bfile:
        buff = bfile.read()
        hasher.update(buff)
    hashfile = open(hashname,"w+")
    hashfile.truncate()
    hashfile.write(hasher.hexdigest())
    hashfile.close()


#Takes a string value for the filename and a boolean value for verboseness. 
#If the verbose value is true, a status update is printed for the user. 
#If the file does not exist, file_check opens and closes the file in w+
#mode to create it. 
def file_check(name, verb):
    if not os.path.exists(name):
        if verb:
            print("[!]", name, "not present, creating it now...\n")
        fh = open(name, "w+")
        fh.close()

#Files fail integrity check until actually tested.
database_integrity_passed = False
typechart_integrity_passed = False
print_more = False
truncated = False
verbose = False
argv = sys.argv
argc = len(sys.argv)
search=''

#We check command line arguments for the '-v' flag.
#This sets verbose to True/False.
if argc > 1:
    if '-v' in argv: 
        verbose = True
        argv.remove('-v')
        argc = len(argv)
    if argc > 1:
        searchstr = argv[1]
        print_more = extend(searchstr)
        search = sanitize(searchstr)





bannertext = '''
                                  ,'\\
    _.----.        ____         ,'  _\   ___    ___     ____
_,-'       `.     |    |  /`.   \,-'    |   \  /   |   |    \  |`.
\      __    \    '-.  | /   `.  ___    |    \/    |   '-.   \ |  |
 \.    \ \   |  __  |  |/    ,','_  `.  |          | __  |    \|  |
   \    \/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  |
    \     ,-'/  /   \    ,'   | \/ / ,`.|         /  /   \  |     |
     \    \ |   \_/  |   `-.  \    `'  /|  |    ||   \_/  | |\    |
      \    \ \      /       `-.`.___,-' |  |\  /| \      /  | |   |
       \    \ `.__,'|  |`-._    `|      |__| \/ |  `.__,'|  | |   |
        \_.-'       |__|    `-._ |              '-.|     '-.| |   |
                                `'                            '-._|
-------------------------------------------------------------------------
'''

file_check("dex_data.csv", verbose)
file_check("dex_hash.md5", verbose)
file_check("type_data.csv", verbose)
file_check("type_hash.md5", verbose)

#See if we can read the files properly and get hashfile contents.
#If there's an IOError, notify the user. 
#Database represents the CSV file containing pokedex number, Name, Type, and all stats for each pokemon.
#Typechart represents the CSV file containing every possible type-matchup table.
#Typechart_hashfile and database_hashfile are both files that contain hashes of the aforementioned CSV files. 
try:
    database = open("./dex_data.csv", "r+")
    database_hashfile = open("./dex_hash.md5", "r+")
    typechart = open("./type_data.csv", "r+")
    typechart_hashfile = open("./type_hash.md5", "r+")
except IOError:
    print("[-] Could not open one or more files. Quitting...")


#database.seek(0)
#database_hashfile.seek(0)
#typechart_hashfile.seek(0)
#typechart.seek(0)

#checking integrity for both data files
database_integrity_passed = is_corrupt("dex_data.csv", database_hashfile, verbose)
database_hashfile.seek(0)
if verbose:
    print("Stored hash in dex_hash.md5 --> "+database_hashfile.read())
typechart_integrity_passed = is_corrupt("type_data.csv", typechart_hashfile, verbose)
typechart_hashfile.seek(0)
if verbose:
    print("Stored hash in type_hash.md5 --> "+typechart_hashfile.read())


#If the database data file is corrupt or over a week old: notify the user,
#grab the data, clean it, export it to a CSV, and save its calculated hash. 
if not(database_integrity_passed) or (time.time() - os.path.getmtime("dex_data.csv") > 604800): 
    print("[-] Database file contains no data or is outdated\nUpdating it now...")
    
    df = urlToFrame("https://pokemondb.net/pokedex/all")
    df = df.applymap(lambda s:s.lower() if type(s) == str else s)
    df['Type'] = df['Type'].map(lambda x: x.strip())
    df.columns = ['Pokédex #', 'Name', 'Type', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk',
       'Sp. Def', 'Speed']
    df.apply(lambda x: x.astype(str).str.lower())
    df.to_csv(r'./dex_data.csv', index = None, header=True)
    save_hash("dex_data.csv","dex_hash.md5")
#Perform the same check as above, but for the typechart. 
if not(typechart_integrity_passed) or (time.time() - os.path.getmtime("type_data.csv") > 604800):
    print("[-] Type chart file contains no data or is outdated\nUpdating it now...")

    df_types = urlToFrame("https://pokemondb.net/type/dual")
    del df_types["PKMN"]
    df_types.columns = ['Defending Type', 'Nor', 'Fir', 'Wat', 'Ele', 'Gra', 'Ice', 'Fig',
       'Poi', 'Gro', 'Fly', 'Psy', 'Bug', 'Roc', 'Gho', 'Dra', 'Dar', 'Ste',
       'Fai']
    df_types = df_types.replace(r'\n',' ', regex=True) 
    df_types.replace('', "- ", inplace=True)
    df_types.replace('½', "1/2", inplace=True)
    df_types.replace('¼', "1/4", inplace=True)
    
    df_types['Defending Type'] = df_types['Defending Type'].str.replace(' — ','')
    df_types['Defending Type'] = df_types['Defending Type'].str.replace('  ','')
    df_types['Defending Type'] = df_types['Defending Type'].map(lambda x: x.strip())
    df_types = df_types.applymap(lambda s:s.lower() if type(s) == str else s)
    df_types.apply(lambda x: x.astype(str).str.lower())
    df_types.to_csv(r'./type_data.csv', index = None, header=True)
    save_hash("type_data.csv","type_hash.md5")

df=pandas.read_csv("dex_data.csv")
df=df.applymap(lambda s:s.lower() if type(s) == str else s)
df_types=pandas.read_csv("type_data.csv")

if search != '' or print_more ==True:
    pass
else:
    searchstr = input(bannertext+"Search by Pokémon name [q --> quit, + --> keep printing]\n> ")
    print_more = extend(searchstr)
    search = sanitize(searchstr)

while search != "q":    
    result = df[df['Name'].str.contains(search, case=False)]
    if not result.empty:
        print('\n\n')
        i=0
        
        for line in result.to_string(index=False).splitlines():
            print("-"*len(line)+'-'+'+')
            print(line, end=' |\n')
            if i >0:
                poke_type=result.iloc[i-1]["Type"]
                type_result = df_types[df_types['Defending Type'].str.match(poke_type, case=False)]
                type_result = type_result[(type_result['Defending Type'] == poke_type)] 
                type_result = type_result.iloc[:,1:]
                
                for lines in type_result.to_string(index=False).splitlines():
                    diff = -7 + (len(line)-len(lines))
                    print('\t'+lines, end=diff*' '+'|\n')
            i+=1
            if not(print_more) and i > 10:
                truncated = True
                break
            
        if print_more or i <= 10:
            truncated = False
        print("-"*len(line)+'-'+'+', end='\n\n\n')
        print("Matches: ",len(result), end="")
        if truncated:
            print(" (truncated to 10 lines)\n")
        else:
            print('\n')
        i=1
        resultNum = result.to_string().count('\n')
    else:
        resultNum=0

    searchstr = input("Search by Pokémon name [q -> quit, + -> keep printing]\n> ")
    print_more = extend(searchstr)
    search = sanitize(searchstr)
    
database.close()
database_hashfile.close()
typechart.close()
typechart_hashfile.close()
