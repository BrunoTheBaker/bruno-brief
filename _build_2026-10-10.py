#!/usr/bin/env python3
import json, os

base = "/home/rory/Projects/news-pwa"
today = "2026-10-10"

# ---------- Load existing ----------
with open(f"{base}/feed.json") as f:
    feed = json.load(f)
prior_days = feed.get("days", [])

with open(f"{base}/deepdives.json") as f:
    deep = json.load(f)
deepdives = deep.get("deepdives", {})

# ---------- Today's stories ----------
E = {"US Bond Market": "\U0001F1FA\U0001F1F8",
     "Australian Politics": "\U0001F1E6\U0001F1FA",
     "European Politics": "\U0001F1EA\U0001F1FA",
     "AI News": "\U0001F916",
     "Conflicts": "\u2694\uFE0F",
     "Science/Tech": "\U0001F52C",
     "Blowing Up Today": "\U0001F6A8"}

stories = [
 {"bucket":"US Bond Market","slug":"us-treasury-yields-week-close-10yr-5p24-2026-10-10",
  "headline":"US Treasury yields end turbulent week with 10-year at 5.24%",
  "summary":"The 10-year Treasury finished October 9 at 5.24% and the 2-year at 4.80%, easing off multi-year highs after this week's 30-year auction drew solid demand, keeping the market focused on next week's inflation report.",
  "sources":["Advisor Perspectives (dshort)"]},
 {"bucket":"US Bond Market","slug":"us-20yr-yield-surges-5p68-long-end-selloff-2026-10-10",
  "headline":"20-year Treasury yield surges to 5.68% as long-end selloff grinds on",
  "summary":"The 20-year Treasury yield has climbed to 5.68% while the benchmark 10-year hovers near 5.29%, extending a month of aggressive bond selloffs that have hammered fixed-income valuations amid persistent inflation and heavy Treasury supply.",
  "sources":["Stock Market Watch"]},
 {"bucket":"Australian Politics","slug":"labor-reverses-credit-card-surcharge-2026-10-10",
  "headline":"Labor reverses credit card surcharge call after backlash, but businesses still angry",
  "summary":"The Albanese government has walked back its position on credit card surcharges following widespread backlash, though business groups remain unhappy with the final stance announced on October 10.",
  "sources":["ABC News"]},
 {"bucket":"Australian Politics","slug":"working-holiday-visa-changes-backlash-2026-10-10",
  "headline":"Working holiday visa changes trigger regional backlash as tourism leaders head to Canberra",
  "summary":"The government's plan to put second- and third-year working holiday extensions into a limited ballot has sparked anger in the regions, with far-north tourism and agriculture leaders travelling to Canberra to push back.",
  "sources":["Cape York Weekly"]},
 {"bucket":"European Politics","slug":"franco-german-tank-mgcs-row-2026-10-10",
  "headline":"Franco-German tank project rows boil over as Berlin insists MGCS 'is not dead'",
  "summary":"Defence ministers from France and Germany moved to calm a dispute over the Main Ground Combat System after France's top general said Berlin had withdrawn, a fresh strain on Paris-Berlin defence cooperation as Steinmeier visits France.",
  "sources":["POLITICO Europe","Reuters"]},
 {"bucket":"European Politics","slug":"eu-leaders-summit-october-15-16-2026-10-10",
  "headline":"EU leaders gear up for 15-16 October summit on competitiveness, Ukraine and next budget",
  "summary":"The EU's October 15-16 summit will focus on competitiveness, Ukraine, the next long-term budget, the Middle East, defence and migration, the Council said, ahead of the European Parliament debate on priorities.",
  "sources":["Council of the European Union"]},
 {"bucket":"AI News","slug":"reflection-beam-501b-open-model-2026-10-10",
  "headline":"Reflection launches Beam, an open-weight 501B-parameter model for coding and reasoning",
  "summary":"Reflection announced Beam, a sparse mixture-of-experts model with 501 billion parameters (23 billion active) aimed at coding, reasoning and agentic workloads, promising open weights, a technical report and developer tools later this month.",
  "sources":["TheNextGenTechInsider"]},
 {"bucket":"AI News","slug":"mistral-large-4-le-chonk-2026-10-10",
  "headline":"Mistral AI unveils Mistral Large 4 'Le Chonk', a 1-trillion-parameter open model",
  "summary":"Mistral's new flagship, Mistral Large 4, is a roughly 1-trillion-parameter natively multimodal mixture-of-experts model with about 49B active parameters and a 1M context window, in preview now with open weights due by the end of October.",
  "sources":["Mistral AI"]},
 {"bucket":"AI News","slug":"odyssey-3-world-model-physics-iq-2026-10-10",
  "headline":"Odyssey launches Odyssey-3 world model, topping Physics-IQ benchmarks",
  "summary":"Odyssey's Odyssey-3, an autoregressive diffusion world model, scores a reported state-of-the-art 66.1 on Physics-IQ Verified and can steer robot arms, with a free real-time browser research preview now live.",
  "sources":["AICoder","MarkTechPost"]},
 {"bucket":"Conflicts","slug":"kramatorsk-bus-strike-33-killed-2026-10-10",
  "headline":"Russian strike on Kramatorsk buses kills 33 in one of deadliest recent attacks",
  "summary":"A Russian glide-bomb strike on two passenger buses in Kramatorsk on October 8 killed at least 33 people and wounded 18, one of the deadliest single attacks in the current phase of the war as Moscow intensifies strikes on cities.",
  "sources":["BBC","Al Jazeera","RBC-Ukraine"]},
 {"bucket":"Conflicts","slug":"ukraine-operation-vivaldi-donetsk-counteroffensive-2026-10-10",
  "headline":"Ukraine pushes Russia back in Donetsk as Operation Vivaldi gains ground",
  "summary":"Ukraine's 'Operation Vivaldi' has reclaimed roughly 175 sq km around Lyman, and Ukrainian forces are advancing east of Sloviansk and Kramatorsk, while Russian casualty rates hit a monthly record according to Ukrainian figures.",
  "sources":["Al Jazeera","Institute for the Study of War"]},
 {"bucket":"Science/Tech","slug":"fda-pritelivir-hovilpri-herpes-2026-10-10",
  "headline":"FDA approves pritelivir (Hovilpri), a long-awaited new herpes treatment",
  "summary":"The FDA approved pritelivir (Hovilpri) for refractory mucocutaneous herpes lesions in immunocompromised adults never before served by a dedicated therapy, after phase 3 data showed complete healing in about two-thirds of patients by day 28.",
  "sources":["Healio","Contemporary OB/GYN"]},
 {"bucket":"Science/Tech","slug":"nasa-final-commercial-leo-station-rfp-2026-10-10",
  "headline":"NASA issues final commercial low-Earth-orbit station solicitation, proposals due December 8",
  "summary":"NASA released its final Request for Proposals for next-generation commercial space stations on October 9, with responses due December 8, as the agency pushes to transition beyond the International Space Station.",
  "sources":["NASA"]},
 {"bucket":"Blowing Up Today","slug":"hurricane-isaias-category3-landfall-2026-10-10",
  "headline":"Hurricane Isaias slams Gulf Coast as first major hurricane of 2026",
  "summary":"Hurricane Isaias strengthened to a Category 3 storm with winds of 111-129 mph and made landfall on the northern Gulf Coast on the night of October 9, bringing damaging winds, storm surge and flooding to Florida, Alabama and Mississippi as evacuations expanded.",
  "sources":["CNN","USA Today","The Guardian"]},
]

