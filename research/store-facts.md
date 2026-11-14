# Store facts: Play testing gate, age ratings, iOS signing key role, trader status, privacy-policy hosting

Ticket: [27-store-facts](../.scratch/mendvale/issues/27-store-facts.md)
Researched and checked: **2026-11-14**. Every source below was read on that date. Sources are first-party only: Google Play Console Help and Policy Center (support.google.com), the Android Developers Blog, Apple Developer and App Store Connect Help (developer.apple.com), and IARC (globalratings.com). Each claim cites its source as `[n]`, and the numbered list is at the bottom. Quotes are exact.

This builds on [store-requirements.md](store-requirements.md) (2026-11-13). Corrections to that file are listed at the end.

Assumptions: Mendvale is free, with no ads, no purchases, no accounts, no chat, no network calls and no analytics. It is published by one person on a **new personal** Google Play account and an **individual** Apple Developer Program membership (not yet bought). Battles are turn-based cartoon creature fights with no blood and no weapons.

---

## Answers

| # | Question | Answer | Certainty |
|---|---|---|---|
| 1 | Is Play's 12-tester / 14-day closed-test gate per app or per account? Does it hit a second app? Is the internal track exempt? | **It applies to Mendvale for certain**, because the account is a personal account created after 2023-11-13 [1]. Google's wording ties the gate to **each app** ("test their apps before those apps are eligible", "run a closed test for their app") and to that app's Production page [1][2], but **no Google page says outright whether a second app on the same account must pass it again**. Plan as if every app must. **Internal testing is not gated** (access requirement "None") **but does not count**: only a closed test satisfies the gate [1]. | Applies to Mendvale: high. Per app: medium (inferred from wording, docs silent). Internal ungated but not counting: high |
| 2a | What do the IARC questionnaires give a bloodless cartoon creature battler? | IARC doesn't publish its questions, and it issues the ratings only when the questionnaire is submitted [8][9]. Going by each authority's published definitions [4], the likely band is **ESRB E or E10+, PEGI 7 (PEGI 3 if the violence reads as purely comical), USK 6, ClassInd 10 ("bloodless fights"), and IARC Generic 7+**. It costs nothing: "free of cost to developers at this time" [9]. | Band: low to medium. Free: high |
| 2b | What does Apple's questionnaire give it? | Apple calculates the rating from frequency answers [10][11]. "Infrequent cartoon or fantasy violence" gives **9+**. "Frequent cartoon or fantasy violence" gives **13+** [10]. Battling is Mendvale's core loop, so "Frequent" is the honest answer, giving **13+** globally (Brazil A12, Korea 12+, Vietnam 12+; on OS versions before 26, 12+) [10]. Apple does not define where "infrequent" ends. | Mapping: high. Which frequency App Review accepts: medium |
| 2c | Does cute art trigger Play Families or Apple Kids by default? How is that avoided? | **Neither is automatic.** On Play, Families applies when *you* select a target age group under 13 [3][5]. But Google "may reject your app" if the listing suggests children "(such as youthful animation or young characters in the graphic assets)", and it may judge "imagery and terminology" against your declared audience [3][5]. **Avoid it by** declaring only 13+ age groups and keeping store graphics from looking aimed at young children. On Apple, the Kids category is **opt-in** through "Made for Kids" in the age-rating flow, and choosing "Not Applicable" keeps the app out [11]. A 13+ calculated rating can't select it anyway, since Made for Kids requires 4+ or 9+ [11]. | High |
| 3 | Does `xcodebuild` cloud signing with an App Store Connect API key need an **Admin** key? | **Use an Admin-role team key. That is the only setup Apple documents end to end.** Individual keys "aren't able to use Provisioning endpoints" [12], so the key must be a **team key**, which only Account Holder or Admin can create [13]. In Apple's permissions table, only Account Holder and Admin have default full access to create cloud-managed certificates, distribution profiles and App IDs. App Manager and Developer need extra Certificates, Identifiers & Profiles (CI&P) access or a separate cloud-certificate permission, and a Developer can't create distribution profiles at all [14]. Apple documents granting those extras to *users*, not to keys. A key's role "can't" be edited after creation [13]. On an **individual** membership, CI&P "is only available to Account Holders and members of an organization's team" [14]. **So App Manager or Developer keys are not documented to work, and on an individual account they very likely can't.** | Admin works: high. App Manager/Developer don't: medium (docs silent on per-key permissions) |
| 4 | What does declaring non-trader mean in the EU (DSA)? What must a trader publish? | Both stores **require the declaration** even if you don't distribute in the EU [6][15]. Both say a hobbyist with no commercial intent is **unlikely to be a trader** [6][15]. **Non-trader means:** no contact details published for DSA, and EU (and on Play, UK) users are told consumer-protection rights "do not apply" to contracts with you [6][15]. Falsely claiming non-trader is prohibited and can mean global removal or suspension [6]. **A trader on an individual account must publish** an address (Apple allows a P.O. Box), phone and email. Apple requires two-factor or document verification, payment details and a compliance self-certification [15]. Play shows the phone, address and terms-of-service link, plus a self-certification, from **2027-03-01** [6]. **For Mendvale: declare non-trader on both.** | High (the legal call is yours; neither store decides it) |
| 5 | Do GitHub Pages or a repo file URL satisfy both stores? | **GitHub Pages: yes, on everything either store states.** Play requires an active, public `https://` URL with valid SSL, no geofencing or login, and a "standard, non-editable webpage (not a PDF or downloadable file)" [7]. The policy must be labelled "privacy policy", must name the developer or app, and must give a contact point [16]. Apple asks only for a URL plus the 5.1.1(i) content rules [17][18]. **A github.com repo file URL** (`…/blob/main/PRIVACY.md`) meets each Play test while the repo stays public, which `andrew689-cpu/rpg` is today. But it is GitHub's page chrome, not a plain webpage, and a raw.githubusercontent.com URL serves plain text. **Neither store names any host or says yes or no to GitHub**, so Pages is the safer choice. | Pages: high. Repo URL: medium (docs silent on hosts) |

