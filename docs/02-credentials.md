# Step 02: Google OAuth Credentials (Personal Use)

This project uses **OAuth (Desktop app)** to access Google Workspace APIs for a single user (you).
You will create two local secret files:

- `credentials.json` (OAuth client ID/secret downloaded from Google Cloud)
- `token.json` (OAuth access + refresh token generated after you approve access once)

These files must **never** be committed to git.

---

## 1) Create a Google Cloud Project

1. Go to Google Cloud Console
2. Create a new project (or pick an existing one you control)
3. Make sure billing is enabled only if you need it (most Workspace APIs do not require billing for basic use)

---

## 2) Configure OAuth Consent Screen

In APIs & Services → OAuth consent screen:

1. Choose **External** (typical for personal Gmail accounts)
2. Fill out the required fields (app name, support email, developer contact)
3. Add yourself under **Test users**
4. Save

Notes:
- During development, your app will likely show as “unverified”. That’s fine for personal use as a test user.

---

## 3) Enable the APIs You Plan to Use

In APIs & Services → Library, enable:

- Google Drive API
- Google Sheets API
- Google Docs API
- Google Calendar API
- Google Tasks API
- Gmail API

---

## 4) Create OAuth Client Credentials (Desktop App)

In APIs & Services → Credentials:

1. Create Credentials → **OAuth client ID**
2. Application type: **Desktop app**
3. Create and download the JSON file

Rename the downloaded file to: `credentials.json`

---

## 5) Store Secrets Locally (NOT in the repo)

Pick a folder on your machine that is NOT inside the repository, for example:

- Windows: `%APPDATA%\google-integrations-suite\`
- macOS: `~/.config/google-integrations-suite/`
- Linux: `~/.config/google-integrations-suite/`

Put `credentials.json` there.

Later, when we implement auth, the library will create `token.json` in the same folder after the first login.

---

## 6) Add to .gitignore (Do Not Commit Secrets)

Add rules that ignore these files everywhere:

- `credentials.json`
- `credentials*.json`
- `token.json`
- `token*.json`

If you ever accidentally commit either file, treat it as compromised:
- delete the files from git history
- rotate/revoke the OAuth client or tokens
- generate new ones

---

## 7) Scope Planning (High-Level)

This library will request OAuth scopes matching the services you use.
Two important behaviors:

- If you add new scopes later, you often need to delete `token.json` and re-authenticate.
- For personal use, it’s fine to request broader scopes (fewer re-consent cycles), as long as you understand the risk.

We will define scopes in code in a later step.

---

## 8) “Done” Checklist

You are done with Step 02 when:

- [ ] All target APIs are enabled in your Google Cloud project
- [ ] OAuth consent screen is configured and you are added as a test user
- [ ] Desktop OAuth client is created
- [ ] `credentials.json` is downloaded and stored outside the repo
- [ ] You have a plan to ignore `credentials.json` + `token.json` in git