for s in stories:
    s["emoji"] = E[s["bucket"]]

today_day = {"date": today, "stories": stories}

# ---------- Prepend today, cap at 60 days ----------
new_days = [today_day] + [d for d in prior_days if d.get("date") != today]
# cap 60 (should be far under)
new_days = new_days[:60]
feed["days"] = new_days

# ---------- Deep dives ----------
D = {}

D["us-treasury-yields-week-close-10yr-5p24-2026-10-10"] = {
 "headline":"US Treasury yields end turbulent week with 10-year at 5.24%",
 "summary":stories[0]["summary"],
 "detail":("The U.S. Treasury market finished a turbulent week on Friday, October 9, 2026, with the yield on the benchmark 10-year note closing at 5.24% and the 2-year note at 4.80%, according to the Advisor Perspectives dshort Treasury snapshot. The week began with yields pressing toward multi-year highs as investors wrestled with sticky inflation and heavy government supply, before a mid-week pullback eased some of the pressure on long-dated debt.\n\nA significant part of the story was the Treasury's weekly refunding, which reopened $22 billion of 30-year bonds on October 9. The auction cleared at a high yield of 5.618%, just above the when-issued level, with a bid-to-cover ratio of 2.54 times — above the recent 2.41 average — and direct bidder participation of 20.89%, also above average. Demand measures suggested investors were willing to absorb long-dated debt at elevated yields, a tentative stabilizing signal for a market that has repriced sharply higher over the past month.\n\nFederal Reserve commentary kept the selloff on trial. Governor Christopher Waller's hawkish remarks about the potential need for more rate hikes remained a counterweight, reinforcing that the retreat in yields could prove shallow if inflation data disappoint. Traders increasingly parsed the auction as a pause in the long-end repricing rather than a durable reversal.\n\nWith markets closed over the weekend, attention now turns to the coming week's economic calendar, led by the Consumer Price Index report, which will help determine whether the recent stabilization holds or whether the multi-year high grind resumes. The 10-year yield has roughly doubled its distance from the lows seen earlier in the cycle, and strategists warn the direction hinges on whether inflation continues to run above the Fed's comfort zone."),
 "sources":["Advisor Perspectives (dshort)","Stock Market Watch","U.S. Treasury"],
 "source_urls":["https://www.advisorperspectives.com/dshort/updates/2026/10/09/treasury-yields-snapshot-october-9-2026","https://stockmarketwatch.com/bonds/reports/october-2026","https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve"]}

