# 04\_GITHUB-CPANEL-DEPLOYMENT [​](#_04-github-cpanel-deployment)

**Version:** 3.0 **Last Updated:** February 7, 2026 **Purpose:** Automated deployment from GitHub to cPanel hosting via GitHub Actions and FTP

* * *

## Overview [​](#overview)

This guide documents deploying any application from a GitHub repository to cPanel hosting using GitHub Actions for CI/CD. When you push commits to your deployment branch, GitHub Actions automatically builds the application and deploys the output to cPanel via FTP.

### Deployment Flow [​](#deployment-flow)

```
Local Development → Git Push → GitHub Actions Build → FTP Deploy → Live on cPanel
```

### Version Control [​](#version-control)

Your GitHub repository is your version control system. Every commit is tracked with full history — you can view changes, compare versions, and revert at any time. There is no need for cPanel's "Git Version Control" feature. cPanel simply receives the built files via FTP; GitHub handles everything else.

### Why This Approach [​](#why-this-approach)

*   **Framework-agnostic** — works with any stack (React, Python, static HTML, etc.)
*   **No build tools needed on cPanel** — the build runs on GitHub's servers
*   **Only built files reach production** — source code stays in your repository
*   **No SSH keys or deploy keys required** — FTP credentials stored securely as GitHub Secrets
*   **Automatic on every push** — no manual steps after initial setup
*   **Full version history on GitHub** — every change tracked, diffable, and revertible

* * *

## Prerequisites [​](#prerequisites)

*   A GitHub account
*   A cPanel hosting account with FTP access
*   Git installed locally

* * *

## Initial Setup [​](#initial-setup)

### 1\. Create a Private GitHub Repository [​](#_1-create-a-private-github-repository)

1.  Go to GitHub.com → **New repository**
2.  Set visibility to **Private**
3.  Initialize with a README or push existing code:

bash

```
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin master
```

### 2\. Get Your cPanel FTP Credentials [​](#_2-get-your-cpanel-ftp-credentials)

You need four values from your cPanel hosting:

Value

Where to Find It

Example

**FTP Server**

cPanel → FTP Accounts or hosting welcome email

`ftp.yourdomain.com`

**FTP Username**

cPanel → FTP Accounts

`user@yourdomain.com`

**FTP Password**

Set in cPanel → FTP Accounts

(your password)

**Remote Path**

The directory on cPanel to deploy into

`/public_html/your-app/`

### 3\. Store FTP Credentials as GitHub Secrets [​](#_3-store-ftp-credentials-as-github-secrets)

GitHub Secrets keep your credentials encrypted and out of your code.

1.  Go to your GitHub repository
2.  Navigate to **Settings → Secrets and variables → Actions**
3.  Click **New repository secret** and add each:

Secret Name

Value

`FTP_SERVER`

Your FTP server hostname

`FTP_USERNAME`

Your FTP username

`FTP_PASSWORD`

Your FTP password

### 4\. Create the GitHub Actions Workflow [​](#_4-create-the-github-actions-workflow)

Create the workflow file in your repository at `.github/workflows/deploy.yml`:

yaml

```
name: Build and Deploy to cPanel

on:
  push:
    branches:
      - master  # Change to your deployment branch

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      # -----------------------------------------------
      # BUILD STEP — customize for your framework
      # -----------------------------------------------

      # Example: Node.js / React / Vite
      # - name: Set up Node.js
      #   uses: actions/setup-node@v4
      #   with:
      #     node-version: '20'
      # - name: Install dependencies
      #   run: npm ci
      # - name: Build
      #   run: npm run build

      # Example: Python / Django
      # - name: Set up Python
      #   uses: actions/setup-python@v5
      #   with:
      #     python-version: '3.12'
      # - name: Install dependencies
      #   run: pip install -r requirements.txt
      # - name: Collect static files
      #   run: python manage.py collectstatic --noinput

      # Example: Static HTML (no build step needed)
      # (skip straight to deploy)

      # -----------------------------------------------
      # DEPLOY STEP — pushes build output to cPanel
      # -----------------------------------------------
      - name: Deploy via FTP
        uses: SamKirkland/FTP-Deploy-Action@v4.3.5
        with:
          server: ${{ secrets.FTP_SERVER }}
          username: ${{ secrets.FTP_USERNAME }}
          password: ${{ secrets.FTP_PASSWORD }}
          local-dir: ./dist/   # Change to your build output folder
          server-dir: /public_html/your-app/  # Change to your cPanel path
```

