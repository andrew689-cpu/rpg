# Store requirements: Google Play and Apple App Store for a free hobby game

Ticket: [04-store-requirements](../.scratch/project-wildling/issues/04-store-requirements.md)
Researched: 2026-11-13. Sources: official Google (support.google.com, developer.android.com, android-developers.googleblog.com) and Apple (developer.apple.com) pages only. Each claim cites its source as `[n]`, and the numbered list is at the bottom.

Assumptions: Project Wildling is free, has no ads, no IAP, no accounts, no network calls and no analytics. It is published by one individual on a personal Play account and an individual Apple account.

---

## TL;DR

| | Google Play | Apple App Store |
|---|---|---|
| Account cost | US$25 one-time [1] | US$99 per membership year; individuals cannot get a fee waiver [16][17] |
| Account type | Personal [2] | Individual; your legal name is shown as the seller [18] |
| Build target today | targetSdk **36** (Android 16) for new apps and updates since 2026-08-31 [4] | Build with **Xcode 26+ / iOS 26 SDK** (since 2026-04-28) [19]. **Xcode 27 / iOS 27 SDK from April 2027** [20] |
| Minimum OS | No Play-imposed minSdk found; the engine and libraries set it | Must target iOS 13+ [19][21], but Xcode 26/27 only offer deployment targets from **iOS 15** [22] |
| Package format | **AAB** required for new apps, with Play-managed signing [6] | Upload through Xcode / App Store Connect; Xcode runs on macOS only [22] |
| Native-code gotcha | **16 KB page size** support required. Updates without it are blocked from 2027-02-01 [5] | Privacy manifest + signature required for listed SDKs (e.g. UnityFramework, Flutter) [27] |
| Content rating | IARC questionnaire in Play Console; mandatory [9] | Age-rating questionnaire in App Store Connect; mandatory, and new questions are being added [23][24] |
| Privacy policy | Required, even with zero data collection [7] | Required for all apps [25][26] |
| Privacy form | Data safety form required; "no data collected" is allowed [8] | App Privacy: "No, we do not collect data from this app" [26] |
| EU DSA | Declare trader/non-trader; existing accounts by **2027-02-01** [14] | Declare trader/non-trader, even if not distributing in the EU [15] |
| Pre-launch testing | **New personal accounts: closed test, 12+ testers opted in for 14 continuous days**, then apply for production (review usually ≤7 days) [3] | TestFlight: 100 internal / 10,000 external testers; builds expire after 90 days; the first external build needs App Review [28][29] |

**Out-of-pocket minimum:** US$25 + US$99/yr, plus access to a Mac running macOS Tahoe 26.x (Xcode 27 needs 26.6+) [22].

---

## Google Play checklist

### Account
- [ ] Pay the **US$25 one-time** registration fee. Prepaid cards are not accepted. You may be asked for a government ID and a credit card in your legal name, and the fee is **not refunded** if verification fails [1].
- [ ] Choose a **personal** account ("students, hobbyists, or amateur developers"). Organization accounts need a D-U-N-S number [2].
- [ ] Personal accounts must verify access to an Android device through the Play Console mobile app [1].
- [ ] Verify your contact email, contact phone and developer email by one-time password. Verify your legal name and address before publishing [10].
- [ ] **Public exposure:** Google Play shows your **legal name, country and developer email**. Your full address is shown only if you monetize, and your phone number is not shown (some regions differ) [10]. If you declare as a trader, your phone and address are shown from 2027-03-01 [14].
- [ ] **Trader status (EU DSA / UK):** every active account must declare. New accounts declare at creation, and existing ones by **2027-02-01**. A trader is someone acting for "trade, business, craft or profession". Google says a personal hobby is unlikely to qualify, and its indicators are profit motive, transaction volume, running it as a business, or having a D-U-N-S number. Misdeclaring can lead to global suspension [14]. A free, no-ads hobby game points to **non-trader**, but that is your declaration to make.
- [ ] Android developer verification: Google Play "automatically registers 99% of apps". Enforcement began 2026-09-30 in Brazil, Indonesia, Singapore and Thailand, and goes global in 2027 [13]. Play-only apps should need no extra action, but check Play Console.