D["us-20yr-yield-surges-5p68-long-end-selloff-2026-10-10"] = {
 "headline":"20-year Treasury yield surges to 5.68% as long-end selloff grinds on",
 "summary":stories[1]["summary"],
 "detail":("The long end of the U.S. Treasury curve has come under sustained pressure, with the 20-year yield climbing to 5.68% while the benchmark 10-year sits near 5.29%, according to Stock Market Watch's October bond market report. Over the past month the market has witnessed aggressive selloffs that have pushed fixed-income valuations sharply lower.\n\nThe move reflects a convergence of forces: persistent inflation readings, expectations of less Federal Reserve easing than previously priced, and a heavy calendar of Treasury issuance as the government finances a large deficit. Longer maturities, which are most sensitive to inflation and term-premium expectations, have borne the brunt of the repricing.\n\nFor borrowers, rising long-term yields feed directly into mortgage rates, corporate borrowing costs and the discount rates used to value equities and other assets, amplifying the market-wide effect. The steep rise in the 20- and 30-year maturities, in particular, has drawn comparisons to the bond-vigilante episodes of previous cycles as investors demand greater compensation for holding long-dated government debt.\n\nStrategists note that stabilisation will depend on evidence that inflation is durably cooling and on the Treasury's ability to place large auctions without weak demand. The coming CPI release and the trajectory of weekly auctions are seen as the key tests of whether the long-end selloff has further to run or is nearing a peak."),
 "sources":["Stock Market Watch"],
 "source_urls":["https://stockmarketwatch.com/bonds/reports/october-2026"]}

D["labor-reverses-credit-card-surcharge-2026-10-10"] = {
 "headline":"Labor reverses credit card surcharge call after backlash, but businesses still angry",
 "summary":stories[2]["summary"],
 "detail":("The Albanese government has reversed its position on credit card surcharges, backing away from an earlier approach after a wave of public and business criticism, according to ABC News chief digital political correspondent Clare Armstrong. The about-face, reported on October 10, 2026, came after the issue became a lightning rod in the cost-of-living debate.\n\nPolitically, surcharges on card payments have become an emotive topic as Australians feel the squeeze of higher living costs. The government had been weighing options to limit or restrict the surcharges merchants pass on to consumers, a move that angered small-business and hospitality groups who rely on the fees to cover payment-processing costs.\n\nWhile Labor's decision to walk back its earlier call was framed as a response to the backlash, business organisations remained unhappy with the final position. Industry representatives argued that any restriction on cost recovery would squeeze already-thin margins and that consumers would ultimately pay in other ways, such as higher prices or surcharge caps that shift costs onto specific customer groups.\n\nThe episode illustrates the balancing act facing the government on consumer-protection measures versus business viability, and it comes as cost-of-living issues dominate the political agenda ahead of the next election. The outcome is likely to be scrutinised closely by both consumer advocates, who wanted tougher limits, and business lobbies, who wanted the government to stay out of pricing decisions."),
 "sources":["ABC News"],
 "source_urls":["https://www.abc.net.au/news/2026-10-10/labor-reverses-credit-card-surcharge-call-after-backlash/107247904"]}

