# TESTES

Utilizamos testes para fazer os possíveis caminhos que o usuário pode tomar na nossa aplicação e saber lidar com cada uma das situações.
<br><br>

# Configuração

Antes de tudo instale as biliotecas apropriadas para isso.

```bash
Linux
pip3 install pytest pytest-django # Use pytest-django apenas se estiver no django

Windows
pip install pytest pytest-django

UV
uv add pytest pytest-django
```

Depois crie um arquivo "pytest.ini" na raiz do projeto e faça as configurações necessárias.

```bash
[pytest]
DJANGO_SETTINGS_MODULE = <NOME_DO_SEU_PROJETO_DJANGO>.settings
python_files = test.py tests.py test_*.py tests_*.py *_test.py *_tests.py # Deixar claro quais arquivos o pytest deve procurar
```
<br>

# Utilizando

SEMPRE utilize a palavra **"test"** no início de qualquer função ou classe.

O pytest já nos entrega diversas funções prontas para cada situação.

```bash
assertEqual(valor_esperado, valor_que_estou_passando) -> Testa se ambos os parâmetros são iguais

assertIs(valor_esperado, valor_que_estou_passando) -> Assim como o "is" no python, testa se ambos os parâmetros ocupam o mesmo valor na memória

assertTemplateUsed(valor_esperado, valor_que_estou_passando) -> Testa se a view está realmente utilizando o template correto

assertIn(valor_esperado, valor_que_estou_passando) -> Testa se um determinado texto existe dentro do template
```
