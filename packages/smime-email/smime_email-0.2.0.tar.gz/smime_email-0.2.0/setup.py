# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smime_email']

package_data = \
{'': ['*']}

install_requires = \
['cryptography==38.0.4']

setup_kwargs = {
    'name': 'smime-email',
    'version': '0.2.0',
    'description': 'A Python library to generate a signed email',
    'long_description': '# python-smime-email\n\n<a href="https://pypi.org/project/smime-email/"><img alt="PyPI" src="https://img.shields.io/pypi/v/smime-email"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n<a href="https://pepy.tech/project/smime-email"><img alt="Downloads" src="https://pepy.tech/badge/smime-email"></a>\n\nGenerate x509 SMIME signed emails with ease!\n\n## Usage\n\n1. Generate the email raw content\n    ```python\n    import smime_email\n\n    data = b"Hello!"\n    SMIME_KEY = smime_email.load_key("key_path.pem")\n    SMIME_INTERMEDIATE = smime_email.load_certificates("intermediate_path.pem")\n    SMIME_CERT = smime_email.load_certificates("cert_path.pem")[0]\n    email_raw_bytes = smime_email.get_smime_attachment_content(data, SMIME_KEY, SMIME_INTERMEDIATE, SMIME_CERT)\n    ```\n\n1. Send it using any email library you like. Here is an example as Django email backend\n\n    ```python\n    email_raw_bytes = smime_email.get_smime_attachment_content(data, SMIME_KEY, SMIME_INTERMEDIATE, SMIME_CERT)\n    # ...\n    class EmailBackend(BaseEmailBackend):\n        def send_messages(self, message) -> int:\n            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:\n                server.sendmail(message.from_email, message.to, email_raw_bytes)\n            return 1\n    ```\n\n## Development\n\nThe code is formatted with **black** and **isort** and checked with various linters.\nTo run the whole linting and formatting process, run `poetry run poe all`.\n',
    'author': 'Siemens',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