D["working-holiday-visa-changes-backlash-2026-10-10"] = {
 "headline":"Working holiday visa changes trigger regional backlash as tourism leaders head to Canberra",
 "summary":stories[3]["summary"],
 "detail":("The Albanese government's changes to the Working Holiday Maker visa program have triggered a regional backlash, with tourism and agriculture leaders from far north Queensland preparing to lobby Parliament House for amendments, the Cape York Weekly reported on October 10, 2026.\n\nThe central controversy is the move to place extensions for a second or third year of a working holiday stay into a limited ballot, effectively capping the number of backpackers who can prolong their time in Australia. Regional employers argue the program is a vital source of seasonal labour for fruit picking and the hospitality and tourism sectors, which are heavily dependent on these workers.\n\nCritics, including LNP Cook MP David Kempton and Shadow Minister for Resources and Northern Australia Senator Susan McDonald, characterised the move as the government squeezing the program to hit migration targets while the big-ticket numbers come from the student-visa cohort. Home Affairs figures cited by Senator McDonald show roughly 592,000 student visa holders against about 211,000 working holiday makers as of June 2025 — about 2.8 students for every backpacker.\n\nLeichhardt MP Matt Smith defended the national framework, arguing the changes would end exploitation and rorts while ensuring the program delivers the skills the economy needs. The group heading to Canberra is seeking a unified front of industry leaders to negotiate amendments with senior cabinet members before the new rules settle."),
 "sources":["Cape York Weekly","The Australian"],
 "source_urls":["https://capeyorkweekly.com.au/tourism-leaders-mp-rally-in-face-of-flagged-working-holiday-visa-changes/27152/"]}

D["franco-german-tank-mgcs-row-2026-10-10"] = {
 "headline":"Franco-German tank project rows boil over as Berlin insists MGCS 'is not dead'",
 "summary":stories[4]["summary"],
 "detail":("Franco-German defence cooperation hit another rough patch in early October 2026 after France's top general said Germany had effectively pulled out of the Main Ground Combat System (MGCS), the flagship next-generation tank project. The admission, made by French Chief of Defence Staff General Fabien Mandon during a parliamentary budget hearing on October 8, prompted an unusually public dispute that spilled across the following days.\n\nThe MGCS — involving KNDS France, KNDS Germany, Rheinmetall and Thales — had been bogged down for years in delays, industrial disputes and political tensions. Mandon told lawmakers that 'the outcome isn't good' and that the Germans had decided to drop out. He later partially backpedalled in a written statement, saying the work had not been in vain and arguing the program was merely delayed into the late 2040s.\n\nGerman Defence Minister Boris Pistorius and French Armed Forces Minister Catherine Vautrin moved on October 9 to contain the damage, meeting near Bordeaux and insisting the MGCS 'remains a relevant project' and 'is not over, is not dead'. Significantly, Pistorius said the two countries would still cooperate on unmanned systems and automated processing, while rejecting that the project would meet the same fate as the Future Combat Air System fighter jet program, which collapsed before the summer.\n\nThe episode deepened a sense among some French lawmakers that defence cooperation with Germany is at an all-time low, with some calling for Paris to seek other partners. It unfolded as German President Frank-Walter Steinmeier was on his first state visit to France in 13 years, a trip centred on space and security that highlighted both the closeness and the strains in the bilateral relationship."),
 "sources":["POLITICO Europe","Reuters","DW"],
 "source_urls":["https://www.politico.eu/article/france-germany-joint-tank-project-mgcs/","https://www.straitstimes.com/world/europe/berlin-rejects-claim-it-dropped-franco-german-tank-project","https://www.dw.com/en/franco-german-relations-steinmeier-and-macron-say-their-farewells-and-create-a-new-momentum-for-europe/a-79618635"]}

