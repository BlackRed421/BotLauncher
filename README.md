PoketLauncher v4.7

ATENÇÃO USANDO O LAUNCHER E O EDITOR DE MACROS SEUS MACROS SÃO COMPARTILHADOS.
EM UPDATES FUTUROS CORRIJO.



📖 Sobre o Projeto
O PoketLauncher é uma interface gráfica moderna e intuitiva, desenvolvida em Python com a biblioteca CustomTkinter, para gerenciar e lançar bots do OpenKore. A aplicação foi criada para simplificar o processo de configuração, execução e gerenciamento de múltiplos bots e suas macros, tudo a partir de um único local.

Com um visual inspirado no universo Pokémon, o launcher permite que os usuários associem seus bots a um Pokémon, tornando a interface mais amigável e divertida com GIFs animados.

✨ Funcionalidades Principais
Gerenciador de Bots: Adicione, edite e remova bots com facilidade, selecionando um dos 151 Pokémon originais para representar cada um.

Lançamento Rápido: Inicie seus bots do OpenKore e o cliente do jogo diretamente pela interface.

Gerenciador de Macros Completo:

Editor Integrado: Edite arquivos de automacro e macro diretamente no programa.

Compilador: Junte todos os seus macros ativos em um único arquivo macros.txt com um clique.

Importador Inteligente: Importe um macros.txt já existente e o divida automaticamente em arquivos individuais.

Configuração Centralizada: Defina todos os caminhos necessários em uma única janela.

Persistência de Dados: Suas configurações e lista de bots são salvas localmente.

🚀 Guia de Uso e Funcionamento
Pré-requisitos e Instalação
Antes de começar, garanta que você tenha o Python 3 instalado. Depois, instale as bibliotecas necessárias com um único comando:

pip install customtkinter pillow requests

Para executar, clone o repositório e rode o script:

git clone [https://github.com/seu-usuario/PoketLauncher.git](https://github.com/seu-usuario/PoketLauncher.git)
cd PoketLauncher
python app_desktop.py

1. Configuração Inicial (Passo a Passo)
Na primeira vez que abrir o launcher, a maioria das funções estará desabilitada. Para ativá-las, siga estes passos:

Na aba Bot Launcher, clique no botão Configurações.

Preencha os seguintes campos:

Pasta OpenKore: O caminho para a pasta principal do seu OpenKore (ex: C:/Users/SeuUsuario/Desktop/openkore).

Pasta de Macros: O caminho para a pasta onde o seu arquivo macros.txt está localizado. Geralmente, é a mesma pasta do OpenKore.

Cliente (.bat): O caminho para o arquivo .bat que inicia o cliente do seu jogo.

Clientes (XML): O caminho para o arquivo clients.xml do seu cliente, se aplicável.

Clique em "Salvar e Fechar". O aplicativo agora está pronto para ser usado.

2. Adicionando e Lançando um Bot
O PoketLauncher simplifica o uso de múltiplos bots, associando cada um a um arquivo de configuração específico.

Crie os Arquivos de Configuração: Dentro da sua pasta openkore/control/, você precisa ter um arquivo de configuração para cada personagem. Por exemplo:

config_MeuSacerdote.txt

config_MeuFerreiro.txt

Adicione um Bot no Launcher:

Clique em "Adicionar Bot".

Apelido: Dê um nome fácil de lembrar (ex: "Sacer Full Suporte").

Nome do Personagem (para config): Digite o nome exatamente como aparece no nome do arquivo de configuração, sem o config_ e o .txt. Para o arquivo config_MeuSacerdote.txt, você digitaria MeuSacerdote.

Pokémon: Escolha um Pokémon na lista para representar o bot.

Clique em "Adicionar Bot".

Como o Lançamento Funciona:

Quando você clica em "Iniciar" em um card, o PoketLauncher executa o OpenKore com um comando especial que aponta para o arquivo de configuração correto.

Por exemplo, para o bot "MeuSacerdote", o comando executado em segundo plano é similar a:

C:/.../openkore/start.exe --config=control/config_MeuSacerdote.txt

Isso garante que cada bot seja iniciado com suas próprias configurações, sem a necessidade de editar arquivos manualmente.

3. Gerenciando Macros
A aba Macro Manager foi projetada para resolver o problema de ter um único arquivo macros.txt gigante e difícil de manter.

Importando Macros (Opcional):

Se você já tem um macros.txt com vários macros, clique em "Importar de macros.txt".

O launcher irá ler o arquivo e criar um .txt separado para cada macro encontrado dentro da pasta KoreNexus_Macros, que será criada na sua "Pasta de Macros".

Editando Macros:

Clique em qualquer macro na lista à esquerda para abri-lo no editor à direita.

Faça suas alterações e clique em "Salvar Alterações".

Compilando o macros.txt:

Quando terminar de editar, clique no botão "Compilar".

O launcher irá pegar o conteúdo de todos os macros ativos (com o switch ligado) e os juntará em um único arquivo macros.txt, substituindo o antigo (um backup é criado).

Agora, o seu OpenKore usará este novo arquivo compilado, contendo apenas os macros que você deixou ativos.

🛠️ Tecnologias Utilizadas
Python: Linguagem de programação principal.

CustomTkinter: Biblioteca para a criação da interface gráfica moderna.

Pillow (PIL Fork): Para manipulação de imagens e GIFs.

Requests: Para buscar as imagens dos Pokémon da PokeAPI.

🤝 Como Contribuir
Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será muito bem-vinda.

Faça um Fork do projeto.

Crie uma Branch para sua feature (git checkout -b feature/AmazingFeature).

Faça o Commit de suas mudanças (git commit -m 'Add some AmazingFeature').

Faça o Push para a Branch (git push origin feature/AmazingFeature).

Abra um Pull Request.

📄 Licença
Distribuído sob a licença MIT. Veja o arquivo LICENSE para mais informações.