### What this changes for Mendvale
- **Recruit 12 closed testers early.** The gate sits between internal testing and production for Mendvale's first app, whatever the per-app answer turns out to be [1].
- **Expect Apple 13+, not 9+**, unless you can honestly answer "Infrequent" for a battle-centred game [10]. If 9+ matters, decide it in design, not at submission.
- **Create one Admin-role team key** for the macOS runner, and keep it in GitHub Actions secrets [12][13][14].
- **Declare non-trader on both stores.** Revisit if Mendvale ever gets ads, IAP, a price or donations, since Play lists those as signs of trading [6].
- **Host the privacy policy on GitHub Pages**, with a support/contact page beside it. Apple's Support URL "must lead to actual contact information … as may be required by local law" [18], and guideline 1.5 asks for "an easy way to contact you" [17]. An email address on that page is the minimum.

---

## Evidence

### 1. Google Play closed-testing gate

**Who it applies to** [1]:
> "Google Play requires personal developer accounts created after November 13, 2023, to test their apps before those apps are eligible for distribution on Google Play. Certain features in Play Console, such as Production ( Test and release > Production ) and Pre-registration ( Test and release > Testing > Pre-registration ), remain disabled until developers meet these testing requirements."

> "Developers with personal accounts created after November 13, 2023, must run a closed test for their app with a minimum of 12 testers who have been opted in continuously for at least 14 days. When you meet these criteria, you can apply for production access on the Dashboard in Play Console to distribute your app on Google Play."

> "At least 12 testers must be opted in to your closed test continuously for the preceding 14 days when you apply for production access."

**Per app or per account: not stated.** The help page [1] and the announcement post [2] both talk about "their apps" and "their app", and both describe the gate in terms of an app's Production page and an app's Dashboard. Neither says whether production access, once granted, carries over to the account's next app. The announcement post [2] (Kobi Gluck, 2023-11-09, updated 2024-12-11) says "developers with newly created personal Play Console accounts will soon be required to test their apps with at least 20 people for a minimum of two weeks before applying for production access", and its update says "starting today, we're requiring 12 instead of 20 testers for personal developer accounts". Neither text settles the second-app question. **Docs are silent.** The reading most consistent with the wording is that each new app goes through the gate.

**Internal track** [1]. The track table:
> "Internal testing | Distribute builds to a small group of trusted testers to identify issues and get early feedback (before or after completing app setup). | None."
> "Closed testing | … | Complete app setup."
> "Open testing | … | Gain access to production."
> "Production | Make your app available to users on Google Play. | Run a closed test with at least 12 opted-in testers continuously for 14 days."

