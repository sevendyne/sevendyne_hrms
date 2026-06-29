# Good first issues (maintainer checklist)

Create these from GitHub **Issues → New issue** and label `good-first-issue` for newcomers.

## Suggested starter issues

### 1. Add README screenshot
**Title:** `docs: add dashboard screenshot to README`  
**Body:** Capture admin dashboard after `docker compose up`, save to `docs/images/dashboard.png`, add to README below hero badges.  
**Labels:** `good-first-issue`, `documentation`

### 2. Export attendance CSV
**Title:** `feat: export monthly attendance register as CSV`  
**Body:** Add a download action on the attendance list view in `apps/employee`. Include pytest for the export view.  
**Labels:** `candidate-challenge`, `enhancement`, `attendance`

### 3. API health check endpoint
**Title:** `feat: add /health/ endpoint for Docker orchestration`  
**Body:** Simple view returning 200 + DB connectivity status. Document in `docs/DOCKER.md`.  
**Labels:** `good-first-issue`, `enhancement`

### 4. Login page link to GitHub
**Title:** `ui: add GitHub star link on login page footer`  
**Body:** Small footer link to repo + MIT license note.  
**Labels:** `good-first-issue`, `documentation`

### 5. pytest coverage for seed_demo_data
**Title:** `test: add tests for seed_demo_data management command`  
**Body:** Verify admin, client, and employee users are created.  
**Labels:** `good-first-issue`, `tests`

---

After creating, **pin** 2–3 issues on the Issues page (pin icon) so they appear at the top for visitors.
