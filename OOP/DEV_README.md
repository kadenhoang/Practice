# Developer Mode

## Authentication Bypass

For development and testing purposes, you can bypass the login/signup screen using either of these methods:

### Method 1: Environment Variable (Automatic)

Set the `BYPASS_AUTH` environment variable before running the app:

**PowerShell:**
```powershell
$env:BYPASS_AUTH="1"
python gui.py
```

**Command Prompt (cmd):**
```cmd
set BYPASS_AUTH=1
python gui.py
```

**Bash (Git Bash/WSL):**
```bash
BYPASS_AUTH=1 python gui.py
```

Accepted values: `1`, `true`, `True`, `TRUE`, `yes`, `Yes`, `YES`

When this environment variable is set, the app will automatically skip the login screen and go directly to the main application.

### Method 2: Keyboard Shortcut (Manual)

When the login screen is displayed, press:
```
Ctrl + Shift + D
```

This will immediately bypass authentication and take you to the main application.

A small hint `(Dev bypass: Ctrl+Shift+D)` is displayed at the bottom of the login screen to remind you of this shortcut.

## Security Note

⚠️ **These bypass methods are for development only.** Do not use them in production environments. The environment variable and keyboard shortcut are intentionally simple to facilitate rapid development and testing.

## Visual Indicators

When `BYPASS_AUTH` is enabled via environment variable:
- The login screen subtitle will show `[DEV MODE: Auth bypassed]`
- The hint for the keyboard shortcut will be hidden (since you're already in dev mode)

## Use Cases

- Testing the UI without creating accounts
- Quickly iterating on features without authentication overhead
- Demonstrating the app to stakeholders
- Running automated tests
