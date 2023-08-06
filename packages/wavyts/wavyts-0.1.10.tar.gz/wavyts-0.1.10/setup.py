# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wavy']

package_data = \
{'': ['*']}

install_requires = \
['ipykernel>=6.15.1,<7.0.0',
 'nbformat>=5.4.0,<6.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas==1.4.3',
 'plotlab>=0.1.0,<0.2.0',
 'plotly>=5.7.0,<6.0.0',
 'sklearn>=0.0,<0.1',
 'tensorflow>=2.8.0,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'wavyts',
    'version': '0.1.10',
    'description': 'Wavy is a library to facilitate time series analysis',
    'long_description': '<!-- Title -->\n## ≈ Wavy: Time-Series Manipulation ≈\n\n<p>\n<img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/logspace-ai/wavy" />\n<img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/logspace-ai/wavy" />\n<!-- <img alt="GitHub Language Count" src="https://img.shields.io/github/languages/count/logspace-ai/wavy" /> -->\n<img alt="" src="https://img.shields.io/github/repo-size/logspace-ai/wavy" />\n<!-- <img alt="GitHub Issues" src="https://img.shields.io/github/issues/logspace-ai/wavy" /> -->\n<!-- <img alt="GitHub Closed Issues" src="https://img.shields.io/github/issues-closed/logspace-ai/wavy" /> -->\n<!-- <img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr/logspace-ai/wavy" /> -->\n<!-- <img alt="GitHub Closed Pull Requests" src="https://img.shields.io/github/issues-pr-closed/logspace-ai/wavy" />  -->\n<!-- <img alt="GitHub Commit Activity (Year)" src="https://img.shields.io/github/commit-activity/y/logspace-ai/wavy" /> -->\n<img alt="Github License" src="https://img.shields.io/github/license/logspace-ai/wavy" />  \n</p>\n\n\nWavy is a time-series manipulation library designed to simplify the pre-processing steps and reliably avoid the problem of data leakage. Its main structure is built on top of Pandas. <a href="https://logspace-ai.github.io/wavy/"><strong>Explore the docs 📖</strong></a>\n    <a href="https://github.com/logspace-ai/wavy">\n        <img width="50%" src="https://github.com/logspace-ai/wavy/blob/main/images/logo.png?raw=true" alt="Logo" width="419" height="235" align="right"></a>\n\n  \n\n<!-- PROJECT LOGO -->\n<!-- <div align="right">\n  <a href="https://github.com/logspace-ai/wavy">\n    <img width="49%" src="https://github.com/logspace-ai/wavy/blob/main/images/logo.png?raw=true" alt="Logo" width="419" height="235">\n  </a>\n\n</div> -->\n\n<!-- GETTING STARTED -->\n## 📦 Installation\n\nYou can install Wavy from pip:\n\n```bash\npip install wavyts\n```\n\n<!-- GETTING STARTED -->\n## 🚀 Quickstart\n\n```python\nimport numpy as np\nimport pandas as pd\nimport wavy\nfrom wavy import models\n\n# Start with any time-series dataframe:\ndf = pd.DataFrame({\'price\': np.random.randn(1000)}, index=range(1000))\n\n# Create panels. Each panel is a frame collection.\nx, y = wavy.create_panels(df, lookback=3, horizon=1)\n\n# x and y contain the past and corresponding future data.\n# lookback and horizon are the number of timesteps.\nprint("Lookback:", x.num_timesteps)\nprint("Horizon:", y.num_timesteps)\n\n# Set train-val-test split. Defaults to 0.7, 0.2 and 0.1, respectively.\nwavy.set_training_split(x, y)\n\n# Instantiate a model:\nmodel = models.LinearRegression(x, y)\nmodel.score()\n```\n    \n\n<!-- Description -->\n## Features\n\n💡 Wavy **is**:\n\n- A **resourceful**, **high-level** package with tools for time-series processing, visualization, and modeling.\n- A facilitator for **time-series windowing** that helps reduce boilerplate code and avoid shape confusion.\n\n❗ Wavy **is not**:\n\n- An efficient, performance-first framework (**yet!**).\n- Primarily focused on models. Processed data can be easily converted to numpy arrays for further exploration.\n\n\n<!-- CONTRIBUTING -->\n## Contributing\n\nContributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make to `wavy` are **greatly appreciated**.\n\nIf you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".\nDon\'t forget to give the project a star! ⭐\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\n\n<!-- LICENSE -->\n## License\n\nDistributed under the MIT License. See `LICENSE.txt` for more information.\n\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n[contributors-shield]: https://img.shields.io/github/contributors/logspace-ai/wavy.svg?style=for-the-badge\n[contributors-url]: https://github.com/logspace-ai/wavy/graphs/contributors\n[forks-shield]: https://img.shields.io/github/forks/logspace-ai/wavy.svg?style=for-the-badge\n[forks-url]: https://github.com/logspace-ai/wavy/network/members\n[stars-shield]: https://img.shields.io/github/stars/logspace-ai/wavy.svg?style=for-the-badge\n[stars-url]: https://github.com/logspace-ai/wavy/stargazers\n[issues-shield]: https://img.shields.io/github/issues/logspace-ai/wavy.svg?style=for-the-badge\n[issues-url]: https://github.com/logspace-ai/wavy/issues\n[license-shield]: https://img.shields.io/github/license/logspace-ai/wavy.svg?style=for-the-badge\n[license-url]: https://github.com/logspace-ai/wavy/blob/main/LICENSE.txt\n<!-- [documentation-url]: https://logspace-ai.github.io/wavy/ -->\n',
    'author': 'Ibis Prevedello',
    'author_email': 'ibiscp@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/logspace-ai/wavy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
