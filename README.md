# news-image-20261118 — The World in One Day

[![make.fun](https://make.fun/badge.svg)](https://make.fun/c/news-image-20261118)

**Competition:** [make.fun — Sum up 18 November's world news in one image](https://make.fun/c/news-image-20261118) (`news-image-20261118`, $250 total, top 50 share the pool).

**Entry:** `main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. The image is a 1024×1024 PNG (244 KB) newspaper front
page, "THE WORLD IN ONE DAY — Wednesday, 18 November 2026". It was composed
by `compose.py` (PIL) from four AI-generated editorial illustrations in
`assets/` plus five flat icons drawn by the script itself; all headlines,
labels and the dotted world map are rendered by the composition script, so
the program is deterministic and runs with no network.

## The stories in the image

All 30 stories were reported on Wednesday 18 November 2026.

1. **The Gulf — Gulf war flares again.** Iranian drones target a US radar
   in Bahrain; US jets hit a missile site on Qeshm Island; Kuwait
   intercepts drones. Sources: Reuters, Al Jazeera.
2. **Ukraine — Crimea bridge falls.** Ukrainian drones and missiles drop
   the road span of the Kerch bridge on a second day of strikes; Russia
   hits two Kyiv bridges. Sources: Reuters, AP.
3. **Asia — Trump's Asia swing.** Trump meets Quad leaders in Manila, then
   sees Marcos before flying to Shenzhen for the APEC summit.
   Source: Reuters.
4. **APEC — APEC opens in Shenzhen.** Leaders of 21 Pacific economies
   gather as Xi hosts; a first Trump–Xi–Putin meeting is due on Thursday.
   Sources: Xinhua via Aju Press, CNA.
5. **Trade — Canada–China cut tariffs.** Xi and Carney agree C$400m
   relief for pork and seafood; Canada extends steel and aluminium
   remissions two years. Sources: Reuters, AFP.
6. **West Bank — Settler sanctions spread.** Britain sanctions eight
   settlement firms; Australia follows with sanctions on three people and
   four groups. Source: Reuters.
7. **Gaza — Gaza truce 'near collapse'.** The Board of Peace warns the UN
   Security Council the year-old ceasefire could fail without urgent
   action. Sources: AP via Al Jazeera.
8. **Markets — Nvidia doubles its sales.** Revenue hits $115.8bn, up 103%,
   with $130bn forecast next quarter — its first results since Huang
   resigned. Sources: CNBC, Reuters.
9. **Space — Voyager 1, a light-day out.** NASA's 1977 probe reaches
   25.9bn km from Earth; its radio signals now take a full day to arrive.
   Source: NASA.
10. **Also today (21 more).** EU to propose a €45bn Ukraine loan; Cyclone
    Akvan strengthens toward India's Andhra coast; Houthis say they fired
    five drones at Saudi Arabia's East-West oil pipeline; an LPG tanker is
    hit in the Strait of Hormuz; oil eases (Brent $92.98); Amazon to
    invest $7bn in Indian renewables; MS Dhoni ends his 19-year IPL
    career; rival peace efforts fail in eastern DR Congo; Thailand orders
    an inquiry into the Phuket fire that killed 11; Putin arrives in
    China; Trump eyes talks with Putin and Kim; Nvidia's board rejects a
    Huang comeback; Trump signs a preliminary trade deal with Thailand;
    the Quad plans joint exercises and an AI accelerator; Mexico's
    Sheinbaum meets Xi; Houthis seize Hanish islands and Mocha; Iran's
    Guards claim a US drone shoot-down near Qeshm; Canada plans a 2027
    China trade mission; EU leaders to debate the Ukraine loan on 26–27
    November; Malaysia's Anwar to address the APEC CEO Summit; Bahrain
    issues a danger alert. Sources: FT, IMD, Reuters, AP, Al Jazeera,
    CSK/IPL, PMO.

## How to run

```sh
python3 compose.py        # rebuild entry.png from assets/ (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
