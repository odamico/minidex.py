# Minidex.py

> Pokedex at your Linux fingertips, providing a quick way to find data on various pokemon using python

To run this program, you will need the python3 and the libraries found in requirements.txt. This was 
tested in Ubuntu 19.10 and CentOS 8.

## Installation for Ubuntu
```sh
sudo apt install python3 python3-pip
git clone https://github.com/odamico/minidex.py
pip3 install -r requirements.txt --user
chmod +x ./minidex.py
./minidex.py
```

## Installation for CentOS
```sh
sudo yum install python3 python3-pip
git clone https://github.com/odamico/minidex.py
pip3 install -r requirements.txt --user
chmod +x ./minidex.py
./minidex.py
```
## Usage 
Normal usage is to run the script and enter a search query at the prompt:
```sh
./minidex.py
```
```

                                  ,'\
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
Search by Pokémon name [q --> quit, + --> keep printing]
> Barbaracle



----------------------------------------------------------------------------------------+
 Pokédex #        Name        Type  Total  HP  Attack  Defense  Sp. Atk  Sp. Def  Speed |
----------------------------------------------------------------------------------------+
       689  barbaracle  rock water    500  72     105      115       54       86     68 |
	 Nor  Fir Wat Ele Gra  Ice Fig  Poi Gro  Fly Psy Bug Roc Gho Dra Dar Ste Fai    |
	 1/2  1/4  -    2   4  1/2   2  1/2   2  1/2  -   -   -   -   -   -   -   -     |
----------------------------------------------------------------------------------------+


Matches:  1

Search by Pokémon name [q -> quit, + -> keep printing]
> q
```
After getting our result, we enter 'q' to quit.

We can perform a fast search by supplying a parameter when running the script

```sh
./minidex.py voltorb
```
```


-----------------------------------------------------------------------------------+
 Pokédex #     Name      Type  Total  HP  Attack  Defense  Sp. Atk  Sp. Def  Speed |
-----------------------------------------------------------------------------------+
       100  voltorb  electric    330  40      30       50       55       55    100 |
	Nor Fir Wat  Ele Gra Ice Fig Poi Gro  Fly Psy Bug Roc Gho Dra Dar  Ste Fai |
	 -   -   -   1/2  -   -   -   -    2  1/2  -   -   -   -   -   -   1/2  -  |
-----------------------------------------------------------------------------------+


Matches:  1

Search by Pokémon name [q -> quit, + -> keep printing]
> q
```
The -v flag can print debugging information
```sh
./minidex.py -v ho-oh
```
```
Calculated hash for dex_data.csv  --> ea91373cc20db8fba4487dbf3a73b9d2
Stored hash in dex_hash.md5 --> ea91373cc20db8fba4487dbf3a73b9d2
Calculated hash for type_data.csv  --> 1f12c6d848c02daf68533f7b5494af1f
Stored hash in type_hash.md5 --> 1f12c6d848c02daf68533f7b5494af1f



-------------------------------------------------------------------------------------+
 Pokédex #   Name         Type  Total   HP  Attack  Defense  Sp. Atk  Sp. Def  Speed |
-------------------------------------------------------------------------------------+
       250  ho-oh  fire flying    680  106     130       90      110      154     90 |
	Nor  Fir Wat Ele  Gra Ice  Fig Poi Gro Fly Psy  Bug Roc Gho Dra Dar  Ste  Fai|
	 -   1/2   2   2  1/4  -   1/2  -    0  -   -   1/4   4  -   -   -   1/2  1/2|
-------------------------------------------------------------------------------------+


Matches:  1

Search by Pokémon name [q -> quit, + -> keep printing]
> q
```
The '+' flag in a query will print all matches instead of truncating to 10 entries.
For example, to print all entries that start with 'a':
```
./minidex.py a+
```
## Note
The program re-scrapes the data it needs once per week. This will require internet connectivity.

More information on this project can be found at https://odamico.github.io/posts/minidex
