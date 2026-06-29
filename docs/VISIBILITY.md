# Growing Visibility for Sevendyne HRMS

Practical steps to attract developers, companies, and collaborators on GitHub and beyond.

## On GitHub (highest impact)

### 1. Repository settings
- **About** (gear icon on repo home): add description, website `https://sevendyne.com`, and topics:
  ```
  django, hrms, human-resources, python, docker, open-source, payroll, attendance, leave-management, postgres, celery
  ```
- **Pin the repository** on your [github.com/sevendyne](https://github.com/sevendyne) organization or profile.
- **Enable Discussions** (Settings → General → Features) for Q&A without opening issues.
- **Add a LICENSE file** — already MIT; GitHub will show “MIT license” in the sidebar.

### 2. README polish
- Lead with value: “Docker-ready Django HRMS — free for commercial use (MIT)”
- Badges: build, Python, Django, **license MIT**, **GitHub stars**
- Clear **star CTA** near the top (done in README)
- GIF or screenshot of the dashboard above the fold (add `docs/images/hrms-screenshot.png` later)

### 3. Issues & labels
Create starter issues and label them:
- `good-first-issue` — docs, small UI fixes
- `candidate-challenge` — slightly harder features
- `help wanted` — community contributions welcome

Pin 2–3 `good-first-issue` items so newcomers know where to start.

### 4. GitHub Social preview
- Settings → General → **Social preview** — upload the banner at [`docs/images/github-social-preview.png`](../docs/images/github-social-preview.png) (1280×640).
- Same image works for LinkedIn article covers and Dev.to post headers (crop if needed).

### 5. Releases
Tag versions (`v1.0.0`) with release notes:
```bash
git tag -a v1.0.0 -m "First open-source release — Docker-ready HRMS"
git push origin v1.0.0
```
Releases appear in GitHub search and “Used by” graphs.

---

## Beyond GitHub

| Channel | What to post |
|---------|----------------|
| **LinkedIn** | “We open-sourced our Django HRMS after 1 year of in-house development. Free for commercial use (MIT). Docker one-command setup.” + link + screenshot |
| **Reddit** | r/opensource, r/django, r/selfhosted — follow each sub’s rules; focus on technical value, not sales |
| **Dev.to / Hashnode** | “How we structured a production Django HRMS with Docker” — link repo at the end |
| **Hacker News** | “Show HN: Open-source Django HRMS, Docker-ready, MIT license” — best on weekday mornings US time |
| **Awesome lists** | PR to awesome-django, awesome-selfhosted (if criteria match) |
| **Product Hunt** | Optional launch as “Developer tool / Open source” |

---

## On your website (sevendyne.com)

- Add an **Open Source** nav item linking to the GitHub repo
- Blog post: story of the 3-person team + why you open-sourced it
- Footer badge: “⭐ Star us on GitHub”

---

## In this app (localhost / production)

- Home page already links to GitHub and CONTRIBUTING
- About page links to sevendyne.com
- Consider a small footer line: “HRMS open source under MIT — [Star on GitHub](https://github.com/sevendyne/sevendyne_hrms)”

---

## Metrics to track

- GitHub **stars** and **forks** (weekly)
- **Clone** traffic (Insights → Traffic)
- **Issues/PRs** from external contributors
- Referrers (where traffic comes from)

Consistency beats one-time posts: one LinkedIn update + one technical blog post per month keeps momentum.
