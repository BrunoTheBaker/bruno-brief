#!/usr/bin/env python3
import json

FEED = "/home/rory/Projects/news-pwa/feed.json"
DEEP = "/home/rory/Projects/news-pwa/deepdives.json"
TODAY = "2026-09-17"

today_stories = [
    {
        "bucket": "US Bond Market", "emoji": "🇺🇸",
        "headline": "Federal Reserve hikes rates 25bp to 3.75%-4%, first increase since 2023",
        "summary": "The FOMC raised the federal funds rate by a quarter point to 3.75%-4% on Sept 16, citing price stability as its top priority amid spiraling oil prices, and signalled one more hike before year-end. It was the Fed's first rate rise in more than three years.",
        "sources": ["CNBC", "Federal Reserve", "Fox Business"],
        "slug": "fed-rate-hike-375-4-2026-09-17"
    },
    {
        "bucket": "US Bond Market", "emoji": "🇺🇸",
        "headline": "10-year Treasury yield tops 5%, highest since July 2007",
        "summary": "The 10-year Treasury yield climbed back above 5% to 5.02% after the Fed's hike, the highest since 2007, as investors demanded more compensation for inflation and record deficits. The yield has risen ~29.5bp in four weeks and ~98.6bp over the past year.",
        "sources": ["TradingEconomics", "CNBC"],
        "slug": "us-10y-tops-5-percent-2026-09-17"
    },
    {
        "bucket": "Australian Politics", "emoji": "🇦🇺",
        "headline": "Burke unveils immigration overhaul: student families barred, backpacker ballot, 77,000 overstayers targeted",
        "summary": "Immigration Minister Tony Burke finally unveiled Labor's migration shake-up at a National Press Club speech — banning international students' families, introducing a backpacker ballot system and directing Border Force to crack down on 77,000 visa overstayers, with no new legislation required. The National Farmers' Federation warned it would push up food prices.",
        "sources": ["SMH", "ABC News", "news.com.au"],
        "slug": "burke-migration-overhaul-2026-09-17"
    },
    {
        "bucket": "Australian Politics", "emoji": "🇦🇺",
        "headline": "RBA rate-hike odds jump to ~90% after Fed's move",
        "summary": "Markets now price a nearly 90% chance the Reserve Bank lifts Australia's cash rate at its Sept 29 meeting — a 25bp increase would take it to 4.85% — in direct response to the US Federal Reserve's hike and surging bond yields, adding to mortgage pressure.",
        "sources": ["ABC News", "Sydney Times"],
        "slug": "rba-rate-hike-odds-90-2026-09-17"
    },
    {
        "bucket": "European Politics", "emoji": "🇪🇺",
        "headline": "Von der Leyen's State of the Union: Canada announcement, under-13s social media ban, new European Security Council",
        "summary": "In her Sept 16 State of the Union address in Strasbourg, Commission President Ursula von der Leyen announced closer cooperation with Canada, proposed a social media ban for under-13s and called for a new European Security Council, while mapping an industrial-AI roadmap as the bloc trails the US and China.",
        "sources": ["The Parliament Magazine", "European Commission"],
        "slug": "soteu-vdl-2026-2026-09-17"
    },
    {
        "bucket": "AI News", "emoji": "🤖",
        "headline": "OpenAI, Anthropic and Google DeepMind confirm weeks of AI safety talks",
        "summary": "OpenAI's global policy chief Chris Lehane confirmed the three frontier labs have been working together on AI safety for weeks, following Anthropic CEO Dario Amodei's call for the industry to slow down. OpenAI also said it backs the FRONTIER Act requiring independent safety assessments — while Trump's team dismisses existential-risk fears as overblown.",
        "sources": ["TechCrunch", "CNBC", "Bloomberg"],
        "slug": "openai-anthropic-google-safety-talks-2026-09-17"
    },
    {
        "bucket": "AI News", "emoji": "🤖",
        "headline": "Amodei's 'slow down' essay roils the industry: executives answer, senators float banning superintelligence",
        "summary": "After Dario Amodei published an essay urging every frontier lab to slow its pace of development, Microsoft, OpenAI and xAI chiefs responded, a US senator proposed banning superintelligence outright, and Trump called Amodei a 'perfect little angel' on Truth Social — while dismissing the safety case as a hoax.",
        "sources": ["TechCrunch", "CNBC"],
        "slug": "amodei-slow-down-essay-2026-09-17"
    },
    {
        "bucket": "Conflicts", "emoji": "⚔️",
        "headline": "Russia launches 157 drones and missiles at Ukraine; Kyiv hit, 16 injured",
        "summary": "Russia attacked Ukraine overnight with 157 drones and ballistic and cruise missiles; Ukraine's air defences destroyed 131 aerial assets but hits were recorded at 36 locations, including Kyiv where at least 16 people were injured and an education facility damaged.",
        "sources": ["RBC-Ukraine", "Kyiv Independent", "Ukrainian Pravda"],
        "slug": "russia-157-drones-ukraine-2026-09-17"
    },
    {
        "bucket": "Conflicts", "emoji": "🌍",
        "headline": "Trump says US 'nearing the end' of Iran war, claims direct talks with Tehran",
        "summary": "At a campaign rally hours after Iran fired missiles at US targets in Jordan, President Trump said the US is nearing the end of its conflict with Iran and claimed Washington is in direct talks with Tehran, as pump prices and the Strait of Hormuz loom over the midterms.",
        "sources": ["Al Jazeera", "GlobalSecurity.org"],
        "slug": "trump-iran-nearing-end-direct-talks-2026-09-17"
    },
    {
        "bucket": "Science/Tech", "emoji": "🔬",
        "headline": "Eight-year Finnish study: more childhood screen time linked to better teen cognition",
        "summary": "Following 260 children for eight years, researchers at the universities of Jyväskylä and Eastern Finland found those with more screen time since childhood tended to show better cognitive processing as teenagers — challenging the view of screens as wholly harmful, with the type of screen activity seen as key.",
        "sources": ["ScienceDaily", "University of Eastern Finland"],
        "slug": "finland-screen-time-cognition-2026-09-17"
    },
    {
        "bucket": "Science/Tech", "emoji": "🚀",
        "headline": "China's Gravity-1 sets sea-launch records deploying Spacesail satellites",
        "summary": "Private rocket maker Orienspace lofted nine satellites from a ship in the East China Sea — its biggest, most powerful solid-propellant rocket yet — setting national records for payload weight (over 3 tonnes) and orbit altitude (800km) for a sea launch, and flying its first mission for the Spacesail internet constellation.",
        "sources": ["Xinhua", "China Daily"],
        "slug": "china-gravity1-sea-launch-2026-09-17"
    },
    {
        "bucket": "Science/Tech", "emoji": "🚀",
        "headline": "NASA's Lunar Reconnaissance Orbiter finds giant new crater on the Moon",
        "summary": "Scientists revealed a steep-sided impact crater about 728 feet across and 141 feet deep — bigger than the Roman Colosseum and formed by a strike two years ago that went undetected — the solar system's biggest known crater carved out in recent times, per NASA's LRO.",
        "sources": ["AP (via NY Post)"],
        "slug": "lro-new-moon-crater-2026-09-17"
    },
    {
        "bucket": "Blowing Up Today", "emoji": "🚨",
        "headline": "Trump lashes out at his Supreme Court picks over mail-ballot ruling",
        "summary": "President Trump launched a fresh attack on the Supreme Court justices he appointed after the Court blocked his administration's plan to tighten mail-in voting rules weeks before the midterms, a ruling that could reshape how ballots are counted in November.",
        "sources": ["TIME", "NYT", "POLITICO"],
        "slug": "trump-scotus-mail-ballot-2026-09-17"
    },
]

