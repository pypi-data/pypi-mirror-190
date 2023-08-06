# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octopusserver',
 'octopusserver.Http',
 'octopusserver.Http.Router',
 'octopusserver.Utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'octopusserver',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Octopusserver\n\n![Octopus](./assets/octopus.png)\n\n## How to install\n### Pypi\n```bash \npip install octopusserver\n```\n### Poetry\n```bash \npoetry add octopusserver\n```\n\n## Getting Started\n```python\nfrom octopusserver import Octopus\nfrom octopusserver import Request\nfrom octopusserver import Response\n\nPORT = 3000\n\napp = Octopus(PORT)\n\ndef hello_world(req: Request, res: Response):\n    res.send("Hello, World!")\n\napp.router.get("/", [hello_world])\n\napp.listen(lambda: print(f"Server listen on http://localhost:{ PORT }/"))\n```\n\n## How to register your application\'s routes\n```python\nfrom octopusserver import Octopus\n\nPORT = 3000\n\napp = Octopus(PORT)\n\nrouter = app.router\n\nrouter.get("path/to/get/route/", [trigger_get_route])\n\nrouter.post("path/to/post/route/", [trigger_post_route])\n\n```\n\n## For the future\n- [ ] Recive files\n- [ ] Handling post and get data\n\n## How did I do this? \n[Here](./HOW_DID_I_DO_THIS.md) \n\n## References\n* [ExpressJs](https://expressjs.com/)\n* [HTTP request methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)\n* [Common MIME types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types)\n* [HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)\n* [HTTP Server: Everything you need to know to Build a simple HTTP server from scratch](https://medium.com/from-the-scratch/http-server-what-do-you-need-to-know-to-build-a-simple-http-server-from-scratch-d1ef8945e4fa)\n* [Writing an HTTP server from scratch](https://bhch.github.io/posts/2017/11/writing-an-http-server-from-scratch/)\n* [Queue](https://en.wikipedia.org/wiki/Queue_(abstract_data_type))\n* [Hash table](https://en.wikipedia.org/wiki/Hash_table)',
    'author': 'pab-h',
    'author_email': 'dev.pab.2020@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
