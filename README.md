Siga os passos abaixo para executar o programa:

1 - O gerenciamento de ambiente virtual do projeto foi desenvolvido usando conda. Esta aplicação deve ser previamente instalada.

https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html

2 - O arquivo ambiente.yml contém uma relação contendo os pacotes necessários para a execução do projeto. Crie um ambiente conda usando o comando     

conda env create -f ambiente.yml

3 - Faca um arquivo na raiz do projeto de nome env.env que segue o modelo do arquivo incluido env-sample.env

OBS : Você deve inserir sua chave da api da openAI corretamente no novo arquivo. Caso não tenha uma chave, siga o passo a passo
abaixo

3.1 - Crie uma Conta na OpenAI

O primeiro passo é criar uma conta na OpenAI. Para isso, siga os passos abaixo:

Acesse o site da OpenAI .
Clique em “Sign Up” no canto superior direito da página.
Preencha os campos necessários com suas informações ou faça login utilizando sua conta do Google.

3.2 - Acesse a Área de API Keys

Depois de criar sua conta e fazer login, você precisa acessar a área onde as API Keys são geradas:

No painel principal da OpenAI, clique em “API” no menu lateral esquerdo.
Em seguida, clique em “API Keys”.

3.3 - Crie uma Nova API Key

Agora, vamos criar a sua API Key:

Clique no botão “Create new secret key”.
Dê um nome para a sua chave, algo que ajude você a identificá-la no futuro, como “API do curso”.
Clique em “Create secret key”.

3.4 - Copie e Guarde sua API Key

Após criar a chave, a OpenAI exibirá o valor da sua API Key. É crucial que você copie e guarde esse valor em um lugar seguro, pois ele só será exibido uma vez. Se você perder essa chave, será necessário criar uma nova.


4 - Agora e necessário ativar o ambiente conda. Rode o comando abaixo:

conda activate gerador_evidence_briefings

5 - Para executar o programa, rode o comando abaixo:

streamlit run main.py