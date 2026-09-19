#!/usr/bin/env python3
"""Bruno Brief build for 2026-09-20. Prepends today's day, preserves prior days (60-day cap)."""
import json, copy

TODAY = "2026-09-20"

stories = [
    {
        "bucket": "US Bond Market", "emoji": "🇺🇸",
        "headline": "US 10-year Treasury yield back to 5.00% — rebound after a week at two-decade highs as oil retreat eases inflation fears",
        "summary": "The 10-year note rose to 5.00% on Friday (Sept 18), up ~6bp on the session after the curve had slipped below 5% midweek as softer oil prices cooled inflation concerns in the wake of the Fed's Sept 16 hike. Long-end borrowing costs remain pinned near levels not seen since 2007, keeping the whole curve, from the 1-month to the 30-year, elevated.",
        "sources": ["TradingEconomics", "CNBC"],
        "slug": "us-10y-back-5-percent-2026-09-20"
    },
    {
        "bucket": "Australian Politics", "emoji": "🇦🇺",
        "headline": "Coalition unveils 'root and branch' school reform built on 'Western values'",
        "summary": "Shadow Education Minister Julian Leeser's plan would strip cross-curricular units on Indigenous history and Asian studies from the curriculum and refocus students on Western values — civics, literature and philosophy — as the Coalition lays out its answer to Australia's sliding academic results.",
        "sources": ["ABC News"],
        "slug": "coalition-education-western-values-2026-09-20"
    },
    {
        "bucket": "Australian Politics", "emoji": "🇦🇺",
        "headline": "Labor's 225,000 migration target is 'an auction it can't win'",
        "summary": "Analysis argues Tony Burke has turned a Treasury forecast into a binding target, legitimising a numbers contest in which One Nation (130,000) and the Coalition (150-170k) can always bid lower — while pollsters say migration moves few voters beyond One Nation's base anyway, leaving Labor adding fight without reward.",
        "sources": ["ABC News"],
        "slug": "labor-migration-target-auction-2026-09-20"
    },
    {
        "bucket": "European Politics", "emoji": "🇪🇺",
        "headline": "Germany votes today: state elections seen as a referendum on Merz's survival",
        "summary": "Sunday's polls in Mecklenburg-Western Pomerania — where the CDU risks falling below the 5% threshold for the first time in the post-war era — and Berlin could decide Chancellor Friedrich Merz's fate, two weeks after the AfD's landslide win in Saxony-Anhalt. Eight CDU state premiers have publicly backed him, but Merz has cancelled his UN General Assembly speech to manage the fallout.",
        "sources": ["POLITICO", "Bloomberg", "DW"],
        "slug": "german-state-elections-merz-2026-09-20"
    },
    {
        "bucket": "European Politics", "emoji": "🇪🇺",
        "headline": "European leaders warn of an 'intensified' Russian hybrid threat; Macron orders a critical-infrastructure plan",
        "summary": "After Poland's Donald Tusk warned Moscow could stage 'accidental' drone or rocket strikes on NATO territory, Emmanuel Macron said the Russian hybrid threat 'has intensified' and ordered a plan to shield critical infrastructure and sensitive defence sites from drone and cyberattacks. Europe has recorded roughly 100 attributed hybrid incidents so far this year, up from 60 in the same period in 2025.",
        "sources": ["POLITICO", "BBC", "Reuters"],
        "slug": "eu-russia-hybrid-threat-warning-2026-09-20"
    },
    {
        "bucket": "AI News", "emoji": "🤖",
        "headline": "Zero-click 'Plugin4Shell' flaw hits the plugin systems of four AI coding agents at once",
        "summary": "A disclosed vulnerability lets attackers achieve remote code execution on Claude Code, Codex, GitHub Copilot and Gemini CLI with no user action, because the agents auto-update installed plugins in the background by default. Researchers flag a shared design assumption four independent teams built in, with Claude Code and Codex since issuing fixes.",
        "sources": ["Help Net Security", "Cybersecurity News"],
        "slug": "plugin4shell-ai-coding-agents-2026-09-20"
    },
    {
        "bucket": "AI News", "emoji": "🤖",
        "headline": "OpenAI rules out a 2026 IPO as a global AI-stock selloff follows leaders' 'slow down' warnings",
        "summary": "Sam Altman told Fortune the company won't go public this year — 'given everything happening with safety, right now would be an ill-advised moment' — as tech shares tumbled worldwide after Anthropic's Dario Amodei, backed by Elon Musk, urged a slower frontier, hammering chip and memory makers (Nvidia, SK Hynix, Samsung, Arm) hardest while software stocks rallied.",
        "sources": ["NBC News", "CBS News", "Morningstar"],
        "slug": "openai-ipo-ai-stock-selloff-2026-09-20"
    },
    {
        "bucket": "Conflicts", "emoji": "⚔️",
        "headline": "Russia reports cyberattacks on voting systems on the second day of its three-day parliamentary election",
        "summary": "Russian authorities said Moscow's online-voting system was hit by a strong overnight attack and that an attempted sabotage of Far East communication lines was thwarted, with no disruption confirmed per state media. Kremlin-aligned officials blamed Ukraine as voting runs Sept 18-20, with residents of occupied Donetsk, Lugansk, Kherson and Zaporozhye voting for the first time.",
        "sources": ["Reuters", "RFE/RL", "TASS"],
        "slug": "russia-election-cyberattacks-2026-09-20"
    },
    {
        "bucket": "Conflicts", "emoji": "🌍",
        "headline": "Hundreds of thousands rally in Tehran in Iran's biggest show of defiance since the war began",
        "summary": "In a government-organised 'Janfaday-e Iran' (sacrifice for Iran) demonstration on Friday, Tehran's Revolutionary Guard chief said over 600,000 have signed up for volunteer military training, as the rial falls past 2.3 million to the dollar under a US naval blockade and fresh sanctions. Iran also claimed a strike on a Togo-flagged tanker in the Strait of Hormuz.",
        "sources": ["AP via PBS", "The Independent", "Iran International"],
        "slug": "iran-tehran-rally-volunteers-2026-09-20"
    },
    {
        "bucket": "Science/Tech", "emoji": "🔬",
        "headline": "Irish team builds a DNA 'molecular computer' that runs 100-bit calculations with no electricity",
        "summary": "Researchers at Maynooth University created a Scaffolded DNA Computer that uses self-assembling strands to execute 10 molecular programs — arithmetic and 100-bit calculations — powered purely by chemical reactions, published in Nature. It points to new possibilities in long-term data storage, energy-efficient computation, and eventually molecular systems that operate inside cells for disease detection.",
        "sources": ["Tom's Hardware", "Nature"],
        "slug": "dna-molecular-computer-ireland-2026-09-20"
    },
    {
        "bucket": "Science/Tech", "emoji": "🚀",
        "headline": "JWST watches a tiny asteroid's rings change over a decade — one denser, one nearly gone",
        "summary": "New James Webb Space Telescope observations of Chariklo — a body barely 250km across with two rings — show one ring has grown denser while the other has almost vanished, likely a real physical evolution of the planetary rings over time, per a study in Science Advances. It suggests even small-body rings shift just as giant-planet rings do.",
        "sources": ["Ars Technica", "Science Advances"],
        "slug": "chariklo-rings-changing-2026-09-20"
    },
    {
        "bucket": "Blowing Up Today", "emoji": "🚨",
        "headline": "Oil ends a volatile week near $100 as Saudi supply fears ease but Hormuz stays badly restricted",
        "summary": "Brent closed at US$103.87 and WTI at US$100.30 on Friday after touching US$108.75 intraweek, as Saudi exports via Oman ship-to-ship transfers and China urging Iran to restrain Houthi attacks eased supply fears — yet only four commodity vessels crossed the Strait of Hormuz on Thursday versus a ~16 average, leaving the waterway severely constrained.",
        "sources": ["Reuters", "EnergyNow", "MarketScreener"],
        "slug": "oil-week-hormuz-saudis-2026-09-20"
    },
    {
        "bucket": "Blowing Up Today", "emoji": "🔥",
        "headline": "Saudi Arabia tells European refiners to expect no crude in October as its East-West pipeline stays damaged",
        "summary": "Saudi Aramco suspended Yanbu loadings and told at least two European refiners they will receive no crude next month after drone attacks damaged three pumping stations on the East-West pipeline, with roughly only half its capacity being restored. North Sea-to-Mediterranean crude differentials are surging to records and European diesel stays exceptionally tight.",
        "sources": ["EnergyNow", "The Business Times"],
        "slug": "saudi-october-europe-crude-2026-09-20"
    }
]

