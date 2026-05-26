# Auth App — Login & Register UI

A clean, responsive authentication UI built with pure **HTML**, **CSS**, and **Vanilla JavaScript**. No frameworks, no dependencies (other than a Google Font and Tabler Icons via CDN).

## Features

- **Login** — email + password, remember me, show/hide password
- **Register** — first/last name, email, password with strength meter, confirm password, terms checkbox
- **Forgot Password** — email input with mock reset flow
- **Password hashing** — uses the native Web Crypto API (`SHA-256`)
- **In-memory user store** — accounts persist during the session
- **Responsive** — sidebar hides on mobile
- **Accessible** — ARIA roles, labels, and keyboard-friendly

## Project Structure

```
auth-project/
├── index.html       # Markup & layout
├── css/
│   └── style.css    # All styles
├── js/
│   └── app.js       # All logic
└── README.md
```

## Getting Started

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/auth-project.git

# Open in browser — no build step needed
open index.html
```

Or just drag `index.html` into any browser.

## Push to GitHub

```bash
git init
git add .
git commit -m "feat: initial auth UI with login, register, forgot password"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/auth-project.git
git push -u origin main
```

## Screenshots

| Login | Register | Forgot Password |
|-------|----------|-----------------|
| Sign in with email + password | Create account with strength meter | Send reset link |

## Tech Stack

- HTML5
- CSS3 (custom properties, grid, flexbox)
- Vanilla JS (ES2020+, Web Crypto API)
- [Tabler Icons](https://tabler-icons.io/) (CDN)
- [Inter](https://fonts.google.com/specimen/Inter) (Google Fonts)

## License

MIT