# --- write feed.json ---
with open(FEED) as f:
    feed = json.load(f)

# remove any existing entry for today (re-run safety)
feed["days"] = [d for d in feed["days"] if d.get("date") != TODAY]
feed["days"].insert(0, {"date": TODAY, "stories": today_stories})
# cap timeline at 60 days
feed["days"] = feed["days"][:60]
with open(FEED, "w") as f:
    json.dump(feed, f, ensure_ascii=False, indent=2)

# --- write deepdives.json ---
with open(DEEP) as f:
    deep = json.load(f)

def dd(slug, headline, summary, detail, sources, urls):
    return {"headline": headline, "summary": summary, "detail": detail,
            "sources": sources, "source_urls": urls, "updated": TODAY}

deep["deepdives"][TODAY] = {
    "fed-rate-hike-375-4-2026-09-17": dd(
        "fed-rate-hike-375-4-2026-09-17",
        "Federal Reserve hikes rates 25bp to 3.75%-4%, first increase since 2023",
        "The FOMC raised the federal funds rate by a quarter point and signalled one more hike this year, its first rate rise since 2023, driven by oil-driven inflation.",
        "The Federal Reserve delivered its most consequential policy move in years on September 16, raising the federal funds rate by 25 basis points to a target range of 3.75% to 4% — the first hike since 2023. The decision passed on a 12-0 vote, with the Committee explicitly citing price stability as its top priority.\\n\\nThe trigger is the energy shock. Spiraling oil prices, driven by the US-Iran war and the disruption of the Strait of Hormuz and Saudi infrastructure, have pushed inflation expectations higher even as domestic spending stays resilient. The Fed's own projections released with the decision showed PCE inflation running at 3.7% for 2026 before easing toward 2.3% in 2027.\\n\\nThe unanimous vote and the explicit signal of 'one more to come' this year mark a pivot from the easing stance of recent years. Fox Business reported the Committee flagged the possibility of an additional hike before year-end, and markets promptly repriced. For borrowers and investors alike, the move confirms that the era of ultra-low rates is over and that the Fed is now actively fighting an inflation battle primed by war-driven energy costs.",
        ["CNBC", "Federal Reserve", "Fox Business"],
        ["https://www.cnbc.com/2026/09/16/fed-rate-decision-september-2026.html",
         "https://www.federalreserve.gov/monetarypolicy/files/monetary20260916a1.pdf",
         "https://www.foxbusiness.com/economy/federal-reserve-interest-rate-decision-september-16-2026"]
    ),
    "burke-migration-overhaul-2026-09-17": dd(
        "burke-migration-overhaul-2026-09-17",
        "Burke unveils immigration overhaul: student families barred, backpacker ballot, 77,000 overstayers targeted",
        "Immigration Minister Tony Burke finally detailed Labor's migration cuts: banning student families, a backpacker ballot and a crackdown on 77,000 visa overstayers.",
        "After weeks of internal negotiation and pressure from One Nation's migration platform, Immigration Minister Tony Burke used a National Press Club address to finally spell out Labor's own migration reset. The package is engineered to bring net overseas migration down without new legislation, using ministerial powers already on the books.\\n\\nThe headline measures: immediate barring of international students' families from accompanying them, a new ballot system for working-holiday (backpacker) visas to ration numbers, and a Border Force push targeting roughly 77,000 visa overstayers. Burke used the speech to attack One Nation's 'net-negative' migration policy, positioning Labor's plan as a middle path that trims numbers without the sweeping cuts the minor party has proposed.\\n\\nThe reaction was immediate and split. The National Farmers' Federation warned that cutting the backpacker workforce would push food prices up and leave supermarket shelves emptier, while business groups that had praised One Nation's plan found themselves re-examining the government's arithmetic. The absence of fresh legislation means the changes can be tightened or reversed quickly — keeping migration firmly on the table as a live political weapon in the run to the next election.",
        ["SMH", "ABC News", "news.com.au"],
        ["https://www.smh.com.au/politics/federal/australia-immigration-announcement-live-updates-tony-burke-to-unveil-major-changes-to-migration-system-in-national-press-club-speech-20260916-p60xxf.html",
         "https://www.abc.net.au/news/2026-09-17/federal-politics-live-blog-sept-17/107161304",
         "https://www.news.com.au/national/politics/border-force-to-target-77000-visa-overstayers-in-crackdown/news-story/12331081fdf6afe419e714502ae7dffa"]
    ),
    "rba-rate-hike-odds-90-2026-09-17": dd(
        "rba-rate-hike-odds-90-2026-09-17",
        "RBA rate-hike odds jump to ~90% after Fed's move",
        "Markets now price a near-90% chance the RBA lifts rates at its Sept 29 meeting, a 25bp rise taking the cash rate to 4.85%.",
        "The Fed's decision rippled directly into Australian monetary policy expectations. Within a day of the US hike, financial markets were pricing in a nearly 90% probability that the Reserve Bank of Australia would lift the cash rate at its September 29 meeting.\\n\\nThe trigger is a mix of domestic inflation pressure and spillover: surging global bond yields have pushed the ASX 200 to a two-month low this month, and the Fed's tightening gives the RBA both cover and reason to follow. A 25 basis point increase would take the cash rate from its current 4.35% to 4.85%, a level the big four banks have begun modelling.\\n\\nFor the roughly 3.5 million Australian households with a mortgage, the stakes are immediate — every rise adds hundreds of dollars a month to repayments. The RBA held in August, citing the need to weigh inflation against growth, but with the Fed now openly fighting an inflation battle and domestic prices showing fresh heat, September's meeting is shaping as one of the most consequential rate calls of the year.",
        ["ABC News", "Sydney Times"],
        ["https://www.abc.net.au/news/2026-09-17/asx-markets-business-live-news-september-19-2026/107162296",
         "https://www.sydtimes.com/2026/09/rba-rate-decision-september-2026-sydney-impact"]
    ),
    "soteu-vdl-2026-2026-09-17": dd(
        "soteu-vdl-2026-2026-09-17",
        "Von der Leyen's State of the Union: Canada announcement, under-13s social media ban, new European Security Council",
        "The Commission President's address charted closer Canada ties, a social media ban for under-13s, a European Security Council and an industrial-AI roadmap.",
        "Ursula von der Leyen's 2026 State of the Union address in Strasbourg was delivered against a backdrop of geopolitical strain — the war-driven energy crisis, the AI race with the US and China, and parliamentary pressure. Announced Sept 16, it doubled as both a vision statement and a positioning exercise as she courts coalition allies for the legislative year ahead.\\n\\nThree concrete proposals stood out. First, a major announcement on deepening cooperation with Canada, signalling the EU's intent to diversify partnerships away from overdependence on Washington. Second, a proposed social media ban for under-13s, a child-safety measure that landed immediately in the EU's long-running online-safety debate. Third, a call to create a new European Security Council, reflecting the bloc's push for a more self-reliant security architecture in a world of open conflict.\\n\\nOn technology, von der Leyen offered a road map for the EU to play a meaningful role in the AI race, pointing to industrial applications as the space where Europe can compete even as it trails the frontier model labs in the US and China. European Parliament analysts, however, noted the speech was thin on hard substance in several areas, underscoring the gap between the bloc's ambitions and its capacity to fund and legislate them.",
        ["The Parliament Magazine", "European Commission"],
        ["https://www.theparliamentmagazine.eu/news/article/10-takeaways-from-von-der-leyens-2026-state-of-the-union-speech",
         "https://commission.europa.eu/strategy-and-policy/state-union_en"]
    ),
    "openai-anthropic-google-safety-talks-2026-09-17": dd(
        "openai-anthropic-google-safety-talks-2026-09-17",
        "OpenAI, Anthropic and Google DeepMind confirm weeks of AI safety talks",
        "The three frontier labs confirmed they have been coordinating on AI safety, backing third-party safety assessments amid a Washington debate over frontier-risk regulation.",
        "AI's three most powerful companies — OpenAI, Anthropic and Google DeepMind — confirmed they have been in direct discussion about AI safety for weeks, an unusually explicit admission for labs that are otherwise fierce competitors. OpenAI's global policy chief, Chris Lehane, made the confirmation public on Tuesday as he worked with US lawmakers on catastrophic-risk policy.\\n\\nThe talks follow Anthropic CEO Dario Amodei's essay urging the industry to slow the pace of frontier development to avoid catastrophic risk — a call that drew public support from OpenAI's Sam Altman, Google's Demis Hassabis and SpaceXAI's Elon Musk. Lehane went further, saying OpenAI supports the FRONTIER Act, which would force leading labs to allow 'independent verification organizations' in to audit model development.\\n\\nThe coordination immediately raised a countervailing concern: antitrust. Some executives, including Altman, noted that if the collaboration were found to suppress competition it could breach US antitrust law. Amodei proposed a narrow government waiver to permit safety coordination, though Lehane argued the firms don't need one. The episode frames the central policy fight — how to govern frontier AI — with the White House, via Trump and advisor David Sacks, dismissing existential-risk concerns as overblown and warning that any slowdown would hand China an advantage.",
        ["TechCrunch", "CNBC", "Bloomberg"],
        ["https://techcrunch.com/2026/09/15/openai-anthropic-google-have-been-in-talks-on-ai-safety-for-weeks/",
         "https://www.cnbc.com/2026/09/15/open-ai-google-anthropic-safety.html"]
    ),
    "russia-157-drones-ukraine-2026-09-17": dd(
        "russia-157-drones-ukraine-2026-09-17",
        "Russia launches 157 drones and missiles at Ukraine; Kyiv hit, 16 injured",
        "A mass overnight Russian attack saw air defences destroy 131 of 157 aerial assets, with hits at 36 locations including Kyiv.",
        "Russia mounted one of its largest combined aerial attacks in recent weeks on the night of September 16-17, launching 157 drones and a mix of ballistic, cruise and anti-ship missiles at targets across Ukraine. Ukrainian air defence forces said they destroyed 131 of the incoming aerial assets, an interception rate the Air Forces described as effective despite the scale.\\n\\nHowever, hits were recorded at 36 locations. Kyiv took the most serious toll: a drone and missile strike on the capital damaged an education facility and injured at least 16 people, according to Kyiv authorities, some of them children. Elsewhere, officials reported strikes on critical infrastructure in the city of Kropyvnytskyi as Russia continued to target energy and logistics.\\n\\nThe attack fits a pattern of escalating Russian barrages aimed at wearing down Ukrainian defences and civilian morale through the autumn. Kyiv has responded by pressing its own long-range drone campaign against Russian infrastructure, a dynamic that has kept both capitals trading strikes while Western diplomacy over possible energy-target pauses remains unresolved.",
        ["RBC-Ukraine", "Kyiv Independent", "Ukrainian Pravda"],
        ["https://newsukraine.rbc.ua/news/all-missiles-got-through-how-ukraine-s-air-1789626405.html",
         "https://kyivindependent.com/",
         "https://www.pravda.com.ua/eng/news/2026/09/17/8053827/"]
    ),
    "trump-iran-nearing-end-direct-talks-2026-09-17": dd(
        "trump-iran-nearing-end-direct-talks-2026-09-17",
        "Trump says US 'nearing the end' of Iran war, claims direct talks with Tehran",
        "Trump claims the US is close to ending its conflict with Iran and in direct talks with Tehran, even as Iranian missiles hit targets in Jordan.",
        "President Trump used remarks in Gastonia, North Carolina — a rally for a Republican Senate candidate — to declare the US is 'nearing the end' of its conflict with Iran and claimed Washington is now in direct talks with Tehran. The comments came hours after Iranian missiles struck US targets in Jordan, underscoring the gap between diplomacy and the battlefield.\\n\\nThe war has become the defining political problem of the run-up to the midterms, now roughly seven weeks away. Soaring pump prices — US diesel has passed $6 a gallon for the first time ever — and the closure of the Strait of Hormuz to normal traffic have made the conflict an acute domestic economic issue for Republicans defending their majorities.\\n\\nOn the ground, the picture is grim and unresolved. Iran has said it will not reopen the strait until Washington meets its conditions for ending the war, Saudi infrastructure remains under attack, and the Houthis have seized Red Sea islands near the Bab el-Mandeb. Trump's claim of direct talks marks a rhetorical opening but, for now, no verified breakthrough — and oil prices remain near record highs.",
        ["Al Jazeera", "GlobalSecurity.org"],
        ["https://1-e8259.azureedge.net/news/liveblog/2026/9/17/iran-war-live-trump-says-us-nearing-end-of-war-claims-tehran-direct-talks",
         "https://www.globalsecurity.org/military/ops/iran-war-update.htm"]
    ),
    "finland-screen-time-cognition-2026-09-17": dd(
        "finland-screen-time-cognition-2026-09-17",
        "Eight-year Finnish study: more childhood screen time linked to better teen cognition",
        "Tracking 260 children for eight years, researchers found greater childhood screen time was linked to better cognitive processing in adolescence.",
        "A Finnish study that followed children for eight years has produced a result that cuts against a decade of conventional wisdom about screens. Researchers at the universities of Jyväskylä and Eastern Finland found that children who accumulated more screen time from childhood tended to show better cognitive processing as teenagers.\\n\\nThe study drew on the long-running PANIC project, tracking physical activity and nutrition in children. The cognitive analysis covered 124 girls and 136 boys with an average age of 15.8, using the CogState test battery to measure learning, attention and working memory alongside device-tracked physical activity and survey data on sedentary behaviour.\\n\\nThe researchers are careful not to give all screen use a free pass. They stress that the essential variable appears to be what children do on screens — activities that demand active thinking, problem-solving, creativity and learning — rather than sheer hours. 'We should not regard screen time solely as harmful,' said doctoral researcher Petri Jalanko, arguing for a balance between physical activity and screen use that stimulates the mind. The finding reframes the parenting debate: instead of a simple hour count, the quality of digital engagement may matter most.",
        ["ScienceDaily", "University of Eastern Finland"],
        ["https://www.sciencedaily.com/releases/2026/08/260815064803.htm",
         "https://oembed.uef.fi/en/article/more-screen-time-since-childhood-associated-with-better-cognitive-processing-in-adolescence"]
    ),
    "china-gravity1-sea-launch-2026-09-17": dd(
        "china-gravity1-sea-launch-2026-09-17",
        "China's Gravity-1 sets sea-launch records deploying Spacesail satellites",
        "Orienspace's Gravity-1 became China's most powerful solid rocket yet, setting national sea-launch records for payload and orbit altitude.",
        "China's private space sector hit a new milestone on September 16 when Orienspace launched nine satellites from a ship in the East China Sea off Shanghai. The mission — the fourth flight of the Gravity-1 rocket — set national records for a sea-based launch, with a combined payload exceeding three tonnes inserted at an orbital altitude of about 800 kilometres.\\n\\nGravity-1 is now the largest and most powerful solid-propellant rocket in the world, and all four of its launches have been conducted at sea: the first two from the Yellow Sea and the latest two from the East China Sea. Wednesday's mission was its first for the Spacesail Constellation — one of two massive Chinese low-earth-orbit internet networks being built as a Starlink rival. Eight of the nine satellites were Spacesail nodes, plus one experimental spacecraft.\\n\\nThe flight followed a LandSpace ZQ-2E methane rocket launch the day before that deployed a further 10 Spacesail satellites. Together the back-to-back missions signal that Spacesail, a Shanghai operator, is now entrusting launch work to private firms rather than state-owned contractors alone — a sign of China's fast-maturing commercial launch ecosystem taking on big national space-infrastructure work.",
        ["Xinhua", "China Daily"],
        ["https://english.news.cn/20260916/2a49fb5cf85f4a86be4786d2a33c9957/c.html",
         "https://www.chinadaily.com.cn/a/202609/17/WS6aab3bcae4b06d4aa055e78a.html"]
    ),
    "trump-scotus-mail-ballot-2026-09-17": dd(
        "trump-scotus-mail-ballot-2026-09-17",
        "Trump lashes out at his Supreme Court picks over mail-ballot ruling",
        "After the Supreme Court blocked the administration's plan to tighten mail-in voting weeks before the midterms, Trump attacked the justices he appointed.",
        "The Supreme Court dealt the Trump administration a significant election-cycle defeat when it refused to allow a new Postal Service plan to screen mail-in ballots just weeks before the November midterms. The Court's refusal to lift a judicial block on the tighter delivery rules averted a scenario critics warned could have disrupted how millions of Americans vote by mail.\\n\\nPresident Trump responded with characteristic force on Tuesday, launching a public attack on the justices he appointed, frustrated that conservative nominees did not side with his administration on the matter. His outburst landed at the intersection of two of the most combustible issues in US politics — voting rules and the Court's legitimacy — with the midterms hanging over both.\\n\\nThe ruling's practical effect is to keep existing mail-in ballot rules in place for the election, preserving the volume of postal voting that has become an entrenched part of American democracy. But the political fallout is immediate: with control of Congress at stake, election administration has become a live and bitterly contested battlefield, and the Court's intervention — and the President's reaction to it — sharpened the stakes for November.",
        ["TIME", "NYT", "POLITICO"],
        ["https://time.com/article/2026/09/16/scotus-mail-ballot-ruling-trump-rant/",
         "https://www.nytimes.com/live/2026/09/14/us/supreme-court-mail-voting-trump",
         "https://www.politico.com/news/2026/09/14/supreme-court-blocks-trump-mail-in-ballot-plan-01076079"]
    ),
}

with open(DEEP, "w") as f:
    json.dump(deep, f, ensure_ascii=False, indent=2)

print(f"feed days: {sum(len(d['stories']) for d in feed['days'])} total stories across {len(feed['days'])} days")
print(f"today stories: {len(today_stories)}")
print(f"deepdive keys for {TODAY}: {len(deep['deepdives'][TODAY])}")
print("top dates:", [d['date'] for d in feed['days'][:4]])