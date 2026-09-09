# DevOps Student Engineering Portal

## Project Description
The DevOps Student Engineering Portal is a simple, static student-information web application developed as part of an academic Git collaboration exercise. The project demonstrates real-world collaborative version control workflows among three developers, including branch management, independent feature development, pull request reviews, intentional merge conflicts, local conflict resolution, and final integration.

## Team Members
- **Student 1 (Base Developer / Team Lead / Integrator)**: Vishwas Vashishtha (`vishwas.vashishtha@mca.christuniversity.in`)
- **Student 2 (UI & Contact Developer)**: Anushka (`lavianu2004@gmail.com`)
- **Student 3 (JavaScript & Feature Developer)**: Varun Singh 2547254 (`varunsinghbot@gmail.com`)

## Technologies Used
- HTML5
- CSS3
- JavaScript
- Git
- GitHub

## Application Features
- **Student Information Record**: Displays student name (`Alex Morgan`), register number (`2447101`), and academic programme (`Master of Computer Applications (DevOps)`).
- **Responsive UI Foundation**: Modern card layout, status badges, avatar initials, and fully responsive CSS grid styling across desktop and mobile screens.
- **Interactive Details Toggle**: Client-side JavaScript interactivity toggling additional academic details (Semester, Section, University) with dynamic button label and ARIA attribute updates.
- **Contact Information Section**: Dedicated subsection with email address (`alex.morgan@university.edu`) and phone number (`+1 (555) 019-2834`).
- **Integrated Application Heading**: Final integrated title `Student Management System – MCA`.

## Git Branching Strategy
The repository maintains an integrated `main` branch along with five dedicated feature branches:
- `main`: Production/integration branch hosting stable releases.
- `feature/ui`: Independent branch for UI enhancements by Student 2.
- `feature/javascript`: Independent branch for interactive client-side logic by Student 3.
- `feature/contact`: Independent branch for contact information section by Student 2.
- `feature/student-name`: Independent branch for application heading modification by Student 2.
- `feature/app-title`: Independent branch for application heading modification by Student 3.

Feature branches were created independently from `main` and integrated exclusively through Pull Requests and code review.

## Pull Requests
All features were integrated into `main` via documented GitHub Pull Requests:
- **PR #1**: `feature/ui` → `main`
  - Author: Anushka (Student 2)
  - Commit: `b5474d0` ("Improve student portal UI")
  - Merge Commit: `e8fad58`
- **PR #2**: `feature/javascript` → `main`
  - Author: Varun Singh (Student 3)
  - Commit: `a1e8a6a` ("Add student details interaction")
  - Merge Commit: `9b86ef3`
- **PR #3**: `feature/contact` → `main`
  - Author: Anushka (Student 2)
  - Commit: `0f6b4f4` ("Add contact information")
  - Merge Commit: `8179e71`
- **PR #4**: `feature/student-name` → `main`
  - Author: Anushka (Student 2)
  - Commit: `727a296` ("Update application heading")
  - Merge Commit: `f67b3f4`
- **PR #5**: `feature/app-title` → `main`
  - Author: Varun Singh (Student 3)
  - Commit: `ece8acd` ("Update application title"), resolved via `3f5aa95` ("Resolve merge conflict in application title")
  - Merge Commit: `0dca45e`

## Commit Ownership
Each commit reflects individual author ownership and specific project milestones:
- **Student 1 (Vishwas Vashishtha)**:
  - `fe3ba34`: Initial student engineering portal (Project baseline)
  - `e8fad58`: Merge pull request #1 from Vishwaxs/feature/ui
  - `9b86ef3`: Merge pull request #2 from Vishwaxs/feature/javascript
  - `8179e71`: Merge pull request #3 from Vishwaxs/feature/contact
  - `f67b3f4`: Merge pull request #4 from Vishwaxs/feature/student-name
  - `0dca45e`: Merge pull request #5 from Vishwaxs/feature/app-title
  - Final integration commit: Document collaborative Git workflow