And: "Internal testing is optional, but recommended as a starting point." So the CI's Play Developer API uploads to the internal track work from day one, **but internal testers don't count**. The gate needs a closed track. Open testing is locked until production access is granted [1].

**Continuity** (FAQ) [1]:
> "Testers who opt in, test for fewer than 14 days, and then opt out do not count toward the requirement. If a tester opts out and opts back in later, the 14 days must be consecutive to count toward the minimum requirement of 12 continuous opted-in testers."

### 2. Age ratings

#### IARC / Google Play
- **Mandatory, per app** [3b]: "All apps must have a content rating from the IARC to be on Google Play." "You must complete the content rating questionnaire for each new app submitted to the Play Console … Apps without a content rating will be removed from the Play Store."
- **How a rating is produced** [8]: "Developer is asked to complete the IARC questionnaire to obtain ratings." "IARC assigns the appropriate Age Rating, Content Descriptors, and Interactive Elements by region." [9]: "Once a developer completes the questionnaire, the ratings are issued immediately." The rules are built from each authority's standards, and "the system generates a unique rating for each territory based on those localized standards."
- **Cost** [9]: "Obtaining ratings via IARC is free of cost to developers at this time."
- **Appeal** [9]: "Developers can request a rating check for any of the ratings their game or app has been assigned by the IARC system." [3b]: "you can appeal directly to the IARC rating authority using the link provided in your certificate email."
- **Reuse** [9]: the IARC certification code "can be used" on another IARC-participating storefront instead of re-rating.
- **The questions themselves are not published** in Play Console Help or on globalratings.com. Play Console Help says only "Select a category and click Next. Complete the questionnaire." [4]

**Published authority definitions that govern a bloodless cartoon creature battle** [4]:

| Authority | Lowest plausible | Next band up | Exact wording |
|---|---|---|---|
| ESRB (Americas) | EVERYONE | EVERYONE 10+ | E: "May contain minimal cartoon, fantasy or mild violence". E10+: "May contain more cartoon, fantasy or mild violence" |
| PEGI (Europe, UK, Middle East) | PEGI 3 | PEGI 7 | 3: "Some violence in a comical context (typically cartoonlike - Bugs Bunny or Tom & Jerry - forms of violence) is acceptable. … they should be distinctly fantasy." 7: "There can only be very mild violence in a PEGI 7 app, like implied violence or non-detailed, non-realistic violence." 12: "violence of a slightly more graphic nature towards fantasy characters, or non-graphic violence towards human-looking characters or animals" |
| USK (Germany) | All ages | 6 | 6: "If violent imageries are present they remain abstract and are not decisive for the overall product. Games in this age category can still be categorized as family-friendly but involve more exciting and competitive aspects." |
| ClassInd (Brazil) | All ages | 10+ | All: "It may contain a little very low impact content, such as cartoon violence." 10+: "It may contain mildly offensive swearing, weapons, **bloodless fights**, scary scenes…" |
| IARC Generic (other regions) | 3+ | 7+ | 3+: "Some violence in a comical or fantasy context is acceptable." 7+: "Mild violence (implied or non-realistic) is permitted." 12+: "Violence involving fantasy characters and/or non-graphic violence involving human-looking characters or animals is permitted." |

**Reading.** Combat is the core loop rather than an occasional gag, and the creatures are often animal-like. So the realistic outcome is **E or E10+, PEGI 7, USK 6, ClassInd 10, Generic 7+**. The PEGI 12 / Generic 12+ wording "violence … towards … animals" is the risk to watch: keep creatures clearly fantastical, not real animals. This is an inference from definitions, not a rating. **The real answer comes only from submitting the questionnaire.**

#### Apple
- **Calculated from frequency answers** [11]: "Navigate through each section of the progress bar, answering the questions and selecting the appropriate level of frequency for each content description". [10]: "Apple generates appropriate ratings based on your answer to the age rating questionnaire."
- **Definition** [10]: "Cartoon or Fantasy Violence: Physical conflict or harm of an exaggerated or fantastical nature that can easily be distinguished from real life. May include: animated magic used to harm animals or animated human wrestling."
- **Global ratings (iOS 26 and later)** [10]:
  - 9+: "Violence Infrequent cartoon or fantasy violence"
  - 13+: "Violence: Frequent cartoon or fantasy violence"