D["eu-leaders-summit-october-15-16-2026-10-10"] = {
 "headline":"EU leaders gear up for 15-16 October summit on competitiveness, Ukraine and next budget",
 "summary":stories[5]["summary"],
 "detail":("EU leaders are preparing for a two-day European Council summit on October 15-16, 2026, in Brussels, with a packed agenda spanning competitiveness, Ukraine, the next Multiannual Financial Framework (the EU's long-term budget), the Middle East, European defence and security, migration, and enlargement reforms, according to the Council of the European Union's forward-looking agenda published October 9.\n\nAhead of the summit, the European Parliament is holding a debate on its priorities for the meeting with Commission President Ursula von der Leyen and the Irish Council Presidency. Lawmakers are also expected to discuss the state of negotiations on the EU's next long-term budget, following the demands MEPs tabled in April.\n\nThe summit comes at a sensitive moment for the EU budget, with the bloc's four centrist parliamentary groups — EPP, S&D, Renew Europe and the Greens/EFA — having threatened in recent days to reject the draft multiannual financial framework for 2028-2034 unless revisions are made. The Council discussions will need to navigate those tensions while also addressing the continued fallout of Russia's war on Ukraine and the push to strengthen European defence production.\n\nOn enlargement, the agenda reflects momentum on Ukraine's accession path after Hungary moved toward lifting its veto on two negotiating clusters, and follows recent EU summit conclusions about the strategic importance of enlargement. The October meeting is widely seen as a staging point for the bloc's competitiveness drive and for locking in financial and security commitments before the end of the year."),
 "sources":["Council of the European Union","EUbusiness"],
 "source_urls":["https://www.consilium.europa.eu/en/press/press-releases/2026/10/09/forward-look-2026/","https://www.eubusiness.com/politics/eucalendar/"]}

D["reflection-beam-501b-open-model-2026-10-10"] = {
 "headline":"Reflection launches Beam, an open-weight 501B-parameter model for coding and reasoning",
 "summary":stories[6]["summary"],
 "detail":("Reflection announced Beam, its first open-weight model designed specifically for coding, reasoning and agentic workloads, according to coverage from TheNextGenTechInsider published October 10, 2026. Beam is a sparse mixture-of-experts (MoE) model with 501 billion total parameters, of which about 23 billion are activated per token during inference.\n\nThe release is positioned as a strategic push to advance the Western open-weight frontier, offering a highly inference-efficient alternative to much larger proprietary models. While some frontier models retain higher raw capability, Reflection argues Beam's superior compute efficiency makes it a practical 'workhorse' for enterprise-scale agentic and coding applications.\n\nAs of the announcement, Beam was still undergoing final red-teaming and evaluations. Reflection plans to release the model weights, its technical report, a model card and developer artifacts later in October, with users able to sign up for early access on the company's website in the meantime.\n\nThe launch is the latest in a wave of large open-weight releases alongside models such as Mistral Large 4, as the open ecosystem pushes toward frontier-level performance on efficiency-conscious enterprise deployments rather than raw benchmark dominance alone."),
 "sources":["TheNextGenTechInsider","Reflection"],
 "source_urls":["https://thenextgentechinsider.com/pulse/reflection-launches-beam-a-501b-parameter-moe-model-for-coding-and-reasoning"]}

