# Publishing the two repositories

The local workspace contains two independent repositories. Publish both under
the same GitHub owner:

- `sgd3dgs-app` — product and coordination;
- `sgd3dgs-research` — experimental methods and artifacts.

## 1. Verify repository ownership metadata

The repository URLs are configured for the GitHub account `sapankowski`.
From the workspace root, verify that no stale owner placeholder remains:

```bash
rg --hidden -n 'github.com/OWNER|github.com:sapankowski' \
  sgd3dgs-app sgd3dgs-research -g '!.git/**'
```

The command should report only `sapankowski` URLs. If ownership or repository
names change later, update URLs, schema IDs, citation metadata, issue forms, and
cross-repository links consistently.

## 2. Create owner-authored initial commits

Configure your identity separately in both repositories if needed:

```bash
git config user.name "Your Name"
git config user.email "your-github-email@example.com"
```

Then, in `sgd3dgs-app`:

```bash
git add --all
git status
git commit -m "chore: initialize SGD3DGS application"
```

In `sgd3dgs-research`:

```bash
git add --all
git status
git commit -m "chore: initialize SGD3DGS research workspace"
```

## 3. Create and push empty GitHub repositories

Do not ask GitHub to add another README, license, or `.gitignore`.

```bash
# from sgd3dgs-app
git remote add origin git@github.com:sapankowski/sgd3dgs-app.git
git push -u origin main

# from sgd3dgs-research
git remote add origin git@github.com:sapankowski/sgd3dgs-research.git
git push -u origin main
```

GitHub CLI can create each repository instead:

```bash
gh repo create sapankowski/sgd3dgs-app --source=. --public --remote=origin --push
gh repo create sapankowski/sgd3dgs-research --source=. --public --remote=origin --push
```

Run the second command from the research directory. Choose private visibility if
the team is not ready to publish discussions/code; data and weights stay outside
Git either way.

## 4. Configure both repositories

For each repository:

1. invite the five collaborators with write access;
2. protect `main` with one approving review;
3. require Actions checks after their first successful run;
4. disallow force pushes and branch deletion;
5. enable squash merging and automatic branch deletion;
6. enable secret scanning and dependency alerts where available;
7. create `task` and `bug` labels; add `experiment` in research;
8. replace the temporary security-contact language in `SECURITY.md`.

## 5. One coordination board

Create one GitHub Project owned by the app repository or organization. Fields:

- Status: Backlog, Ready, In progress, In review, Done;
- Repository: App, Research;
- Workstream: Product, Scene understanding, Research quality;
- Week: 1–10;
- Owner, reviewer, and evidence link.

Populate Week 1 only. Later weeks remain in the plan until the prior Tuesday
meeting confirms scope. Cross-repository outcomes use linked issues and one
board item as the status authority.

## 6. Verify clean clones

Clone both into a new parent folder, preserving sibling names. In app:

```bash
./scripts/check_system.sh
make core-sync
make verify
./scripts/verify_repository.sh
```

In research:

```bash
./scripts/check_system.sh
make sync
make check
./scripts/verify_repository.sh
```