# ---- Load existing feed ----
with open("/home/rory/Projects/news-pwa/feed.json") as f:
    feed = json.load(f)

days = feed["days"]
# drop any existing today (re-run) so we replace rather than duplicate
days = [d for d in days if d.get("date") != TODAY]
today_day = {"date": TODAY, "stories": stories}
new_days = [today_day] + days
# 60-day cap
new_days = new_days[:60]

feed["days"] = new_days
with open("/home/rory/Projects/news-pwa/feed.json", "w") as f:
    json.dump(feed, f, ensure_ascii=False, indent=2)

# ---- Deep-dives ----
deep = copy.deepcopy(stories)
deepdive_urls = {
    "us-10y-back-5-percent-2026-09-20": ["https://tradingeconomics.com/united-states/government-bond-yield"],
    "coalition-education-western-values-2026-09-20": ["https://www.abc.net.au/news/2026-09-19/coalition-education-policy-western-values-julian-leeser/107172572"],
    "labor-migration-target-auction-2026-09-20": ["https://www.abc.net.au/news/2026-09-19/migration-labor-numbers-political-catch/107165434"],
    "german-state-elections-merz-2026-09-20": ["https://www.politico.eu/article/germany-friedrich-merz-political-survival-fight-regional-elections/", "https://www.bloomberg.com/news/articles/2026-09-19/german-elections-on-baltic-coast-and-berlin-may-seal-merz-s-fate"],
    "eu-russia-hybrid-threat-warning-2026-09-20": ["https://www.politico.eu/article/russia-vladimir-putin-nato-drone-attacks-europe-leaders-warning/", "https://www.bbc.com/news/articles/cm2dw1w9d3yjo"],
    "plugin4shell-ai-coding-agents-2026-09-20": ["https://www.helpnetsecurity.com/2026/09/18/plugin4shell-ai-coding-agents-vulnerability/", "https://cybersecuritynews.com/plugin4shell-zero-click-rce/"],
    "openai-ipo-ai-stock-selloff-2026-09-20": ["https://www.nbcnews.com/business/markets/stocks-tumble-ai-leaders-warning-slowdown-ipos-amodei-altman-rcna597643", "https://www.cbsnews.com/news/tech-stock-selloff-ai-warning/"],
    "russia-election-cyberattacks-2026-09-20": ["https://www.reuters.com/world/europe/russia-reports-online-attacks-electoral-system-second-day-parliamentary-vote-2026-09-19/", "https://www.rferl.org/a/russia-duma-vote-election-ukraine/33859408.html"],
    "iran-tehran-rally-volunteers-2026-09-20": ["https://www.pbs.org/newshour/world/iranians-rally-by-the-hundreds-of-thousands-in-biggest-show-of-defiance-since-war-began", "https://www.independent.co.uk/news/world/middle-east/iran-rally-war-volunteer-forces-b3052635.html"],
    "dna-molecular-computer-ireland-2026-09-20": ["https://www.tomshardware.com/tech-industry/researchers-create-dna-computer-that-performs-100-bit-calculations-without-electricity-molecular-system-uses-self-assembling-strands-to-perform-computing"],
    "oil-week-hormuz-saudis-2026-09-20": ["https://energynow.ca/2026/09/oil-ends-volatile-week-at-100-as-saudi-supply-fears-ease-but-hormuz-risks-persist/", "https://www.reuters.com/business/energy/oil-prices-fall-1-hopes-limited-supply-disruptions-2026-09-18/"]
}

