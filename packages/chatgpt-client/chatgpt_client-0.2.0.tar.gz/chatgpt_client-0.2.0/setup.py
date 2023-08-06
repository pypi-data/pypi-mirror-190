# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['chatgpt_client']
install_requires = \
['aiohttp>=3.8.3,<4.0.0']

setup_kwargs = {
    'name': 'chatgpt-client',
    'version': '0.2.0',
    'description': 'Python client for the unofficial ChatGPT API.',
    'long_description': '# ChatGPT Client\n\n[![Latest Release](https://img.shields.io/github/v/release/vsakkas/chatgpt-client.svg)](https://github.com/vsakkas/chatgpt-client/releases/tag/0.1.0)\n[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)\n[![MIT License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/vsakkas/chatgpt-client/blob/master/LICENSE)\n[![CI](https://github.com/vsakkas/chatgpt-client/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/vsakkas/chatgpt-client/actions/workflows/main.yml)\n\nPython client for the unofficial [ChatGPT](https://openai.com/blog/chatgpt/) API by [OpenAI](https://openai.com/).\n\n## Installation\n\nTo install the ChatGPT Client, run the following command:\n\n```bash\npip install chatgpt-client\n```\n\n## Usage\n\nSign up for an [OpenAI API key](https://platform.openai.com/overview) and store it in your environment.\n\n```python\nimport asyncio\nimport os\n\nfrom chatgpt_client import ChatGPTClient\n\nasync def main() -> None:\n    api_key = os.getenv("OPENAI_API_KEY")\n    client = ChatGPTClient(api_key)\n\n    response = await client.get_completion("What is the meaning of life?")\n    print(response["choices"][0]["text"])\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](https://github.com/vsakkas/chatgpt-client/blob/master/LICENSE) file for details.\n',
    'author': 'vsakkas',
    'author_email': 'vasileios.sakkas96@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
