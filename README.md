# **LoginChecker**

- [x] O LoginChecker automatiza o processo de validação de credenciais em portais de login, facilitando tanto a verificação de credenciais já obtidas quanto a execução de técnicas como password spraying.

🔍 Com essa ferramenta, você pode melhorar significativamente a eficiência e a eficácia dos testes de segurança das suas aplicações, garantindo que vulnerabilidades relacionadas a autenticações sejam rapidamente identificadas e corrigidas.

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
