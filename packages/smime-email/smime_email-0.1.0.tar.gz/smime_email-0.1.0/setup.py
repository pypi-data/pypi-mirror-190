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
    'version': '0.1.0',
    'description': 'A Python library to generate a signed email',
    'long_description': '# python-smime-email\n\nGenerate x509 SMIME signed emails with ease!\n\n## Usage\n\n1. Generate the email raw content\n    ```python\n    import smime_email\n\n    data = b"Hello!"\n    SMIME_KEY = smime_email.load_key("key_path.pem")\n    SMIME_INTERMEDIATE = smime_email.load_certificates("intermediate_path.pem")\n    SMIME_CERT = smime_email.load_certificates("cert_path.pem")[0]\n    email_raw_bytes = smime_email.get_smime_attachment_content(data, SMIME_KEY, SMIME_INTERMEDIATE, SMIME_CERT)\n    ```\n\n1. Send it using any email library you like. Here is an example as Django email backend\n\n    ```python\n    email_raw_bytes = smime_email.get_smime_attachment_content(data, SMIME_KEY, SMIME_INTERMEDIATE, SMIME_CERT)\n    # ...\n    class EmailBackend(BaseEmailBackend):\n        def send_messages(self, message) -> int:\n            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:\n                server.sendmail(message.from_email, message.to, email_raw_bytes)\n            return 1\n    ```\n',
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
