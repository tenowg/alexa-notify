import json
import os
import threading

import requests

NOTIFY_ME_URL = "https://api.notifymyecho.com/v1/NotifyMe"
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")


class AnyType(str):
    def __ne__(self, other):
        return False


any_type = AnyType("*")


def _load_saved_access_code():
    code = os.environ.get("ALEXA_NOTIFY_ACCESS_CODE", "").strip()
    if code:
        return code
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("access_code", "").strip()
    except (OSError, ValueError):
        return ""


def _send_notification(message, access_code):
    try:
        resp = requests.post(
            NOTIFY_ME_URL,
            json={"notification": message, "accessCode": access_code},
            timeout=10,
        )
        if resp.status_code == 200:
            print(f"[Alexa Notify] Sent: {message}")
        else:
            print(f"[Alexa Notify] Failed ({resp.status_code}): {resp.text}")
    except requests.RequestException as e:
        print(f"[Alexa Notify] Error sending notification: {e}")


class AlexaNotify:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "message": ("STRING", {"default": "Your ComfyUI workflow has finished.", "multiline": True}),
            },
            "optional": {
                "passthrough": (any_type, {}),
                "access_code": ("STRING", {"default": "", "tooltip": "Notify Me skill access code. Leave blank to use config.json or the ALEXA_NOTIFY_ACCESS_CODE environment variable."}),
                "enabled": ("BOOLEAN", {"default": True}),
                "wait_for_send": ("BOOLEAN", {"default": False, "tooltip": "If True, the workflow waits until the notification request completes."}),
            },
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("passthrough",)
    FUNCTION = "notify"
    CATEGORY = "notifications"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def notify(self, message, passthrough=None, access_code="", enabled=True, wait_for_send=False):
        if enabled:
            code = access_code.strip() or _load_saved_access_code()
            if not code:
                print("[Alexa Notify] No access code set. Provide one on the node, in config.json, or via ALEXA_NOTIFY_ACCESS_CODE.")
            elif not message.strip():
                print("[Alexa Notify] Empty message, nothing sent.")
            else:
                if wait_for_send:
                    _send_notification(message, code)
                else:
                    threading.Thread(target=_send_notification, args=(message, code), daemon=True).start()
        return (passthrough,)


NODE_CLASS_MAPPINGS = {
    "AlexaNotify": AlexaNotify,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AlexaNotify": "Alexa Notify (Notify Me)",
}
