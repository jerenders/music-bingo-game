"""Builds dist/index.html from src/template.html + data/categories/*.json.
Also writes songs/<category>-<hash>.json for every song-list version (never delete these).
Run from the repo root: python3 scripts/build.py
"""
import json, os, re
cats = [
    ("halloween", "Spooky Sounds", ["data/categories/new_spooky2.json"]),
    ("80s", "Best of the '80s", ["data/categories/songs_80s.json", "data/categories/new_80s.json"]),
    ("90s", "Best of the '90s", ["data/categories/songs_90s.json", "data/categories/new_90s.json"]),
    ("funnymovies", "Funny Movie Soundtracks", ["data/categories/new_funnymovies.json"]),
    ("80smovies", "'80s Movie Soundtracks", ["data/categories/new_80smovies.json"]),
    ("90smovies", "'90s Movie Soundtracks", ["data/categories/new_90smovies.json"]),
    ("tv", "TV Theme Songs", ["data/categories/new_tv.json"]),
    ("misheard", "Misheard Lyrics", ["data/categories/new_misheard.json"]),
    ("kids", "Kids' Favorites", ["data/categories/new_kids.json"]),
    ("comedy", "Novelty & Comedy Songs", ["data/categories/new_comedy.json"]),
    ("internet", "Internet Famous", ["data/categories/new_internet.json"]),
    ("wedding", "Wedding Reception Bangers", ["data/categories/new_wedding.json"]),
    ("karaoke", "Drunk Karaoke", ["data/categories/new_karaoke.json"]),
    ("guilty", "Guilty Pleasures", ["data/categories/new_guilty.json"]),
    ("sad", "Secretly Sad Songs", ["data/categories/new_sad.json"]),
    ("food", "Food & Drink", ["data/categories/new_food.json"]),
    ("stadium", "Stadium Anthems", ["data/categories/new_stadium.json"]),
    ("onehit", "One Hit Wonders", ["data/categories/songs_onehit.json", "data/categories/new_onehit.json"]),
    ("hiphop", "Hip Hop", ["data/categories/songs_hiphop.json", "data/categories/new_hiphop.json"]),
    ("movies", "Movie Soundtracks", ["data/categories/songs_movies.json", "data/categories/new_movies.json"]),
    ("musicals", "Musicals Through the Years", ["data/categories/new_musicals.json"]),
    ("yacht", "Yachty by Nature", ["data/categories/songs_yacht.json", "data/categories/new_yacht.json", "data/categories/new_yacht_cards.json"]),
    ("money", "Money and Wealth", ["data/categories/songs_money.json", "data/categories/songs_money_add.json", "data/categories/new_money.json"]),
    ("places", "Places", ["data/categories/songs_places.json", "data/categories/new_places.json", "data/categories/new_places_cards.json"]),
    ("summer", "Summertime", ["data/categories/songs_summer.json", "data/categories/new_summer.json", "data/categories/new_summer_cards.json"]),
    ("reggae", "Reggae", ["data/categories/songs_reggae.json", "data/categories/new_reggae.json"]),
    ("pop", "Best of Pop", ["data/categories/new_pop.json"]),
    ("weather", "Weather Forecast", ["data/categories/new_weather.json"]),
    ("late", "Late Greats", ["data/categories/new_late.json"]),
    ("everyday", "Everyday Tunes", ["data/categories/new_everyday.json"]),
    ("rock00", "2000's Rock", ["data/categories/new_rock00.json"]),
    ("grammar", "Grammar Police", ["data/categories/new_grammar.json"]),
    ("disco", "Disco Hits", ["data/categories/new_disco.json"]),
    ("lucky", "Lucky Numbers", ["data/categories/new_lucky.json"]),
    ("sweets", "Sugar & Sweets", ["data/categories/new_sweets.json"]),
    ("quarantine", "Quarantine 2020", ["data/categories/songs_quarantine.json", "data/categories/new_quarantine.json"]),
]
# Retired categories stay in the data (old join codes and saved lineups still need them) but are hidden from the picker.
RETIRED = {"quarantine"}
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
data = {}
for key, name, files in cats:
    songs, missing, ids, titles = [], [], set(), set()
    for fn in files:
        if not os.path.exists(fn):
            print("MISSING FILE", fn); continue
        for r in json.load(open(fn)):
            vid = r.get("videoId")
            if not vid:
                missing.append(r["title"]); continue
            if vid in ids or norm(r["title"]) in titles:
                continue
            ids.add(vid); titles.add(norm(r["title"]))
            song = {"t": r["title"], "a": r["artist"], "id": vid}
            if r.get("start") is not None: song["s"] = r["start"]  # per-song start time in seconds (default is the fixed 0:45)
            songs.append(song)
    if len(songs) < 30:
        print(f"SKIPPED {name}: only {len(songs)} songs (needs 30+)"); continue
    data[key] = {"name": name, "songs": songs}
    if key in RETIRED: data[key]["hide"] = 1
    print(f"{name}: {len(songs)} playable; missing: {missing}")
