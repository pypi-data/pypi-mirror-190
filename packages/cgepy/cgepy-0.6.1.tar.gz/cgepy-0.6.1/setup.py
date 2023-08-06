# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cgepy', 'cgepy.unstable']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cgepy',
    'version': '0.6.1',
    'description': 'Tools for developing graphical programs inside the console.',
    'long_description': '\n# Licence\nFirstly, I prefer some credit for all programs made with cgePy, though this is your choice.\nClaiming that this library\'s code is yours is explicitly NOT ALLOWED. If you would like to develop cgePy, please contact me at **lion712yt@gmail.com**.\n***\n# Basic Usage\nFirst off, try this code:\n```py\ngrid = cgepy.Grid()\ngrid.Update()\n```\nIt will print (show the most recent version of) the grid!\\\nNow,\n```py\ngrid.write(1,cgepy.RED+"  ")\n#"  " is a blank pixel on the grid.\n#Each pixel must be EXACTLY two characters long!\ngrid.Update()\n```\nThe result will be the same as before, but the 2nd \'pixel\' on the grid red. Try experimenting with this for a little.\n\n## Maps\n\nNow, this process of writing to the grid is very repetitive, right? Well, there\'s a solution to that: Maps.\n\n```py\ngrid2 = cgepy.Map(\n    \'\'\'\nBB BB BB BB BB BB BB BB BB BB\nBB BG BG BG BG BG BG BG BG BB\nBB BG BG BG BG BG BG BG BG BB\nBB BG BG BG BG BG BG BG BG BB\nBB BG BG BG BG BG BG BG BG BB\nBB BG BG BG BG BG BG BG BG BB\nBB BG BG BG BG BG BG BG BG BB \nBB BG BG BG BG BG BG BG BG BB\nBB BG BG BG BG BG BG BG BG BB\nBB BB BB BB BB BB BB BB BB BB\n\'\'\')\ngrid2.Paint()\ngrid2.Update()\n```\n\nOkay, that\'s a little confusing right?\\\nYou might need to wait until I\'m finished making this README. (sorry!)\\\nFor now, try and figure out what each part of the code does.\n\n## Sprites\n\nOf course, you\'ll need a way to animate objects.\\\nTry this code:\n\n```py\nimport time\n\ngrid = cgepy.Grid()\ngrid.Update()\n\nsprite = cgepy.Sprite()\n\nsprite.Drop(grid)\ntime.sleep(1)\n\ngrid.Update()\n```\n\nDo you see the red pixel in the corner of the grid? There\'s your sprite!\n\nNow, try adding this to your code:\n\n```py\ntime.sleep(1)\nsprite.Move("down")\ngrid.Update()\n```\n\nI don\'t need to explain this.\nTo remove a sprite:\n```py\ngrid.sprites.remove(sprite)\n```\n***\n### Changing the sprite\'s color\n***\nWhen you create a sprite, you can provide the color as a parameter:\n ```py\n sprite = cgepy.Sprite(color=CYAN)\n ```\n***\n Or, you can try this after a sprite is made:\n ```py\nsprite.Color(CYAN)\n ```\n Alternately:\n\n ```py\n sprite.sprite = CYAN+"  "\n```\nYou can replace `"  "` with anything, as long as it is two characters long.\n\n\n# Customization\n\nNow that you\'ve learned the basics cgePy, you might get ask, "Can I change the color of the background" or "How do I make the grid bigger?"\n\nWell, look no further as your problem is solved!\n***\nFirst off, cgePy uses two variables for this:\n`gridsize`,  `background`.\n\n Please note that the gridsize should be a perfect square (9, 25, 100, etc) or else cgePy may not work.\\\n `background` should be set to a background color variable. In cgePy, `red` = text color, `RED` = background color, etc. You can also use ansi codes if you need.\n***\n\nSadly, I haven\'t finished with this README yet. However, I wish you good luck, and hope this helped!\n',
    'author': 'catbox305',
    'author_email': 'lion712yt@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