deepdives = {
    "us-10y-back-5-percent-2026-09-20": {
        "headline": "US 10-year Treasury yield back to 5.00% — rebound after a week at two-decade highs",
        "summary": stories[0]["summary"],
        "source_urls": deepdive_urls["us-10y-back-5-percent-2026-09-20"],
        "content": (
            "The US 10-year Treasury note closed Friday (Sept 18) at 5.00%, up about six basis points on the session, after the yield curve had briefly slipped below the 5 percent mark midweek. The rebound keeps long-term American borrowing costs pinned at levels not seen since 2007, a striking reassertion of the sell-off that has dominated the market since the Federal Reserve's September 16 rate decision.\n\n"
            "Friday's modest uptick came as crude oil retreated for a third straight session, softening the inflation premium that has been pushing yields higher, yet investors still demanded more compensation for a stubbornly hot inflation picture, record US deficits and the lingering effects of the Iran war on energy prices. The whole curve remains elevated: the 1-month to 30-year tenor all hold above psychologically significant thresholds.\n\n"
            "The dynamics echo a market that has spent the past month keying off the Fed's pivot. After the FOMC raised the federal funds rate a quarter point to 3.75%-4.00% on Sept 16 — its first increase in more than three years — and signalled at least one more hike before year-end, short-dated yields jumped and the dollar surged to a seven-week high. Prediction markets swung toward a roughly 53% probability of another hike in October.\n\n"
            "For borrowers and the US government alike, the message is costly: elevated Treasuries ripple into mortgage rates, corporate credit and the roughly $1 trillion-plus annual AI data-centre buildout that is heavily financed through public debt markets. Analysts cautioned that until oil prices durably stabilise and the Fed signals a pause, two-decade-high yields could be 'here to stay'."
        )
    },
    "coalition-education-western-values-2026-09-20": {
        "headline": "Coalition unveils 'root and branch' school reform built on 'Western values'",
        "summary": stories[1]["summary"],
        "source_urls": deepdive_urls["coalition-education-western-values-2026-09-20"],
        "content": (
            "Shadow Education Minister Julian Leeser has unveiled the Coalition's plan for 'root and branch' educational reform aimed at improving Australia's sliding academic results. The centrepiece is a shift in the curriculum's cultural centre of gravity: removing cross-curricular units on Indigenous history and Asian studies, and instead having students learn more about Western values, including civics, literature and philosophy.\n\n"
            "The proposal lands in a heated national debate over school performance, which has become a live political issue as Australia's results on international assessments continue to drift. The plan reframes the remedy as one of content and cultural orientation rather than simply funding or class sizes, signalling the Opposition's intent to make education a central platform in the next federal campaign.\n\n"
            "Critics will likely raise concerns about marginalising Indigenous and Asian perspectives at a time when Australia's economic and strategic relationships — and a large share of its migration intake — are tied to the region. Supporters frame the change as restoring the 'common core' of knowledge and citizenship that schools are meant to transmit, and as a direct response to falling literacy, numeracy and civics scores.\n\n"
            "The exact mechanics — how any federal plan interacts with state-controlled school curricula, textbook changes and teacher training — remain to be detailed. But the announcement gives voters a clear, values-laden contrast between the major parties on education heading into the next election cycle."
        )
    },
    "labor-migration-target-auction-2026-09-20": {
        "headline": "Labor's 225,000 migration target is 'an auction it can't win'",
        "summary": stories[2]["summary"],
        "source_urls": deepdive_urls["labor-migration-target-auction-2026-09-20"],
        "content": (
            "ABC chief digital political correspondent Clare Armstrong argues that Home Affairs Minister Tony Burke, by formally accepting Treasury's 225,000 net overseas migration (NOM) forecast as a binding target at last Thursday's National Press Club address, has handed the political opposition a permanent benchmark — and permanently entered a numbers contest Labor cannot win on its own terms.\n\n"
            "The argument runs that once the government publicly commits to a single headline number, the migration debate becomes an auction: One Nation wants to drive NOM into negative territory before settling at 130,000 within three years, while the Coalition is tying its number to housing completions and likely landing between 150,000 and 170,000. Whoever promises a lower number can always outbid Labor, moving the argument from how migration is managed to who will cut it furthest.\n\n"
            "Yet the political prize may be illusory. Redbridge pollster Kos Samaras concludes migration is a salient issue for only about 10% of voters — most of them already supporters of One Nation. On housing, roughly 30% believe migration has contributed at all. The voters most inclined to reward a government for cutting intake are already parked with the party promising to go much further.\n\n"
            "For Burke, the policy package — barring international students' families, a backpacker ballot that limits third-year stays to about 5,000 (down from 31,000), a 'No Further Stay' condition for visitor visas, and a crackdown on overstayers and rogue migration agents — is about asserting control over a system he calls 'demand driven'. But as even he concedes, control over the system is not the same as precise control over the final NOM number, which depends heavily on when temporary migrants already in Australia choose to leave."
        )
    },
    "german-state-elections-merz-2026-09-20": {
        "headline": "Germany votes today: state elections seen as a referendum on Merz's survival",
        "summary": stories[3]["summary"],
        "source_urls": deepdive_urls["german-state-elections-merz-2026-09-20"],
        "content": (
            "German voters go to the polls Sunday in two state elections — the northeastern Baltic state of Mecklenburg-Western Pomerania and the city-state of Berlin — that are widely being read less as regional contests than as a referendum on Chancellor Friedrich Merz's ability to survive. The context is brutal: two weeks ago the far-right AfD won a historic 43.8% in Saxony-Anhalt, more than doubling its 2021 score and collapsing the CDU to 17.2%.\n\n"
            "Mecklenburg-Western Pomerania is the graver threat. Polls show the CDU, which has struggled in the state for years, collapsing to around 6-7% and at genuine risk of failing to clear the 5% threshold needed to return to the state parliament in Schwerin — a result one anonymous conservative official said would mean 'all hell breaks loose'. The race there has shaped up as a knife-edge contest between the SPD's incumbent premier Manuela Schwesig and the AfD on roughly 37%.\n\n"
            "Berlin is a different shape but carries its own risk: polling shows the CDU narrowly trailing the hard-left Die Linke around 20%, with the Left's Elif Eralp — the party's most vocal opponent of the AfD — in contention to become governing mayor, a first for the party. The CDU's likely loss of the capital's city government would strip it of another seat of power.\n\n"
            "Merz's own actions betray the stakes: he has cancelled a planned speech at the UN General Assembly to stay in Berlin and manage the fallout, and has scheduled a meeting of CDU leaders for Sunday just before polls close. Eight CDU state premiers issued a public letter backing him, but North Rhine-Westphalia's Hendrik Wüst has emerged as a likely successor. Rumours swirl that party chiefs could press for Merz's resignation as soon as this weekend if results are as bad as polls suggest."
        )
    },
    "eu-russia-hybrid-threat-warning-2026-09-20": {
        "headline": "European leaders warn of an 'intensified' Russian hybrid threat",
        "summary": stories[4]["summary"],
        "source_urls": deepdive_urls["eu-russia-hybrid-threat-warning-2026-09-20"],
        "content": (
            "A wave of European leaders has gone public this week with unusually specific warnings that Moscow is escalating a hybrid campaign — part conventional military pressure and part cyberattacks, misinformation and sabotage — aimed at Europe and France's support for Ukraine. Polish Prime Minister Donald Tusk told parliament on Thursday that Russia is preparing 'accidental' drone or rocket strikes on the territory of NATO countries supporting Ukraine, intended to weaken or split the alliance.\n\n"
            "On Friday, President Emmanuel Macron summoned France's party leaders and 2027 presidential candidates for an emergency meeting on Ukraine, Iran and the deepening energy crisis. He declared that 'the Russian hybrid threat against Europeans and against France has intensified,' and ordered the government to prepare a plan to protect critical infrastructure and the most sensitive defence-industry and technology sites from drone and cyberattacks.\n\n"
            "The warnings are grounded in a documented uptick. The Sahaidachnyi Security Center counted 100 formally attributed hybrid incidents across Europe between January and August 2026, up from 60 in the same period of 2025, with a sharp rise in airspace violations — NATO jets shot down a Russian drone over Lithuania, a Russian ship fired flares at a Danish helicopter, and Berlin blamed an attempted drone attack at Leipzig airport on a suspected Russian spy. A senior NATO official put the true figure at 'easily 200-plus' excluding cyberattacks.\n\n"
            "Yet NATO's formal assessment has not changed: the alliance sees no imminent threat of a direct attack, and allies say there is currently no multilateral response planned. Russian Foreign Minister Sergey Lavrov, for his part, warned that if Europe attacks Russia it would be 'a completely different war, and it will be very short.' The tension — urgent national warnings against a calm alliance consensus — is precisely what makes the situation delicate as Russia's campaign in Ukraine grinds on."
        )
    },
    "plugin4shell-ai-coding-agents-2026-09-20": {
        "headline": "Zero-click 'Plugin4Shell' flaw hits the plugin systems of four AI coding agents at once",
        "summary": stories[5]["summary"],
        "source_urls": deepdive_urls["plugin4shell-ai-coding-agents-2026-09-20"],
        "content": (
            "Security researchers have disclosed a vulnerability — dubbed Plugin4Shell — that affects four major AI coding agents simultaneously: Anthropic's Claude Code, OpenAI's Codex, GitHub Copilot and Google's Gemini CLI. The flaw allows attackers to achieve remote code execution with zero user interaction, and the mechanism makes it particularly insidious.\n\n"
            "The vulnerability is described as 'zero-click' because of how the agents handle plugin updates. Claude Code and Codex, among others, update installed plugins in the background by default. An attacker therefore does not need to trick a victim into installing a malicious plugin; a compromised or malicious update to a legitimate plugin could be delivered automatically, with the code executing in the developer's environment without any confirmation.\n\n"
            "The deeper point flagged by researchers is architectural: four independent engineering teams built the same flawed design assumption into their products simultaneously — that installing and auto-updating plugins can be trusted by default. That convergence, the analysis argues, points to something more durable than a single bug, and suggests the incident-handling and supply-chain practices of AI coding assistants need a rethink.\n\n"
            "Because these tools sit inside developers' terminals and repositories with broad permissions, the potential blast radius is substantial — the agents have access to source code, secrets and build pipelines. Anthropic and OpenAI have issued patches for Claude Code and Codex, and users are urged to update promptly. The finding adds a security dimension to the broader debate over how much trust to place in increasingly autonomous AI tools."
        )
    },
    "openai-ipo-ai-stock-selloff-2026-09-20": {
        "headline": "OpenAI rules out a 2026 IPO as a global AI-stock selloff follows leaders' 'slow down' warnings",
        "summary": stories[6]["summary"],
        "source_urls": deepdive_urls["openai-ipo-ai-stock-selloff-2026-09-20"],
        "content": (
            "The most consequential AI market story of the week is the global selloff in technology shares that followed a striking convergence of warnings from the industry's leaders — and OpenAI's decision to shelve its long-anticipated IPO. In an interview with Fortune, Sam Altman said the company would not go public this year: 'Given everything happening with safety, right now would be an ill-advised moment to go public.'\n\n"
            "The market rout was triggered by Anthropic CEO Dario Amodei's essay calling for every frontier lab to 'slow the pace at which we improve the capabilities of AI models.' His view drew backing from Elon Musk and, notably, Altman himself, who acknowledged AI could go 'very badly.' The effect on markets was immediate and global: US tech futures tumbled (Nasdaq 100 futures down 1.5%), Nvidia fell 3%, Arm and Marvell slipped 6%, and Asian memory-chip makers were hit hardest — Samsung Electronics fell 5% and SK Hynix more than 7%.\n\n"
            "The selloff was not uniform. Software stocks, pummelled all year on fears of AI disruption, rallied: CrowdStrike added 15%, ServiceNow 6%, and Microsoft rose after posting a provisional code of conduct for its AI models. Bank of America figures underline just how much of the market now leans on AI — five stocks (Alphabet, Apple, Micron, Microsoft, Nvidia) are forecast to drive 27% of S&P 500 growth over the next year, and AI capex is expected to top $1 trillion in 2026.\n\n"
            "Analysts are split on whether this is the start of the AI bubble hissing air or a blip. Capital Economics forecasts the S&P 500 to 8,250 by year-end before a 20%-plus correction in 2027 as 'bubble' dynamics bite; HSBC and UBS argue calls for a slower buildout are overblown and that stronger safeguards can coexist with rising compute demand. The one near-certainty is that the relationship between frontier-lab safety politics and public markets is now firmly on the radar — a factor made vivid by Altman choosing to stay private."
        )
    },
    "russia-election-cyberattacks-2026-09-20": {
        "headline": "Russia reports cyberattacks on voting systems on the second day of its parliamentary election",
        "summary": stories[7]["summary"],
        "source_urls": deepdive_urls["russia-election-cyberattacks-2026-09-20"],
        "content": (
            "Russia is holding its first full State Duma election since the full-scale invasion of Ukraine, running in three days from September 18 to 20, and the vote has been shadowed by official claims of cyberattacks on the electoral system. On Saturday, the second day, Russian authorities reported multiple attacks on voting systems and communication lines across the country.\n\n"
            "Central Election Commission chief Ella Pamfilova said Moscow's online-voting system was subjected to a strong attack overnight but that the situation 'remains under control' and all attacks 'are being successfully repelled.' The Digital Ministry separately said it registered an attempted sabotage of communication lines in Russia's Far East, which it said was thwarted. None of the claims was independently confirmed, and RFE/RL noted the officials provided few details.\n\n"
            "The political framing is pointed. President Vladimir Putin accused Ukraine of trying to interfere with the vote, without presenting evidence, and foreign ministry officials and OSCE-linked Russian figures blamed a Western campaign to disrupt the elections. Moscow election commission chief Olga Kirillova said online voting terminals suffered a glitch on the first day — blamed on 'enemy attacks' — but were restored within 20 minutes.\n\n"
            "The electoral mechanics matter for the war's political consolidation. This is the first time residents of the recently incorporated Donetsk and Lugansk People's Republics, and the Kherson and Zaporozhye regions, are voting in legislative elections. Russian state media cast turnout and stability as a show of resolve amid a war entering its fifth year, even as analysts point to voter apathy and frustration over the conflict as the backdrop against which the announcement of the attacks — and their attribution — lands."
        )
    },
    "iran-tehran-rally-volunteers-2026-09-20": {
        "headline": "Hundreds of thousands rally in Tehran in Iran's biggest show of defiance since the war began",
        "summary": stories[8]["summary"],
        "source_urls": deepdive_urls["iran-tehran-rally-volunteers-2026-09-20"],
        "content": (
            "On Friday, hundreds of thousands of Iranians marched through central Tehran in the largest government-organised demonstration since the US and Israel attacked Iran in February, in an event named 'Janfaday-e Iran' — roughly 'the ones who give their lives for Iran.' The march was a carefully staged display of national unity and readiness to fight, with volunteers in combat uniform, flags, and crowds chanting 'Death to America' and 'Death to Israel.'\n\n"
            "Tehran's Revolutionary Guard commander, Gen. Hassan Hassanzadeh, told state television that more than 600,000 people had registered to take part in limited military training, with more than one million expected to join in total. The new head of the Basij militia, Hossein Taeb, called the trainees 'resistance battalions' ready for 'full-fledged defense' and declared the campaign 'the biggest popular movement in the history of the world's wars.' Roughly 300,000 people were estimated on the streets.\n\n"
            "The defiant imagery sits against a stark economic backdrop. Under a US naval blockade of Iranian ports and fresh sanctions, the rial has fallen past 2.3 million to the dollar, and state media has urged citizens to enlist for weeks. The rally came two days after the fourth anniversary of Mahsa Amini's death in morality-police custody, and Iran International noted the show of force doubles as preparation to suppress any future domestic protest against the theocracy. On the same day, Iran claimed a new strike on a Togo-flagged oil tanker in the Strait of Hormuz, which it said was making an 'illegal attempt' to pass through.\n\n"
            "The event is a reminder that, seven months into a war over the Strait of Hormuz and its oil flows, Tehran is projecting both military capability and internal cohesion. Whether the demonstrations reflect genuine popular sentiment is hard to verify independently — such rallies are state-organised — but the mass mobilisation of civilian volunteers signals a regime preparing its population for a long conflict and a hardening line on any domestic dissent."
        )
    },
    "dna-molecular-computer-ireland-2026-09-20": {
        "headline": "Irish team builds a DNA 'molecular computer' that runs 100-bit calculations with no electricity",
        "summary": stories[9]["summary"],
        "source_urls": deepdive_urls["dna-molecular-computer-ireland-2026-09-20"],
        "content": (
            "A team of researchers at Maynooth University in Ireland has built what they describe as a 'first-of-its-kind' DNA molecular computer that uses self-assembling strands of DNA to perform complex mathematical operations without electricity. Detailed in the journal Nature in mid-September, the system — a Scaffolded DNA Computer (SDC) — is one of the most complex and fastest molecular computers yet demonstrated.\n\n"
            "The machine is powered entirely by chemical reactions rather than electrical current. DNA strands self-assemble into structures that encode and process information, with the team running ten different molecular programs and successfully executing addition, subtraction, multiplication and division — including complex 100-bit calculations performed reliably without errors. Because the system is constrained by the laws of physics, the researchers say it removes the need for error-correction software that conventional computing relies on.\n\n"
            "The potential applications span both near- and long-term horizons. The researchers point to new possibilities for long-term data storage — DNA is extraordinarily dense and durable as an information medium — and for energy-efficient computation, at a time when data centres are becoming a major consumer of electricity. In Ireland, the researchers note, data centres consumed roughly 23% of the country's electricity in 2025, a vivid illustration of the appetite such molecular alternatives could one day help satisfy.\n\n"
            "Further out, the team envisions molecular systems that could operate inside cells for applications such as disease detection — computation at the biological scale, embedded in living tissue. That remains a distant goal, but the demonstration that arbitrary arithmetic can be done reliably in wet chemistry, with no power draw and no error-correcting software, is a meaningful step toward a distinctly different kind of computer."
        )
    },
    "oil-week-hormuz-saudis-2026-09-20": {
        "headline": "Oil ends a volatile week near $100 as Saudi supply fears ease but Hormuz stays badly restricted",
        "summary": stories[11]["summary"],
        "source_urls": deepdive_urls["oil-week-hormuz-saudis-2026-09-20"],
        "content": (
            "Crude ended an extraordinary week almost exactly where it began, but the surface calm masks some of the most violent intraday swings in months. Brent crude settled Friday at US$103.87 a barrel (down 0.9% on the day, and 0.7% for the week after briefly approaching US$110), while US benchmark WTI closed at US$100.30 after dipping below US$100 intraday. Both remained above the psychologically critical US$100 mark.\n\n"
            "The week was dominated by Saudi Arabia. Drone attacks damaged three pumping stations on the kingdom's East-West pipeline — the alternative export route that bypasses the Strait of Hormuz — after Houthi forces stepped up their naval blockade of Riyadh. That disruption initially sent Brent to US$108.75 on Tuesday and WTI to US$105.83, their highest closes since May, as Saudi Aramco suspended Yanbu loadings and warned European refiners they would receive no crude in October.\n\n"
            "Prices then retreated as alternatives emerged: Saudi Arabia arranged additional exports via ship-to-ship transfers near Sohar, Oman, easing fears of an immediate severe shortage, and Friday brought a further bearish catalyst when China — at Saudi request — urged Iran to help restrain Houthi attacks on Saudi oil infrastructure. Capital Economics nevertheless warned that Houthi advances and the stalled diplomacy raise the risk of a longer, more severe conflict keeping prices in triple digits well into 2027.\n\n"
            "The physical market is far from normal. Only four commodity vessels crossed the Strait of Hormuz on Thursday against a recent 10-day average of about 16, and North Sea-to-Mediterranean crude differentials are surging to records as the pipeline shutdown roils European physical markets. With Hormuz badly constrained and Saudi infrastructure still damaged, analysts say the direction next week may depend as much on tanker flows as on diplomatic headlines — with attention shifting to the UN General Assembly in New York, where Washington has reportedly allowed Iranian leaders to participate."
        )
    }
}