### Build and technical
- [ ] **targetSdkVersion 36** (Android 16). It has been required for new apps and updates since **2026-08-31**, and the extension window ended **2026-11-01** [4].
- [ ] Publish as an **Android App Bundle (AAB)**, required for new apps since August 2021. Google Play generates and signs the APKs. The compressed download must be ≤ 4 GB, and AAB does not support `.obb` files. Use Play Asset Delivery for large assets [6].
- [ ] **16 KB page size:** apps targeting API 35+ must support 16 KB pages on 64-bit devices. From **2027-02-01**, updates without it can't be released. This affects any app with native `.so` code, which covers almost every game engine. AGP ≥ 8.5.1 + NDK ≥ r28 are compatible by default. Unity and Unreal have their own guides. Check with APK Analyzer or `zipalign -c -P 16` [5].
- [ ] **Technical quality thresholds from February 2027:** games must stay under memory "bad behavior" thresholds (Anon RSS + Swap, p90; e.g. 2.25 GB foreground on 4 GB devices). The ≥ 25% DEX optimization rule applies only to games with > 50 MB of DEX. Missing them "can affect an app's visibility and publishing capabilities" [12]. A small pixel-art game should pass easily, but keep the targets in mind.
- [ ] No minSdk floor was found in Play policy. The chosen engine sets it (feeds [ticket 01](../.scratch/project-wildling/issues/01-engine-choice.md)).

### App content declarations (Play Console → App content)
- [ ] **Privacy policy URL**, linked both on the store listing **and inside the app**, "even if your app doesn't access personal or sensitive user data" [7].
- [ ] **Data safety form** is mandatory. You may declare that no data is collected or shared. "Collection" means data transmitted off the device, so data processed only on the device is not disclosed. **Data sent by third-party SDKs counts** as your collection [8].
- [ ] **Content rating (IARC questionnaire)** is mandatory. Unrated apps are removed, and you must resubmit if content changes [9].
- [ ] **Target audience and content:** declare target ages and whether the app has ads. A privacy policy is needed before this section can be completed [11].
  - **Gotcha for a cute creature game:** if the game isn't designed for under-13s "but your listing contains marketing elements that suggest otherwise (such as youthful animation or young characters in the graphic assets), Google Play may reject your app." The options are to remove those elements or target under-13s and comply with the Families Policy [11].
  - If children are a target audience, the **Families Policy** applies: an accurate privacy policy, only Families Self-Certified ad SDKs (we have no ads), no SDKs that aren't approved for child-directed services, and accurate declarations [30].

### Testing gate (new personal accounts)
- [ ] Personal accounts created after **2023-11-13** must run a **closed test with ≥ 12 testers opted in continuously for ≥ 14 days** before applying for production. Testers who opt out reset their count, so the 14 days must be consecutive [3].
- [ ] Then use Dashboard → "Apply for production". The form asks about the closed test, the app's audience and value, first-year install estimate, and changes made after feedback. Review "usually takes seven days or less" and may ask for more testing [3].
- [ ] Tracks: internal (≤ 100 testers, may skip policy review), closed (email lists up to 2,000 each, or Google Groups), open [31].
- The page doesn't say whether the gate applies per app or only to the first app [3].

---

## Apple App Store checklist

### Account
- [ ] **Apple Developer Program: US$99 per membership year** [16]. Fee waivers are only for nonprofits, schools and governments, and explicitly "Not be an individual" [17].
- [ ] Enroll as an **individual**. You need an Apple Account with 2FA, must be of legal age (or a guardian enrolls), and must use your **legal name**. **Your name is displayed as the seller** [18].
- [ ] A free Apple Account can sideload to your own devices with a "Personal Team", but apps expire after 7 days and you are limited to 3 devices. Membership is needed for App Store Connect and distribution [32].
- [ ] **DSA trader status:** declare in App Store Connect → Business → Agreements → Compliance. **Non-trader** needs no contact info. A trader must publish address, phone and email on EU product pages. You must declare "even if you don't distribute apps in the EU" [15].

