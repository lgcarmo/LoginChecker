# **LoginChecker**

- [x] O LoginChecker realiza a automatização do processo de validação das credenciais em portais de login. Como uma credencial já obtida ou um password spray

**Principais opções:**

- `-f`: arquivos com URL 
- `-u`: Usuario.
- `-p`: Password

**USO:**
```bash
$ python3 LoginChecker.py -f urls.txt -u john -p password
```
**Ferramentas relacionadas:**

O Luiz Carmo ([K40S](https://github.com/lgcarmo)) criou a ferramenta [ScrapForever](https://github.com/lgcarmo/Scrap_Forever). Esta ferramenta é utilizada para coletar URLs em uma página de forma que não termine enquanto não chegar à última página.
