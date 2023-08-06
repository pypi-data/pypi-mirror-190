import setuptools
    
setuptools.setup(
  name = 'Aquar',         # How you named your package folder (MyLib)
  version = '1.0.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'a simple package for CTA backtest',   # Give a short description about your library
  # long_description=l_description,
  author = 'Andy Lee',                   # Type in your name
  author_email = '1245824150@qq.com',      # Type in your E-Mail
  keywords = ['CTA', 'GTJA', 'BACKTEST'],   # Keywords that define your package best
  install_requires=[         
    'clickhouse_driver>=0.2.0',
    'colorlog>=4.6.2',
    'matplotlib>=3.3.4',
    'numpy>=1.21.0',
    'pandas>=1.2.2',
    'prettytable>=2.0.0',
    'PyMySQL>=0.10.1',
    'python_dateutil>=2.8.2',
    'seaborn>=0.11.1',
    ],  
  packages=setuptools.find_packages(),# 自动找到项目中导入的模块
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',
  ],
)