### Build and technical
- [ ] **Xcode 26+ with the iOS 26 SDK** has been required for uploads since **2026-04-28** [19][33].
- [ ] **From April 2027: iOS 27 SDK (Xcode 27) required** [20]. Plan to build with Xcode 27.x, which is available now (27.2 stable, needs macOS Tahoe 26.6+) [22].
- [ ] **Minimum OS:** uploads must target iOS 13 or later (since 2026-09-09) [21]. Xcode 26/27 support deployment targets from **iOS 15** only, so iOS 15 is the practical floor [22].
- [ ] **Xcode is macOS-only:** Apple lists only macOS hosts and distributes Xcode through the Mac App Store [22]. **Xcode Cloud** (25 compute hours/month included, more sold from US$49.99/mo) runs builds in the cloud but is set up "in Xcode", so you still need a Mac at least for setup [34].
- [ ] **Third-party SDK privacy manifests and signatures** are required when your submission includes a listed SDK. The list includes **UnityFramework**, **Flutter** and **hermes**. Any SDK that repackages a listed one also counts [27].
- [ ] **Required-reason APIs:** since 2024-05-01, uploads must declare approved reasons for listed APIs, including ones used inside third-party SDKs [19]. Engines that read file timestamps, disk space or UserDefaults trigger this.
- [ ] **Screenshots:** from April 2027, all submissions need iPhone Duo screenshots [35].

### App Store Connect metadata
- [ ] **Privacy policy URL** is required for all apps. Also link it inside the app "in an easily accessible manner" [25][26].
- [ ] **App Privacy ("nutrition label"):** choose "No, we do not collect data from this app" and publish [26]. "Collect" means data sent off the device and kept longer than needed to serve the request, so on-device-only data is not disclosed. **Third-party SDK behaviour counts** [36].
- [ ] **Age rating questionnaire** is mandatory. Unrated apps can't be published [23]. The ratings are 4+, 9+, 13+, 16+ and 18+. **"Infrequent cartoon or fantasy violence" gives 9+, and "frequent" gives 13+** [23]. A turn-based creature battler will likely land at 9+ or 13+ depending on how you answer frequency.
  - The questionnaire keeps growing: social-media questions have been required since September 2026 [20]. "Shared Location" and "Dating and Relationships" arrive on **2026-11-16** and must be answered by **2027-01-12** [24]. Answer "none" for each, but answer them.
- [ ] **App name ≤ 30 characters.** Don't put trademarked terms or popular app names in metadata or keywords [25] (feeds [ticket 06](../.scratch/project-wildling/issues/06-naming-and-branding.md)).
- [ ] Submit a complete build. Placeholder text and broken URLs are rejected under 2.1 [25].

### TestFlight
- [ ] Up to **100 internal** testers (App Store Connect users) and **10,000 external** testers. A public invite link is available [28][29].
- [ ] **The first build added to an external group goes to App Review.** Later builds may not need a full review [29].
- [ ] **Builds expire after 90 days** [29].
- [ ] A beta description and beta review info are required for external testing [28].
- There is no Apple equivalent of Play's "N testers for N days" gate (nothing like it was found on the TestFlight pages).

---

## IP, impersonation and spam rules that matter for a genre game

Genre mechanics (catching, types, parties) are not restricted by either store. What is restricted is **resemblance to a specific franchise or app**:

- **Apple 4.1 Copycats:** "Don't simply copy the latest popular app ... or make some minor changes to another app's name or UI." 4.1(b): impersonating other apps can mean **removal from the Developer Program**. 4.1(c): you can't use another developer's icon, brand or product name in your icon or name [25].
- **Apple 5.2.1:** don't use third-party trademarks, copyrighted works or "copycat representations, names, or metadata" without permission [25].
- **Apple 4.3 Spam:** no apps "indistinguishable from what's already widely available", and no "opportunistically creating variants of existing app categories or popular apps" [25]. An original setting, art and creature roster is the defence.
- **Apple 4.2 Minimum functionality:** the app must provide "lasting entertainment value" [25]. A full RPG easily meets this.
- **Play Impersonation:** "Don't imply that your app is related to or authorized by someone that it isn't." Violations include titles and icons "so similar to existing products ... that users may be misled", with the example of copying a TV show's characters [37].
- **Play Intellectual Property:** violations include "fan art indistinguishable from the original work" and trademark use "likely to cause confusion". Google's advice: "the safest approach is to create something that's original" [38].
- **Play Spam / Minimum functionality:** no apps that "merely provide the same experience as other apps already on Google Play", and no apps with very limited content [39].

