# What exactly do Google Play and Apple require of Mendvale's accounts and rating?

Type: research
Status: resolved
Blocked by: none

## Question

Settle the store facts `spec.md` §7 lists as unverified (see the answers to tickets 04, "What do Google Play and the Apple App Store require for a free hobby game?", and 17, "How are Mendvale's Android and iOS builds made and released?"):
- Is Google Play's 12-tester, 14-day closed-testing gate **per app or per new personal account**? Does it apply again to a second app, and is the internal track exempt?
- **Age ratings:** what the IARC and Apple age-rating questionnaires give a game with cartoon creature battles, no blood, no purchases and no chat. Does cute art trigger the Families policy or Apple's Kids category by default, and how is that avoided?
- **iOS cloud signing:** does `xcodebuild` cloud signing with an App Store Connect API key need an **Admin**-role key, or is App Manager or Developer enough?
- **Trader status:** what declaring as a non-trader means for a free hobby app in the EU (DSA), and what a trader must publish.
- **Privacy policy hosting:** do GitHub Pages or a repo file URL satisfy both stores?

## Answer

Findings: branch `research/store-facts`, file `research/store-facts.md` (first-party Google Play, Apple, IARC and DSA pages, checked 2026-11-14). The file also corrects `research/store-requirements.md`: one Play link had moved, IARC is confirmed free, and the expected Apple rating is now 13+, not "9+ or 13+".

1. **Play's 12-tester, 14-day gate:** it **applies to Mendvale**, because it covers personal accounts created after 2023-11-13 (high certainty). Google words it per app, but no page says whether a second app must pass again, so **plan as if every app must** (medium). The internal track has no gate, but internal testers don't count; only a closed test does (high).
2. **IARC rating:** the questions aren't published, so this comes from each body's definitions. Likely ESRB E or E10+, PEGI 7, USK 6, ClassInd 10 ("bloodless fights") and IARC Generic 7+ (low to medium). Rating is free (high).
3. **Apple age rating:** "Infrequent" cartoon violence gives 9+, "Frequent" gives 13+. Battles are the core loop, so **13+ is the honest answer** (high on the mapping, medium on what review accepts).
4. **Families and Kids:** cute art doesn't switch either on (high).
   - **Play:** Families applies only if an under-13 audience is chosen, but Play may reject a listing whose graphics look aimed at children. **Declare 13+ age groups only** and keep store art from reading as a kids' app.
   - **Apple:** Kids is opt-in, and isn't offered at 13+.
5. **iOS cloud signing:** use an **Admin**-role team API key (high). Individual keys can't use the provisioning endpoints. App Manager and Developer roles need extra access Apple documents only for people (medium).
6. **Trader status:** both stores require the declaration and say a hobbyist is unlikely to be a trader. **Declare non-trader on both** (high; the legal call is the human's).
   - **As a non-trader:** nothing extra is published, but EU users (and UK users on Play) are told consumer-protection rights don't apply. A false claim can mean removal worldwide.
   - **A trader** would have to publish a verified address (a P.O. box on Apple), phone and email.
7. **Privacy policy hosting:** **GitHub Pages** meets every test both stores state (high). A github.com repo file URL passes Play's tests while the repo is public, but isn't a plain webpage (medium). Apple's Support URL must lead to contact details, so **put a contact page next to the policy**.

**Consequences:**
- Ticket 17's iOS signing uses an Admin-role key.
- Ticket 34, "How is Mendvale listed on the stores, and who tests it?", is now unblocked. It should assume a 13+ Apple rating, 13+ Play age groups, a non-trader declaration, GitHub Pages hosting, and a closed test for every app.