# chariklo + saudi deep-dives appended to the dict
deepdives["chariklo-rings-changing-2026-09-20"] = {
        "headline": "JWST watches a tiny asteroid's rings change over a decade",
        "summary": stories[10]["summary"],
        "source_urls": ["https://arstechnica.com/science/2026/09/rings-around-a-tiny-body-have-changed-over-the-past-decade/"],
        "content": (
            "Astronomers have long thought planetary rings were the preserve of the giant planets — Jupiter, Saturn, Uranus and Neptune. That changed in 2013 when a small, dark body orbiting between Saturn and Uranus passed in front of a distant star and 'blinked' twice, revealing two narrow rings around an object barely about 250 kilometres across, now known as Chariklo. Ever since, the question has been what such rings are made of and how long they can last.\n\n"
            "In a recent study, astronomer Pablo Santos-Sanz and colleagues used the James Webb Space Telescope to watch Chariklo pass in front of a background star again, this time at infrared wavelengths. The team found something striking: one of the asteroid's two rings has grown denser while the other has almost completely vanished. The change is dramatic enough that the researchers' models point toward real physical evolution of the rings rather than a trick of the telescope.\n\n"
            "The evidence is subtle but telling. The older visible-light observations were consistent with a mixture of ice and silicates, but once the JWST data points are added, no combination of materials and grain sizes could explain what the telescope recorded. 'We are witnessing a real evolution of the rings with time,' Santos-Sanz said, describing the physical change as the preferred explanation rather than a certainty. Notably, measured as equivalent width, the inner ring gained about ten times more than the outer ring lost — so material is not simply shifting inward.\n\n"
            "The finding, published in Science Advances, adds Chariklo to a growing list of small bodies now known to host rings: the similar body Chiron, the dwarf planet Haumea, and the trans-Neptunian object Quaoar. Giant-planet rings are already known to shift over months and years — Saturn's D ring has measurably shrunk and Neptune's Adams arcs rearrange themselves. That small, distant bodies also appear to evolve their rings over a human lifetime underscores how dynamic the solar system remains, even far from the planets we usually study."
        )
    }