What this means for the design: no Pokémon names, silhouettes, type icons, UI layouts or ball-like capture items that copy the originals, and no "like Pokémon" text in store keywords or descriptions. This matches the map's Out-of-scope rule.

---

## Timeline gotchas (as of 2026-11-13)

| Date | What | Store |
|---|---|---|
| Passed (2026-08-31) | targetSdk 36 required for new apps and updates [4] | Play |
| Passed (2026-11-01) | Last target-API extension expired [4] | Play |
| Passed (2026-09-09) | Uploads must target iOS 13+ [21] | Apple |
| **2026-11-16** | New age-rating descriptors in the questionnaire [24] | Apple |
| **2027-01-12** | Answers to the new descriptors due for all apps [24] | Apple |
| **2027-02-01** | Trader-status declaration deadline for existing accounts [14][40] | Play |
| **2027-02-01** | Updates without 16 KB support are blocked [5] | Play |
| **February 2027** | Memory / DEX quality thresholds enforced [12] | Play |
| 2027-03-01 | Play becomes an "online marketplace" in the EEA/UK, and trader details are shown [14] | Play |
| **April 2027** | iOS 27 SDK (Xcode 27) required for uploads, and iPhone Duo screenshots required [20][35] | Apple |
| 2027 | Android developer verification goes global [13] | Android |
| Expected ~Aug 2027 (not yet announced) | Google Play has raised the target API by one level each August (2026 → API 36). Plan for API 37 | Play (pattern, not policy) |
| Expected spring 2028 | Apple has required the new SDK each spring (Apr 2026 → 26, Apr 2027 → 27). Plan for Xcode 28 | Apple (pattern, not policy) |

**Lead time before launch:**
- Play: create the account → internal test → closed test with **≥ 12 testers for 14 continuous days** → apply for production (usually ≤ 7 days) → production review. Budget **at least ~3–4 weeks**, and recruit the 12 testers early [3].
- Apple: enrollment approval, then TestFlight external review of the first build, then App Review.

---

## Constraints on engine and build pipeline (input to tickets 01 and 09)

1. **You need a Mac.** Xcode runs on macOS only, and current Xcode 27 needs macOS Tahoe 26.6+ [22]. Xcode Cloud reduces local build load but is configured from Xcode [34]. Every engine's iOS export ends in an Xcode build, so this applies whichever engine is chosen.
2. **Native engines must produce 16 KB-aligned `.so` files** (NDK r28+ or linker flags, AGP ≥ 8.5.1) by 2027-02-01 [5]. Check the chosen engine version's 16 KB support explicitly. Google publishes guides for Unity and Unreal only [5].
3. **The Android export must produce an AAB** with targetSdk 36 today [4][6], and the engine must be able to move to API 37 when Google raises the floor.
4. **The iOS export must build with the current Xcode SDK** (26 now, 27 by April 2027) [19][20]. Engines that lag Xcode releases are a risk.
5. **Bundled SDKs determine the privacy answers.** Any analytics or crash SDK an engine adds by default turns "no data collected" into a disclosure on both stores [8][36]. Check the engine's default telemetry and strip it. Listed SDKs (UnityFramework, Flutter) need privacy manifests and signatures [27].
6. **Keep the game fully offline** so the privacy policy can be a short "we collect nothing" page. Both stores still require that URL [7][26]. Hosting a static page (e.g. GitHub Pages) is enough. Neither store specifies the host.
7. **Stay well under the memory thresholds** (p90 2.25 GB foreground on 4 GB devices for games) [12]. This is easy for 2D pixel art, but large uncompressed texture atlases are what to watch.

---

## Open questions / not verified

- Whether Play's closed-testing gate applies to every new app on a personal account or only the first. The help page doesn't say [3].
- The exact IARC rating Project Wildling will get. It depends on questionnaire answers, and Google's page doesn't list the authorities [9].
- Whether the IARC questionnaire costs anything. Not stated, though Play Console offers it as part of the normal flow [9].
- Xcode Cloud's supported source hosts and whether it can be used entirely without a Mac. Apple's page says setup happens "in Xcode" [34].
- Future target-API and Xcode deadlines beyond those listed are extrapolated from past patterns, not announced.

---

## Sources

