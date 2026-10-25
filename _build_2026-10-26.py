#!/usr/bin/env python3
# Bruno Brief builder for 2026-10-26 (Monday). Prepends today to the multi-day feed.
import json, os

BASE = "/home/rory/Projects/news-pwa"
FEED = os.path.join(BASE, "feed.json")
DEEP = os.path.join(BASE, "deepdives.json")
DATE = "2026-10-26"

def slug(s):
    return s.strip().lower().replace(" ", "-")

stories = [
    {
        "bucket": "US Bond Market",
        "emoji": "🇺🇸",
        "headline": "Fed decision week: markets expect a hold, but big tech earnings and PCE loom",
        "summary": "The Federal Reserve's two-day meeting ends Wednesday (Oct 28) with futures pricing under a 10% chance of a hike — the Fed raised to 3.75-4.00% in September and economists expect it to hold. The 10-year yield starts the week near 5.00% with oil above $100 on US-Iran tension; Microsoft and Alphabet report Wednesday after the decision, then Q3 GDP and September PCE land Thursday.",
        "sources": ["Regards of Wallstreet", "Investing.com"],
        "slug": "fed-decision-week-oct28-hold-2026-10-26",
    },
    {
        "bucket": "Australian Politics",
        "emoji": "🇦🇺",
        "headline": "Parliament returns without Helen Haines as MPs urged to sign civility pledge, security tightened",
        "summary": "Federal parliament reconvened Monday with Indi MP Helen Haines in a serious-but-stable condition in hospital after being struck by a car outside her Wangaratta office in an alleged deliberate attack; both legs were amputated. Tributes open the sitting week, crossbenchers are backing a civility pledge inspired by murdered British MP Jo Cox, and security has been strengthened at Parliament House.",
        "sources": ["ABC News", "The Guardian", "The Sydney Morning Herald"],
        "slug": "parliament-returns-helen-haines-civility-pledge-2026-10-26",
    },
    {
        "bucket": "Australian Politics",
        "emoji": "🇦🇺",
        "headline": "First international flight lands at Western Sydney International",
        "summary": "Air New Zealand flight 165 from Auckland touched down at Western Sydney International (Nancy Bird-Walton) Airport at 7:27am Monday — its first overseas service, arriving 18 minutes early, a day after Jetstar flew the inaugural domestic flight. NZ will run three weekly Auckland services, with Singapore Airlines, VietJet and Qatar services to follow.",
        "sources": ["The Sydney Morning Herald", "The Guardian"],
        "slug": "wsi-first-international-flight-2026-10-26",
    },
    {
        "bucket": "Australian Politics",
        "emoji": "🇦🇺",
        "headline": "One in three Australian households facing food insecurity, Foodbank research finds",
        "summary": "New Foodbank research released Monday found one in three Australian households are going hungry amid the cost-of-living crisis, with many people cutting meal portions to make ends meet — fresh evidence of financial strain as parliament returns to debate Labor's Digital Duty of Care bill.",
        "sources": ["The Sydney Morning Herald", "ABC News"],
        "slug": "foodbank-one-in-three-hunger-2026-10-26",
    },
    {
        "bucket": "European Politics",
        "emoji": "🇪🇺",
        "headline": "Serbia's Vučić concedes defeat to student-led movement in seismic shift",
        "summary": "Aleksandar Vučić conceded Serbia's snap parliamentary election Sunday night, saying the student-backed Students' List won an estimated 135-140 of 250 seats versus ~105 for his SNS — ending his 14-year grip on power in the region's biggest political upset of the year. The movement grew from the 2024 Novi Sad station collapse; celebrations erupted in Belgrade on turnout near 70%, the highest since 2000.",
        "sources": ["AP News", "The Guardian", "BBC", "Euronews"],
        "slug": "serbia-vucic-concedes-students-list-win-2026-10-26",
    },
    {
        "bucket": "European Politics",
        "emoji": "🇪🇺",
        "headline": "Le Pen launches presidential bid as protests rattle France",
        "summary": "French far-right leader Marine Le Pen formally opened her presidential campaign at the National Rally congress in Orléans, telling about 10,000 supporters she would crack down on crime and immigration and curb EU influence, against a backdrop of massive cost-of-living protests gripping the country. She remains the frontrunner for the 2027 vote.",
        "sources": ["Reuters", "France 24"],
        "slug": "le-pen-launches-presidential-bid-2026-10-26",
    },
    {
        "bucket": "AI News",
        "emoji": "🤖",
        "headline": "Anthropic opens waitlist for Claude Duet, a proactive agent that works while you're away",
        "summary": "Anthropic launched a research preview (by waitlist) of Claude Duet, an agent app built on Claude Opus 5.5 that messages users first with what needs attention and keeps running tasks in its own virtual machine when the phone or laptop is off. It sends a morning brief, checks accounts periodically, and holds payments, document-signing and deletions for approval — open to US Pro and Max subscribers.",
        "sources": ["Anthropic", "AI Review Rating"],
        "slug": "anthropic-claude-duet-agent-preview-2026-10-26",
    },
    {
        "bucket": "AI News",
        "emoji": "🤖",
        "headline": "OpenAI and Anthropic models land on Google Cloud, billable against existing cloud commitments",
        "summary": "OpenAI frontier models and Codex agentic workflows are coming to Google Cloud's Model Garden, and the full Anthropic-managed Claude Platform is now generally available on Google Cloud — both purchasable against existing Google Cloud spend commitments. Enterprise customers can now buy OpenAI and Claude on a single invoice, loosening the cloud lock-in that has corralled AI procurement.",
        "sources": ["AI Briefing", "OpenAI", "AI Review Rating"],
        "slug": "openai-anthropic-on-google-cloud-2026-10-26",
    },
    {
        "bucket": "Conflicts",
        "emoji": "⚔️",
        "headline": "Israel votes Tuesday in its most seismic election in decades",
        "summary": "Israelis go to the polls Oct 27 in the sixth election since 2019 and first since the Gaza and regional wars, widely framed as a referendum on Benjamin Netanyahu. The latest polls give his outgoing coalition roughly 50 of 120 seats — more than a majority is 61 — while Trump has endorsed Netanyahu though some US advisers see opportunity in an alternative. Official results are confirmed Nov 4.",
        "sources": ["Al Jazeera", "ABC News", "Axios"],
        "slug": "israel-election-october-27-2026-2026-10-26",
    },
    {
        "bucket": "Conflicts",
        "emoji": "⚔️",
        "headline": "Russia strikes Poltava hypermarket as Ukraine hits radar systems; Oleshky humanitarian ceasefire due to begin",
        "summary": "A Russian strike on an Epicentr hypermarket in Poltava sparked a fire and injured a woman (Oct 25), even as Ukraine struck Russian radar systems and command posts. Meanwhile the US-brokered localized ceasefire around Russian-occupied Oleshky — negotiated with First Lady Melania Trump as 'Exclusive Intermediary' — is set to begin Oct 27 to allow a humanitarian mission to deliver aid and evacuate civilians.",
        "sources": ["RBC-Ukraine", "Kyiv Independent", "AP News"],
        "slug": "ukraine-poltava-strike-oleshky-ceasefire-2026-10-26",
    },
    {
        "bucket": "Blowing Up Today",
        "emoji": "🚨",
        "headline": "Oil holds above $100 and US stocks sink on renewed US-Iran confrontation",
        "summary": "Friday's session ended with the Dow down 652 points (1.23%) as oil climbed back above $100 a barrel on concern over renewed conflict between the US and Iran, with Strait of Hormuz supply risk and Houthi attacks on Saudi energy infrastructure in focus — energy shares rose while gold fell on higher expected inflation. The S&P 500 closed at 7,623.68 with the 10-year Treasury yield at 5.00%.",
        "sources": ["Regards of Wallstreet (CNBC/Yahoo)", "Reuters", "Britannica"],
        "slug": "oil-above-100-us-iran-stocks-sink-2026-10-26",
    },
    {
        "bucket": "Blowing Up Today",
        "emoji": "🚨",
        "headline": "Typhoon Champi slams China's east coast after battering Taiwan and Japan",
        "summary": "Typhoon Champi — the strongest storm on Earth of 2026 before weakening — hit China's eastern coast after leaving one dead and 600+ injured in Taiwan and knocking out power to thousands in Okinawa. China issued an orange alert for Jiangsu, Shanghai and Zhejiang, suspended some train services, evacuated tens of thousands in Shanghai and cancelled hundreds of flights.",
        "sources": ["AFP", "AS English", "China Meteorological Administration"],
        "slug": "typhoon-champi-china-coast-2026-10-26",
    },
    {
        "bucket": "Science/Tech",
        "emoji": "🔬",
        "headline": "JWST finds three giant black holes in a single galaxy from the dawn of time",
        "summary": "Astronomers led by the Max Planck Institute detected three actively feeding supermassive black holes in galaxy J0148-4214, 12.5 billion light-years away (seen just 1.2 billion years after the Big Bang) — the first evidence of three active black holes in one ancient galaxy. Two, just 620 light-years apart, are expected to merge; one ~600,000-solar-mass black hole is feeding faster than theory's Eddington limit.",
        "sources": ["ScienceDaily (Max Planck Institute)", "Astronomy & Astrophysics"],
        "slug": "jwst-three-black-holes-dawn-of-time-2026-10-26",
    },
]