- **Regional tables** [10]: Brazil A6 = "Infrequent cartoon or fantasy violence", A12 = "Frequent cartoon or fantasy violence". Korea All = infrequent, 12+ = frequent. Vietnam 12+ = both infrequent and frequent.
- **Earlier OS versions** [10]: 9+ = "Infrequent or mild cartoon or fantasy violence", 12+ = "Frequent or intense cartoon or fantasy violence".
- **Other answers for Mendvale** [10]: Advertising, Messaging and Chat, User-Generated Content, Social Media, Unrestricted Web Access, Gambling, Simulated Gambling and Loot Boxes are all **none**. "Guns or Other Weapons" ("guns, swords, or knives") is none if no one wields one. **Contests** is defined as "Events that allow users to compete with one another for rankings, rewards, or the achievement of personal goals". A single-player game has no user-vs-user competition, but "achievement of personal goals" is ambiguous. Infrequent contests only gives 4+, and frequent gives 13+, the same as frequent violence, so it doesn't change the expected result.
- **Apple does not define "frequent" vs "infrequent".** Docs are silent.
- The new "Shared Location" and "Dating and Relationships" descriptors arrive 2026-11-16 and must be answered by 2027-01-12 (see [store-requirements.md](store-requirements.md) [24]).

#### Families policy and the Kids category
**Play.** The target audience is your declaration, but Google checks it [3][5]:
> "Any apps that have at least one target audience age group that includes children must comply with Google Play's Families Policy Requirements" [3].

> "If your app is not primarily designed for children under 13 but your listing contains marketing elements that suggest otherwise (such as youthful animation or young characters in the graphic assets ), Google Play may reject your app. If that happens, you'll have the following options: Remove any marketing elements in your store listing that may appeal to children … Change the target age group(s) of your app to only include children under 13 (which will require complying with Google Play Families Policy )." [3]

> "Regardless of what you identify in the Google Play Console, if you choose to include imagery and terminology in your app that could be considered targeting children, this may impact Google Play's assessment of your declared target audience. Google Play reserves the right to conduct its own review of the app information that you provide to determine whether the target audience that you disclose is accurate." [5]

> "You should only select age groups that include both adults and children if you truly have designed your app for all ages, not just because you want your app to be available to users of all ages. Please note that if your app targets any users who are under the age of 21, you must consider if they would be considered children under their local laws." [3]

So cute art does not switch Families on, but it can get a 13+ declaration challenged. **How to avoid it:** declare only 13+ age groups. Make the store icon, feature graphic and screenshots show the RPG (map, battle UI, story) rather than baby-faced mascots on bright toy-like backgrounds. Avoid "for kids" wording. If Google rejects anyway, its two documented remedies are the options [3]. Families compliance itself would be light for an app with no ads and no data [5], but it is a policy commitment the spec (§7) says to avoid unless chosen on purpose.

**Apple** [11]:
> "If you don't need to override your rating or display your app in the Kids category on the App Store, choose Not Applicable under Age Categories and Override".

> "If your calculated rating is 4+ or 9+ and you want your app to also display in the Kids category on the App Store, under Age Categories and Override, choose Made for Kids … You can't change this selection once your app is approved by App Review. The app and all subsequent updates will need to follow the Kids category guidelines."

Guideline 1.3 [17]: "If you want to participate in the Kids Category, you should focus on creating a great experience specifically for younger users." The Kids category is opt-in, and Apple documents no art-based trigger.

### 3. iOS cloud signing: which API key role

