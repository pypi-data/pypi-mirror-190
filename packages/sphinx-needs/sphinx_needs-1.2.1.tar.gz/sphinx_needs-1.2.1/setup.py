# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_needs',
 'sphinx_needs.api',
 'sphinx_needs.directives',
 'sphinx_needs.functions',
 'sphinx_needs.lsp',
 'sphinx_needs.nodes',
 'sphinx_needs.roles',
 'sphinx_needs.services',
 'sphinx_needs.services.config']

package_data = \
{'': ['*'],
 'sphinx_needs': ['css/*',
                  'css/blank/*',
                  'css/dark/*',
                  'css/modern/*',
                  'images/*',
                  'images/feather_png/*',
                  'images/feather_svg/*',
                  'libs/html/*',
                  'libs/html/Buttons-1.5.1/css/*',
                  'libs/html/Buttons-1.5.1/js/*',
                  'libs/html/Buttons-1.5.1/swf/*',
                  'libs/html/ColReorder-1.4.1/css/*',
                  'libs/html/ColReorder-1.4.1/js/*',
                  'libs/html/DataTables-1.10.16/css/*',
                  'libs/html/DataTables-1.10.16/images/*',
                  'libs/html/DataTables-1.10.16/js/*',
                  'libs/html/FixedColumns-3.2.4/css/*',
                  'libs/html/FixedColumns-3.2.4/js/*',
                  'libs/html/FixedHeader-3.1.3/css/*',
                  'libs/html/FixedHeader-3.1.3/js/*',
                  'libs/html/JSZip-2.5.0/*',
                  'libs/html/Responsive-2.2.1/css/*',
                  'libs/html/Responsive-2.2.1/js/*',
                  'libs/html/Scroller-1.4.4/css/*',
                  'libs/html/Scroller-1.4.4/js/*',
                  'libs/html/pdfmake-0.1.32/*',
                  'templates/*']}

install_requires = \
['docutils>=0.15',
 'esbonio>=0.11.3',
 'jsonschema>3.2.0',
 'matplotlib>=3.3.0',
 'pygls',
 'requests-file>=1.5.1,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'sphinx-data-viewer>=0.1.1,<0.2.0']

extras_require = \
{':extra == "docs"': ['sphinx>=5.0']}

setup_kwargs = {
    'name': 'sphinx-needs',
    'version': '1.2.1',
    'description': 'Sphinx needs extension for managing needs/requirements and specifications',
    'long_description': '**Complete documentation**: http://sphinx-needs.readthedocs.io/en/latest/\n\n**Attention**: ``sphinxcontrib-needs`` got renamed to ``sphinx-needs``. This affects also the URLs for documentation and repository:\n\n* Docs: https://sphinx-needs.readthedocs.io/en/latest/\n* Repo: https://github.com/useblocks/sphinx-needs\n\n\nIntroduction\n============\n\n``Sphinx-Needs`` allows the definition, linking and filtering of class-like need-objects, which are by default:\n\n* requirements\n* specifications\n* implementations\n* test cases.\n\nThis list can be easily customized via configuration (for instance to support bugs or user stories).\n\nA default requirement need looks like:\n\n.. image:: https://raw.githubusercontent.com/useblocks/sphinxcontrib-needs/master/docs/_images/need_1.png\n   :align: center\n\nLayout and style of needs can be highly customized, so that a need can also look like:\n\n.. image:: https://raw.githubusercontent.com/useblocks/sphinxcontrib-needs/master/docs/_images/need_2.png\n   :align: center\n\nTake a look into our `Examples <https://sphinxcontrib-needs.readthedocs.io/en/latest/examples/index.html>`_ for more\npictures and ideas how to use ``Sphinx-Needs``.\n\nFor filtering and analyzing needs, ``Sphinx-Needs`` provides different, powerful possibilities:\n\n.. list-table::\n   :header-rows: 1\n   :widths: 46,14,40\n\n   - * `needtable <https://sphinxcontrib-needs.readthedocs.io/en/latest/directives/needtable.html>`_\n     * `needflow <https://sphinxcontrib-needs.readthedocs.io/en/latest/directives/needflow.html>`_\n     * `needpie <https://sphinxcontrib-needs.readthedocs.io/en/latest/directives/needpie.html>`_\n   - * .. image:: https://raw.githubusercontent.com/useblocks/sphinxcontrib-needs/master/docs/_images/needtable_1.png\n     * .. image:: https://raw.githubusercontent.com/useblocks/sphinxcontrib-needs/master/docs/_images/needflow_1.png\n     * .. image:: https://raw.githubusercontent.com/useblocks/sphinxcontrib-needs/master/docs/_images/needpie_1.png\n\nInstallation\n============\n\nUsing poetry\n------------\n\n.. code-block:: bash\n\n    poetry add sphinx-needs\n\nUsing pip\n---------\n\n.. code-block:: bash\n\n    pip install sphinx-needs\n\n.. note::\n\n   Prior version **1.0.1** the package was named ``sphinxcontrib-needs``.\n\nUsing sources\n-------------\n\n.. code-block:: bash\n\n    git clone https://github.com/useblocks/sphinx-needs\n    cd sphinx-needs\n    pip install .\n    # or\n    poetry install\n\n\nActivation\n----------\n\nFor final activation, please add `sphinx_needs` to the project\'s extension list of your **conf.py** file.\n\n.. code-block:: python\n\n   extensions = ["sphinx_needs",]\n\n.. note::\n\n   Prior version **1.0.1** the extensions was called ``sphinxcontrib.needs``.\n\n',
    'author': 'team useblocks',
    'author_email': 'info@useblocks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://github.com/useblocks/sphinx-needs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0',
}


setup(**setup_kwargs)
