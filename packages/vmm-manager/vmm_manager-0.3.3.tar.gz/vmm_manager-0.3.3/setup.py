# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vmm_manager',
 'vmm_manager.entidade',
 'vmm_manager.infra',
 'vmm_manager.parser',
 'vmm_manager.scvmm',
 'vmm_manager.util']

package_data = \
{'': ['*'], 'vmm_manager': ['includes/*', 'includes/ps_templates/*']}

install_requires = \
['configargparse>=1,<2',
 'jinja2>=3,<4',
 'paramiko>=2,<3',
 'pytz>=2022.4',
 'ruamel.yaml>=0.17,<0.18',
 'tqdm>=4,<5',
 'yamale>=4,<5',
 'yamlable>=1,<2']

entry_points = \
{'console_scripts': ['vmm_manager = vmm_manager.vmm_manager:main']}

setup_kwargs = {
    'name': 'vmm-manager',
    'version': '0.3.3',
    'description': 'Management of resources on System Center Virtual Machine Manager (SCVMM) in a declarative way.',
    'long_description': '# vmm-manager\n\nScript python que gerencia recursos no System Center Virtual Machine Manager (SCVMM), de forma declarativa, com base em um arquivo de configuração YAML.\n\n[![License](https://img.shields.io/github/license/MP-ES/vmm_manager.svg)](LICENSE)\n[![Integration](https://github.com/MP-ES/vmm_manager/workflows/Integration/badge.svg)](https://github.com/MP-ES/vmm_manager/actions?query=workflow%3AIntegration)\n[![Release](https://github.com/MP-ES/vmm_manager/workflows/Release/badge.svg)](https://github.com/MP-ES/vmm_manager/actions?query=workflow%3ARelease)\n[![Python](https://img.shields.io/pypi/pyversions/vmm-manager.svg)](https://pypi.python.org/pypi/vmm-manager)\n[![PyPI](http://img.shields.io/pypi/v/vmm-manager.svg)](https://pypi.python.org/pypi/vmm-manager)\n\n## Pré-requisitos\n\nÉ necessário ter uma máquina Windows, que servirá como ponto de acesso ao SCVMM, com as seguintes ferramentas:\n\n- OpenSSH\n- Módulo PowerShell do SCVMM (**virtualmachinemanager**), instalado junto com o Console do Virtual Machine Manager (VMM). Você também pode obtê-lo em <https://github.com/MP-ES/VirtualMachineManager-PowerShellModule>\n\n## Instalação\n\n```shell\npip install -U vmm-manager\n```\n\n## Uso\n\nPara consultar as funções e os parâmetros disponíveis, utilize o comando:\n\n```shell\nvmm_manager -h\n```\n\n### Exemplo de arquivo de inventário\n\n[inventario_exemplo.yaml](inventario_exemplo.yaml)\n\n## Desenvolvimento\n\n### Instalação e configuração do python-poetry\n\nExecute os comandos a seguir:\n\n```shell\n# instalar o poetry\ncurl -sSL https://install.python-poetry.org | python3 -\n\n# Configurar autocomplete\n# Bash\npoetry completions bash >> ~/.bash_completion\n```\n\n### Variáveis de ambiente\n\nDefina as variáveis de ambiente de acordo com as instruções do arquivo **.env.default**. Você pode criar um arquivo **.env** e executar o comando `export $(cat .env | xargs)` para defini-las antes da execução do script.\n\n### Como executar\n\n```shell\n# Carregando envs (opcional)\nexport $(cat .env | xargs)\n\n# Instalando dependências\npoetry install --no-root\n\n# Executando script\npoetry run python -m vmm_manager -h\n```\n\n### Comandos úteis para DEV\n\n```shell\n# Habilitar shell\npoetry shell\n\n# Incluir uma dependência\npoetry add <pacote> [--dev]\n\n# Executar lint\npylint --load-plugins pylint_quotes tests/* vmm_manager/*\n\n# Executar testes\npython -m pytest -vv\n\n# listar virtualenvs\npoetry env list\n\n# Remover um virtualenv\npoetry env remove <nome>\n```\n\n## Referências\n\n- [Virtual Machine Manager](https://docs.microsoft.com/en-us/powershell/module/virtualmachinemanager/?view=systemcenter-ps-2019)\n- [Poetry](https://python-poetry.org/)\n',
    'author': 'Estevão Costa',
    'author_email': 'ecosta@mpes.mp.br',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MP-ES/vmm_manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
