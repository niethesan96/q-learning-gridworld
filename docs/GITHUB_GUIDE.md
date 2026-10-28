# Push this project to GitHub

These instructions use Windows PowerShell. They upload the project code, documentation, presentation, and saved example results together. No GitHub upload has been performed for you.

## 1. Install Git and prepare your account

Install Git for Windows from https://git-scm.com/download/win using the default options. Reopen PowerShell after installation. Create or sign in to your account at https://github.com.

```powershell
git --version
```

If PowerShell cannot find `git`, reopen the terminal or check the Git installation.

## 2. Create an empty repository

On GitHub, select **New repository**, name it `q-learning-gridworld`, choose Public or Private, and select **Create repository**. Leave the README, .gitignore, and license options unchecked because this local project already contains files. Copy the repository HTTPS URL.

## 3. Open the project folder

```powershell
cd 'C:\Users\Dell\Documents\Codex\2026-10-28\q-learning-implement-q-learning-to\outputs\q_learning_gridworld'
Get-ChildItem
py gridworld.py
py -m unittest -v
```

You should see `gridworld.py`, `test_gridworld.py`, `README.md`, `docs`, `presentation`, and `results`. Run Git commands in this folder, not the parent Codex workspace.

## 4. Initialize Git and set your commit identity

```powershell
git init
git branch -M main
git config user.name 'YOUR NAME'
git config user.email 'YOUR GITHUB EMAIL'
```

Replace both placeholders. You can use the no-reply email shown in GitHub Settings > Emails. These settings apply only to this repository.

## 5. Review and commit the files

```powershell
git status
git add .
git diff --cached --stat
git commit -m 'Add Q-learning grid world project'
```

The supplied `.gitignore` excludes Python caches and temporary files. Check the staged file list before committing. It should contain your project deliverables and no private credentials.

## 6. Connect GitHub and push

Replace `YOUR_USERNAME` with your GitHub username. If you chose a different repository name, update it too.

```powershell
git remote add origin https://github.com/YOUR_USERNAME/q-learning-gridworld.git
git remote -v
git push -u origin main
```

Complete the browser sign-in if Git Credential Manager prompts you. GitHub account passwords are not accepted for HTTPS Git authentication. If your setup explicitly requests a password/token instead of opening a browser, use a personal access token with access to this repository. Never place a token in a URL, source file, or commit.

## 7. Confirm the upload

Refresh the repository page and verify that the source code and README appear. Check `docs/` for documentation and `presentation/` for the PowerPoint. Open `results/summary.json` to see the example result.

```powershell
git status
```

It should report a clean working tree.

## 8. Push future changes

After editing and testing:

```powershell
git add .
git diff --cached --stat
git commit -m 'Describe the change'
git push
```

## Common problems

| Message | Action |
| --- | --- |
| `remote origin already exists` | Check `git remote -v`. If incorrect, use `git remote set-url origin YOUR_REPOSITORY_URL`. |
| `Repository not found` | Check the URL, signed-in account, and repository permissions. |
| `src refspec main does not match any` | Ensure the first commit succeeded and run `git branch -M main`. |
| Push rejected because the remote contains commits | If the remote is new and contains only setup files, the easiest approach is to clone it into a different folder, copy these project files into that clone, then add, commit, and push. Preserve any existing remote work. |
| Authentication failed | Sign in with the account that owns or can write to the repository. Use Git Credential Manager or an appropriate token. |

## Official references

- GitHub: https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github
- HTTPS authentication: https://docs.github.com/en/get-started/git-basics/about-remote-repositories
