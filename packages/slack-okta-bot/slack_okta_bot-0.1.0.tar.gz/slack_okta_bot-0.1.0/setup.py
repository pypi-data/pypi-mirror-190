# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slack_okta_bot']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'slack-bolt>=1.16.1,<2.0.0']

entry_points = \
{'console_scripts': ['slack-okta-bot = slack_okta_bot:slack.run_local']}

setup_kwargs = {
    'name': 'slack-okta-bot',
    'version': '0.1.0',
    'description': 'Provides quick access to Okta user management from Slack',
    'long_description': '# slack-okta-bot\n\n### Provides the backend service for an Okta application that gives users the ability to execute common tasks\nThe backend can run:\n* As a standalone server\n* AWS Lambda Function URL\n* AWS Lambda as an ELB target\n\nCurrent features:\n* Reset MFA Factors\n* Reset password\n\n## Configuration\nThe following env vars are used for configuration\n\n| Name                   | Description                                                               | Required | Default                                              |   |\n|------------------------|---------------------------------------------------------------------------|----------|------------------------------------------------------|---|\n| HELP_CHANNEL           | Help channel displayed in responses to user                               | no       | #devops-help                                         |   |\n| HOME_HEADER            | Header displayed in app home page                                         | no       | :gear: Get help with common DevOps Okta tasks :gear: |   |\n| HOME_VIEW              | Additional info to show in app home page                                  | no       |                                                      |   |\n| RESET_MFA_COMMAND      | Command the user sends to reset MFA                                       | no       | /reset-mfa                                           |   |\n| RESET_PASSWORD_COMMAND | Command the user sends to reset password                                  | no       | /reset-password                                      |   |\n| TEST_USER              | An email address that, if set, be used instead of the user\'s slack email. | no       |                                                      |   |\n| PORT                   | Port to run the local server on                                           | no       | 3000                                                 |   |\n| SLACK_BOT_TOKEN        | Slack Bot User Oauth Token                                                | yes      |                                                      |   |\n| SLACK_SIGNING_SECRET   | Slack Signing Secret                                                      | yes      |                                                      |   |\n| OKTA_URL               | Okta api endpoint <yourdomain.okta.com/api/v1>                            | yes      |                                                      |   |\n| OKTA_TOKEN             | Okta API token                                                            | yes      |                                                      |   |\n\n\n\n## Usage\n\n### With AWS Lambda: The easy way\nFor convenience, if you don\'t need any additional logic in your handler, you can just\nbuild your package using `build_lambda.sh` (Described below) and set your Lambda\'s handler to `slack_okta_bot.aws_lambda.lambda_handler`.\n\n\n\n### AWS Lambda: Manual way\n```python\nfrom json import dumps\nfrom logging import getLogger\n\nfrom slack_okta_bot.slack import slack_app\nfrom slack_okta_bot.aws_lambda import LambdaHandler\n\n\ngetLogger().setLevel("INFO")\n\n\ndef handler(event, context):\n  getLogger().info(dumps(event, indent=2))\n  handler = LambdaHandler(slack_app)\n  try:\n    res = handler.handle(event, context)\n    getLogger().info(res)\n    return res\n  except Exception as e:\n    getLogger().info(e)\n```\n\nIn your Lambda config You would set your lambda handler to `module.handler` where `module` is the name of your Lambda package module\n\n\n## Building a basic Lambda package\n\nFrom source:\n* Run `build_with_poetry.sh`. It requires that `poetry` be installed and will install it if missing.\n* Upload the created zip file to S3 and configure your Lambda to pull from S3\n* Optionally upload the package manually in the AWS Lambda console\n* Set your Lambda\'s handler to `slack_okta_bot.aws_lambda.lambda_handler`\n\nUsing PIP\n* Run `pip install slack-okta-bot -t packages`\n* `cd` into ./packages directory\n* Run `zip -r ../lambda.zip . -x \'*.pyc\'`\n* Upload ../lambda.zip to S3 and configure your Lambda to pull from S3\n* Optionally upload the package manually in the AWS Lambda console\n* Set your Lambda\'s handler to `slack_okta_bot.aws_lambda.lambda_handler`\n\n\n### Running as a server\nThe package will install a shell script that can run a server\n\n```\n> slack-okta-bot\nINFO:slack_okta_bot:Logging to stdout\n⚡️ Bolt app is running! (development server)\n127.0.0.1 - - [23/Dec/2022 12:11:02] "POST /slack/events HTTP/1.1" 200 -\n```\n\nIf you need to import and run from your own script:\n\n```python\nfrom slack_okta_bot import run_local\n\n# do cool stuff\n\nrun_local()\n\n```\n\n## Slack App\nTo install in Slack:\n\n* Update slack-okta-bot.yaml with the domain you will be using\n* Update any other options you would like to change\n* Go to applications in your Slack org\'s admin area (https://api.slack.com/apps)\n* Click the "Create New App" button\n* Click "From an app manifest"\n* Select workspace to install to\n* Make sure that "YAML" tab is selected\n* Under "Basic Information" save your Signing Secret so you can export it to the required env var\n* Get the Bot User Oauth Token from the "Oauth & Permissions" tab so you can export it to the required env var\n* Deploy your application backend\n* In the Slack app configuration page go to "Event Subscriptions"\n* If the Request URL is not marked as "Verified" click the verify button/link\n\nYour app\'s homepage should now show and commands will become active. Test by entering a slash command in any channel in slack. Your interaction with the bot will be private and won\'t be displayed to other users in the chat. If the application is installed into the Apps side pane in Slack then you can also access the app\'s home page to see the description and available commands.\n',
    'author': 'Mathew Moon',
    'author_email': 'me@mathewmoon.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mathewmoon/slack-okta-bot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
