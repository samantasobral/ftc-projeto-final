# Projeto final do curso FTC - Analisando dados com Python

# 1. O problema de negócio
A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.

O CEO foi recém contratado e precisa entender melhor o negócio
para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a
Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da
empresa e que sejam gerados dashboards.

# 2. As premissas do negócio
 - O modelo de negócio é um marketplace;
 - As visões dos negócio foram: geral, países, cidades e culinárias
 
# 3. As estratégias da solução
O painel foi desenvolvido utilizando as métricas que refletem as 4 visões do modelo de 
negócio da empresa:
 - Visão geral
 - Visão países
 - Visão cidades
 - Visão culinárias

Cada visão é representada pelo seguinte conjunto de métricas:
 - Visão geral: quantidade de restaurantes, países, cidades e culinárias cadastradas; 
 quantidade de avaliações feitas; mapa com a localização dos restaurantes.
 - Visão países: quantidade de restaurantes registrados por país; 
 quantidade de cidades registradas por país; média de avaliações feitas por país;
 média de preço de um prato para duas pessoas por país.
 - Visão cidades: top 10 cidades com mais restaurantes cadastrados; 
 top 7 cidades com restaurantes com média de avaliação acima de 4;
 top 7 cidades com restaurantes com média de avaliação abaixo de 2.5;
 top 10 ciades com mais restaurantes com tipos culinários distintos.
 - Visão culinárias: top restaurantes; melhores tipos culinários; piores tipos culinários.

# 4. Top 3 insights de dados
- A Índia possui a maior quantidade de cidades e restaurantes cadastrados;
- A Inglaterra possui a maior quantidade de restaurantes com melhores avaliações e cidades
com tipos culinários distintos;
- Os melhores tipos culinários são o americano e o italiano, enquanto os piores são
o brasileiro e o árabe.

# 5. O produto final do projeto
Painel online, hospedado em um cloud e disponível para acesso em qualquer dispositovo conectado à internet.

O painel pode ser acessado através do link: https://samantasobral-ftc-projeto.streamlit.app/

# 6. Conclusão
O objetivo deste projeto é criar um conjunto de gráficos e tabelas que exibam as métricas da melhor forma possível
para o CEO.

# 7. Próximos passos
Melhorar o mapa; criar novos filtros; adicionar novas visões de negócio.
