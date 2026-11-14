# What do Google Play and the Apple App Store require for a free hobby game?

Type: research
Status: resolved
Blocked by: none

## Question

What must Project Wildling satisfy to be published free on Google Play and the Apple App Store: developer account costs, target API level / minimum OS rules, content rating questionnaires (IARC, Apple age rating), privacy policy & data-safety forms for an offline game, IP / impersonation policies relevant to a genre game, testing requirements (e.g. Play's closed-testing requirement for new personal accounts), and anything that constrains the engine or build pipeline.

## Answer

Findings: branch `research/store-requirements`, file `research/store-requirements.md` (40 official Google/Apple sources).

- **Costs:** Play US$25 once; Apple US$99/yr (no individual waiver). Both show the developer's legal name publicly. iOS builds need a Mac + current Xcode.
- **Android:** new apps target API 36; AAB uploads; 16 KB page-size support required for updates from 2027-02-01 (constrains engine native libs).
- **iOS:** Xcode 26 now, Xcode 27 / iOS 27 SDK from Apr 2027; practical minimum iOS 15.
- **Play testing gate (new personal account):** closed test with ≥12 testers opted in for 14 consecutive days before production access. Budget ~3–4 weeks and recruit testers early. TestFlight: first external build needs review; builds expire after 90 days.
- **Privacy:** a privacy-policy URL is mandatory on both stores even with zero data collection; "no data collected" is possible only if the engine ships no analytics/crash SDKs.
- **Ratings:** IARC + Apple questionnaires mandatory; fantasy violence → Apple 9+ (infrequent) / 13+ (frequent).
- **Families risk:** Play may treat a cute-creature game with youthful art as child-directed, which would require Families Policy compliance. Store art/listing must be deliberate.
- **IP:** copycat/impersonation bans make the original-IP rule a store requirement, not just a preference.
- **EU trader status:** must be declared on both stores; a free hobby game points to non-trader (the human's call).
- **Unverified:** whether the Play testing gate applies per app or per account; exact rating; whether Xcode Cloud can be used with no Mac at all.