**Key settings to customize:**

Setting

Description

Examples

`branches`

Which branch triggers deployment

`master`, `main`, `production`

Build step

Uncomment and adjust for your framework

See examples in the workflow

`local-dir`

Your build output folder (trailing slash required)

`./dist/`, `./build/`, `./public/`, `./`

`server-dir`

Destination path on cPanel (trailing slash required)

`/public_html/`, `/public_html/my-app/`

### 5\. Push and Verify [​](#_5-push-and-verify)

bash

```
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Actions deployment workflow"
git push origin master
```

Then check progress:

1.  Go to your GitHub repository → **Actions** tab
2.  Watch the workflow run
3.  Once complete, visit your live URL to verify

* * *

## Day-to-Day Workflow [​](#day-to-day-workflow)

After initial setup, deployment is automatic:

bash

```
# 1. Make your changes locally
# 2. Stage and commit
git add .
git commit -m "Description of changes"

# 3. Push — deployment happens automatically
git push origin master
```

That's it. GitHub Actions builds and deploys on every push.

### Monitoring Deployments [​](#monitoring-deployments)

*   **GitHub Actions tab** — shows build status, logs, and errors for every push
*   **Green checkmark** on a commit means deployment succeeded
*   **Red X** means the build or deploy failed — click into the workflow run for details

* * *

## Configuration [​](#configuration)

### .gitignore [​](#gitignore)

Keep credentials and unnecessary files out of your repository:

gitignore

```
# Environment / credentials
.env
.env.local
.env.production

# Dependencies
node_modules/
vendor/
venv/
__pycache__/

# Build output (built on CI, not committed)
dist/
build/

# OS files
.DS_Store
Thumbs.db

# IDE files
.vscode/
.idea/

# Logs
*.log
```

### Excluding Files from Deployment [​](#excluding-files-from-deployment)

The FTP action syncs your `local-dir` to `server-dir`. To exclude specific files from being uploaded, add an `.ftp-deploy-sync-exclude` file or use the `exclude` option in the workflow:

yaml

```
- name: Deploy via FTP
  uses: SamKirkland/FTP-Deploy-Action@v4.3.5
  with:
    server: ${{ secrets.FTP_SERVER }}
    username: ${{ secrets.FTP_USERNAME }}
    password: ${{ secrets.FTP_PASSWORD }}
    local-dir: ./dist/
    server-dir: /public_html/your-app/
    exclude: |
      **/.git*
      **/.git*/**
      **/node_modules/**
      **/.env
```

### SPA Routing (Single Page Applications) [​](#spa-routing-single-page-applications)

If you're deploying a single page application (React, Vue, etc.), add an `.htaccess` file in your build output so all routes resolve correctly:

apache

```
RewriteEngine On
RewriteBase /
RewriteRule ^index\.html$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]
```

Place this file in your `public/` folder (or wherever your build tool copies static assets from) so it gets included in the build output.

### HTTPS Redirect [​](#https-redirect)

Force HTTPS on cPanel by adding to your `.htaccess`:

apache

```
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

* * *

## Database Migrations [​](#database-migrations)

Migration scripts live in your repository and are run manually on cPanel after deployment. This keeps your database changes version-controlled alongside your code.

### Where to Store Migration Files [​](#where-to-store-migration-files)

Keep migrations in a dedicated folder in your repository:

```
your-repo/
├── migrations/
│   ├── 001_create_users_table.sql
│   ├── 002_add_role_column.sql
│   └── 003_create_invoices_table.sql
├── src/
├── .github/workflows/
└── ...
```

Or use your framework's built-in migration system:

Framework

Migration Location

Run Command

Django

`app/migrations/` (auto-generated)

`python manage.py migrate`

Laravel

`database/migrations/`

`php artisan migrate`

Raw SQL

`migrations/` (manual files)

`mysql -u user -p dbname < migrations/001_file.sql`

### Running Migrations After Deployment [​](#running-migrations-after-deployment)

1.  Log into **cPanel → Terminal** (or SSH into your server)
2.  Navigate to your application directory:

bash

```
cd ~/public_html/your-app
```

3.  Run the migration:

bash

```
# Django
python manage.py migrate

# Laravel
php artisan migrate

