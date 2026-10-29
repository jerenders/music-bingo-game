# Music Bingo

A music bingo game for hosting nights out. Line up categories, print cards (or let players use their phones), and play song clips from YouTube on a projector. One static page, no server, no accounts.

**Play it:** https://endrs.us/bingo  (personal, non-commercial use only; see [Please note](#please-note) and `NOTICE.md`)

## What it does

- 36 categories (decades, movie soundtracks, one-hit wonders, hip hop, spooky songs, sugar and sweets, and more), each with roughly 40 to 90 songs.
- Host mode: pick the games for the night, choose a win type (any line, outside edges, both diagonals, full card), and play 30 second to 90 second clips with a join QR and a played list for the room. Present mode is laid out for a TV or projector.
- Players join by scanning a QR code and get a card on their phone, with no server. Printed cards work too, with a number you type into the host's card checker.
- Card numbers are deterministic: a card is a seeded shuffle of the category's song list, so any card can be rebuilt and checked later.

## Run it

Needs Python 3. Optional: `pip install pyphen` for word hyphenation on phone cards.

```bash
./dev
```

Open http://localhost:8765. It rebuilds when the source changes. To build once:

```bash
python3 scripts/build.py   # writes dist/index.html and songs/<category>-<hash>.json
```

`dist/index.html` is a single file. Host it anywhere that serves static files over https (the phone camera scanner needs https), and publish the `songs/` folder and `vendor/jsqr.min.js` next to it.

## Song lists

Songs live in `data/categories/*.json` (title, artist, YouTube video ID). Categories are listed in `scripts/build.py`.

Each build writes the category's song list to `songs/<category>-<hash>.json`, named by a hash of its contents. Phones and printed cards rebuild their exact card from that hash, so **never delete or edit files in `songs/` once you have handed out cards**.

Release years are in `data/years.json` and movie names in `data/movies.json`.

Videos must be embeddable. Check an ID with:

```
https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json
```

200 with the right title means good, 401 means embedding is disabled, 404 means the video is gone. Videos get removed over time, so re-check before a night. See `data/research/finding-videos.md`.

## Please note

**This is for personal, non-commercial use only**: family, friends and other free, private gatherings. Do not use it at paid or commercial events, in bars, restaurants or venues, or for anything that earns money. Full details are in [`NOTICE.md`](NOTICE.md).

- The game plays copyrighted music through YouTube's embedded player. YouTube's terms don't allow that at paid or commercial events, and the music belongs to its rights holders. A business version would need a properly licensed music service.
- If you host from a browser signed in to YouTube Premium, clips play without ads. Without it, ads can appear and delay a clip.
- Song lists were assembled from memory and from public bingo cards. Artists, years and movie names may be wrong, and many videos are third-party uploads that can disappear. Nothing was listened to in full, so check clips yourself before a night with kids.
- Not affiliated with YouTube or any music label, venue or bingo company.

## Credits and licenses

The code is MIT licensed (see `LICENSE`). Bundled third-party files in `vendor/`:

- `qrcode.min.js`: qrcode-generator by Kazuhiko Arase (MIT)
- `jsqr.min.js`: jsQR 1.4.0 (Apache-2.0, see `vendor/jsqr.LICENSE`)
- `anton-latin-400.woff2`: Anton font (SIL OFL, see `vendor/anton.OFL.txt`)
