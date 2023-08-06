# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dcurves']

package_data = \
{'': ['*'], 'dcurves': ['data/*']}

install_requires = \
['lifelines>=0.27.4,<0.28.0',
 'matplotlib>=3.5.2,<4.0.0',
 'pandas>=1.5.3,<1.6.0',
 'statsmodels>=0.13.2,<0.14.0',
 'typing>=3.7.4.3,<3.8.0.0']

setup_kwargs = {
    'name': 'dcurves',
    'version': '1.0.5',
    'description': 'A Python package for Decision Curve Analysis to evaluate prediction models, molecular markers, and diagnostic tests. For RELEASE NOTES, check RELEASE.md here: https://github.com/MSKCC-Epi-Bio/dcurves/RELEASE.md',
    'long_description': "# dcurves\nDiagnostic and prognostic models are typically evaluated with measures of accuracy that do not address clinical\nconsequences. Decision-analytic techniques allow assessment of clinical outcomes, but often require collection of\nadditional information that may be cumbersome to apply to models that yield continuous results. Decision Curve\nAnalysis is a method for evaluating and comparing prediction models that incorporates clinical consequences,\nrequiring only the data set on which the models are tested, and can be applied to models that have either continuous or\ndichotomous results. The dca function performs decision curve analysis for binary and survival outcomes. Review the\nDCA tutorial (towards the bottom) for a detailed walk-through of various applications. Also, see\nwww.decisioncurveanalysis.org for more information.\n\n#### Installation\n\n###### Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dcurves\n\n###### While this is the quick-and-dirty method to install a package such as `dcurves` into your local environment, you should use a virtual environment and make sure your dependencies are compatible while using `dcurves`\n\n```bash\npip install dcurves\n```\n###### Import dcurves and numpy\n```python\nfrom dcurves import dca, plot_graphs, load_test_data\nimport numpy as np\n```\n##### Usage - Binary Outcomes\n```python\nfrom dcurves import dca, plot_graphs, load_test_data\nimport numpy as np\n\ndca_results = \\\n    dca(\n        data=load_test_data.load_binary_df(),\n        outcome='cancer',\n        modelnames=['famhistory'],\n        thresholds=np.arange(0,0.46,0.01)\n    )\n\nplot_graphs(\n    plot_df=dca_results,\n    graph_type='net_benefit',\n    y_limits=[-0.05, 0.15],\n    color_names=['blue', 'red', 'green']\n)\n```\n##### Usage - Survival Outcomes\n```python\nfrom dcurves import dca, plot_graphs, load_test_data\nimport numpy as np\n\ndca_results = \\\n    dca(\n        data=load_test_data.load_survival_df(),\n        outcome='cancer',\n        modelnames=['famhistory', 'marker', 'cancerpredmarker'],\n        models_to_prob=['marker'],\n        thresholds=np.arange(0,0.46,0.01),\n        time_to_outcome_col='ttcancer',\n        time=1\n    )\n\nplot_graphs(\n    plot_df=dca_results,\n    graph_type='net_benefit',\n    y_limits=[-0.025, 0.175],\n    color_names=['blue', 'red', 'green', 'purple', 'black']\n)\n```\n#### In-depth tutorial and explanations:\n###### https://www.danieldsjoberg.com/dca-tutorial/dca-tutorial-python.html\n\n#### Contributing\n\n###### Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change\n\n###### Please make sure to update tests as appropriate\n\n#### License\n[Apache 2.0]([https://choosealicense.com/licenses/apache-2.0/])\n\n##### Note\n###### setup.py is deprecated now that dependencies are managed by `poetry` package manager\n",
    'author': 'shaunporwal',
    'author_email': 'shaun.porwal@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11.1,<3.12.0',
}


setup(**setup_kwargs)