D["mistral-large-4-le-chonk-2026-10-10"] = {
 "headline":"Mistral AI unveils Mistral Large 4 'Le Chonk', a 1-trillion-parameter open model",
 "summary":stories[7]["summary"],
 "detail":("Mistral AI opened a public preview of Mistral Large 4, nicknamed 'Le Chonk', on October 6, 2026, marking a major escalation in the European lab's frontier ambitions. The model is a natively multimodal mixture-of-experts architecture with roughly 1.05 trillion total parameters and about 49 billion active per token, supporting a 1 million-token context window and native image input.\n\nAccording to Mistral and independent analysis from MarkTechPost, the model was trained from scratch on 3,800 NVIDIA Grace Blackwell GPUs in Mistral's own EU data centres, underscoring the company's push for sovereign European compute. The 1M context window and native multimo-dality position it for long-document and enterprise agentic workloads.\n\nMistral celebrates the model's size — the nickname 'Le Chonk' plays on its heft — but emphasises that the granular MoE design keeps inference efficient despite the scale. An API preview is available now on Mistral Studio, with open weights promised by the end of October.\n\nFor the Western open-weight ecosystem, Mistral Large 4 is a significant entry, joining a crowded field of large open models released over the past week, including Reflection's Beam. It reflects an accelerating trend of labs publishing frontier-scale open weights aimed squarely at enterprise-scale, agent-heavy deployments."),
 "sources":["Mistral AI","MarkTechPost","Mistral Docs"],
 "source_urls":["https://mistral.ai/news/mistral-large-4/","https://www.marktechpost.com/2026/10/06/mistral-ai-releases-mistral-large-4-le-chonk-a-1-05t-parameter-open-weight-multimodal-moe/","https://docs.mistral.ai/models/mistral-large-4-0"]}

D["odyssey-3-world-model-physics-iq-2026-10-10"] = {
 "headline":"Odyssey launches Odyssey-3 world model, topping Physics-IQ benchmarks",
 "summary":stories[8]["summary"],
 "detail":("Odyssey released Odyssey-3 on October 8, 2026, describing it as its most capable foundation world model. Built as an autoregressive diffusion transformer, it predicts in real time how an environment evolves given past observations and the latest actions or injected events, rather than only generating short clips.\n\nOn benchmark results reported by the company, Odyssey-3 Pro (720p) scores 66.1 on Physics-IQ Verified for video-to-video with best-of-8 sampling (63.4 prompt-enhanced), which Odyssey calls the highest reported score, alongside 54.7 for image-to-video. The standalone 480p model scores 51.8 base and 64.4 with best-of-8. Odyssey also claims first place in three of four WorldMark categories in its own evaluations.\n\nA notable feature is the physical-AI dimension: an action decoder trained on observation-action pairs maps the model's representations to robot-arm controls, and Odyssey says tens of hours of demonstrations are enough to steer several robot arms, including showing recovery behaviours not present in the training data.\n\nAccess-wise, Odyssey is offering a free browser research preview running a faster Flash variant with first- and third-person navigation and an independent camera, while API access is by request. No open weights or public pricing have been published, and the public API docs still describe the older Odyssey-2 Pro. The release signals intensifying competition in world models, which aim to give AI systems an internal model of physical environments."),
 "sources":["AICoder","MarkTechPost"],
 "source_urls":["https://aicoder.com/news/news-20261009-odyssey-3-world-model-physics-iq-sota"]}

D["kramatorsk-bus-strike-33-killed-2026-10-10"] = {
 "headline":"Russian strike on Kramatorsk buses kills 33 in one of deadliest recent attacks",
 "summary":stories[9]["summary"],
 "detail":("A Russian glide-bomb strike on two passenger buses in the eastern Ukrainian town of Kramatorsk on the morning of October 8, 2026, killed at least 33 people and wounded 18, according to Donetsk Regional Military Administration Head Vadym Filashkin. The attack, which sparked fires in both buses and an open area, is one of the deadliest single strikes in the current phase of the war.\n\nThe strike was part of a broader surge of Russian attacks on Ukrainian cities and civilian infrastructure. Since the start of October, strikes have also hit Pryluky in the Chernihiv region, where a cruise missile demolished a five-storey building, and Kyiv, as Russian forces escalate their long-range bombardment while Ukrainian units press counteroffensives in the east.\n\nThe Kramatorsk attack drew international condemnation. The scale of recent civilian casualties prompted a United Nations Security Council emergency meeting on October 9, where UN human rights chief Volker Türk described the manner and scale of attacks as 'reprehensible'. The UN reported at least 85 Ukrainian civilians killed and 346 injured in Russian strikes in the week since the previous Monday, with long-range strikes on power infrastructure leaving parts of the country without electricity.\n\nUkrainian officials and analysts note that Russia's use of jet-powered Geran-4 and Geran-5 drones, guided by satellite, inertial navigation and on-board landmark cameras, points to deliberate targeting of civilian sites. The Kramatorsk bus strike, occurring as two cities halted public transport, fits a pattern of attacks designed to force civilians to flee the Donetsk fortress cities ahead of possible ground assaults."),
 "sources":["BBC","Al Jazeera","RBC-Ukraine","UN News"],
 "source_urls":["https://www.bbc.com/news/articles/c875pwq134l3o","https://www.aljazeera.com/news/2026/10/8/more-killed-in-kramatorsk-as-russia-targets-ukraines-transportation-system","https://newsukraine.rbc.ua/news/deadly-kramatorsk-bus-strike-claims-30-lives-1791455240.html","https://news.un.org/en/story/2026/10/1168564"]}

