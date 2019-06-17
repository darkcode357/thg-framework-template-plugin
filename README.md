# cmd2 Plugin Template

## Table of Contents

- [Using this template](#using-this-template)
- [Naming](#naming)
- [Adding functionality](#adding-functionality)
- [Examples](#examples)
- [Development Tasks](#development-tasks)
- [Packaging and Distribution](#packaging-and-distribution)
- [License](#license)


## Usando este template

Este template assume que você está criando um novo plugin cmd2_thg_ chamado `myplugin`. Seu
plugin terá um nome diferente. Você precisará renomear alguns dos arquivos e
diretórios neste template. Não esqueça de modificar as importações e o `setup.py`.

Você provavelmente também vai querer reescrever o README descrevendo oque o seu plugin pode fazer :)
#gddev

## nome 


Você deve prefixar o nome do seu projeto com `cmd2-thg-`. Dentro desse projeto,
você deve ter um pacote com o prefixo `cmd2_thg_`.


## Adicionando funcionalidade

Existem muitas maneiras de adicionar funcionalidades ao `thg` usando um plugin. 
A maioria dos plugins
será implementado como um mixin. Um mixin é uma classe que encapsula e injeta
o código em outra classe(class principal). Desenvolvedores que usam um plugin no  `thg`,
irá injetar o código do plugin em sua subclasse de `THGBASECONSOLE(Cmd):`.



### Mixin e Inicialização

O exemplo a seguir mostra como e o inicio de um plugin e como funciona o plugin

Aqui está o plugin:

```python
class MyPlugin:
    def __init__(self, *args, **kwargs):
        # código colocado aqui é executado antes do cmd2.Cmd inicializar
        super().__init__(*args, **kwargs)
        # O código colocado aqui é executado antes do cmd2.Cmd inicializar

```

exemplo de um aplicativo que usa o plug-in:

```python
import cmd2
import cmd2_thg_

class Example(cmd2_thg_.MyPlugin, cmd2.Cmd):
    """Uma class para mostrar como usar um plugin"""
    def __init__(self, *args, **kwargs):
        # o código colocado aqui é executado antes de cmd2.Cmd ou antes de 
        # quaisquer plugins inicializar
        super().__init__(*args, **kwargs)
        # código colocado aqui é executado após cmd2.Cmd todos os outros plugins forem
        # inicializados
```


observe como o plugin deve ser herdado antes do `cmd2.Cmd`. Isto é
necessário por dois motivos:

- O método `cmd.Cmd .__ init __ ()` na biblioteca padrão do python não ira ser chama
  - `super().__init__()`.Devido a esse descuido, se você não herdar do `MyPlugin` o
  - `MyPlugin.__init__()`método nunca será chamado
- Você pode querer que seu plugin seja capaz de sobrescrever métodos  `cmd2.Cmd`.
  Se você herdar o plugin depois do `cmd2.Cmd`, a ordem de resolução dos métodos do python
  irá chamar os métodos `cmd2.Cmd` antes de chamar os metodos do seu plugin.



### Adicionar comandos

Seu plugin pode adicionar comandos visíveis ao usuário. Você faz do mesmo jeito 
que você fazeria em um aplicativo `cmd2.Cmd`:

```python
class MyPlugin:

    def do_say(self, statement):
        """Comando simples"""
        self.poutput(statement)
```


Você tem os todos os recursos dentro de um plugin, que contruiu dentro de um
aplicativo `cmd2.Cmd`, incluindo a análise de argumentos por meio de `decoradores` e ajuda  para personalizada
métodos.


### Adicionar (ou ocultar) configurações

Um plugin pode adicionar configurações controláveis ​​pelo usuário ao aplicativo
exemplo:

```python
class MyPlugin:
    def __init__(self, *args, **kwargs):
        # código colocado aqui é executado antes de cmd2.Cmd inicializar
        super().__init__(*args, **kwargs)
        # código colocado aqui é executado após o cmd2.Cmd inicializar
        self.mysetting = 'somevalue'
        self.settable.update({'mysetting': 'short help message for mysetting'})
```


Você também pode ocultar as configurações do usuário, removendo `self.settable`.


### Decoradores

Seu plugin pode fornecer um decorador que os usuários do seu plugin podem usar para finalizar
funcionalidade em torno de seus próprios comandos.


### Substituir métodos

Seu plugin pode sobrescrever os métodos principais `cmd2.Cmd`, mudando seu comportamento.
Essa abordagem deve ser usada com parcimônia, porque é muito frágil. Se um
O desenvolvedor escolhe usar vários plug-ins em seus aplicativos e vários
plugins sobrescrevem o mesmo método, somente o primeiro plugin a ser mixado
terá o método substituído chamado.

Os Hooks são uma abordagem muito melhor.
### Hooks


Plugins podem registrar hooks, que são chamados por `cmd2.Cmd` durante vários pontos
no ciclo de vida do programa `aplicativos e comandos`. Plugins não devem anular
qualquer um dos métodos de gancho obsoletos, eles devem registrar seus ganchos como
[descrito](https://cmd2.readthedocs.io/en/latest/hooks.html) na documentação do  cmd2.

Você deve nomear seus hook para que eles comecem com o mesmo nome do seu plugin. hooks
métodos são misturados no aplicativo `cmd2` e essa convenção de nomenclatura ajuda
evitar a substituição não intencional do método.


exemplo simples

```python
class MyPlugin:

    def __init__(self, *args, **kwargs):
        # O código colocado aqui é executado antes que o cmd2 inicialize
        super().__init__(*args, **kwargs)
        # O código colocado aqui é executado após o cmd2 inicializar
        # é aqui que você registra as funções do gancho
        self.register_postparsing_hook(self.cmd2_myplugin_postparsing_hook)

    def cmd2_myplugin_postparsing_hook(self, data: cmd2.plugin.PostparsingData) -> cmd2.plugin.PostparsingData:
        """Método a ser chamado após analisar a entrada do usuário, mas antes de executar o comando"""
        self.poutput('in postparsing_hook')
        return data
```

O registro permite que vários plugins sejam registados 

- Veja a [documentação do cmd2 hook](https://cmd2.readthedocs.io/en/latest/hooks.html)
para obter detalhes completos sobre o ciclo de vida do aplicativo e dos comando, incluindo todos os
ganchos disponíveis e as maneiras como os ganchos podem influenciar no ciclo de vida.


### Classes e Funções

Seu plugin também pode fornecer classes e funções que podem ser usadas no 
desenvolvimento de aplicativos baseados em cmd2 no caso do thg. Descrever essas classes e funções em
sua documentação para que os usuários do seu plugin saibam o que está disponível.

## Exemplos

Inclua um exemplo ou dois no diretório `examples` que demonstra como o seu
Plugin funciona. Isso ajudará os desenvolvedores a utilizá-lo de dentro de suas
aplicação.


## Development Tasks
```
$ invoke -l
```
Você pode executar várias tarefas em uma única chamada, por exemplo:
```
$ invoke clean docs sdist wheel
```


Esse comando removerá todo o cache superflous, testando e construindo
arquivos, renderizar a documentação e construir uma source distribution and a
wheel distribution.

para mais informacoes leia  `tasks.py`.


Ao desenvolver seu plugin, você deve se certificar de que suporta todas as versões do
python suportado por cmd2 e todas as plataformas suportadas. 
cmd2 usa três estratégia de teste hierárquico para atingir esse objetivo.

- [pytest](https://pytest.org) executa os testes unitários
- [tox](https://tox.readthedocs.io/) executa os testes de unidade em várias versões de python
- [AppVeyor](https://www.appveyor.com/) e [TravisCI](https://travis-ci.com)
executar os testes nas várias plataformas suportadas

Este modelo de plug-in está configurado para usar a mesma estratégia.



### Criar ambientes python

Este projeto usa [tox](https://tox.readthedocs.io/en/latest/) para executar o teste
com várias versões do python. Eu recomendo
[pyenv](https://github.com/pyenv/pyenv) com o
[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv>) plugin para gerenciar
estas várias versões. Se você é um usuário do Windows, o `pyenv` não funcionará para você,
mas [conda](https://conda.io/) também pode ser usado para resolver este problema.

Esta distribuição inclui um script de shell `build-pyenvs.sh` que
automatiza a criação desses ambientes.

Se você preferir criar esses virtualenvs manualmente, faça o seguinte:
```
$ cd cmd2_abbrev
$ pyenv install 3.7.0
$ pyenv virtualenv -p python3.7 3.7.0 cmd2-3.7
$ pyenv install 3.6.5
$ pyenv virtualenv -p python3.6 3.6.5 cmd2-3.6
$ pyenv install 3.5.5
$ pyenv virtualenv -p python3.5 3.5.5 cmd2-3.5
$ pyenv install 3.4.8
$ pyenv virtualenv -p python3.4 3.4.8 cmd2-3.4
```
Agora defina o pyenv para disponibilizar todos os três ao mesmo tempo:
```
$ pyenv local cmd2-3.7 cmd2-3.6 cmd2-3.5 cmd2-3.4
```


Se você executou o script ou o fez manualmente, agora você tem virtualenvs isolados
para cada uma das principais versões do python. Esta tabela mostra vários comandos python,
a versão do python que será executado, e o virtualenv será
utilizar.

| Command     | python | virtualenv |
| ----------- | ------ | ---------- |
| `python`    | 3.7.0  | cmd2-3.6   |
| `python3`   | 3.7.0  | cmd2-3.6   |
| `python3.7` | 3.7.0  | cmd2-3.7   |
| `python3.6` | 3.6.5  | cmd2-3.6   |
| `python3.5` | 3.5.5  | cmd2-3.5   |
| `python3.4` | 3.4.8  | cmd2-3.4   |
| `pip`       | 3.7.0  | cmd2-3.6   |
| `pip3`      | 3.7.0  | cmd2-3.6   |
| `pip3.7`    | 3.7.0  | cmd2-3.7   |
| `pip3.6`    | 3.6.5  | cmd2-3.6   |
| `pip3.5`    | 3.5.5  | cmd2-3.5   |
| `pip3.4`    | 3.4.8  | cmd2-3.4   |

## Instalar dependências

Instale todas as dependências de desenvolvimento:
```
$ pip install -e .[dev]
```
Este comando também instala `cmd2-myplugin` in-place", então o pacote aponta para
o código-fonte, em vez de copiar os arquivos para a pasta python `site-packages`.

Todas as dependências agora foram instaladas no `cmd2-3.7`
virtualenv. Se você quer trabalhar em outros virtualenvs, você precisará manualmente
selecione-o e instale novamente ::

   $ pyenv shell cmd2-3.4
   $ pip install -e .[dev]

Agora que você criou seus ambientes python, é necessário instalar o
pacote no lugar, junto com todas as outras dependências de desenvolvimento:
```
$ pip install -e .[dev]
```



### Testes de unidade em execução

Execute `invoke pytest` no diretório de nível superior do seu plugin para executar todas as
testes unitários encontrados no diretório `tests`.


### Use o tox para executar testes de unidade em várias versões do python

O `tox.ini` incluído está configurado para executar os testes unitários em python 3.4, 3.5, 3.6,
e 3.7. Você pode executar seus testes de unidade em todas essas versões do python por:
```
$ invoke tox
```

### Executa testes de unidade em várias plataformas

[AppVeyor](https://github.com/marketplace/appveyor) e
[TravisCI](https://docs.travis-ci.com/user/getting-started/) oferece planos gratuitos
para projetos de código aberto.


## Embalagem e Distribuição

Ao criar seu arquivo `setup.py`, tenha em mente o seguinte:

- use as palavras-chave `cmd2 plugin` para tornar mais fácil para as pessoas encontrarem o seu plugin
- como o cmd2 usa o versionamento semântico, você deve usar algo como
  `install_requires = ['cmd2> = 0.9.4, <= 2']` para ter certeza de que o seu plugin
  não tenta rodar com uma versão futura de `cmd2` com a qual pode não ser
  compatível


Licença ##

cmd2 [usa a licença muito liberal do MIT](https://github.com/python-cmd2/cmd2/blob/master/LICENSE).
Convidamos os autores de plugins a considerar fazer o mesmo.
