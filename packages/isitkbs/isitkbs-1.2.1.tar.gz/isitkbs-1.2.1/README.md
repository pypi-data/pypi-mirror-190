# ![Detecting Keyboard Smashing](https://raw.githubusercontent.com/fga-eps-mds/2022-2-Squad03/main/docs/images/title.png)

<div align="center">
    <img src="https://raw.githubusercontent.com/fga-eps-mds/2022-2-Squad03/main/docs/images/logo.png" width="250"></img>
</div>

<br>

<div align="center">
    <img src="https://img.shields.io/github/issues-raw/fga-eps-mds/2022-2-IsItKbs?color=00a8f0&style=for-the-badge"></img>
    <img src="https://img.shields.io/github/issues-pr-raw/fga-eps-mds/2022-2-IsItKbs?color=00a8f0&label=open%20PRs&style=for-the-badge"></img>
    <img src="https://img.shields.io/pypi/v/isitkbs?color=00a8f0&style=for-the-badge"></img>
    <img src="https://img.shields.io/github/license/fga-eps-mds/2022-2-IsItKbs?color=00a8f0&style=for-the-badge"></img>
</div>

<h4 align="center">
    <img src="https://img.shields.io/coverallsCoverage/github/fga-eps-mds/2022-2-IsItKbs?color=%2300FF00&&style=for-the-badge"></img>
    <img src="https://img.shields.io/codeclimate/maintainability-percentage/fga-eps-mds/2022-2-IsItKbs?color=00FF00&style=for-the-badge"></img>
    <img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=%2300FF00&&&style=for-the-badge"/>
</h4>


