#!/usr/bin/env python3
"""Builds the game and gathers everything a web host needs into ./site/:
index.html, songs/ and jsqr.min.js. Upload the contents of site/ to any static host.
Usage: python3 scripts/make_site.py"""
import os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
subprocess.run([sys.executable, "scripts/build.py"], check=True)
shutil.rmtree("site", ignore_errors=True)
os.makedirs("site")
shutil.copy("dist/index.html", "site/index.html")
shutil.copytree("songs", "site/songs")
shutil.copy("vendor/jsqr.min.js", "site/jsqr.min.js")  # QR reader, loaded only when a phone has no built-in one
print("\nReady: upload everything inside ./site/ to a static host (GitHub Pages, Netlify, any web server).")
