# ComfyUI Alexa Notify

A ComfyUI custom node that sends notifications to your Amazon Alexa device when a workflow executes. Perfect for long-running image generation tasks — get notified the moment your workflow finishes without constantly checking the UI.

## Features

- **Passthrough any data type** — wire the node inline anywhere in your workflow; it passes through images, latents, strings, or any other data unchanged
- **Non-blocking** — notifications send in the background by default, never slowing down your workflow
- **Simple setup** — uses Amazon's official "Notify Me" skill; no password or complex authentication required
- **Flexible configuration** — set your access code via the node UI, a config file, or an environment variable
- **Always executes** — never cached, so you get a notification on every run

## Installation

1. Clone or download this repository into your ComfyUI `custom_nodes` folder:
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/yourusername/alexa-notify.git
   ```

2. Restart ComfyUI. The node will appear under the `notifications` category as **"Alexa Notify (Notify Me)"**.

## Setup

### Get Your Alexa Access Code

1. In the **Alexa app** (or [alexa.amazon.com](https://alexa.amazon.com)), search for and enable the **"Notify Me"** skill by Thomptronics (it's free).

2. Say **"Alexa, open Notify Me"** on any of your Echo devices, or open the skill in the app. Alexa will email your Amazon account an **access code** — a long string starting with `nmac...`. (this is the code I receive, it might be different to others)

3. Copy this code; you'll need it in the next step.

### Configure the Node

Choose one of these three methods (checked in order):

#### Option A: Node UI (simplest for single workflows)
- Add the node to your workflow
- Paste your access code into the `access_code` field
- Done

#### Option B: Config File (recommended for sharing workflows)
1. In the `alexa-notify` folder, copy `config.json.example` to `config.json`
2. Open `config.json` and replace the placeholder with your access code:
   ```json
   {
     "access_code": "nmac.YOUR_CODE_HERE"
   }
   ```
3. Save and restart ComfyUI

#### Option C: Environment Variable (for deployment/automation)
Set the environment variable before starting ComfyUI:
```bash
# Linux/macOS
export ALEXA_NOTIFY_ACCESS_CODE="amzn1.ask.account.YOUR_CODE_HERE"

# Windows (PowerShell)
$env:ALEXA_NOTIFY_ACCESS_CODE="amzn1.ask.account.YOUR_CODE_HERE"

# Windows (Command Prompt)
set ALEXA_NOTIFY_ACCESS_CODE=amzn1.ask.account.YOUR_CODE_HERE
```

## Usage

### Basic Example

1. Add the **"Alexa Notify (Notify Me)"** node to your workflow
2. Connect any output (image, latent, string, etc.) to the `passthrough` input
3. Connect the output to the next node in your workflow
4. Set the `message` field to what you want Alexa to say (e.g., "Your image generation is done")
5. Run your workflow

When the node executes, your Echo device will:
- Chime with a yellow notification ring
- Store the notification in your Alexa app

To hear the message, say **"Alexa, what are my notifications?"** on any Echo device.

### Node Inputs

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `message` | STRING | "Your ComfyUI workflow has finished." | The notification text |
| `passthrough` | Any | (optional) | Any data type; passes through unchanged |
| `access_code` | STRING | "" | Your Notify Me skill access code (overrides config file/env var) |
| `enabled` | BOOLEAN | True | Toggle notifications on/off without unplugging the node |
| `wait_for_send` | BOOLEAN | False | If True, the workflow waits for the HTTP request to complete; if False (default), sends in background |

### Node Outputs

| Output | Type | Description |
|--------|------|-------------|
| `passthrough` | Any | The same data passed into the `passthrough` input |

## Examples

### Notify when image generation finishes
```
KSampler → Alexa Notify → VAE Decode → Save Image
```
Connect the latent output from KSampler to the `passthrough` input of Alexa Notify, then connect its output to VAE Decode.

### Notify at the end of a complex workflow
```
... (your workflow) → Alexa Notify (with nothing connected to passthrough)
```
Use as a terminal node to notify when everything is done.

### Conditional notifications
Use the `enabled` toggle to only notify on certain runs, or wire it to a Switch node for conditional logic.

## Troubleshooting

### "No access code set" message in console
- Verify your access code is correct (should start with `amzn1.ask.account.`)
- Check that `config.json` exists and is valid JSON if using that method
- Verify the environment variable is set if using that method
- Restart ComfyUI after changing the config

### Notification doesn't arrive
- Confirm the Notify Me skill is enabled in your Alexa app
- Check your Amazon account email for the access code (it may be in spam)
- Verify your Echo device is online and connected to WiFi
- Check the ComfyUI console for error messages

### "Failed (4xx/5xx)" error in console
- Your access code may be invalid or expired
- Try re-opening the Notify Me skill on your Echo to generate a new code
- Check your internet connection

## How It Works

This node uses Amazon's official **Notify Me** skill, which provides a simple HTTP API for sending notifications. When the node executes:

1. It sends an HTTPS POST request to `https://api.notifymyecho.com/v1/NotifyMe` with your message and access code
2. Amazon's servers deliver the notification to your Alexa account
3. Your Echo device receives and displays the notification
4. The workflow continues immediately (or waits, if `wait_for_send` is enabled)

No passwords, no unofficial APIs, no complex authentication — just a simple, reliable HTTP call.

## Why Not Use alexapy?

The `alexapy` library allows Alexa to *speak* announcements aloud, which is more impressive. However, it requires:
- Storing your Amazon password in ComfyUI
- Managing 2FA cookies
- Dealing with Amazon's unofficial API, which breaks frequently

The Notify Me skill approach is simpler, more reliable, and doesn't require any sensitive credentials.

## Requirements

- ComfyUI (any recent version)
- An Amazon account with at least one Echo device
- Internet connection (to reach Amazon's notification API)

No additional Python packages required — `requests` is already included with ComfyUI.

## License

MIT

## Contributing

Issues and pull requests are welcome! If you find bugs or have feature ideas, please open an issue on GitHub.

## Disclaimer

This node is not affiliated with Amazon or Alexa. It uses the official Notify Me skill API. Amazon may change or discontinue this API at any time, though it's been stable for years.
