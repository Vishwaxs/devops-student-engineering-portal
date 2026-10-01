# Lab 2: CI Workflow using GitHub Actions

## Objective
Design and implement a basic CI workflow triggered by commits using GitHub Actions.

## Implementation

### CI Workflow: `.github/workflows/ci.yml`

The CI pipeline validates the DevOps Student Engineering Portal on every push and pull request.

### Workflow Triggers
- **Push**: Triggers on `main` and all `feature/**` branches
- **Pull Request**: Triggers when PRs target `main`

### Validation Steps
1. **Checkout** — Clone the repository using `actions/checkout@v4`
2. **Node.js Setup** — Install Node.js 20 for linting tools
3. **Dependency Caching** — Cache npm packages using `actions/cache@v4` *(Self-Learning)*
4. **HTML Validation** — Lint HTML using `htmlhint`
5. **CSS Validation** — Lint CSS using `csslint`
6. **JavaScript Validation** — Lint JS using `jshint`
7. **Structure Verification** — Ensure required project files exist
8. **Job Summary** — Generate a GitHub Actions Job Summary *(Self-Learning)*

### Self-Learning Additions
1. **Dependency Caching** — `actions/cache@v4` caches npm packages to speed up subsequent runs
2. **Job Summary** — Uses `$GITHUB_STEP_SUMMARY` to generate a formatted summary table

## Branch
- `feature/lab-2-ci`

## How to Verify
1. Push to `feature/lab-2-ci`
2. Navigate to GitHub → Actions tab
3. Observe the "CI - Student Portal Validation" workflow
4. Verify green checkmark on successful run