- **Student 2 (Anushka)**:
  - `b5474d0`: Improve student portal UI
  - `0f6b4f4`: Add contact information
  - `727a296`: Update application heading
- **Student 3 (Varun Singh)**:
  - `a1e8a6a`: Add student details interaction
  - `ece8acd`: Update application title
  - `3f5aa95`: Resolve merge conflict in application title

## Merge Conflict

### Common Baseline
Commit `8179e71` (`Merge pull request #3 from Vishwaxs/feature/contact`) served as the common baseline from which both conflicting branches were created.

### Cause
Student 2 and Student 3 independently modified the exact same logical line in `index.html` starting from commit `8179e71`:
- Original baseline heading at `8179e71`:
  ```html
  <h1 class="title">DevOps Student Engineering Portal</h1>
  ```

### Student 2 Version (`feature/student-name`)
In commit `727a296`:
```html
<h1>Student Management System</h1>
```

### Student 3 Version (`feature/app-title`)
In commit `ece8acd`:
```html
<h1 class="title">MCA Student Information Portal</h1>
```

### Why Git Reported Conflict
Student 2's branch (`feature/student-name`) was reviewed and merged into `main` first via PR #4 (`f67b3f4`). When Student 3 attempted to merge or integrate `main` into `feature/app-title`, Git detected that both branches made conflicting modifications to the identical line in `index.html`. Because Git cannot automatically determine business priority between competing edits, an automatic merge was halted and conflict markers were inserted.

### Resolution
Student 3 resolved the conflict locally by pulling the updated `main` branch into `feature/app-title`:
1. Switched to `feature/app-title` and executed `git merge main`.
2. Inspected the conflict markers (`<<<<<<< HEAD`, `=======`, `>>>>>>> main`).
3. Manually resolved the conflict by synthesizing the two titles into a single unified heading:
   ```html
   <h1 class="title">Student Management System – MCA</h1>
   ```
4. Removed all conflict markers, verified application syntax, and committed the resolution with message `Resolve merge conflict in application title` (commit `3f5aa95`).
5. Pushed `feature/app-title` to GitHub and completed PR #5.

### Final Result
```html
<h1 class="title">Student Management System – MCA</h1>
```

## How To Run
The portal is a lightweight static web application with no build tools or package managers required.
1. Clone the repository:
   ```bash
   git clone https://github.com/Vishwaxs/devops-student-engineering-portal.git
   cd devops-student-engineering-portal
   ```
2. Open `index.html` directly in any modern web browser:
   - Double-click `index.html`, OR
   - Run a simple local HTTP server:
     ```bash
     python -m http.server 8080
     ```
   - Navigate to `http://localhost:8080/index.html`.

## Git History
To inspect the complete branch divergence, merge history, and commit graph:
```bash
git log --oneline --graph --decorate --all
```

## Collaboration Workflow
1. `main` branch serves as the central stable branch.
2. Each developer creates an isolated feature branch (`git checkout -b feature/<name> main`).
3. Developer implements changes and makes meaningful, atomic commits under their own identity.
4. Feature branch is pushed to remote repository (`git push -u origin feature/<name>`).
5. A Pull Request is opened against `main`.
6. Team Lead (Student 1) reviews code, verifies tests, and approves/merges the PR.
7. Local branches sync with updated `main` (`git pull origin main`).

## Conflict Workflow
1. Both developers branch from the same common baseline (`8179e71`).
2. Both developers independently modify the same line of code.
3. First feature branch (`feature/student-name`) is merged into `main`.
4. Second feature branch (`feature/app-title`) encounters a merge conflict against the updated `main`.
5. Second developer resolves the conflict locally:
   - Synchronizes `main`.
   - Merges `main` into their feature branch (`git merge main`).
   - Resolves conflicting lines and cleans up conflict markers.
   - Tests and commits the resolution (`Resolve merge conflict in application title`).
6. Second developer pushes updated branch and completes the Pull Request merge.