- **Only team keys can provision** [12]: "There are two types of API keys: Team: Access to all apps, with varying levels of access based on selected roles. Individual: Access and roles of the associated user. Individual keys aren't able to use Provisioning endpoints, access [Sales and Finance], or `notaryTool`."
- **Who can make team keys, and that roles are fixed** [13]: "Generate a team API key Required role: Account Holder or Admin." "Under Access, select the role permissions to determine what the API can be used for." "Once you generate an API key, you can't edit its name or access level." [12]: "The roles that apply to keys are the same roles that apply to users on your team".
- **What `-allowProvisioningUpdates` does with the key.** From Apple's WWDC21 session "Distribute apps in Xcode with cloud signing" [19]: "New in Xcode 13, you can use App Store Connect keys to sign in to xcodebuild without ever signing into Xcode. … `-authenticationKeyIssuerID` … `-authenticationKeyID` … `-authenticationKeyPath`. xcodebuild still requires allow provisioning updates, as it still needs to communicate with the developer website." And: "Anyone with an Admin or Account Holder role on App Store Connect can cloud sign for App Store Connect distribution by default. If I want someone with a Developer role to upload Baker using cloud signing, I can grant them permission on App Store Connect by checking the Access to Cloud Managed Distribution Certificate checkbox." That checkbox is described for a *person*. No Apple page describes it for an API key.
- **Role table** [14]. Parsed from the icons on the Apple Developer Program table. Legend: ● = "Full access."; ◐ = "Requires access to Certificates, Identifiers & Profiles, granted in Users and Access in App Store Connect."; ✓ = "Granted as a separate permission in Users and Access in App Store Connect. Requires access to Certificates, Identifiers & Profiles"; ⓘ = "Requires Xcode Automatic Signing."

  | Permission | Admin | App Manager | Developer |
  |---|---|---|---|
  | Create other cloud-managed certificate types (incl. distribution) | ● | ✓ | ✓ |
  | Create and revoke distribution certificates | ● | ◐ | — |
  | Create and delete distribution provisioning profiles | ● | ◐ | — |
  | Register and configure App IDs | ● | ◐ | ⓘ |
  | Upload builds | ● | ◐ | ◐ |
  | Generate API keys | ● | — | — |

- **Individual memberships** [14]: "\* Certificates, Identifiers & Profiles is only available to Account Holders and members of an organization's team." And: "If you're enrolled as an individual and add users in App Store Connect, users receive access only to your content in App Store Connect and are not considered part of your team in the Apple Developer Program." [20]: "Additional permissions are available in App Store Connect to enable Admins and Developers to sign apps and software with these certificates."

**Conclusion.** Only Admin has, by default, every permission the `archive` + `-exportArchive` run touches: registering the bundle ID, creating the App Store profile, creating or using the cloud-managed distribution certificate, and uploading. App Manager and Developer depend on CI&P and cloud-certificate grants. Apple documents those grants for users only, a key's access can't be edited after creation, and on an individual membership CI&P isn't available to non-Account-Holders. **Use an Admin team key.** Store it as a CI secret, since it can also manage users and keys [12]. Docs are silent on whether any non-Admin key can be given the extra grants.

### 4. EU DSA trader status

**Google Play** [6]:
> "all active developer accounts must declare whether they are a trader or non-trader under European Economic Area (EEA) and United Kingdom (UK) laws in Play Console. This declaration must be completed by February 1, 2027, regardless of where apps are targeted or distributed."

> "All new developer accounts are required to submit the declaration immediately upon account creation."

> "a trader is any natural or legal person acting for purposes relating to their trade, business, craft or profession. If you are acting outside of these purposes (such as a personal hobby or other non-commercial activity), you are unlikely to be a trader."

Its listed indicators are "Profit-seeking motive", "Transaction volume", "Business setup" and "Legal status (such as a D-U-N-S number)".

> "If you declare yourself as a "non-trader," we will inform consumers in these regions that consumer rights stemming from consumer protection laws do not apply to contracts between you and them . Note that under the EU Unfair Commercial Practices Directive (UCPD) and the UK Digital Markets, Competition and Consumers Act (DMCCA), it is strictly prohibited to falsely claim or create the impression that you are not acting as a trader, and doing so may result in global removal."

What a trader on Play must provide or show:
> "If you use a personal developer account, you must provide a contact phone number to be displayed on Google Play. Be aware that your address will also be publicly displayed." "Starting March 1, 2027, users everywhere will see: Contact details : … if you have an individual account and are a trader, a phone number and address will now be displayed. … Terms of Service : A link to your app's Terms of Service, if you provided one. Starting March 1, 2027, users in the EEA and UK will also see: Developer name : Your developer/trader name will replace Google in the "Offered by" field … Self-certification".

Traders are also asked "to provide the link to the terms of service for each of your apps."

Enforcement: "Failure to declare your trader status by the February 1, 2027 deadline may trigger enforcement including app update blocks and removal from the Play Store globally." "If you've declared as a non-trader but we detect activity that indicates you may qualify as a trader, we may ask you to confirm or update your status."

**Apple** [15]:
> "Articles 30 and 31 of the Digital Services Act (DSA) require Apple to verify and display trader contact information for all traders distributing apps on the App Store in the European Union (EU). This includes an address, phone number, and email address … Even if you don't distribute apps in the EU, you'll still need to declare a trader status."

