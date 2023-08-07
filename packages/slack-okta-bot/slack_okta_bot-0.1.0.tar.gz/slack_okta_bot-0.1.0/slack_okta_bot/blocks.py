#!/usr/bin/env python3
from typing import Dict, List
from .config import HELP_CHANNEL, HOME_HEADER, RESET_MFA_COMMAND, RESET_PASSWORD_COMMAND, HOME_VIEW


def get_reset_password_form(email) -> List[Dict]:
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":gear: *Confirm that you want to reset password for {email}. Okta will send you a password reset email.*",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*Are you sure?*"},
            "accessory": {
                "action_id": "confirm_password_reset",
                "type": "button",
                "text": {"type": "plain_text", "text": "Reset My Password"},
            },
        },
    ]


def get_reset_mfa_form(
    email: str, factors: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":gear: *Reset MFA Devices for {email}* :gear:",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "You can select multiple devices. Resetting all MFA devices will force Okta to prompt you to re-enroll a device on next login. If you reset a single device you will be required to use an existing device for your next login and can add a device in your personal account settings.\n",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":gear: *Select MFA devices to reset*",
            },
            "accessory": {
                "action_id": "reset_selected_mfa",
                "type": "multi_static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Click to select MFA Devices",
                },
                "options": [
                    {
                        "text": {"type": "plain_text", "text": name},
                        "value": id,
                    }
                    for id, name in factors.items()
                ],
            },
        },
    ]


def get_home_view() -> Dict:
    form = {
        "type": "home",
        "callback_id": "home_view",
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": HOME_HEADER}},
            {"type": "divider"},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "\n *Available Commands:* \n"},
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"\n\nTo reset MFA devices: `{RESET_MFA_COMMAND}`\nReset your password: `{RESET_PASSWORD_COMMAND}`\n\n",
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"\n\nWhen resetting MFA you won't be prompted on login to re-enroll if you have any other methods still enrolled. If you have at least one working MFA you can add or remove authenticators under your personal settings in Okta. Resetting all MFA devices will cause Okta to prompt you to enroll a device after a successful password login.\n\n:slack: For additional help reach out in {HELP_CHANNEL} :slack:",
                },
            },
        ],
    }

    if HOME_VIEW:
        homeview = [
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": HOME_VIEW
                }
            }
        ]
        form["blocks"] += homeview

    return form
