# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib']

package_data = \
{'': ['*']}

install_requires = \
['xonsh>=0.13.4']

setup_kwargs = {
    'name': 'xontrib-rtx',
    'version': '0.0.1',
    'description': 'Initializes rtx (polyglot asdf-like runtime manager)',
    'long_description': '<p align="center">\nInitialize <a href="https://github.com/jdxcode/rtx" target="_blank">rtx</a> (polyglot asdf-like runtime manager in Rust)</br>\nin a more performant and flexible way\n</p>\n\n<p align="center">  \nIf you like the idea click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Nice%20xontrib%20for%20the%20xonsh%20shell!&url=https://github.com/eugenesvk/xontrib-rtx" target="_blank">tweet</a>.\n</p>\n\nThis xontrib adds a couple of (maybe too tiny to notice) improvements:\n\n  - (no cost) replaces the subprocess syntax for the hook rtx function with a pure python syntax, which for some reason improves hook runtime by __~60%__ (but in absolute terms maybe just a dozen or two `ms`)\n  - (less convenient) replaces a hook on every prompt paint with hooks on\n    - shell launch\n    - changing dirs\n    - empty commands</br>\n      useful to refresh shell status when you edit `.tool-versions` _outside_ of shell (optional)\n    - commands that containt custom text chunks</br>\n      useful to refresh shell status when you edit `.tool-versions`  _in_ a shell (optional)\n\n## Installation\n\nTo install use pip:\n\n```bash\nxpip install xontrib-rtx\n# or: xpip install -U git+https://github.com/eugenesvk/xontrib-rtx\n```\n\n## Usage\n\nThis xontrib requires `rtx` to be in `PATH` or `~/bin`; or if it\'s added to `PATH` via another xontrib (e.g, you installed it via Homebrew and use `xontrib-homebrew`), then you should load this xontrib after the one setting `PATH`\n\n1. Add the following to your `.py` xontrib loading config and `import` it in your xonsh run control file (`~/.xonshrc` or `~/.config/rc.xsh`):\n```py\nfrom xonsh.xontribs \timport xontribs_load\nfrom xonsh.built_ins\timport XSH\nenvx = XSH.env\n\nxontribs = [ "rtx", # Initializes rtx (polyglot asdf-like runtime manager)\n # your other xontribs\n]\n# ↓ optional configuration variables\nif \'rtx\' in xontribs: # Configure rtx only if you\'re actually loading\n  # config var                       \t  value             \t  |default|alt_cmd¦ comment\n  envx[\'XONTRIB_RTX_CHUNK_LIST\']     \t= [\'.tool-versions\']\t# |[\'.tool-versions\']|False¦ (feeble attempts to track edits to `.tool-versions` in the command line) update rtx status if command contains any of the string chunks in this list; False to disable this listener completely\n  envx[\'XONTRIB_RTX_NEWLINE_REFRESH\']\t= True              \t# |True|False¦ update rtx status if command is empty (e.g, ⏎ on a blank line to refresh after editing `.tool-versions` in a text editor); False to disable this listener completely\n  envx[\'XONTRIB_RTX_FORCE_COLOR\']    \t= True              \t# |True|False¦ preserve colored rtx output\n  envx[\'XONTRIB_RTX_LOGLEVEL\']       \t= 1                 \t# |1|0¦ print xontrib log messages: 0 none, 1 error; \'rtx\' stderr is always passed through\n\nxontribs_load(xontribs_manual) # actually load all xontribs in the list\n```\n\n2. Or just add this to your xonsh run control file\n```xsh\nxontrib load rtx # Initializes rtx (polyglot asdf-like runtime manager)\n# configure like in the example above, but replace envx[\'VAR\'] with $VAR\n$XONTRIB_RTX_LOGLEVEL = 1\n```\n\n## Known issues\n\n- In the future xontrib-rtx will be autoloaded, but this is currently blocked due to a [xonsh bug](https://github.com/xonsh/xonsh/issues/5020): too early autoload prevens reading user config; also, autoloading can\'t be disabled\n\n## Credits\n\nThis package was created with [xontrib template](https://github.com/xonsh/xontrib-template)\n',
    'author': 'Evgeny',
    'author_email': 'es.bugzilla@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eugenesvk/xontrib-rtx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