# Raw SQL file
mysql -u dbuser -p dbname < migrations/001_create_users_table.sql
```

### Keeping Track of Applied Migrations [​](#keeping-track-of-applied-migrations)

**Framework ORMs** (Django, Laravel, etc.) handle this automatically — they maintain a migrations table in the database and only run new migrations.

**Raw SQL migrations** — track manually. Options:

*   **Naming convention** — prefix with sequential numbers (`001_`, `002_`, etc.) and keep a log of what's been applied
*   **Migrations table** — create a simple tracking table:

sql

```
CREATE TABLE IF NOT EXISTS applied_migrations (
    filename VARCHAR(255) PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

After running a migration:

sql

```
INSERT INTO applied_migrations (filename) VALUES ('001_create_users_table.sql');
```

Check what's been applied:

sql

```
SELECT * FROM applied_migrations ORDER BY applied_at;
```

### Migration Best Practices [​](#migration-best-practices)

*   **Always test migrations locally first** before running on production
*   **Never edit a migration that's already been applied** — create a new one instead
*   **Back up the database before running migrations** — cPanel → Backup Wizard or `mysqldump`
*   **One change per migration file** — easier to track and rollback
*   **Include both up and down** — if possible, write a rollback script for each migration

* * *

## Rollback [​](#rollback)

### Option 1: Re-run a Previous Deployment (Recommended) [​](#option-1-re-run-a-previous-deployment-recommended)

1.  Go to GitHub → **Actions** tab
2.  Find the last successful workflow run
3.  Click **Re-run all jobs**

This rebuilds and deploys the code from that commit.

### Option 2: Revert the Commit [​](#option-2-revert-the-commit)

bash

```
git revert HEAD
git push origin master
```

This creates a new commit that undoes the last change, and triggers a fresh deployment.

* * *

## Troubleshooting [​](#troubleshooting)

### Build Fails on GitHub Actions [​](#build-fails-on-github-actions)

Symptom

Cause

Solution

Workflow never runs

Workflow file in wrong location

Must be at `.github/workflows/deploy.yml`

Build step fails

Missing dependencies or wrong versions

Check Node/Python version, verify `package.json` or `requirements.txt`

Build succeeds but output is empty

Wrong build command or output directory

Verify `local-dir` matches your actual build output folder

### FTP Deploy Fails [​](#ftp-deploy-fails)

Symptom

Cause

Solution

Authentication failed

Wrong FTP credentials

Verify secrets in GitHub → Settings → Secrets

Connection timeout

Wrong FTP server hostname

Check cPanel for correct FTP host

Permission denied

FTP user lacks write access to target directory

Check FTP account permissions in cPanel

Files deployed to wrong location

Wrong `server-dir`

Verify the path matches your cPanel directory structure

### Site Not Working After Deployment [​](#site-not-working-after-deployment)

Symptom

Cause

Solution

404 on all routes

SPA routing not configured

Add `.htaccess` rewrite rules (see SPA Routing section)

Old content showing

Browser cache

Hard refresh (Ctrl+Shift+R)

Blank page

Build output missing `index.html`

Check `local-dir` setting and build output

Mixed content warnings

HTTP resources on HTTPS page

Update asset URLs to use HTTPS or relative paths

500 Internal Server Error

`.htaccess` syntax error

Check `.htaccess` file for typos

* * *

## Security Best Practices [​](#security-best-practices)

1.  **Keep the repository private** — source code and workflow files are not publicly exposed
2.  **Use GitHub Secrets for all credentials** — never hardcode FTP passwords or API keys in workflow files
3.  **Use `.gitignore` for environment files** — `.env` files should never be committed
4.  **Force HTTPS** — add the HTTPS redirect to `.htaccess`
5.  **Set correct file permissions on cPanel** — 644 for files, 755 for directories

* * *

## Resources [​](#resources)

*   [GitHub Actions Documentation](https://docs.github.com/en/actions)
*   [FTP Deploy Action (SamKirkland)](https://github.com/SamKirkland/FTP-Deploy-Action)
*   [GitHub Encrypted Secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)

* * *

## Project Implementation: Business Manager App [​](#project-implementation-business-manager-app)

This section documents the specific CI/CD setup for the Business Manager app (`app.salesfield.net`).

### Architecture [​](#architecture)

Component

Deployment Method

Details

React SPA (Vite)

**Automated** — GitHub Actions builds + FTP

Push to `master` → builds → FTP to cPanel

Django Backend

**Manual** — cPanel Terminal

Pull code + run update commands when backend changes

### Workflow File [​](#workflow-file)

Located at `.github/workflows/deploy.yml`. Single job:

**`deploy-frontend`** — Builds React SPA with Node 20, deploys `dist/` contents via FTP to cPanel

### GitHub Secrets Required [​](#github-secrets-required)

Configure at: **Repository → Settings → Secrets and variables → Actions**

Only 3 secrets needed (FTP credentials):

Secret

Description

`FTP_SERVER`

cPanel FTP hostname

`FTP_USERNAME`

cPanel FTP username

`FTP_PASSWORD`

cPanel FTP password

### Critical: .htaccess Protection [​](#critical-htaccess-protection)

The FTP deploy **excludes `.htaccess`** from upload. This is essential because:

1.  Vite copies `public/.htaccess` (SPA routing only) into `dist/.htaccess` during build
2.  The production server's `.htaccess` contains **Passenger WSGI directives** (`PassengerEnabled On`, `PassengerAppType wsgi`, etc.) that are NOT in the build `.htaccess`
3.  If FTP overwrites the production `.htaccess`, Django/Passenger stops working entirely

The production `.htaccess` is set up once during initial deployment (`deploy.sh`) and must not be touched by CI.

### Server Directory Layout [​](#server-directory-layout)

```
/home/salesfield/
├── app-salesfield/                  # Git repo clone
│   ├── django-backend/              # Django source
│   ├── src/                         # React source
│   └── dist/                        # React build (gitignored, built by CI)
│
├── public_html/app.salesfield.net/  # Subdomain document root
│   ├── index.html                   # React SPA entry
│   ├── assets/                      # Vite JS/CSS chunks
│   ├── .htaccess                    # Passenger + SPA routing (DO NOT overwrite)
│   ├── passenger_wsgi.py            # Symlink to django/passenger_wsgi.py
│   └── tmp/restart.txt              # Passenger restart trigger
│
└── app-salesfield/django/           # Django runtime
    ├── venv/                        # Python virtual environment
    ├── .env                         # Production environment variables
    ├── manage.py
    ├── config/                      # Django settings
    ├── apps/                        # Django apps
    ├── staticfiles/                 # Collected static files
    ├── media/                       # User uploads
    ├── logs/                        # Error and cron logs
    └── tmp/restart.txt              # Passenger restart trigger
```

### Django Backend Updates (via cPanel Terminal) [​](#django-backend-updates-via-cpanel-terminal)

When you make changes to Django code (models, views, serializers, etc.), run these commands in **cPanel → Terminal**:

bash

```
cd ~/app-salesfield
git pull origin master
cp -r django-backend/* django/

cd ~/app-salesfield/django
source venv/bin/activate
pip install -r requirements.txt --quiet
python manage.py migrate --noinput
python manage.py collectstatic --noinput --verbosity=0
touch tmp/restart.txt
```

For quick reference, these steps are:

1.  Pull latest code from GitHub
2.  Copy updated Django files to the runtime directory
3.  Install any new Python dependencies
4.  Run database migrations
5.  Collect static files
6.  Restart Passenger

### Implementation Phases [​](#implementation-phases)

Phase

Status

Description

1\. Workflow file created

DONE

`.github/workflows/deploy.yml` — frontend FTP deploy

2\. `.gitignore` updated

DONE

Added `/dist` — CI builds artifacts, not committed

3\. GitHub Secrets configured

TODO

Add 3 FTP secrets to repository settings

4\. Initial server setup

TODO

Run `deploy.sh` via cPanel Terminal for first-time provisioning

5\. First CI deployment

TODO

Push to master, verify workflow passes

6\. SSL setup

TODO

Let's Encrypt via cPanel for `app.salesfield.net`

7\. Cron jobs

TODO

Set up daily manifest and overdue invoice checks

### Monitoring [​](#monitoring)

*   **GitHub Actions**: `https://github.com/richardtheshannon/app.salesfield.net/actions`
*   **Re-run failed jobs**: Click into the failed run → "Re-run failed jobs"
*   **Server logs**: cPanel Terminal → `tail -f ~/app-salesfield/django/logs/error.log`

* * *

## Revision History [​](#revision-history)

Version

Date

Changes

1.0

2026-02-02

Initial documentation (cPanel Git Version Control approach)

2.0

2026-02-07

Complete rewrite: GitHub Actions + FTP deployment model, framework-agnostic

2.1

2026-02-07

Added Database Migrations section, version control clarification

3.0

2026-02-07

Added project-specific implementation section, frontend-only CI/CD, backend via cPanel Terminal

* * *

**End of Documentation**