D["ukraine-operation-vivaldi-donetsk-counteroffensive-2026-10-10"] = {
 "headline":"Ukraine pushes Russia back in Donetsk as Operation Vivaldi gains ground",
 "summary":stories[10]["summary"],
 "detail":("Ukrainian forces are pushing Russia back in the eastern Donetsk region, with the counteroffensive dubbed 'Operation Vivaldi' reclaiming roughly 175 square kilometres (67 square miles) of previously occupied territory around Lyman this year, according to Al Jazeera reporting on October 9, 2026.\n\nRussian sources, including the Kremlin-aligned Rybar channel, acknowledged that Moscow's forces were losing villages south of Lyman and being forced to defend previously occupied positions rather than launch new offensives. The Institute for the Study of War (ISW) reports Ukrainian counterattacks east of Sloviansk and Kramatorsk, including reported advances toward the key high-ground village of Kryva Luka on the Siverskyi-Donets River, which could serve as a base for further eastward pushes.\n\nThe Ukrainian Ministry of Defence says its campaign to disrupt Russian ammunition and fuel flows struck a record number of air-defence assets and targets more than 50km behind the front in September. On casualties, Ukraine's military puts Russian losses at a record monthly high of 46,230 for September, with more than 70 percent confirmed kills, and the commander of Ukraine's Unmanned Systems Forces reported enemy casualties up 40 percent in the first five days of October versus the same period in September.\n\nISW cautions that Russian milbloggers are acknowledging the Ukrainian advances may have cascading effects, complicating Moscow's efforts to seize the 'Fortress Belt' cities of Sloviansk and Kramatorsk. President Zelenskyy told Reuters that Operation Vivaldi has been successful but incomplete, as Russia responds with intensified glide-bomb and drone strikes on Ukrainian cities."),
 "sources":["Al Jazeera","Institute for the Study of War"],
 "source_urls":["https://www.aljazeera.com/news/2026/10/9/ukraine-pushes-russia-back-in-donetsk-as-military-civilian-casualties-soar","https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-8-2026/"]}

D["fda-pritelivir-hovilpri-herpes-2026-10-10"] = {
 "headline":"FDA approves pritelivir (Hovilpri), a long-awaited new herpes treatment",
 "summary":stories[11]["summary"],
 "detail":("The U.S. Food and Drug Administration approved pritelivir (branded Hovilpri) for the treatment of mucocutaneous herpes simplex virus (HSV) lesions in immunocompromised adults who have not responded to acyclovir, valacyclovir or famciclovir, according to Healio and Contemporary OB/GYN reporting on October 9, 2026.\n\nPritelivir is a novel helicase-primase inhibitor, a different mechanism of action from the nucleoside analogues that have long been the standard of care. It received priority review, and the approval was based on Part C of the phase 3 PRIOH-1 trial, a randomized, open-label, comparator-controlled superiority study.\n\nIn the trial, pritelivir completely healed lesions by day 28 in about 63 percent of patients versus 34 percent in the comparator group across the 101 adults studied, per the FDA. The therapy targets a patient population with few good options — immunocompromised individuals with recurrent, sometimes painful lesions that fail to clear on standard antivirals, some due to documented acyclovir resistance.\n\nFor patients with weakened immune systems — from HIV, transplant or cancer treatment — persistent HSV lesions can be debilitating and slow to heal, making a new-mechanism treatment a meaningful advance. The approval also underscores the continued viability of antiviral drug development for infections that, while common, lack adequate options for the highest-risk patients."),
 "sources":["Healio","Contemporary OB/GYN","FDA"],
 "source_urls":["https://www.healio.com/news/infectious-disease/20261009/fda-approves-hovilpri-for-herpes-simplex-virus-lesions","https://www.contemporaryobgyn.net/view/fda-approves-pritelivir-hovilpri-refractory-hsv-immunocompromised"]}