deepdives = {
    "fed-decision-week-oct28-hold-2026-10-26": {
        "headline": "Fed decision week: markets expect a hold, but big tech earnings and PCE loom",
        "summary": "The Federal Reserve's two-day meeting ends Wednesday (Oct 28) with futures pricing under a 10% chance of a hike — the Fed raised to 3.75-4.00% in September and economists expect it to hold. The 10-year yield starts the week near 5.00% with oil above $100 on US-Iran tension; Microsoft and Alphabet report Wednesday after the decision, then Q3 GDP and September PCE land Thursday.",
        "detail": "The US Federal Reserve delivers its interest-rate decision at 2:00pm ET on Wednesday, October 28, wrapping up a two-day meeting (October 27-28). Futures markets put the chance of a rate increase below 10%, with economists expecting the committee to hold the federal funds rate at the 3.75%-4.00% range it set in September, when it delivered its first hike of the year on a unanimous 12-0 vote. Chairman Kevin Warsh holds a press conference at 2:30pm. There is no dot plot at this meeting; the next set of officials' rate forecasts comes in December.\n\nThe decision lands in a split market backdrop. The 10-year Treasury yield ended last week at 5.00%, dipping under 5% midweek as investors sold AI shares and bought bonds on worries about hyperscaler debt, before rebounding. West Texas Intermediate crude is back above $100 a barrel on concern over renewed US-Iran conflict and the Strait of Hormuz supply risk, which pushes expected inflation up and keeps the Fed from easing. That tension — AI-debt relief pulling yields down versus an oil-driven inflation shock — is the central story bond markets are weighing.\n\nWednesday afternoon is a double-header: about two hours after the Fed statement, Microsoft and Alphabet both report earnings (analysts expect $4.72 a share from Microsoft on ~$90.7 billion of revenue and $3.00 from Alphabet on ~$127.7 billion). Thursday brings third-quarter GDP and the September PCE price index together at 8:30am ET — PCE is the Fed's preferred inflation gauge — with Amazon and Intel reporting after the close. Markets will read the Fed statement for whether the September hike was a one-off or the start of a tightening campaign.",
        "sources": ["Regards of Wallstreet", "Investing.com", "Federal Reserve"],
        "source_urls": [
            "https://www.regardsofwallstreet.com/news/stock-market-week-ahead-october-26-2026",
            "https://www.investing.com/news/stock-market-news/economic-data-and-treasury-auctions-highlight-mondays-schedule-93CH-4970204",
            "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm",
        ],
    },
    "parliament-returns-helen-haines-civility-pledge-2026-10-26": {
        "headline": "Parliament returns without Helen Haines as MPs urged to sign civility pledge, security tightened",
        "summary": "Federal parliament reconvened Monday with Indi MP Helen Haines in a serious-but-stable condition in hospital after being struck by a car outside her Wangaratta office in an alleged deliberate attack; both legs were amputated. Tributes open the sitting week, crossbenchers are backing a civility pledge inspired by murdered British MP Jo Cox, and security has been strengthened at Parliament House.",
        "detail": "Federal parliament resumed on Monday, October 26, for one of its most sombre starts in years, with the seat of Indi MP Helen Haines empty. Haines is in a serious-but-stable condition in hospital after being hit by a four-wheel-drive outside her electorate office in Wangaratta last Monday in what police are treating as a deliberate attack. Both her legs have been amputated. Her condition was downgraded from critical to serious but stable over the weekend.\n\nPrime Minister Anthony Albanese is expected to move a motion setting aside much of the day for MPs to share messages of support for Haines, who is admired across the political divide for her integrity. Independent colleagues Kate Chaney and Monique Ryan have pledged to carry forward her example. Crossbench MPs are backing a civility pledge inspired by the family of Jo Cox, the British MP murdered in 2016: 'In my political life, I pledge to act with honesty, respect and compassion.' Haines was the first federal MP to sign it; Chaney says she will add her name.\n\nThe attack has forced a rethink of MP security. Extra security measures are in place at Parliament House, including in committee rooms, and cabinet is weighing options including fast-tracking the recommendations of an inquiry into support for MPs. AFP Commissioner Krissy Barrett drew a direct link between inflamed political rhetoric and a rise in threats, a view echoed by Social Services Minister Tanya Plibersek. Health Minister Mark Butler said the environment for MPs 'has changed dramatically' over his 20 years in parliament, citing threats against members and their families.",
        "sources": ["ABC News", "The Guardian", "The Sydney Morning Herald"],
        "source_urls": [
            "https://www.abc.net.au/news/2026-10-26/helen-haines-parliament-returns-canberra-federal-politics/107306604",
            "https://www.theguardian.com/australia-news/live/2026/oct/26/australia-politics-live-helen-haines-tribute-anthony-albanese-labor-liberal-one-nation-pauline-hanson-angus-taylor-question-time-senate-estimates-ntwnfb",
            "https://www.smh.com.au/national/australia-news-live-haines-tributes-to-open-parliamentary-proceedings-today-one-in-three-households-experiencing-food-insecurity-new-research-finds-20261026-p618h5.html",
        ],
    },
    "wsi-first-international-flight-2026-10-26": {
        "headline": "First international flight lands at Western Sydney International",
        "summary": "Air New Zealand flight 165 from Auckland touched down at Western Sydney International (Nancy Bird-Walton) Airport at 7:27am Monday — its first overseas service, arriving 18 minutes early, a day after Jetstar flew the inaugural domestic flight. NZ will run three weekly Auckland services, with Singapore Airlines, VietJet and Qatar services to follow.",
        "detail": "Western Sydney International Airport (WSI) welcomed its first international arrival on the morning of Monday, October 26: Air New Zealand flight 165 from Auckland touched down at 7:27am, 18 minutes ahead of schedule. The landing marks the start of Air New Zealand's three-times-weekly Auckland service and the airport's entry into the international stage, exactly a day after Jetstar operated the inaugural domestic departure to the Gold Coast on Sunday.\n\nWSI, at Badgerys Creek about 50 kilometres from Sydney's CBD (and named for aviator Nancy Bird-Walton), is Australia's first new major airport in more than half a century and operates 24/7. More international routes are already committed: Singapore Airlines begins daily services from Changi in November 2026, VietJet starts two weekly Ho Chi Minh City flights in January 2027, and Qatar Airways begins three Doha services a week in December 2027 following an updated bilateral air-services agreement.\n\nThe airport is positioned to relieve pressure on the congested Kingsford Smith airport and is a marker of a long-awaited economic hub for western Sydney. Transport Minister Catherine King has noted the new routes are partly a product of renegotiated bilateral agreements, though the government continues to cap how many services Gulf carriers like Qatar can operate into Australia's four major existing airports. WSI's terminal was designed with growth in mind, with stated capacity to reach 82 million passengers a year by the 2060s.",
        "sources": ["The Sydney Morning Herald", "The Guardian"],
        "source_urls": [
            "https://www.smh.com.au/national/australia-news-live-haines-tributes-to-open-parliamentary-proceedings-today-one-in-three-households-experiencing-food-insecurity-new-research-finds-20261026-p618h5.html",
            "https://www.theguardian.com/australia-news/2026/oct/25/western-sydney-international-airport-wsi-open-airlines-flights-cost-transport-history",
        ],
    },
    "foodbank-one-in-three-hunger-2026-10-26": {
        "headline": "One in three Australian households facing food insecurity, Foodbank research finds",
        "summary": "New Foodbank research released Monday found one in three Australian households are going hungry amid the cost-of-living crisis, with many people cutting meal portions to make ends meet — fresh evidence of financial strain as parliament returns to debate Labor's Digital Duty of Care bill.",
        "detail": "Foodbank Australia released new research on Monday, October 26, showing that one in three Australian households are experiencing food insecurity amid the ongoing cost-of-living crisis. The finding indicates that many families are now skipping meals or reducing meal portions to make ends meet, with grocery-price pressure a persistent driver of household financial stress despite headline inflation easing in other categories.\n\nThe scale of the figure — roughly a third of households — points to a broadening of hardship beyond traditionally vulnerable groups into middle-income families, a pattern that has been documented across Australian food-relief organisations through 2026. Charities have repeatedly reported record demand for food parcels and community meals as rents, energy and groceries absorb an outsized share of household budgets.\n\nThe research lands on the same day parliament returns for a sitting week. Alongside the tributes to Helen Haines, the government is due to debate its Digital Duty of Care legislation, which would allow social media users to turn off algorithms and sue platforms for online harm — a bill that has drawn significant pushback from tech companies and the US administration and faces a Senate inquiry. The juxtaposition highlights a parliamentary agenda that is simultaneously confronting online safety, political civility and the cost-of-living squeeze documented by the Foodbank data.",
        "sources": ["The Sydney Morning Herald", "ABC News"],
        "source_urls": [
            "https://www.smh.com.au/national/australia-news-live-haines-tributes-to-open-parliamentary-proceedings-today-one-in-three-households-experiencing-food-insecurity-new-research-finds-20261026-p618h5.html",
            "https://www.abc.net.au/news/2026-10-26/federal-politics-live-blog-october-26/107307606",
        ],
    },
    "serbia-vucic-concedes-students-list-win-2026-10-26": {
        "headline": "Serbia's Vučić concedes defeat to student-led movement in seismic shift",
        "summary": "Aleksandar Vučić conceded Serbia's snap parliamentary election Sunday night, saying the student-backed Students' List won an estimated 135-140 of 250 seats versus ~105 for his SNS — ending his 14-year grip on power in the region's biggest political upset of the year. The movement grew from the 2024 Novi Sad station collapse; celebrations erupted in Belgrade on turnout near 70%, the highest since 2000.",
        "detail": "Serbia's long-serving strongman Aleksandar Vučić conceded defeat in Sunday's parliamentary election, ending his Serbian Progressive Party's 14 years in power and handing victory to a leaderless student-led movement. 'Based on a stratified sample, it is clear that we have lost the election,' Vučić told supporters at his party headquarters, saying the Students' List would take between 135 and 140 of the 250 seats in parliament while his SNS would hold about 105. He blamed independent media and alleged interference by unnamed European countries and an 'American deep state' for the loss.\n\nThe results — Students' List ~2.2 million votes to SNS ~1.7 million, roughly 52% to 32% by Vučić's own accounting — triggered euphoric celebrations across Belgrade, with crowds driving through the capital honking horns and chanting 'Aleksandar is gone.' Demonstrators tore down fences and tents from the pro-Vučić protest camp that had occupied a central park for over a year. Dijana Hrka, whose son died in the disaster that started it all, told N1 television she had been 'waiting for this moment for two years.'\n\nThe movement traces to November 2024, when a concrete canopy collapsed at Novi Sad's railway station, killing 16 people. Students blamed the disaster on corruption and cronyism during renovation work and spent nearly two years leading protests that broadened into a demand to end Vučić's rule. The campaign deliberately fielded no students as candidates — instead little-known experts, athletes, farmers and artists represented a non-partisan platform; the students cycled and walked through rural areas, traditionally Vučić's strongholds, to reach voters.\n\nTurnout was the highest since the breakup of Yugoslavia: monitors put participation near 70%, with some polling-station waits of two hours. The result mirrors the ousting of Vučić ally Viktor Orbán in Hungary earlier this year — another youth-driven defeat of an autocrat — and is being closely watched in Brussels given Serbia's EU candidate status. Vučić had been endorsed by Russia's Vladimir Putin, adding a geopolitical dimension to what is the most significant political shift in the Western Balkans in more than a decade.",
        "sources": ["AP News", "The Guardian", "BBC", "Euronews"],
        "source_urls": [
            "https://apnews.com/article/serbia-election-students-vucic-fdf5def8a20aebc8ae139fd719478775",
            "https://www.theguardian.com/world/2026/oct/25/serbian-leader-aleksandar-vucic-concedes-defeat-in-fiercely-contested-parliamentary-election",
            "https://www.bbc.co.uk/news/articles/cw5yn3xlprpmo",
            "https://www.euronews.com/2026/10/25/vucic-concedes-defeat-in-pivotal-serbian-elections-says-student-movement-has-won",
        ],
    },
    "le-pen-launches-presidential-bid-2026-10-26": {
        "headline": "Le Pen launches presidential bid as protests rattle France",
        "summary": "French far-right leader Marine Le Pen formally opened her presidential campaign at the National Rally congress in Orléans, telling about 10,000 supporters she would crack down on crime and immigration and curb EU influence, against a backdrop of massive cost-of-living protests gripping the country. She remains the frontrunner for the 2027 vote.",
        "detail": "Marine Le Pen formally launched her presidential campaign on Sunday, October 25, addressing around 10,000 supporters at the National Rally congress in Orléans. The far-right leader, who is the frontrunner for the 2027 French presidential election, used the kick-off to promise a crackdown on crime and immigration, pledge to curb EU influence and boost French sovereignty, and position herself as the answer to the cost-of-living crisis that has driven the country's most sustained street protests in years.\n\nThe launch took place against a volatile national backdrop. Roughly 410,000 people marched across France on Saturday in cost-of-living and anti-government protests that were largely peaceful during the day but turned to tear gas and water cannons in the evening, with close to 1,000 arrests and about 70,000 police deployed. The unrest has added political pressure to a minority government already reeling from a bond-market crisis that pushed French 10-year yields above 5% for the first time since 2002, and which Moody's only narrowly avoided downgrading last week.\n\nThe National Rally is betting that the combination of protest fatigue, economic pain and the government's difficulty passing a credible 2027 budget widens Le Pen's path to the presidency. Jordan Bardella was re-elected party leader at the congress, and Le Pen's platform leans on restoring order and national control. For President Emmanuel Macron, the campaign launch crystallises the squeeze between the streets and the bond market as his government, already deeply unpopular, faces a budget that analysts say may struggle to pass parliament.",
        "sources": ["Reuters", "France 24"],
        "source_urls": [
            "https://www.reuters.com/world/frances-le-pen-launches-presidential-bid-protests-rattle-nation-2026-10-25/",
            "https://www.france24.com/en/france/20261025-french-far-right-leader-le-pen-seeks-to-leverage-unrest-in-presidential-campaign-kick-off",
        ],
    },
    "anthropic-claude-duet-agent-preview-2026-10-26": {
        "headline": "Anthropic opens waitlist for Claude Duet, a proactive agent that works while you're away",
        "summary": "Anthropic launched a research preview (by waitlist) of Claude Duet, an agent app built on Claude Opus 5.5 that messages users first with what needs attention and keeps running tasks in its own virtual machine when the phone or laptop is off. It sends a morning brief, checks accounts periodically, and holds payments, document-signing and deletions for approval — open to US Pro and Max subscribers.",
        "detail": "Anthropic opened a research preview on October 21 for Claude Duet, an agentic app built around Claude Opus 5.5 that inverts the normal assistant relationship: rather than waiting for the user to prompt it, Duet messages the user first with what needs attention and keeps working on tasks after the user steps away. It is available by waitlist to US Pro and Max subscribers and is included in those plans, using the same usage limits as the rest of Claude.\n\nDuet runs as a standalone app on iOS and Android and on claude.ai. Anthropic says it sends a morning brief across a user's connected applications, checks those accounts every few hours, and operates inside a virtual machine with its own browser so tasks continue running even when the phone or laptop is off — a step beyond chat assistants toward autonomous background work.\n\nSafety controls are central to the design. Before it sends a message, makes a payment, signs a document or deletes anything, Duet shows the action and waits for approval; trading securities and moving money between accounts are blocked entirely, even with approval. Anthropic cites an early-access tester — a restaurant owner with about 110 employees — who used it for accounting, customer support and marketing.\n\nThe release is part of a broader move in mid-to-late October toward proactive, always-on agents: OpenAI in the same window made its Decisions API generally available and Google launched a Gemini hub for small businesses. For small business owners already paying for Claude Pro or Max, Duet offers offloaded scheduling, invoice review and client-call preparation at no extra subscription cost, with every send and payment still gated behind approval.",
        "sources": ["Anthropic", "AI Review Rating"],
        "source_urls": [
            "https://www.anthropic.com/news/claude-duet",
            "https://aireviewrating.com/articles/ai-news-week-of-2026-10-26",
        ],
    },
    "openai-anthropic-on-google-cloud-2026-10-26": {
        "headline": "OpenAI and Anthropic models land on Google Cloud, billable against existing cloud commitments",
        "summary": "OpenAI frontier models and Codex agentic workflows are coming to Google Cloud's Model Garden, and the full Anthropic-managed Claude Platform is now generally available on Google Cloud — both purchasable against existing Google Cloud spend commitments. Enterprise customers can now buy OpenAI and Claude on a single invoice, loosening the cloud lock-in that has corralled AI procurement.",
        "detail": "Enterprise AI procurement is becoming cloud-agnostic in a burst of deals announced the week of October 21. OpenAI and Google Cloud confirmed that OpenAI frontier models and Codex agentic workflows would come to Google Cloud's Model Garden, transacted through the Google Cloud Marketplace and purchasable against existing Google Cloud spend commitments. Models will also be available in Google Antigravity and the Gemini Agent. No general availability date was set, and Microsoft remains OpenAI's primary cloud partner, but the move lets Google Cloud customers buy OpenAI alongside other AI on one invoice.\n\nOn the same day, OpenAI made its frontier models available in the Google Cloud Model Garden with private-preview access to GPT-6 Astra and related models. Separately, Anthropic made the full Claude Platform generally available on Google Cloud on October 22 — the Anthropic-managed offering that bills on a single Google Cloud invoice, uses existing Google Cloud IAM credentials and draws down existing Google Cloud commitments. It carries the full Claude API including Managed Agents (beta), computer use, agent skills, web search and batch processing, with Fast Mode on Claude Opus 5.5 at $8 per million input tokens and $40 per million output tokens.\n\nFor customers, the practical effect is that choosing a model no longer implies signing a second cloud contract: OpenAI, Anthropic and Google models can all be purchased against a single Google Cloud commitment. Anthropic is also pushing ecosystem standardisation — it donated the Agent Skills standard, already used by more than 70 agent platforms, to the Linux Foundation's Agentic AI Foundation on October 22. The deals mark a notable realignment of the frontier-lab–cloud relationships that had previously been organised largely around Microsoft and Amazon.",
        "sources": ["AI Briefing", "OpenAI", "AI Review Rating"],
        "source_urls": [
            "https://aibriefing.dev/",
            "https://openai.com/index/openai-models-on-google-cloud-model-garden/",
            "https://aireviewrating.com/articles/ai-news-week-of-2026-10-26",
        ],
    },
    "israel-election-october-27-2026-2026-10-26": {
        "headline": "Israel votes Tuesday in its most seismic election in decades",
        "summary": "Israelis go to the polls Oct 27 in the sixth election since 2019 and first since the Gaza and regional wars, widely framed as a referendum on Benjamin Netanyahu. The latest polls give his outgoing coalition roughly 50 of 120 seats — more than a majority is 61 — while Trump has endorsed Netanyahu though some US advisers see opportunity in an alternative. Official results are confirmed Nov 4.",
        "detail": "Israelis vote on Tuesday, October 27, to elect the 26th Knesset — the sixth general election since 2019 and the first since the Gaza war and the wider regional conflicts that have defined the last several years. ABC News describes it as the most seismic Israeli election in decades, and it is widely framed as a referendum on Benjamin Netanyahu, the longest-serving prime minister in Israeli history and the central figure of the wars that have reshaped the Middle East since 2023.\n\nThe arithmetic is tight. Polls published late last week give Netanyahu's outgoing coalition about 50 of the 120 Knesset seats, well short of the 61 needed for a majority. Polling more than a month out had suggested a potential comeback, but recent surveys show the coalition's path narrowing; challengers, including former military chiefs running on rival right-wing and centrist tickets, are competing for the same voter base.\n\nThe international dimension is unusually active. President Trump has endorsed Netanyahu, reversing weeks of hesitation, but some US officials tell Axios that advisers see opportunity in a government led by someone else for Trump's Middle East agenda — Gaza reconstruction and normalisation. The vote is also shadowed by the day's security backdrop: Netanyahu ordered a 'very extensive' West Bank operation last week after two soldiers were killed near Hebron, and the closure of the territory has been discussed.\n\nPolls open at 7am Israel time (4pm AEDT) and close at 10pm, when television networks publish exit polls; official results are confirmed on November 4. Campaign winners need 61 seats to form a government, a process that will again hinge on coalition negotiations in a deeply fragmented parliament.",
        "sources": ["Al Jazeera", "ABC News", "Axios"],
        "source_urls": [
            "https://www.aljazeera.com/news/2026/10/20/israels-elections-2026-explained-in-maps-and-charts",
            "https://www.abc.net.au/news/2026-10-23/israel-election-2026-explained/107287156",
            "https://www.axios.com/2026/10/24/israel-election-trump-netanyahu-advisers",
        ],
    },
    "ukraine-poltava-strike-oleshky-ceasefire-2026-10-26": {
        "headline": "Russia strikes Poltava hypermarket as Ukraine hits radar systems; Oleshky humanitarian ceasefire due to begin",
        "summary": "A Russian strike on an Epicentr hypermarket in Poltava sparked a fire and injured a woman (Oct 25), even as Ukraine struck Russian radar systems and command posts. Meanwhile the US-brokered localized ceasefire around Russian-occupied Oleshky — negotiated with First Lady Melania Trump as 'Exclusive Intermediary' — is set to begin Oct 27 to allow a humanitarian mission to deliver aid and evacuate civilians.",
        "detail": "Russia's war on Ukrainian civilian infrastructure continued over the weekend. On October 25, a Russian strike on an Epicentr hypermarket in Poltava sparked a fire and injured a woman, according to RBC-Ukraine, in the latest in a series of attacks on civilian targets. Russia has spent October battering Ukrainian cities and the power grid ahead of winter; earlier strikes killed civilians in Dnipropetrovsk and Kharkiv regions, part of an autumn campaign that humanitarian agencies warn is worsening an already severe humanitarian situation.\n\nUkraine has been striking back at Russian military infrastructure. Over the same period Ukraine hit Russian radar systems and command posts, according to Ukrainian reports, alongside continued long-range drone attacks on Russian oil and industrial targets. The pattern — Russia pummelling Ukrainian cities while Ukraine degrades Russian air-defence and command nodes — has persisted as negotiators prepare a renewed diplomatic track in Abu Dhabi in the first half of November.\n\nA concrete humanitarian development is due to begin this week. The US-brokered localized ceasefire around the Russian-occupied city of Oleshky in the Kherson region is set to start on Tuesday, October 27 (Russian and US accounts cite late October; Ukraine's ombudsman said the ceasefire begins a couple of days before the humanitarian convoy enters), to allow a mission to deliver food, medicine and clean water to the largely elderly remaining population and evacuate those who want to leave. The arrangement was negotiated with First Lady Melania Trump, acting as 'Exclusive Intermediary', and could serve as a model for future humanitarian missions. The broader 'energy ceasefire' declared by Trump on October 11, however, has so far failed to hold, with strikes continuing on both sides.",
        "sources": ["RBC-Ukraine", "Kyiv Independent", "AP News"],
        "source_urls": [
            "https://newsukraine.rbc.ua/war-in-ukraine",
            "https://kyivindependent.com/",
            "https://apnews.com/article/russia-ukraine-war-ceasefire-oleshky-melania-trump-60167627316e0e2f62fc359cf78f317d",
        ],
    },
    "oil-above-100-us-iran-stocks-sink-2026-10-26": {
        "headline": "Oil holds above $100 and US stocks sink on renewed US-Iran confrontation",
        "summary": "Friday's session ended with the Dow down 652 points (1.23%) as oil climbed back above $100 a barrel on concern over renewed conflict between the US and Iran, with Strait of Hormuz supply risk and Houthi attacks on Saudi energy infrastructure in focus — energy shares rose while gold fell on higher expected inflation. The S&P 500 closed at 7,623.68 with the 10-year Treasury yield at 5.00%.",
        "detail": "Crude oil is trading back above $100 a barrel and US equities ended last week lower as markets repriced the risk of renewed conflict between the United States and Iran. On Friday, October 23, the Dow Jones Industrial Average fell 652.82 points, or 1.23%, to close at 52,215.16; the S&P 500 dropped 0.52% to 7,623.68 and the Nasdaq Composite 0.21% to 25,955.34, per Yahoo Finance and CNBC data. Energy shares rose — almost three in four S&P 500 stocks fell — while gold declined, because dearer oil raises expected inflation, which raises expected interest rates.\n\nThe oil move is supply-driven. The 2026 Iran war, initiated by the US and Israel in late February, has included a US naval blockade of Iran's ports, Iranian threats against the Strait of Hormuz — through which a fifth of global seaborne oil passes — and, this month, a Houthi campaign of ballistic-missile and drone attacks on Saudi airports and energy infrastructure that killed at least 20 people and injured hundreds. With Houthis vowing more strikes on Saudi energy facilities and Hormuz risk unresolved, the supply premium has returned.\n\nFor markets the oil shock cuts directly against the bond rally of the previous week, when the 10-year Treasury yield fell sharply on fears about AI-hyperscaler debt. Higher energy prices feed into inflation expectations, keeping the Federal Reserve from easing — markets still price some odds of a December hike — and pressing on stretched credit markets. The 10-year yield ended the week at 5.00%. The interaction of an Iran/Hormuz supply shock with AI-debt relief is exactly the tension the Fed and markets are now trying to price ahead of Wednesday's decision and Thursday's PCE report.",
        "sources": ["Regards of Wallstreet (CNBC/Yahoo)", "Reuters", "Britannica"],
        "source_urls": [
            "https://www.regardsofwallstreet.com/news/stock-market-week-ahead-october-26-2026",
            "https://en.wikipedia.org/wiki/2026_Iran_war",
            "https://www.britannica.com/event/2026-Iran-war",
        ],
    },
    "typhoon-champi-china-coast-2026-10-26": {
        "headline": "Typhoon Champi slams China's east coast after battering Taiwan and Japan",
        "summary": "Typhoon Champi — the strongest storm on Earth of 2026 before weakening — hit China's eastern coast after leaving one dead and 600+ injured in Taiwan and knocking out power to thousands in Okinawa. China issued an orange alert for Jiangsu, Shanghai and Zhejiang, suspended some train services, evacuated tens of thousands in Shanghai and cancelled hundreds of flights.",
        "detail": "Typhoon Champi moved on from Taiwan and Japan's southern islands to strike China's eastern coast over the weekend, the latest phase of a storm that was the strongest on Earth in 2026 before weakening. Taiwan's fire authorities counted more than 600 injuries and one death (a man swept away by waves off Liuqiu island) as the system hammered the island with destructive winds, toppling trees and knocking out power to more than 340,000 households; authorities restored power to over 90% of those as the storm moved away.\n\nIn Okinawa, Japan's southernmost prefecture, two people were injured and power was knocked out to thousands as Champi passed close to the Sakishima Islands and headed northeast toward Kyushu. Hundreds of flights were cancelled across the region, and tourists on Ishigaki island waited for services to resume.\n\nChina braced for the system's arrival with an orange warning — the second-highest alert — for Jiangsu, Shanghai and Zhejiang, warning of heavy to torrential rainfall and strong winds. Authorities suspended some train services, evacuated tens of thousands of residents in Shanghai and cancelled hundreds of flights. The China Meteorological Administration subsequently downgraded Champi, which by late October 25 had transitioned into an extratropical cyclone over the East China Sea and was de-numbered.\n\nForecasters were also tracking another system, Typhoon Rosal, maintaining strength over the sea east of Taiwan, with the Philippines on alert for gale-force winds across parts of Luzon, the Visayas and Mindanao — suggesting the western Pacific's unusually active storm season is not yet over.",
        "sources": ["AFP", "AS English", "China Meteorological Administration"],
        "source_urls": [
            "https://www.afp.com/en/tropical-storm-champi-nears-china-after-battering-taiwan-japan",
            "https://en.as.com/latest_news/typhoon-champi-tracker-live-path-of-strongest-storm-on-earth-in-2026-updates-f202610-d/",
            "https://www.hko.gov.hk/textonly/tc/tcp.htm",
        ],
    },
    "jwst-three-black-holes-dawn-of-time-2026-10-26": {
        "headline": "JWST finds three giant black holes in a single galaxy from the dawn of time",
        "summary": "Astronomers led by the Max Planck Institute detected three actively feeding supermassive black holes in galaxy J0148-4214, 12.5 billion light-years away (seen just 1.2 billion years after the Big Bang) — the first evidence of three active black holes in one ancient galaxy. Two, just 620 light-years apart, are expected to merge; one ~600,000-solar-mass black hole is feeding faster than theory's Eddington limit.",
        "detail": "Astronomers using the James Webb Space Telescope have discovered three actively feeding supermassive black holes inside a single galaxy more than 12.5 billion light-years away — the first evidence of three active black holes in one early-Universe galaxy. The international team, led by the Max Planck Institute for Extraterrestrial Physics (MPE), studied galaxy J0148-4214 at a redshift of z=5.02, meaning its light has taken about 12.5 billion years to reach Earth and we are seeing it just 1.2 billion years after the Big Bang.\n\nTwo of the black holes sit near the galaxy's centre, separated by only about 620 light-years and expected to merge within a few hundred million years. 'This is the first evidence of three active black holes in a single galaxy in the distant Universe,' said Hannah Übler, MPE research group leader and lead author. A third black hole lies about 5,500 light-years from the centre, possibly the remnant of an earlier merger pushed outward by gravitational recoil, or one still drifting inward.\n\nTheir masses are strikingly varied — roughly 80 million, 600,000 and 2 million times the mass of the Sun. The surprise is that the smallest of them, the ~600,000-solar-mass black hole, is feeding most aggressively: its accretion rate exceeds the Eddington limit, the maximum rate predicted by basic models of black hole growth. That unusually rapid growth may help explain how some black holes became extraordinarily massive so early in cosmic history.\n\nThe detection relied on JWST's Near Infrared Spectrograph in integral-field spectroscopy mode (NIRSpec-IFS), which resolves how light varies across the galaxy, allowing the team to separate signals that would otherwise appear as a single black hole. The results, published in Astronomy & Astrophysics (programme BlackTHUNDER), suggest other distant galaxies may harbour multiple growing black holes that have so far gone undetected — and that black hole merging may be an additional fast route to building cosmic giants, with such mergers potentially detectable by future gravitational-wave observatories like LISA.",
        "sources": ["ScienceDaily (Max Planck Institute)", "Astronomy & Astrophysics"],
        "source_urls": [
            "http://www.sciencedaily.com/releases/2026/10/261024222000.htm",
            "https://www.aanda.org/articles/aa/full_html/2026/08/aa57419-25/aa57419-25.html",
        ],
    },
}

