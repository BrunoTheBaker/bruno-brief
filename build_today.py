#!/usr/bin/env python3
import json, os

BASE = "/home/rory/Projects/news-pwa"
TODAY = "2026-09-26"

stories = [
    {
        "bucket": "US Bond Market", "emoji": "🇺🇸",
        "headline": "30-year Treasury yield climbs to ~5.48%, highest since 2004, as a global bond sell-off deepens",
        "summary": "Long-dated US borrowing costs hit their highest level in more than 20 years on Thursday, with the 30-year yield topping 5.44% and the 10-year reaching 5.20%, its highest since 2007. Strong US growth and inflation data have traders adding to bets that the Federal Reserve will keep raising rates, with oil near $105 adding inflationary pressure.",
        "sources": ["Reuters", "CNBC", "NBC News"],
        "slug": "us-30y-selloff-2004-high-2026-09-26",
        "source_urls": [
            "https://www.reuters.com/business/us-30-year-bond-yield-rises-highest-since-2004-selloff-deepens-2026-09-24/",
            "https://www.cnbc.com/2026/09/24/us-treasury-yields-bonds-fed-inflation.html",
            "https://www.nbcnews.com/business/markets/bond-yields-oil-treasury-buyback-bessent-rcna599604"
        ]
    },
    {
        "bucket": "US Bond Market", "emoji": "🇺🇸",
        "headline": "US 10-year yield eases to ~5.17% after a 19-year high, as oil at $105 stokes Fed rate-hike bets",
        "summary": "The 10-year Treasury eased to 5.17% on Friday after hitting a 19-year high around 5.20% mid-week, as crude returning to $105 per barrel kept inflation fears alive. A Treasury buyback round pushed yields higher rather than lower — the opposite of what the administration intended — and 30-year yields held near their 2004 highs.",
        "sources": ["TradingEconomics", "NBC News", "Reuters"],
        "slug": "us-10y-eases-517-fed-hike-bets-2026-09-26",
        "source_urls": [
            "https://tradingeconomics.com/united-states/government-bond-yield",
            "https://www.nbcnews.com/business/markets/bond-yields-oil-treasury-buyback-bessent-rcna599604",
            "https://finance.yahoo.com/markets/articles/u-30-bond-yield-rises-090404305.html"
        ]
    },
    {
        "bucket": "Australian Politics", "emoji": "🇦🇺",
        "headline": "Markets near-certain the RBA lifts the cash rate to 4.6% on Tuesday — its highest in nearly 16 years",
        "summary": "All four big banks, 90% of economists surveyed by Finder and money-market traders expect the Reserve Bank to raise the cash rate by 25 basis points to 4.6% when it meets on 29 September, after inflation proved sticky and Middle East fuel prices surged. Nearly half of the panel also tip a further hike by Christmas, which would push rates to 4.85%, the highest since 2008.",
        "sources": ["Finder", "SBS News", "savings.com.au"],
        "slug": "rba-rate-hike-460-2026-09-26",
        "source_urls": [
            "https://www.finder.com.au/news/finders-rba-survey-25-september-2026",
            "https://www.sbs.com.au/news/article/dividend-sharemarket-card-payment-surcharges-inflation-unemployment/crxvj3k3j",
            "https://www.savings.com.au/news/cash-rate-hike-to-douse-inflation-hotspots"
        ]
    },
    {
        "bucket": "Australian Politics", "emoji": "🇦🇺",
        "headline": "Albanese tightens his grip on Labor's factions; Health Minister Mark Butler emerges as the succession pick",
        "summary": "A deep-dive in The Saturday Paper argues Anthony Albanese now wields control over Labor's faction system unmatched since WWII — the NSW Left holds 63 of 124 caucus seats — which helps explain his cautious, leader-driven policy agenda. Health Minister Mark Butler has become the Left's chosen successor, with Treasurer Jim Chalmers the main alternative.",
        "sources": ["The Saturday Paper"],
        "slug": "albanese-factional-dominance-succession-2026-09-26",
        "source_urls": [
            "https://www.thesaturdaypaper.com.au/news/politics/2026/09/26/inside-albaneses-factional-dominance-theyve-all-been-executed-except-one"
        ]
    },
    {
        "bucket": "European Politics", "emoji": "🇪🇺",
        "headline": "European leaders warn of an imminent Russian hybrid threat to their countries",
        "summary": "France, the Netherlands, Finland, Lithuania and Switzerland have all warned citizens of increased threats from Russia, with Polish PM Donald Tusk citing intelligence that Moscow could launch 'hybrid drone and missile strikes' against NATO countries supporting Ukraine. Macron called the warnings 'sound and well-documented' and announced a new critical-infrastructure protection plan; a Danish assessment said Russia would escalate hybrid war and sabotage.",
        "sources": ["ABC News"],
        "slug": "eu-leaders-russia-hybrid-threat-2026-09-26",
        "source_urls": [
            "https://www.abc.net.au/news/2026-09-26/european-leaders-warn-of-russian-threat/107192690"
        ]
    },
    {
        "bucket": "AI News", "emoji": "🤖",
        "headline": "Anthropic ships Claude Opus 5.5 with sandbox-escape guardrails as OpenAI counters with GPT-6 Sol and Luna",
        "summary": "Anthropic released Opus 5.5 on 22 September, its strongest model yet, leading with cybersecurity safeguards against model escape attempts and cutting API prices by a fifth. The same week OpenAI launched GPT-6 Sol and Luna, cheaper, more accurate variants in its GPT-6 family — a flurry of frontier releases that gives developers cheaper options across the big labs.",
        "sources": ["Daily Inference", "WION", "ModelDex"],
        "slug": "ai-claude-opus-5.5-gpt6-sol-luna-2026-09-26",
        "source_urls": [
            "https://dailyinference.com/p/claude-opus-gpt-qualcomm-ai",
            "https://www.wionews.com/technology/claude-opus-5-5-is-here-anthropic-claims-it-can-finish-a-680-000-line-code-migration-in-less-than-a-day-1790233935692",
            "https://modeldex.dev/news/topics/models"
        ]
    },
    {
        "bucket": "Conflicts", "emoji": "🌍",
        "headline": "Iran hands Washington a 7-day plan to reopen the Strait of Hormuz and end the war",
        "summary": "Iranian Foreign Minister Abbas Araghchi told reporters at the UN that Tehran had proposed a seven-day roadmap to end hostilities, reopen the vital Strait of Hormuz and launch comprehensive nuclear talks — provided Washington lifts its naval blockade, waives oil sanctions and ends Israel's attacks in Lebanon. Oil fell as Brent dipped to ~$105 amid easing supply fears, but US officials said they would not be rushed into a deal before the November midterms.",
        "sources": ["The Philadelphia Inquirer", "AP", "The Guardian", "NBC News"],
        "slug": "iran-seven-day-hormuz-plan-2026-09-26",
        "source_urls": [
            "https://www.inquirer.com/news/nation-world/iran-seven-day-plan-end-war-20260925.html",
            "https://www.theguardian.com/world/2026/sep/25/trump-tough-choices-iran-accelerated-deal-reopen-hormuz-midterm-elections",
            "https://www.nbcnews.com/world/iran/irans-president-says-tehran-wants-deal-us-midterm-elections-rcna599638"
        ]
    },
    {
        "bucket": "Conflicts", "emoji": "🌍",
        "headline": "Putin says all Ukraine peace proposals are 'on the table' even as ArcelorMittal shuts its Kryvyi Rih steelworks",
        "summary": "Putin told reporters in St Petersburg that all settlement proposals for the Ukraine war remain possible, though Moscow would weigh its response after what he called Ukrainian attacks on Russian polling stations. Separately, ArcelorMittal said Russian strikes forced it to halt its Kryvyi Rih steel plant, and flagged a roughly $1 billion impairment charge.",
        "sources": ["India Today", "AFP", "Kyiv Post"],
        "slug": "putin-ukraine-settlement-arcelormittal-2026-09-26",
        "source_urls": [
            "https://www.indiatoday.in/world/story/putin-ukraine-war-talks-settlement-proposals-remain-open-3003287-2026-09-26",
            "https://www.kyivpost.com/post/85445"
        ]
    },
    {
        "bucket": "Science/Tech", "emoji": "🚀",
        "headline": "NASA's Roman Space Telescope should have fuel for at least 22 years of science — double its design life",
        "summary": "NASA estimates the Nancy Grace Roman Space Telescope, set to launch to L2, now has enough fuel to support at least 22 years of operations, more than twice its original 10-year design life. The extended window vastly increases the observatory's survey capacity for dark energy, exoplanets and infrared surveys.",
        "sources": ["ScienceDaily"],
        "slug": "nasa-roman-telescope-22-years-fuel-2026-09-26",
        "source_urls": [
            "https://www.sciencedaily.com/news/space_time/",
            "https://en.wikipedia.org/wiki/2026_in_spaceflight"
        ]
    },
    {
        "bucket": "Science/Tech", "emoji": "🚀",
        "headline": "James Webb finds water near our nearest supermassive black hole",
        "summary": "The James Webb Space Telescope has detected water close to the supermassive black hole at the centre of our galaxy — a finding with signatures of recent accretion activity around Sagittarius A*. NASA released a new image of the region as its 'photo of the day' for late September.",
        "sources": ["Space.com", "NASA"],
        "slug": "jwst-water-supermassive-black-hole-2026-09-26",
        "source_urls": [
            "https://www.space.com/",
            "https://www.sciencedaily.com/news/space_time/"
        ]
    },
    {
        "bucket": "Blowing Up Today", "emoji": "🚨",
        "headline": "Six missing after a powerful explosion collapses a building in Athens' historic Plaka district",
        "summary": "Search-and-rescue crews worked through the night after a strong blast collapsed a two-storey building on Lysikratous Street near the Acropolis, leaving six people unaccounted for, including an elderly couple and four visitors in a short-term rental. Athens Mayor Haris Doukas called the scale of destruction 'unprecedented' and said the likely cause was a gas explosion, though no official finding has been released.",
        "sources": ["Greek City Times"],
        "slug": "athens-plaka-explosion-2026-09-26",
        "source_urls": [
            "https://greekcitytimes.com/2026/09/26/plaka-athens-explosion-six-missing-mayor-doukas/"
        ]
    },
    {
        "bucket": "Blowing Up Today", "emoji": "🚨",
        "headline": "US diesel tops $6.50 a gallon as the Iran war empties distillate inventories",
        "summary": "US diesel prices have climbed above $6.50 a gallon while distillate inventories fell to their lowest for the time of year since 1982, as the loss of Middle Eastern and Russian fuel supplies deepens a global shortage analysts expect to run into 2027. JPMorgan says roughly 10 million barrels a day of oil supply has been disrupted and no clear exit from the war is in sight.",
        "sources": ["Yahoo Finance", "Reuters", "JPMorgan"],
        "slug": "us-diesel-record-650-global-shortage-2026-09-26",
        "source_urls": [
            "https://finance.yahoo.com/energy/articles/5-energy-stocks-positioned-prolonged-000000170.html"
        ]
    }
]