D["nasa-final-commercial-leo-station-rfp-2026-10-10"] = {
 "headline":"NASA issues final commercial low-Earth-orbit station solicitation, proposals due December 8",
 "summary":stories[12]["summary"],
 "detail":("On October 9, 2026, NASA issued its final Request for Proposals for the next generation of commercial space stations, with proposals due December 8, according to an advisory updated that day on the agency's news page.\n\nThe solicitation is the culmination of NASA's strategy to transition human spaceflight in low-Earth orbit from the International Space Station to commercially owned and operated destinations. The agency has been steadily working to seed a private LEO economy, and this final RFP formalises the requirements for companies seeking to build and operate stations that can host NASA astronauts and research.\n\nThe move comes shortly after the departure of resupply/crew cargo traffic to the ISS was adjusting for newer vehicles — NASA noted revised timing for the Cygnus XL spacecraft's deorbit after it delivered more than 11,000 pounds of supplies, science experiments and other cargo to the station.\n\nThe commercial LEO strategy is central to NASA's plan for a smooth handoff from the ISS, which is expected to be deorbited in the early 2030s. Timing of the December deadline signals NASA's intent to lock in its commercial-partner architecture on a firm schedule, giving industry a clear target as multiple private station concepts compete for federal and commercial customers."),
 "sources":["NASA"],
 "source_urls":["https://www.nasa.gov/2026-news-releases/"]}

D["hurricane-isaias-category3-landfall-2026-10-10"] = {
 "headline":"Hurricane Isaias slams Gulf Coast as first major hurricane of 2026",
 "summary":stories[13]["summary"],
 "detail":("Hurricane Isaias strengthened into a Category 3 storm with maximum sustained winds between 111 and 129 mph and closed in on the U.S. Gulf Coast for an expected landfall on the night of October 9, 2026, according to CNN, USA Today and The Guardian live coverage.\n\nIsaias is the ninth named storm, the first hurricane and the first major hurricane of the 2026 Atlantic hurricane season. It formed from a low-pressure area over the southwestern Gulf of Mexico on October 6 and, upon reaching hurricane strength, broke the record for the latest first hurricane of a season before rapidly intensifying as it headed north.\n\nForecasters warned residents in the storm's path faced a 'gustier-than-normal' hurricane, with impacts expected across portions of Florida, Alabama and Mississippi, including a dangerous storm surge, damaging winds, heavy rainfall and the risk of flash and river flooding. The northern Gulf Coast expanded evacuations as the storm neared, and President Trump reportedly cancelled a trip to the Alabama-Georgia football game amid the hurricane.\n\nAfter landfall, the storm is expected to weaken as it moves inland, but it will continue to pose threats through rainfall, flooding and the possibility of tornadoes well inland. State and local emergency management agencies coordinated shelter and evacuation efforts as the first major storm of the season bore down on a densely populated stretch of coastline."),
 "sources":["CNN","USA Today","The Guardian"],
 "source_urls":["https://www.cnn.com/2026/10/09/weather/live-news/hurricane-isaias-gulf-storm","https://www.usatoday.com/story/news/weather/2026/10/09/hurricane-isaias-landfall-updates-forecast--live/92157423007/","https://www.theguardian.com/world/live/2026/oct/09/hurricane-isaias-path-landfall-florida-category-3-storm-latest-updates"]}

deepdives[today] = D
deep["deepdives"] = deepdives

# ---------- Write ----------
with open(f"{base}/feed.json","w") as f:
    json.dump(feed, f, indent=2, ensure_ascii=False)
    f.write("\n")
with open(f"{base}/deepdives.json","w") as f:
    json.dump(deep, f, indent=2, ensure_ascii=False)
    f.write("\n")

# ---------- Validate ----------
print("feed days:", [d["date"] for d in feed["days"]])
print("today stories:", len(feed["days"][0]["stories"]))
print("deepdives today:", len(deepdives[today]))
for slug, entry in deepdives[today].items():
    detail_len = len(entry.get("detail",""))
    assert detail_len > 300, f"short detail {slug}: {detail_len}"
print("all details >300 chars OK")