# ---- Load existing feed and prepend today ----
with open(FEED) as f:
    feed = json.load(f)

new_day = {"date": DATE, "stories": stories}

# Replace if today already exists (re-run), else prepend
existing = [d for d in feed["days"] if d["date"] != DATE]
days = [new_day] + existing
# Cap at most recent 60 days
days = days[:60]
feed["days"] = days

with open(FEED, "w") as f:
    json.dump(feed, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"feed.json: {len(days)} days, today={DATE} with {len(stories)} stories")

# ---- Deep dives ----
with open(DEEP) as df:
    dd = json.load(df)

today_dd = {}
for st in stories:
    entry = deepdives.get(st["slug"])
    if entry:
        entry = dict(entry)
        entry["updated"] = DATE
        entry["slug"] = st["slug"]
        today_dd[st["slug"]] = entry

# Replace today's date key (re-run) or add
# Drop any stale keys that are no longer in today's story list (re-run safety)
dd["deepdives"][DATE] = today_dd

with open(DEEP, "w") as df:
    json.dump(dd, df, indent=2, ensure_ascii=False)
    df.write("\n")

print(f"deepdives.json: {len(today_dd)} deep-dives for {DATE}")
for k, v in today_dd.items():
    print(f"  {k}: detail_len={len(v.get('detail',''))}, urls={len(v.get('source_urls',[]))}")