deepdives["saudi-october-europe-crude-2026-09-20"] = {
        "headline": "Saudi Arabia tells European refiners to expect no crude in October as its East-West pipeline stays damaged",
        "summary": stories[12]["summary"],
        "source_urls": ["https://energynow.ca/2026/09/oil-ends-volatile-week-at-100-as-saudi-supply-fears-ease-but-hormuz-risks-persist/"],
        "content": (
            "Behind the headlines of crude prices easing back near US$100 a barrel lies a physical market that remains severely distorted by damage to Saudi Arabia's critical East-West pipeline. Drone attacks struck three pumping stations on the roughly 745-mile line — which bypasses the Strait of Hormuz and normally carries about 4 million barrels a day, some 4% of global output — and Saudi Aramco has been working to restore only about half its capacity.\n\n"
            "The consequences are falling hardest on European buyers. Saudi Aramco has told at least two European refiners they will receive no crude at all in October, a direct result of suspended Yanbu loadings. European physical crude markets are roiling: differentials for North Sea crude to the Mediterranean are surging to records as buyers scramble for alternative barrels, and European diesel remains exceptionally tight on top of an already inflated global market.\n\n"
            "Traders note that near-term supplies remain tight, reflected in a widening time spread — the unusually large gap between October and November WTI contracts has kept buyers on the acquisition side. At one point this week, the premium was more than US$5 a barrel, signalling how much the market fears a supply crunch before restoration efforts and alternative routings, including ship-to-ship transfers near Sohar in Oman, can compensate.\n\n"
            "The situation is a live illustration of how the Red Sea and Hormuz chokepoints have become the central fault line of the 2026 oil market: a single pipeline's closure, compounded by fierce Houthi-Saudi fighting, has ripple effects from the Gulf to European refineries and retail diesel pumps. With only a fraction of the line's capacity restored and no durable ceasefire in sight, analysts caution that the physical tightness — and its price consequences — could persist well into next year."
        )
    }

with open("/home/rory/Projects/news-pwa/deepdives.json") as f:
    dd = json.load(f)
d = dd["deepdives"]
if TODAY in d:
    del d[TODAY]
d[TODAY] = deepdives
with open("/home/rory/Projects/news-pwa/deepdives.json", "w") as f:
    json.dump(dd, f, ensure_ascii=False, indent=2)

print("OK — feed days:", [x["date"] for x in new_days][:3], "... total:", len(new_days))
print("deepdives for today:", len(deepdives))