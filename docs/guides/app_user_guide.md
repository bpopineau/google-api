# User Guide: MyGoog Desktop App

Welcome to the **MyGoog** Desktop Application. This guide walks you through the features and usage of the GUI.

## Getting Started

### 1. Launching the App
After installation, simply run:
```bash
mygoog
```

### 2. Authentication
On your first run, the app will open your default web browser to sign in with your Google Account.
1.  **Authorize**: Click "Allow" to grant MyGoog access to your data.
2.  **Confirm**: Close the browser tab when prompted.
3.  **Use**: The app will automatically detect success and load your dashboard.

> **Note**: Your credentials are stored securely in your home directory. You do not need to sign in every time.

## Dashboard Overview

The **Home Dashboard** is your command center. It provides a quick summary:
- **Upcoming Events**: Your next 3 calendar meetings.
- **Recent Files**: The last 5 files accessed in Drive.
- **Inbox Zero Status**: Unread email count.

## Features

### 📂 Drive Explorer
Navigate your Google Drive as if it were a local folder.
- **Double Click**: Open folders.
- **Right Click**: Context menu for Download/Delete (coming soon).

### 📧 Gmail
Quickly scan your inbox.
- **Search**: Use the search bar to find emails by sender or subject.
- **View**: Click an email to view the snippet and metadata.

### ⚙️ Settings
Customize your experience.
- **Theme**: Switch between **Dark Mode** (default) and Light Mode (requires restart).
- **Sign Out**: Click "Sign Out" to clear your credentials. This is useful if you want to switch accounts.

## Troubleshooting

- **App Freezes on "Authenticating..."**: Check your internet connection. If the issue persists, try deleting the credentials file manually (see [Configuration](configuration.md)) and relaunching.
- **Window Size Not Saving**: Ensure you are closing the app normally (X button or File -> Exit).
