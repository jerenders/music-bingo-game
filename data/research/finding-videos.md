# Finding YouTube videos for music bingo

Goal: for each song, a YouTube video ID that (a) is the right song and (b) is EMBEDDABLE.

1. Before searching, check data/research/known_ids.json (keys "title | artist" lowercased -> verified videoId). Reuse a match without searching.
2. Otherwise use ONE WebSearch per song, e.g. `"<title>" <artist> official video youtube`. Pick a youtube.com/watch?v=ID from the artist's own channel, VEVO, label, or "<artist> - Topic" (official audio). Avoid fan/lyric re-uploads when an official one exists. Prefer clean/radio versions.
   The shared WebSearch budget is small. Never spend more than 2 searches on one song; if it fails, record null and move on.
3. VERIFY every new ID with WebFetch on
   https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=ID&format=json
   (prompt: "return the title and author_name, or the error"). 200 + matching title = good. 401 = embedding disabled (try another upload). 404 = bad ID.
   Pace it: at most 4 WebFetch calls at a time. If you get HTTP 429, wait, then continue more slowly. Never record an unverified ID.
4. youtube.com/results search pages are blocked; don't try them.
5. Budget: the WebSearch limit is shared by every helper running at once (about 200 per round). Spend at most 40 searches per category. Reuse known IDs first; when the budget runs out, record null rather than guessing.
