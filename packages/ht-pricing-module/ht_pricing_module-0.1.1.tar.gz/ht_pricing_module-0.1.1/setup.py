from setuptools import setup, find_packages


setup(name="ht_pricing_module",
      version="0.1.1",
      author="wangjun",
      readme="README.md",
      description="huatai option pricing module",
      author_email="wangjun@htgwfzb.com",
      url='http://10.17.75.129:9002/wangjun/ht_pricing_server/-/tree/main/ht_pricing_module',
      requires_python=">=3.6",

      packages=['ht_pricing_module', 'ht_pricing_module.one_asset_pricing_module',
                'ht_pricing_module.monte_carlo_engine', 'ht_pricing_module.api_and_utils',
                'ht_pricing_module.muti_asset_pricing_module', 'ht_pricing_module.finite_difference_engine'],
      include_package_data=True,
      platforms="any",
      install_requires=['numpy', 'scipy', 'pandas']
      )

# py -m build
# python .\setup.py bdist_egg
# py -m twine upload .\dist\*
# py -m twine upload --repository testpypi dist/*
# pip install ht-pricing-module==0.1 -i https://pypi.python.org/simple
# pip install ht-pricing-module==0.1 -i https://test.pypi.org/simple/