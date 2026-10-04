# PROGRESS

Last updated: 2026-10-04

## Current phase
Phase 5 (AI client + fallback + usage monitoring). Phase 1 still blocked on credits.

## Status at a glance
| Phase | Status |
|---|---|
| 0. Architecture, rubric, specifications, decisions | Done |
| 1. Nebius/Nemotron capability testing | Blocked (waiting on credits) |
| 2. Repository hygiene | Done |
| 3. Neon PostgreSQL + SQLAlchemy + database foundation | Done |
| 4. Login + Demo account | Done |
| 5. AI client + fallback + usage monitoring | Not started |
| 6. First Render deployment + health checks | Not started |
| 7. Freeze rubric/schemas + evaluator testing | Not started |
| 8. Speaking MVP | Not started |
| 9. Speaking follow-up practice | Not started |
| 10. Writing module | Not started |
| 11. Learning agent + dashboard | Not started |
| 12. Reading module | Not started |
| 13. Reading + Speaking integration/polish | Not started |
| 14. Rate limits, usage UI, demo evaluations, disclaimers | Not started |
| 15. README, video, final checklist, submission preparation | Not started |

## Session log

### 2026-10-04 (Phase 4)
**Done**
-phase 4 register, login, logout and demo accout page set up
-created a flask application and added routes such as register, login, logout and demo acc
-Installed flask and flask_login
-app/auth.py: /register, /login, /logout, /demo routes
-app/templates: landing.html, login.html, register.html
-guards.py: to take care of demo account 
-scripts/seed_demo.py: demo account setup  

**In progress**
- None

**Next**
- Phase 5: AI client + fallback + usage monitoring
- Phase 1 when credits arrive
- Offline: normalize, evidence.py, metrics.py

**Blockers**
- Token Factory credits not yet received

### 2026-10-03 (Phase 3)
**Done**
- Phase 2 repository hygiene complete (.env.example, README title)
- Neon Postgres project created; pooled and direct connection strings stored in .env
- Installed sqlalchemy, psycopg[binary], python-dotenv
- app/db.py: make_engine() with pool_pre_ping; pooled URL for the app, direct URL for setup
- app/models.py: users, practice_sessions, attempts, evaluations, usage_events, crisis_events
- scripts/create_tables.py creates the tables; all six confirmed in Neon
- Insert / read / delete test on users passed

**In progress**
- None

**Next**
- Phase 4: Login + Demo account (decide D-05 first)
- Phase 1 when credits arrive
- Offline: normalize, evidence.py, metrics.py

**Blockers**
- Token Factory credits not yet received

### 2026-10-03 (Phases 0-2)
**Done**
- Repo created and cloned
- Docs, README, LICENSE, .gitignore, scripts/ created
- docs/PROJECT_SPEC.md completed

## Open decisions
See the Decision log in docs/PROJECT_SPEC.md (§18).

## Notes for later
- Fill §12 of the spec with model IDs, JSON method, and response times after Phase 1
- Add dates to the §16 timeline
- Add the official rules link to §2

### 2026-10-03
**Done**
- Repo created and cloned
- Docs, README, LICENSE, .gitignore, scripts/ created
- docs/PROJ_SPEC.md completed

**In progress**
- Phase 0 cleanup (README title, .gitignore check, .env.example, virtual environment)

**Next**
- Phase 1: script that calls Nemotron on Token Factory and prints a reply

**Blockers**
- None

## Open decisions
See the Decision log in docs/PROJ_SPEC.md (§18).

## Notes for later
- Fill §12 of the spec with model IDs, JSON method, and response times after Phase 1
- Add dates to the §16 timeline
- Add the official rules link to §2