[Read this in english.](https://github.com/fga-eps-mds/2022-2-IsItKbs/blob/main/README.EN.md)

## 📑 Sumário

- [](#)
  - [📑 Sumário](#-sumário)
  - [🔎 Visão Geral](#-visão-geral)
  - [🛠 Tecnologias utilizadas](#-tecnologias-utilizadas)
  - [📝 Guia de instalação](#-guia-de-instalação)
  - [⚙ Funcionalidades](#-funcionalidades)
    - [is\_kbs(input\_data, analyzer, model)](#is_kbsinput_data-analyzer-model)
  - [📋 Exemplos](#-exemplos)
  - [📚 Documentação](#-documentação)
  - [📁 Diretórios](#-diretórios)
  - [👨‍💻 Contribuidores](#-contribuidores)
  - [©Licença](#licença)

<br>

## 🔎 Visão Geral

<li>Qual o objetivo desse software?</li>
O Is it KBS é um pacote python com funções capazes de determinar se entradas de texto são consideradas ou não keyboard smashing, sendo assim, cientistas de dados podem usar a biblioteca para auxiliá-los no processo de limpeza de bases de dados.

<br>

<li>O que é keyboard smashing?</li>
Keyboard smashing é a entrada ilógica e desordenada de dados, que acaba por comprometer a análise textual por sistemas de software.
Ex.:
<li>yyyyyy - É keyboard smashing.</li>
<li>aslkhfg - É keyboard smashing.</li>
<li>hello - Não é keyboard smashing.</li>

<br>

## 🛠 Tecnologias utilizadas

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NLTK](https://img.shields.io/badge/-NLTK-lightgrey?style=for-the-badge)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

<br>

## 📝 Guia de instalação

<li>Necessário python 3 e pip.</li>
<li>Faça a instalação do nosso pacote com o pip no seu terminal python (as demais bibliotecas necessárias são instaladas  automáticamente com o comando abaixo):</li>

```
pip install isitkbs
```

<br>

## ⚙ Funcionalidades

### is_kbs(model)

```python
from isitkbs import *
kbs = is_kbs()
```
- model: modelo utilizado ('randomForest' por padrão, há também naivebayes)

<br>

Para novas versões, a ideia é desenvolver features que auxiliam no tratamento de keyboard smashing em textos, banco de dados, entre outros.

<br>

## 📋 Exemplos

```python
kbs.wordkbs('yyyyyy')
1
```

```python
kbs.wordkbs('Hello')
0
```

```python
kbs.sentkbs('Hello world')
[]
```

```python
kbs.sentkbs('aspdo asocjn')
['aspdo', 'asocjn']
```
<br>

## 📚 Documentação

* [Código de conduta](https://fga-eps-mds.github.io/2022-2-IsItKbs/projeto/conduct_code.html)<br>
* [Metodologia de Comunicação](https://fga-eps-mds.github.io/2022-2-IsItKbs/projeto/metodologia_comunicacao.html)<br>
* [Mapa de histórias de usuário](https://fga-eps-mds.github.io/2022-2-IsItKbs/projeto/usermap_story.html)<br>
* [WorkFlow](https://fga-eps-mds.github.io/2022-2-IsItKbs/projeto/workflow.html)<br>
* [RoadMap](https://fga-eps-mds.github.io/2022-2-IsItKbs/projeto/roadmap.html)

<br>

## 📁 Diretórios

<p>/.github <- Templates para issues e pull requests.<p>
<p>/estudos <- Projetos e scripts pequenos para treino da equipe.<p>
<p>/data <- Bases de dados utilizadas no treinamento do algoritmo.<p>
<p>/dist <- Distribuições do nosso pacote comprimidas.<p> 
<p>/docs <- Documentações, principalmente da gitpage.<p> 
<p>/isitkbs.egg-info <- Informações de empacotamento.<p> 
<p>/isitkbs <- Definição das funções que serão utilizadas pelos usuários.<p> 
<p>/models <- Modelos já treinados.<p>
<p>/notebooks <- Jupyter notebooks usados para testes de funcionalidades.<p>
<p>/src <- Scripts para tratamento de dados, feature engineering e treinamento de algoritmos.<p>

<br>

## 👨‍💻 Contribuidores

<table>
  <tr>
    <td align="center"><a href="https://github.com/arthurmlv"><img style="border-radius: 50%;" src="https://raw.githubusercontent.com/fga-eps-mds/2022-2-Squad03/main/docs/images/arthur m.jpg" width="100px;" alt=""/><br /><sub><b>Arthur de Melo</b></sub></a><br />
    <td align="center"><a href="https://github.com/arthurgrandao"><img style="border-radius: 50%;" src="https://raw.githubusercontent.com/fga-eps-mds/2022-2-Squad03/main/docs/images/arthur grandao.jpg" width="100px;" alt=""/><br /><sub><b>Arthur Grandão</b></sub></a><br />
    <td align="center"><a href="https://github.com/dougAlvs"><img style="border-radius: 50%;" src="https://raw.githubusercontent.com/fga-eps-mds/2022-2-Squad03/main/docs/images/douglas.jpg" width="100px;" alt=""/><br /><sub><b>Douglas Alves</b></sub></a><br /><a href="Link git" title="Rocketseat"></a></td>
    <td align="center"><a href="https://github.com/g16c"><img style="border-radius: 50%;" src="https://raw.githubusercontent.com/fga-eps-mds/2022-2-Squad03/main/docs/images/gabriel.jpg" width="100px;" alt=""/><br /><sub><b>Gabriel Campello</b></sub></a><br /><a href="Link git" title="Rocketseat"></a></td>
    <td align="center"><a href="https://github.com/PauloVictorFS"><img style="border-radius: 50%;" src="https://raw.githubusercontent.com/fga-eps-mds/2022-2-Squad03/main/docs/images/paulo victor.jpg" width="100px;" alt=""/><br /><sub><b>Paulo Victor</b></sub></a><br />
    <td align="center"><a href="https://github.com/RafaelCLG0"><img style="border-radius: 50%;" src="https://raw.githubusercontent.com/fga-eps-mds/2022-2-Squad03/main/docs/images/rafael.jpg" width="100px;" alt=""/><br /><sub><b>Rafael Ferreira</b></sub></a><br />
    <td align="center"><a href="https://github.com/nando3d3"><img style="border-radius: 50%;" src="https://raw.githubusercontent.com/fga-eps-mds/2022-2-Squad03/main/docs/images/sidney.jpg" width="100px;" alt=""/><br /><sub><b>Sidney Fernando</b></sub></a><br /> 
  </tr>
</table>

<br>

## ©Licença

This software is licensed under the [MIT](https://github.com/nhn/tui.editor/blob/master/LICENSE) ©