> "If you're not a trader, consumers in the EU will be informed that consumer rights stemming from applicable consumer protection laws won't apply to contracts between you and them."

> "Apple can't determine whether you're a trader." "For example, if you're a hobbyist and you developed your app with no intention of commercializing it, you may not be considered a trader. Regardless of whether you're an individual developer or organization, if you have a legal status associated with a business activity, that would suggest you may be a trader."

Apple's listed factors are revenue (IAP, paid or ad-sponsored), commercial practices such as advertising, VAT registration, and developing "in connection with your trade, business, craft, or profession".

> "Individuals: You'll need to enter the following for display on your App Store product pages: Address or P.O. Box Phone number Email address" "All traders: You'll need to provide payment account details … You'll also be asked to certify that you only offer products or services that comply with the applicable rules of EU law."

Verification is two-factor on the email and phone, or manual verification with "a current document that verifies your business name and address". The non-trader option reads: "'This is not a trader account.' You won't need to provide any contact information." Required role: "Account Holder or Admin."

**Not trader-related but still public.** Without trader status, Play still shows the legal name, country and developer email (see [store-requirements.md](store-requirements.md) [10]). Apple shows the individual's legal name as seller (ibid. [18]).

### 5. Privacy-policy hosting

**Google Play, form-level checklist** [7] (the "Prepare your app for review" page):
> "You must link to a privacy policy on your store listing and within your app, even if your app doesn't access personal or sensitive user data or target children. … make sure your privacy policy meets the following requirements: It is hosted on an active, publicly accessible URL (starting with http:// or https:// ) with a valid SSL certificate. It is accessible worldwide without geographical restrictions, geofencing, or login requirements. It is displayed on a standard, non-editable webpage (not a PDF or downloadable file). It applies specifically to your app, covers user privacy, and comprehensively discloses how your app collects, uses, and shares user data".

**Google Play, User Data policy** [16]:
> "All apps must post a privacy policy link in the designated field within Play Console, and a privacy policy link or text within the app itself. … This must include: Developer information and a privacy point of contact or a mechanism to submit inquiries." "Clear labeling as a privacy policy (for example, listed as "privacy policy" in title). The entity (for example, developer, company) named in the app's Google Play store listing must appear in the privacy policy or the app must be named in the privacy policy. Apps that do not access any personal and sensitive user data must still submit a privacy policy. Please make sure your privacy policy is available on an active, publicly accessible and non-geofenced URL (no PDFs) and is non-editable."

**Apple**:
- [18] (App information reference): "Privacy Policy URL A URL that links to your company's privacy policy. Required for iOS and macOS apps." And "Support URL … This URL must lead to actual contact information (legal address, email address, telephone number), as may be required by local law, so that users can reach you … This property is required".
- Guideline 5.1.1(i) [17]: "All apps must include a link to their privacy policy in the App Store Connect metadata field and within the app in an easily accessible manner. The privacy policy must clearly and explicitly: Identify what data, if any, the app/service collects…".
- Guideline 1.5 [17]: "Make sure your app and its Support URL include an easy way to contact you".

**Assessment against those tests**

