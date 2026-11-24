# 24 November 2026 — The World in One Day

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/adelbudi88-crypto/news-image-24-nov/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/adelbudi88-crypto/news-image-24-nov/reward.svg)](https://make.fun/bounty/news-image-20261124)

A one-image front page summing up the world's news of Tuesday 24 November 2026, built for the [make.fun bounty](https://make.fun/bounty/news-image-20261124).

The image is a newspaper-style poster (1024x1024): a big navy header names the day, **24 November 2026**, and ten stories cover the day across regions and fields:

1. **COP31 ends in deadlock** (Climate, hero panel) — talks collapse in Antalya with no pact, the first COP to close without a deal since Copenhagen 2009; Pacific islands go home empty-handed.
2. **US weighs weeks-long Iran campaign** (US–Iran) — a second carrier sails to the Gulf as Trump warns of "very traumatic" fallout if talks fail.
3. **Strike kills 2, wounds 22 in Zaporizhzhia** (Ukraine) — overnight attack hits homes; 2 children among the wounded, per Reuters.
4. **Russian war dead near 700,000** (War toll) — Meduza–Mediazona estimate from leaked Rosstat records; about 490,000 deaths registered.
5. **Ukraine sinks Russian corvette off Libya** (Sea war) — naval drones hit the Merkury at Benghazi; the Novoshakhtinsk refinery is ablaze and halted.
6. **Candy factory fire: 3 dead, 34 missing** (Indonesia) — blaze guts PT Fonusa Agung Mulia in Cikande, Banten; DNA tests to identify the victims.
7. **EU unveils 22nd Russia sanctions package** (Europe) — 60 banks cut from SWIFT; 70+ shadow-fleet ships listed; Russian flag barred at EU sports events.
8. **Mexico to try "El Chapo Isidro" at home** — despite a US extradition request, the attorney general says he faces trial in Mexico.
9. **Women's World Cup hosts set** — 2031: USA, Mexico, Costa Rica, Jamaica (48 teams); 2035: England, Northern Ireland, Scotland, Wales.
10. **Russian jets enter Korea's air zone** — Seoul scrambles fighters off Ulleung; the alert is lifted in 3 minutes, with no violation.

## How the image was made

`entry.png` was drawn from scratch with Python + Pillow (`tools/draw.py`): flat geometric illustrations (a Pacific island under a hard sun with a "NO DEAL" stamp, a carrier deck at dusk, a damaged block under a rescue beam, a rising toll chart, a listing corvette, a factory in flames, the EU stars over a bank facade) on an off-white newsprint background, navy ink, brick red and gold. No AI image generation, no downloaded images.

Every number on the poster was verified against live news reports on 24 November 2026 before drawing — and three stories from the first draft were **dropped** after verification failed: the "Himalaya floods, 4 dead, ~100 missing" (only matches are the August 2025 Dharali flood, recycled by aggregators), the "Bangladesh typhoid drive for 50 million children" (that campaign launched in October 2025), and the "SoftBank $2bn Intel investment" (signed in August 2025). They were replaced with fresh, verified 23–24 November stories: the EU's 22nd sanctions package, Mexico's decision on "El Chapo Isidro", and the Russian jets over Korea's air defence zone.

## Run

```sh
python3 tools/draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) validates `entry.png` — PNG signature, exactly 1024x1024, at most 1 MiB, and a 10-story manifest — then copies it to `/output/entry.png` and verifies the copy byte-for-byte. Running it twice writes byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