# ---- song-list versions: every category version is published under its hash, so a night locked
# to an older list (printed cards, phone players) still loads exactly the same songs later ----
import hashlib
LETTERS = {"halloween":"H","80s":"E","90s":"N","onehit":"O","hiphop":"P","movies":"M","yacht":"Y",
           "money":"D","places":"L","summer":"S","reggae":"R","quarantine":"Q",
           "funnymovies":"F","80smovies":"A","90smovies":"B","tv":"T","misheard":"W",
           "comedy":"C","internet":"I","wedding":"G","karaoke":"K","guilty":"U","sad":"Z","food":"J","stadium":"X","kids":"V","musicals":"1",
           "pop":"2","weather":"3","late":"4","everyday":"5","rock00":"6","grammar":"7","disco":"8","lucky":"9","sweets":"0"}
os.makedirs("songs", exist_ok=True)
idx_path = "songs/index.json"
index = json.load(open(idx_path)) if os.path.exists(idx_path) else {}
for key, cat in data.items():
    h = hashlib.sha1(json.dumps(cat["songs"], ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:8]
    cat["h"] = h
    cat["c"] = LETTERS[key]
    json.dump({"name": cat["name"], "songs": cat["songs"]}, open(f"songs/{key}-{h}.json", "w"), ensure_ascii=False)
    index.setdefault(key, [])
    if h not in index[key]: index[key].append(h)
json.dump(index, open(idx_path, "w"))
qr = open("vendor/qrcode.min.js").read()
import base64
anton = base64.b64encode(open("vendor/anton-latin-400.woff2","rb").read()).decode()
# Hyphenation points for long words in song titles (phone cards break "Ghost-busters" instead of shrinking it to nothing).
# Kept outside the song data so song-list hashes don't change.
hy = {}
try:
    import pyphen, glob as _glob
    _d = pyphen.Pyphen(lang="en_US")
    _titles = {x["t"] for c in data.values() for x in c["songs"]}
    for f in _glob.glob("songs/*-*.json"):
        _titles |= {x["t"] for x in json.load(open(f))["songs"]}
    for t in _titles:
        for w in re.findall(r"[A-Za-z'\u2019]{8,}", t):
            pts = [p for p in _d.positions(w) if 3 <= p <= len(w) - 3]  # keep at least 3 letters on each side
            if pts:
                p = min(pts, key=lambda p: abs(p - len(w) / 2))  # one break, nearest the middle
                hy[w] = w[:p] + "\u00ad" + w[p:]
except ImportError:
    print("pyphen not installed (pip install pyphen): phone cards will shrink long words instead of hyphenating them")
movies = json.load(open("data/movies.json")) if os.path.exists("data/movies.json") else {}  # category -> title -> movie; kept out of song data so song-list hashes don't change
years = json.load(open("data/years.json")) if os.path.exists("data/years.json") else {}  # "title|artist" -> release year; kept out of song data so song-list hashes don't change
html = open("src/template.html").read().replace("/*DATA*/{}", json.dumps(data, ensure_ascii=False)).replace("/*MOVIES*/{}", json.dumps(movies, ensure_ascii=False)).replace("/*YEARS*/{}", json.dumps(years, ensure_ascii=False)).replace("/*QRLIB*/", qr).replace("/*HYPH*/{}", json.dumps(hy, ensure_ascii=False)).replace("/*ANTON*/", anton)
os.makedirs("dist", exist_ok=True)
open("dist/index.html", "w").write(html)
print("built dist/index.html")