1. Google Play: Get started with Play Console (registration fee, ID, device verification). https://support.google.com/googleplay/android-developer/answer/6112435
2. Google Play: Choose a developer account type. https://support.google.com/googleplay/android-developer/answer/13634885
3. Google Play: App testing requirements for new personal developer accounts. https://support.google.com/googleplay/android-developer/answer/14151465
4. Android Developers: Meet Google Play's target API level requirement. https://developer.android.com/google/play/requirements/target-sdk
5. Android Developers: Support 16 KB page sizes. https://developer.android.com/guide/practices/page-sizes
6. Android Developers: About Android App Bundles. https://developer.android.com/guide/app-bundle
7. Google Play: User Data policy (privacy policy requirement). https://support.google.com/googleplay/android-developer/answer/9859455
8. Google Play: Provide information for Google Play's Data safety section. https://support.google.com/googleplay/android-developer/answer/10787469
9. Google Play: Content ratings. https://support.google.com/googleplay/android-developer/answer/9898843
10. Google Play: Required information to create a Play Console developer account. https://support.google.com/googleplay/android-developer/answer/13628312
11. Google Play: Target audience and app content. https://support.google.com/googleplay/android-developer/answer/9867159
12. Google Play: Play Console technical quality requirements. https://support.google.com/googleplay/android-developer/answer/17492799?hl=en
13. Android Developers: Android developer verification. https://developer.android.com/developer-verification
14. Google Play: Trader status declaration. https://support.google.com/googleplay/android-developer/answer/17594752?hl=en
15. Apple: Manage EU Digital Services Act trader requirements. https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements
16. Apple: Apple Developer Program, what's included (US$99/yr). https://developer.apple.com/programs/whats-included/
17. Apple: Fee waivers. https://developer.apple.com/help/account/membership/fee-waivers/
18. Apple: Enrollment. https://developer.apple.com/programs/enroll/
19. Apple: Upcoming requirements. https://developer.apple.com/news/upcoming-requirements/
20. Apple News (2026-09-09): App Store submissions now open for the latest OS releases. https://developer.apple.com/news/?id=k1mtkt1k
21. Apple: iOS and iPadOS minimum system requirements. https://developer.apple.com/news/upcoming-requirements/?id=0992026a
22. Apple: Xcode system requirements. https://developer.apple.com/xcode/system-requirements/
23. Apple: Age ratings values and definitions. https://developer.apple.com/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions/
24. Apple News (2026-11-02): Upcoming: New age rating content descriptors in App Store Connect. https://developer.apple.com/news/?id=yxkh08us
25. Apple: App Review Guidelines (2.1, 2.3.7, 4.1, 4.2, 4.3, 5.1.1, 5.2.1). https://developer.apple.com/app-store/review/guidelines/
26. Apple: Manage app privacy (App Store Connect Help). https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy
27. Apple: Third-party SDK requirements. https://developer.apple.com/support/third-party-SDK-requirements/
28. Apple: TestFlight. https://developer.apple.com/testflight/
29. Apple: TestFlight overview (App Store Connect Help). https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview
30. Google Play: Families policy. https://support.google.com/googleplay/android-developer/answer/9893335
31. Google Play: Set up an open, closed, or internal test. https://support.google.com/googleplay/android-developer/answer/9845334
32. Apple: Compare memberships. https://developer.apple.com/support/compare-memberships/
33. Apple News (2026-02-03): Upcoming SDK minimum requirements. https://developer.apple.com/news/?id=ueeok6yw
34. Apple: Xcode Cloud. https://developer.apple.com/xcode-cloud/
35. Apple News (2026-10-05): Prepare and submit your apps for iPhone Duo. https://developer.apple.com/news/?id=kkphp5qo
36. Apple: App privacy details on the App Store. https://developer.apple.com/app-store/app-privacy-details/
37. Google Play: Impersonation policy. https://support.google.com/googleplay/android-developer/answer/9888374?hl=en
38. Google Play: Intellectual Property policy. https://support.google.com/googleplay/android-developer/answer/9888072
39. Google Play: Spam policy. https://support.google.com/googleplay/android-developer/answer/9899034?hl=en
40. Google Play: Policy announcement, 29 October 2026 (trader status, quality thresholds). https://support.google.com/googleplay/android-developer/answer/18100766?hl=en-GB
