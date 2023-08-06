# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cgepy', 'cgepy.unstable']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cgepy',
    'version': '0.5.10',
    'description': 'Tools for developing graphical programs inside the console.',
    'long_description': '# Welcome to cgePy!\nHi! I\'m the creator of cgePy. Thanks for using my template!\nThis document will tell you everything you need to know in order to start using cgePy.\n***\n## Licence\nFirstly, I prefer some credit for all programs made with cgePy, though this is your choice.\nClaiming that this library\'s code is yours is explicitly NOT ALLOWED. If you would like to develop cgePy, please contact me at **lion712yt@gmail.com**.\n***\n## Getting Started\n\n\n\n***\n## Customization\n\nNow that you\'ve set cgePy, you might ask, "Can I change the color of the background" or "How can I change the player to a different color?"  and maybe even "How do I make the grid bigger?"\n\nWell, look no further as your problem is solved!\\\nFirst off, t:\n> ``````\n===\n\n***\n## Standard Methods\nWith the recent update, cgePy has been switching to an object-based system.\n\nFirst off, try this code:\n```py\ngrid = cge.Grid()\ngrid.Update()\n```\nIt will update (show the most recent version of) the grid!\\\nNow,\n```py\ngrid.write(1,YELLOW+"  ")\n#"  " is a blank pixel on the grid\n#Each pixel must be EXACTLY two characters long\ngrid.Update()\n```\nThe result will be the same as before, but the 2nd \'pixel\' on the grid will be yellow... ish, more of an orange, actually. \n\nA complete list of these \'functions\':\n> clear - resets the grid\\\n> write\\\n> swap\\\n> Update\\\n> Self\n***\n\n## Legacy Functions\nAlthough these methods aren\'t reccommended, you can still use them.\n\n**Add ```cge.legacy.``` before them, as in ```cgepy.cge.legacy.updategrid()```!**\n***\n### updategrid():\nPrints out the grid that a game uses. This function is basically a frame, and without it any movements or changes won\'t be shown.\\\nUsage:\n```python\nupdategrid(my_grid)\n```\n```python\nupdategrid() #support for this "context" feature may not work\n```\n\n\n### creategrid():\nFunction for creating grids.\\\nUsage:\n```python\nmy_grid = creategrid()\n```\n\n### updatepos():\nMoves the player\'s sprite to the position entered in the parameters.\\\nUsage:\n```python\nupdatepos(position)\n```\n\n### movepos(): \nMoves the player\'s sprite one positon to the direction you input.\n Valid parameters are: "up", "down", "right", "left". No other parameters will work.\\\nUsage:\n```python\nmovepos("direction")\n```\n\n### paint():\n>This function is a little more complicated than the others.\\\nIn an older version of the README, I talked about how creating maps and art was repetitive. For example you might have done\n>```python\n>cm[0] = RED+"  " #support for this may not work\n>```\n>```python\n>cm[1] = BLUE+"  " #support for this may not work\n>```\n>in order to set the first two elements in the list to be red and blue.\\\nHowever, when making grids on a larger scale, that would be an issue. After a while, I came up with a solution for this.\n\nCreates a grid using a special string with certain values arranged like an array.\n\nUsage:\n```python\n#In this case, our grid will be 10x10\nmy_string = \'\'\'\nRE RE RE BG RE RE BG RE RE RE\nRE BG BG BG BG BG BG RE RE RE\nRE BG RE RE RE RE RE RE RE RE\nRE BG BG BG BG BG BG BG BG RE\nRE RE RE RE RE RE RE RE BG RE\nRE RE RE BG BG BG BG BG BG RE\nRE RE RE BG RE RE RE BG RE RE\nRE RE RE BG RE RE RE BG RE RE\nRE RE RE BG BG BG BG BG RE RE\nRE RE RE RE RE BG RE RE RE RE\n\'\'\'\n#with RE being RED\n#and BG being BACKGROUND\nmy_grid = paint(my_string)\n```\n> Now, for our example,\n```python\nupdategrid(my_grid)\n```\n> After running the code shown above, the result would be:\n>![The sprite isn\'t visible because it\'s also colored red](/readme-assets/paintresult.png)\n> ###### The sprite isn\'t visible in this picture because it\'s also colored red.\n\nYou can find a full list of the ID\'s used for ```paint()``` strings inside of ```cge/init.py```\\\nHopefully this function helps!\n***\n### Functions found in driver-extras.py\n\n>### targetroll():\n>Rolls the position of a target sprite.\nPlease note that this does not change the positon or display the sprite, as this requires you to manualy update the grid\\\nUsage:\n> ```python\n> targetroll()\n> ``` \n> ### squaregame(max score, target color):\n> Sends the user into a game where they must capture the target the amount of times you input.\n Once the user has captured the target enough times, the code will proceed.\\\n Usage:\n>```python\n>squaregame(maxscore,color)\n> ```\nNote that these functions might not work\n***\n\n### That\'s about it as of now.\n\n#### Happy coding!',
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