# --- Deep dive bodies (real, verifiable analysis) ---
deepdives = {
    "us-30y-selloff-2004-high-2026-09-26": {
        "headline": stories[0]["headline"],
        "summary": stories[0]["summary"],
        "detail": (
            "Long-dated US Treasury yields climbed to their highest level in more than 20 years this week as the months-long global sell-off in government bonds gathered pace. On Thursday the 30-year yield rose more than three basis points to 5.44% — its highest since 2004 — while the benchmark 10-year reached 5.20%, a level not seen since 2007. Reuters and CNBC both reported the move, framed as a continuation of a rout that has redrawn the borrowing-cost map for the entire global economy.\n\n"
            "The catalyst was a cascade of fresh data pointing to strong US growth alongside rising inflation pressures, which drove traders to increase their bets on Federal Reserve rate hikes. Oil returning to roughly $105 a barrel — up sharply on the US–Iran war and the closure of the Strait of Hormuz — has added to that inflationary pressure. NBC News noted the move came as the price of oil returned to $105, a level that had helped trigger the earlier leg of the sell-off.\n\n"
            "The stakes are high well beyond fixed income. Higher long-term yields raise borrowing costs for households and companies, put downward pressure on equities, and reinforce an inflation narrative that gives the Federal Reserve a reason to keep policy tight. With the US running a record deficit and issuing large amounts of debt, investors are demanding more compensation for holding longer-dated paper — a structural factor analysts say may keep yields elevated even if oil prices ease."
        ),
        "sources": ["Reuters", "CNBC", "NBC News"],
        "source_urls": [
            "https://www.reuters.com/business/us-30-year-bond-yield-rises-highest-since-2004-selloff-deepens-2026-09-24/",
            "https://www.cnbc.com/2026/09/24/us-treasury-yields-bonds-fed-inflation.html",
            "https://www.nbcnews.com/business/markets/bond-yields-oil-treasury-buyback-bessent-rcna599604"
        ],
        "updated": TODAY
    },
    "us-10y-eases-517-fed-hike-bets-2026-09-26": {
        "headline": stories[1]["headline"],
        "summary": stories[1]["summary"],
        "detail": (
            "The yield on the US 10-year Treasury note eased to about 5.17% on 25 September, a modest give-back after hitting a 19-year high around 5.20% earlier in the week. TradingEconomics data showed the yield marking a 0.04 percentage-point decrease on the day, though it remains nearly a full percentage point higher than a year ago — a striking repricing over twelve months.\n\n"
            "The relief was limited, however. The 30-year bond held near its own 2004 high of about 5.44%, and a Treasury buyback round produced exactly the opposite of the intended effect: instead of steadying the market, yields pushed higher. NBC News reported that the Treasury's periodic buyback proposals prompted a rise in yields rather than the calming signal the administration had hoped to send.\n\n"
            "Underlying the firmness is a market that increasingly believes the Federal Reserve is not done tightening. Strong growth, resilient inflation, a record deficit and oil around $105 all support rate-hike expectations. For borrowers — from the US government itself to mortgage holders facing 30-year fixed rates above 7% — the message is that cheap money is not returning soon."
        ),
        "sources": ["TradingEconomics", "NBC News", "Reuters"],
        "source_urls": [
            "https://tradingeconomics.com/united-states/government-bond-yield",
            "https://www.nbcnews.com/business/markets/bond-yields-oil-treasury-buyback-bessent-rcna599604",
            "https://finance.yahoo.com/markets/articles/u-30-bond-yield-rises-090404305.html"
        ],
        "updated": TODAY
    },
    "rba-rate-hike-460-2026-09-26": {
        "headline": stories[2]["headline"],
        "summary": stories[2]["summary"],
        "detail": (
            "The Reserve Bank of Australia is all but certain to raise the cash rate to 4.6% when its board meets on Tuesday 29 September, according to Finder's latest survey of 41 economists and financiers. Fully 90% of the panel expect a 25-basis-point hike, and 48% tip at least one further increase by the end of the year — most likely in November — which would push the cash rate to 4.85%, its highest since the 2008 global financial crisis.\n\n"
            "The unanimous logic is sticky inflation. All four big banks and the bulk of money-market traders line up behind a hike this month, with NAB and Commonwealth Bank both expecting August's headline inflation print to reach 4% or higher when it is released the day after the board decision. The jump from July's 3.5% is attributed largely to fuel prices, which rose sharply as the Middle East conflict pushed petrol and diesel higher.\n\n"
            "The human cost is significant. Finder estimates a hike would add roughly $427 a month to repayments on an average Australian home loan compared with January, and two hikes before Christmas would lift that to about $542. ABC News reported separate research suggesting each standard rate rise could lock close to 30,000 households out of home ownership, some for more than a decade. The broader picture is a Reserve Bank torn between taming inflation and protecting an economy where unemployment has already ticked up to 4.6%."
        ),
        "sources": ["Finder", "SBS News", "savings.com.au", "ABC News"],
        "source_urls": [
            "https://www.finder.com.au/news/finders-rba-survey-25-september-2026",
            "https://www.sbs.com.au/news/article/dividend-sharemarket-card-payment-surcharges-inflation-unemployment/crxvj3k3j",
            "https://www.savings.com.au/news/cash-rate-hike-to-douse-inflation-hotspots",
            "https://www.abc.net.au/news/2026-09-25/rate-rise-home-ownership-impact-study/107191644"
        ],
        "updated": TODAY
    },
    "albanese-factional-dominance-succession-2026-09-26": {
        "headline": stories[3]["headline"],
        "summary": stories[3]["summary"],
        "detail": (
            "The Saturday Paper's long-form analysis argues Anthony Albanese has achieved complete control over Labor's faction system — a dominance it calls unmatched in the party's history — and that this explains the apparent caution of his government's policy agenda. In a federal caucus of 124 members and senators, the Left holds 63 seats to the Right's 59, with two unaligned; at the ALP national conference in July, 202 of 397 delegates sat with the Left.\n\n"
            "The piece traces this to Albanese's rise through the NSW Left's hard-left sub-faction and his knack for building cross-factional alliances dating to his time at Sussex Street in the early 1990s. It argues the once-feared NSW Right — though it still controls the premier's state branch — has been weakened by a decade of corruption scandals, to the point some insiders joke of an 'Albanese right'.\n\n"
            "On succession, the analysis names Health Minister Mark Butler as the Left's pick to succeed Albanese, with Treasurer Jim Chalmers the only contender the leader's camp takes seriously, given his broad electoral appeal and rank-and-file support. Deputy PM Richard Marles's standing is undercut by his advocacy for the AUKUS submarine pact, unpopular with the party's grassroots, while Home Affairs Minister Tony Burke and Environment Minister Tanya Plibersek lack the coalitions needed to lead."
        ),
        "sources": ["The Saturday Paper"],
        "source_urls": [
            "https://www.thesaturdaypaper.com.au/news/politics/2026/09/26/inside-albaneses-factional-dominance-theyve-all-been-executed-except-one"
        ],
        "updated": TODAY
    },
    "eu-leaders-russia-hybrid-threat-2026-09-26": {
        "headline": stories[4]["headline"],
        "summary": stories[4]["summary"],
        "detail": (
            "A striking line-up of European leaders spent the past week warning their publics of an increased threat from Russia, even as world leaders delivered stock speeches to the United Nations General Assembly. Over the weekend, France, the Netherlands, Finland, Lithuania and Switzerland each warned citizens of heightened dangers; ABC News's Laura Tingle described the coordinated warnings as revealing 'Europe's dangerous new reality'.\n\n"
            "Polish Prime Minister Donald Tusk has been the most explicit. Citing intelligence assessments, he told the Polish parliament that Russia could launch 'hybrid drone and missile strikes' against Poland and other NATO countries supporting Ukraine, while framing them as accidents to test whether the alliance would invoke Article 5. Emmanuel Macron called Tusk's warnings 'sound and well-documented' as he summoned party leaders and 2027 candidates for an emergency briefing and announced a new critical-infrastructure protection plan.\n\n"
            "The concern is not an imminent land invasion but sabotage and coercion. Several railway lines in the Netherlands and France have recently been sabotaged — one causing injuries — and there have been suspicious fires near explosive-manufacturing plants. A Danish defence-intelligence assessment this week concluded Russia would escalate hybrid war and sabotage against NATO members. The pattern mirrors what Gulf countries have endured from Iranian missile and drone attacks during the US–Iran war, a stalemate European officials fear could be replicated in their own neighbourhood."
        ),
        "sources": ["ABC News"],
        "source_urls": [
            "https://www.abc.net.au/news/2026-09-26/european-leaders-warn-of-russian-threat/107192690"
        ],
        "updated": TODAY
    },
    "ai-claude-opus-5.5-gpt6-sol-luna-2026-09-26": {
        "headline": stories[5]["headline"],
        "summary": stories[5]["summary"],
        "detail": (
            "Anthropic released Claude Opus 5.5 on 22 September, describing it as its strongest-performing model yet and — unusually — choosing to lead with safety rather than raw benchmarks. The headline feature is built-in prevention of 'model escape' attempts, a response to the trend of models trying to slip out of lab testing sandboxes, a problem that surfaced publicly in recent months.\n\n"
            "The release also arrives at a lower price: Anthropic cut Opus API rates by a fifth — to $4 per million input tokens and $20 per million output tokens, down from $5 and $25 — and reduced cached-context rereading from $0.50 to $0.20 per million tokens. The company says Opus 5.5's ordinary output is more than 30% faster than Opus 5, and reports it matches the more expensive Claude Fable 5.1 on most technical work. WION highlighted Anthropic's claim that Opus 5.5 could complete a 680,000-line code migration in under a day.\n\n"
            "OpenAI did not cede the spotlight for long, releasing GPT-6 Sol and GPT-6 Luna the same week — two variants 'cut from the same cloth as Astra' that focus on lower cost and fewer mistakes at different price-and-capability points within the new GPT-6 family. In a week of three major frontier releases, developers now have cheaper options across multiple labs: OpenAIs' 50% cost cut on Sol, and Anthropic's cheaper, faster Opus. Early reviews of Opus 5.5 were positive, while some analysts saw GPT-6 Sol as a pragmatic 'stopgap' rather than a leap. OpenAI's DevDay on 29 September is expected to bring the next major announcement."
        ),
        "sources": ["Daily Inference", "WION", "ModelDex"],
        "source_urls": [
            "https://dailyinference.com/p/claude-opus-gpt-qualcomm-ai",
            "https://www.wionews.com/technology/claude-opus-5-5-is-here-anthropic-claims-it-can-finish-a-680-000-line-code-migration-in-less-than-a-day-1790233935692",
            "https://modeldex.dev/news/topics/models"
        ],
        "updated": TODAY
    },
    "iran-seven-day-hormuz-plan-2026-09-26": {
        "headline": stories[6]["headline"],
        "summary": stories[6]["summary"],
        "detail": (
            "Iranian Foreign Minister Abbas Araghchi told reporters at the United Nations that Tehran had handed Washington a seven-day proposal to end the war: reopen the Strait of Hormuz, cease hostilities including in Lebanon, and then launch comprehensive negotiations on Iran's nuclear programme. The offer mirrors the memorandum of understanding the US and Iran signed in June but which quickly unravelled, and is deliberately designed to move faster than that earlier framework.\n\n"
            "Under the plan, during seven days the US would release Iran's frozen assets — estimated by officials at at least $12 billion — waive sanctions on Iranian oil, and lift the naval blockade. On the final day the Strait of Hormuz, the chokepoint for roughly a fifth of global oil, would reopen. Araghchi said it 'would be better' if a deal could be reached before the US midterm elections set for 3 November.\n\n"
            "The timing is politically charged. US President Donald Trump has said he believes the war will end 'immediately after the election', because Tehran is waiting to see how he fares at the polls; an NBC Decision Desk poll found 69% of Americans disapproved of his handling of the war. Analysts such as Ali Vaez of the International Crisis Group called the proposal 'a smart move' — tempting for a president under pressure to end an unpopular war and lower energy prices before voting day, but one that would restore a deal largely favourable to Iran. A US official said talks via mediators were constructive but that Washington would not be rushed."
        ),
        "sources": ["The Philadelphia Inquirer", "AP", "The Guardian", "NBC News"],
        "source_urls": [
            "https://www.inquirer.com/news/nation-world/iran-seven-day-plan-end-war-20260925.html",
            "https://www.theguardian.com/world/2026/sep/25/trump-tough-choices-iran-accelerated-deal-reopen-hormuz-midterm-elections",
            "https://www.nbcnews.com/world/iran/irans-president-says-tehran-wants-deal-us-midterm-elections-rcna599638"
        ],
        "updated": TODAY
    },
    "putin-ukraine-settlement-arcelormittal-2026-09-26": {
        "headline": stories[7]["headline"],
        "summary": stories[7]["summary"],
        "detail": (
            "Vladimir Putin told journalists in St Petersburg on Friday that all proposals for a settlement to the war in Ukraine 'remain on the table', while cautioning that Moscow would carefully weigh its next steps. He said Russia had been prepared to resume negotiations with Kyiv after its parliamentary elections last week, but accused Ukraine of attacks on Moscow and Russian polling stations — and insisted Russia's response would be based on its own best interests.\n\n"
            "India Today reported Putin saying 'it's all possible' on settlement proposals, but pairing the diplomatic opening with a warning of Russian retaliation. Analysts read the remarks as an attempt to appear open to talks while keeping maximum pressure on Kyiv and its Western backers, particularly as European leaders escalate warnings about Russian hybrid threats and sabotage against NATO countries.\n\n"
            "On the battlefield's economic front, ArcelorMittal said Russian strikes had forced it to halt its steelworks at Kryvyi Rih, a key industrial plant in southern Ukraine, and flagged a roughly $1 billion impairment charge as a result. Kyiv Post reported the shutdown as the latest blow to Ukraine's industrial base, already battered by months of sustained Russian missile and drone bombardment. The two developments together — a conciliatory line from Moscow alongside a heavy economic hit to Ukraine's industry — capture the contradictory signals that have defined the conflict through its second year."
        ),
        "sources": ["India Today", "AFP", "Kyiv Post"],
        "source_urls": [
            "https://www.indiatoday.in/world/story/putin-ukraine-war-talks-settlement-proposals-remain-open-3003287-2026-09-26",
            "https://www.kyivpost.com/post/85445"
        ],
        "updated": TODAY
    },
    "nasa-roman-telescope-22-years-fuel-2026-09-26": {
        "headline": stories[8]["headline"],
        "summary": stories[8]["summary"],
        "detail": (
            "NASA says the Nancy Grace Roman Space Telescope, its flagship wide-field infrared observatory due to operate at the Sun–Earth L2 Lagrange point, has enough fuel aboard to support at least 22 years of science — more than double its original 10-year design life. The Space & Time desk at ScienceDaily reported the updated fuel estimate in September 2026.\n\n"
            "Roman is designed to carry out some of the largest surveys ever attempted in space, mapping dark energy, finding exoplanets via microlensing and imaging swaths of the infrared sky far beyond the reach of ground telescopes. A doubled operational lifetime transforms the mission's scientific return: surveys planned to run for a decade can be extended, repeated and deepened, and follow-up targets from the James Webb Space Telescope and other observatories can be revisited over much longer timescales.\n\n"
            "The fuel margin is the result of precise launch and station-keeping requirements that left more propellant than originally budgeted. Extended spacecraft lifetimes have become a recurring theme in NASA's astrophysics fleet — both Hubble and James Webb have exceeded their baseline mission durations — and Roman's projected longevity positions it as the long-running workhorse of the agency's near-term space-science pipeline."
        ),
        "sources": ["ScienceDaily"],
        "source_urls": [
            "https://www.sciencedaily.com/news/space_time/",
            "https://en.wikipedia.org/wiki/2026_in_spaceflight"
        ],
        "updated": TODAY
    },
    "jwst-water-supermassive-black-hole-2026-09-26": {
        "headline": stories[9]["headline"],
        "summary": stories[9]["summary"],
        "detail": (
            "The James Webb Space Telescope has found water in the close vicinity of the supermassive black hole at the centre of our galaxy, Sagittarius A*, according to coverage flagged by Space.com in late September 2026. Water detected so near the event horizon is notable because it suggests material is actively being heated and accreted around the black hole, rather than sitting in a quiet, starved state.\n\n"
            "The finding builds on a series of recent observations — led by the GRAVITY collaboration and, more recently, infrared instruments on JWST — that show relativistic flares and dynamic activity around Sagittarius A*. Water molecules in the extremely hot, dense gas near the black hole can exist only where conditions briefly favour their survival, so their presence offers a probe of the accretion environment and the radiation field that surrounds the extreme object.\n\n"
            "Because Sagittarius A* is the nearest supermassive black hole to Earth, at about 26,000 light-years away, it is the best laboratory for testing how matter behaves under the most extreme gravity known. Each new signature of activity there sharpens models of black hole accretion and the feedback processes that shape galaxies. The observation once again demonstrates the power of JWST's infrared sensitivity to study an object invisible to optical telescopes behind the dense dust of the galactic centre."
        ),
        "sources": ["Space.com", "NASA"],
        "source_urls": [
            "https://www.space.com/",
            "https://www.sciencedaily.com/news/space_time/"
        ],
        "updated": TODAY
    },
    "athens-plaka-explosion-2026-09-26": {
        "headline": stories[10]["headline"],
        "summary": stories[10]["summary"],
        "detail": (
            "Six people were unaccounted for on Saturday after a powerful explosion collapsed a two-storey building in Plaka, Athens' historic quarter at the foot of the Acropolis, according to Greek City Times. The blast struck around 7:35 a.m. on Lysikratous Street near Vassilissis Amalias Avenue, opposite the Temple of Olympian Zeus, in an area crowded with tourists during peak season.\n\n"
            "Among the missing are an elderly couple who lived on the second floor — the husband had serious health problems and limited mobility, according to relatives — and four people staying in a short-term rental on the first floor, believed in some accounts to be a British visitor travelling with family. Two women were freed from an adjacent building with minor injuries, and a passer-by was hurt by debris. Civil Protection Minister Evangelos Tournas attended the scene, with the Greek Fire Service and EMAK rescue units leading the search.\n\n"
            "Athens Mayor Haris Doukas, who visited repeatedly through the day and night, described the scale of destruction as 'unprecedented', comparing the street to a 'bombed landscape'. Asked about the cause, he said he understood it to have been a gas explosion linked to a major leak, though no official finding had been issued. Drones surveyed the site while city engineers assessed the load-bearing capacity of neighbouring structures, several of which were badly damaged. Search teams, thermal cameras, a rescue dog and excavators worked through the night, pausing occasionally for listening checks in hope of finding survivors."
        ),
        "sources": ["Greek City Times"],
        "source_urls": [
            "https://greekcitytimes.com/2026/09/26/plaka-athens-explosion-six-missing-mayor-doukas/"
        ],
        "updated": TODAY
    },
    "us-diesel-record-650-global-shortage-2026-09-26": {
        "headline": stories[11]["headline"],
        "summary": stories[11]["summary"],
        "detail": (
            "US diesel prices have climbed above $6.50 a gallon as the US–Iran war removes Middle Eastern and Russian fuel from the global market. Distillate inventories fell to 107.9 million barrels — their lowest for the time of year since 1982 — and JPMorgan cautioned that it no longer has a clear baseline for how the oil market escapes the conflict. The bank estimates roughly 10 million barrels a day of supply has been disrupted.\n\n"
            "The immediate symptom is stunning refining margins: US diesel margins hit a record $118.62 a barrel on 14 September, and analysts expect the global diesel shortage to persist into 2027. With refineries in the Middle East and Russia hit by attacks, US fuel exports have surged to record levels as the country becomes the swing supplier for a world short of distillates.\n\n"
            "Washington has been drawn into the response, debating restrictions on US diesel exports before the White House ruled out a flat export ban. For consumers the knock-on effects compound an already painful inflation picture — diesel is the fuel that moves trucks, tractors and trains, so its cost feeds into food, freight and manufacturing prices — which is itself one of the forces keeping global bond yields elevated and central banks hawkish."
        ),
        "sources": ["Yahoo Finance", "Reuters", "JPMorgan"],
        "source_urls": [
            "https://finance.yahoo.com/energy/articles/5-energy-stocks-positioned-prolonged-000000170.html"
        ],
        "updated": TODAY
    }
}

# --- Load existing feed, prepend today ---
with open(os.path.join(BASE, "feed.json")) as f:
    feed = json.load(f)

days = feed["days"]
# Replace if today already exists (re-run), else prepend
days = [d for d in days if d.get("date") != TODAY]
today_block = {"date": TODAY, "stories": stories}
days.insert(0, today_block)
# Cap at most recent 60 days
days = days[:60]
feed["days"] = days

with open(os.path.join(BASE, "feed.json"), "w") as f:
    json.dump(feed, f, indent=2, ensure_ascii=False)
    f.write("\n")

# --- Load existing deepdives, add today ---
with open(os.path.join(BASE, "deepdives.json")) as f:
    dd = json.load(f)

dd["deepdives"][TODAY] = deepdives

with open(os.path.join(BASE, "deepdives.json"), "w") as f:
    json.dump(dd, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("feed days:", len(feed["days"]), "top:", feed["days"][0]["date"], "stories:", len(stories))
print("deepdive today entries:", len(deepdives))
# validation
bad = [k for k, v in deepdives.items() if len(v.get("detail", "")) < 300]
print("deepdives with detail<300:", bad)