| Test | GitHub Pages (`https://andrew689-cpu.github.io/…`) | Repo file (`https://github.com/andrew689-cpu/rpg/blob/main/PRIVACY.md`) |
|---|---|---|
| Active, public, `https`, valid SSL [7] | Yes | Yes, only while the repo is public (it is today) |
| No geofencing or login [7] | Yes | Yes (GitHub doesn't require login to view public files) |
| "standard, non-editable webpage (not a PDF or downloadable file)" [7] | Yes, plain HTML you control | Rendered as a GitHub page with repo chrome. Viewers can't edit it, but it isn't a standalone page. `raw.githubusercontent.com` serves plain text, which is closer to "downloadable file" |
| Labelled "privacy policy", names developer/app, contact point [16] | Content-dependent, easy | Content-dependent, easy |
| Apple: a URL [18] | Yes | Yes |

**Neither store names, approves or forbids any host.** Use GitHub Pages and put a support/contact page next to it for Apple's Support URL [18].

---

## Corrections to [store-requirements.md](store-requirements.md)

- Its source **[7]**, `answer/9859455`, is now titled **"Prepare your app for review"**, not "User Data policy". The User Data policy is `answer/10144311` (here [16]). The quoted requirement still holds, and the page now lists concrete hosting tests (SSL, no geofence, no PDF, non-editable) [7].
- "Hosting a static page (e.g. GitHub Pages) is enough. Neither store specifies the host." That is still true, but the policy page must also be **labelled** as a privacy policy, **name the developer or app**, and give a **contact point** [16]. Apple's **Support URL** must lead to contact information [18].
- "A turn-based creature battler will likely land at 9+ or 13+ depending on how you answer frequency." That is confirmed, but for a battle-centred loop the honest answer is "Frequent", so **13+ is the expected result**. Regional variants are Brazil A12, Korea 12+, Vietnam 12+ [10].
- "The page doesn't say whether the gate applies per app or only to the first app." That still holds. Google's announcement post [2] doesn't say either. Added: **internal testing is ungated but does not count** toward the gate [1].
- "Whether the IARC questionnaire costs anything. Not stated." IARC states it is **free to developers** [9].
- Content-rating authorities are listed on `answer/9859655` [4], not on `answer/9898843` (the policy page, here [3b]).

## Still open / not verifiable from the docs

- Whether Play's gate applies again to a second app on the same personal account. No Google page says [1][2].
- The exact IARC ratings. The questions aren't published, and ratings are issued only when the questionnaire is submitted [8][9].
- Where Apple draws the line between "infrequent" and "frequent" cartoon violence [10].
- Whether a non-Admin **team API key** can carry CI&P or cloud-managed-certificate access. Apple documents those grants for users only [13][14][19].
- Whether either store accepts or rejects a github.com repo URL specifically. Neither names hosts [7][16][18].

---

## Sources

All checked 2026-11-14.

1. Google Play Console Help: App testing requirements for new personal developer accounts. https://support.google.com/googleplay/android-developer/answer/14151465?hl=en
2. Android Developers Blog (2023-11-09, updated 2024-12-11): Ensuring high-quality apps on Google Play. https://android-developers.googleblog.com/2023/11/ensuring-high-quality-apps-on-google-play.html
3. Google Play Console Help: Manage target audience and app content settings. https://support.google.com/googleplay/android-developer/answer/9867159?hl=en
3b. Google Play Policy Center: Content Ratings. https://support.google.com/googleplay/android-developer/answer/9898843?hl=en
4. Google Play Console Help: Content rating requirements for apps, games, and the ads served on both (rating authorities and definitions; how to take the questionnaire). https://support.google.com/googleplay/android-developer/answer/9859655?hl=en
5. Google Play Policy Center: Google Play Families Policies. https://support.google.com/googleplay/android-developer/answer/9893335?hl=en
6. Google Play Console Help: Trader status declaration. https://support.google.com/googleplay/android-developer/answer/17594752?hl=en
7. Google Play Console Help: Prepare your app for review (privacy policy URL requirements). https://support.google.com/googleplay/android-developer/answer/9859455?hl=en
8. IARC: How IARC works. https://globalratings.com/how-iarc-works/
9. IARC: FAQ. https://globalratings.com/faq/
10. App Store Connect Help: Age ratings values and definitions. https://developer.apple.com/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions/
11. App Store Connect Help: Set an app age rating. https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating/
12. Apple Developer Documentation: Creating API Keys for App Store Connect API. https://developer.apple.com/documentation/appstoreconnectapi/creating-api-keys-for-app-store-connect-api
13. App Store Connect Help: App Store Connect API (request access, team keys, individual keys). https://developer.apple.com/help/app-store-connect/get-started/app-store-connect-api/
14. Apple Developer Account Help: Roles and access (permissions tables). https://developer.apple.com/help/account/access/roles/
15. App Store Connect Help: Manage European Union Digital Services Act trader requirements. https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements
16. Google Play Policy Center: User Data. https://support.google.com/googleplay/android-developer/answer/10144311?hl=en
17. Apple: App Review Guidelines (1.3, 1.5, 5.1.1(i)). https://developer.apple.com/app-store/review/guidelines/
18. App Store Connect Help: App information (Privacy Policy URL) and Platform version information (Support URL). https://developer.apple.com/help/app-store-connect/reference/app-information/app-information/ and https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/
19. Apple WWDC21 session 10204: Distribute apps in Xcode with cloud signing (transcript). https://developer.apple.com/videos/play/wwdc2021/10204/
20. Apple Developer Account Help: Cloud-managed certificates. https://developer.apple.com/help/account/certificates/cloud-managed-certificates/
