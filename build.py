# Génère le site officiel d'ABYSSAL (abyssal-game.fr) dans le dossier donné.
import os, re, shutil, sys
from PIL import Image
G = '/home/user/Abyssal'
OUT = sys.argv[1]
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(f'{OUT}/img/shots'); os.makedirs(f'{OUT}/fonts')
# polices (licences OFL jointes)
for f in os.listdir(f'{G}/assets/fonts'):
    if f.startswith(('Cinzel', 'AlegreyaSans', 'OFL-cinzel', 'OFL-alegreyasans')): shutil.copy(f'{G}/assets/fonts/{f}', f'{OUT}/fonts/{f}')
css = open(f'{G}/css/fonts.css').read().replace('../assets/fonts/', 'fonts/')
blocks = re.findall(r'(/\*[^*]*\*/\s*@font-face \{.*?\})', css, re.S)
keep = [b for b in blocks if "'Cinzel'" in b or "'Alegreya Sans'" in b]
open(f'{OUT}/fonts.css', 'w').write('/* Polices : Cinzel et Alegreya Sans (SIL Open Font License 1.1, fichiers OFL-*.txt dans fonts/) */\n' + '\n'.join(keep) + '\n')
# images
shutil.copy(f'{G}/assets/brand/title.webp', f'{OUT}/img/titre.webp')
shutil.copy(f'{G}/assets/brand/emblem.webp', f'{OUT}/img/embleme.webp')
shutil.copy(f'{G}/icons/favicon.png', f'{OUT}/favicon.png')
shutil.copy(f'{G}/icons/apple-touch-icon.png', f'{OUT}/apple-touch-icon.png')
_p = Image.open(f'{G}/store/ui/partage-source.jpg').convert('RGB'); _h = round(_p.width * 630 / 1200); _y = (_p.height - _h) // 2
_p.crop((0, _y, _p.width, _y + _h)).resize((1200, 630), Image.LANCZOS).save(f'{OUT}/img/partage.jpg', quality=84)  # image de partage (Gemini)
Image.open(f'{G}/store/apple/icone-1024.png').convert('RGB').resize((512, 512), Image.LANCZOS).save(f'{OUT}/img/icone.webp', quality=86)
SHOTS = [('accueil', 'L’Accueil et tes objectifs du jour'), ('ouverture', 'L’ouverture d’un booster'), ('combat', 'Un combat contre un gardien'), ('collection', 'Ta collection de plus de 500 créatures'), ('equipe', 'Ton équipe'), ('sceaux', 'Les Duels des Sceaux'), ('bestiaire', 'Le Bestiaire'), ('carte', 'Une carte en détail')]
for k, _ in SHOTS:
    im = Image.open(f'{G}/store/raw/{k}.png').convert('RGB'); w = 540
    im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(f'{OUT}/img/shots/{k}.webp', quality=78)
shot_w, shot_h = Image.open(f'{OUT}/img/shots/accueil.webp').size
# grande image d'ouverture (Gemini : cartes en éventail devant l'œil de l'Abysse)
Image.open(f'{G}/store/ui/partage-source.jpg').convert('RGB').save(f'{OUT}/img/hero.webp', quality=80)
# une créature par royaume, gardiens, jeux
CREA = [('infernal', 'Infernal', 'INF-051', 'Lilith'), ('abyssal', 'Abyssal', 'ABY-045', 'Léviathan'), ('celeste', 'Céleste', 'CEL-044', 'L’Ange aux Mille Yeux'),
        ('sauvage', 'Sauvage', 'SAU-049', 'Fenrir'), ('necrotique', 'Nécrotique', 'NEC-042', 'Le Roi Sans Tombe'), ('primordial', 'Primordial', 'PRI-048', 'Tiamat'),
        ('artificiel', 'Artificiel', 'ART-041', 'Le Dragon d’Horlogerie')]
os.makedirs(f'{OUT}/img/cartes'); os.makedirs(f'{OUT}/img/royaumes'); os.makedirs(f'{OUT}/img/gardiens'); os.makedirs(f'{OUT}/img/jeux')
for f, _, cid, _ in CREA:
    Image.open(f'{G}/assets/art/{cid}.webp').convert('RGB').resize((360, 504), Image.LANCZOS).save(f'{OUT}/img/cartes/{cid}.webp', quality=80)
    Image.open(f'{G}/assets/factions/{f}.webp').convert('RGBA').resize((96, 96), Image.LANCZOS).save(f'{OUT}/img/royaumes/{f}.webp', quality=86)
BOSSES = [('roi', 'Le Roi sans Visage', 'étage 5'), ('matriarche', 'La Matriarche du Givre', 'étage 10'), ('abysse', 'L’Abysse', 'étage 100'), ('titan', 'Le Titan Endormi', 'étage 80'), ('chasseur', 'Le Chasseur sans Ombre', 'étage 70')]
for k, _, _ in BOSSES:
    Image.open(f'{G}/assets/bosses/combat-{k}.webp').convert('RGB').resize((360, 504), Image.LANCZOS).save(f'{OUT}/img/gardiens/{k}.webp', quality=82)
GAMES = [('sceaux', 'Les Duels des Sceaux', 'Pose tes cartes sur le plateau et retourne celles de l’adversaire.'),
         ('pacte', 'Le Pacte', 'Tire des cartes et additionne… sans jamais tirer deux fois le même royaume.'),
         ('cryptes', 'Les Cryptes', 'Un duel de mémoire : chaque paire trouvée réveille le pouvoir de son royaume.'),
         ('encheres', 'Les Enchères de Mammon', 'Des offrandes secrètes, des créatures à gagner, des malédictions à éviter.')]
for k, _, _ in GAMES + [('enligne', '', ''), ('amis', '', ''), ('descente', '', ''), ('trial', '', ''), ('echoppe', '', ''), ('codex', '', '')]:
    shutil.copy(f'{G}/assets/ui/bn-{k}.webp', f'{OUT}/img/jeux/{k}.webp')
for k in ('standard3', 'abysse2'):
    im = Image.open(f'{G}/assets/packs/{k}.webp').convert('RGBA'); h = 420
    im.resize((round(im.width * h / im.height), h), Image.LANCZOS).save(f'{OUT}/img/{k}.webp', quality=84)

STYLE = """
:root { --bg: #08070C; --panel: #13111A; --panel2: #1B1724; --ink: #EEE6D3; --muted: #B5AA92; --gold: #E5BC62; --gold2: #F6DA98; --line: rgba(229, 188, 98, .26); --violet: #9B6BFF; color-scheme: dark; }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 400 1.05rem/1.62 'Alegreya Sans', system-ui, sans-serif; }
html, body, main, .sec, .hero { overflow-x: clip; }
a { color: var(--gold); }
img { max-width: 100%; height: auto; display: block; }
.wrap { max-width: 68rem; margin: 0 auto; padding: 0 max(18px, env(safe-area-inset-left)); }
.top { position: sticky; top: 0; z-index: 20; background: rgba(8, 7, 12, .82); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 1px solid var(--line); padding-top: env(safe-area-inset-top); }
.top .wrap { display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 58px; }
.brand { display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--gold); font: 700 1.08rem/1 'Cinzel', Georgia, serif; letter-spacing: .1em; }
.brand img { width: 36px; height: 36px; border-radius: 50%; box-shadow: 0 0 18px rgba(155, 107, 255, .35); }
nav { display: flex; gap: 2px; }
nav a { text-decoration: none; color: var(--ink); padding: 10px 11px; border-radius: 10px; font-size: .96rem; min-height: 44px; display: inline-flex; align-items: center; }
nav a[aria-current="page"] { color: var(--gold); background: rgba(229, 188, 98, .09); }
@media (max-width: 460px) { .brand span { display: none; } nav a { padding: 10px 8px; font-size: .92rem; } }
h1, h2, h3 { font-family: 'Cinzel', Georgia, serif; color: var(--gold); letter-spacing: .03em; text-wrap: balance; }
h1 { font-size: clamp(1.7rem, 6vw, 2.5rem); line-height: 1.15; margin: 32px 0 10px; }
h2 { font-size: clamp(1.35rem, 5vw, 2rem); line-height: 1.18; margin: 0 0 12px; }
h3 { font-size: 1.08rem; margin: 0 0 6px; }
.muted { color: var(--muted); }
.kick { font: 700 .78rem/1 'Cinzel', Georgia, serif; letter-spacing: .22em; text-transform: uppercase; color: var(--violet); margin: 0 0 10px; }
.card { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; padding: 16px 18px; }
/* ouverture */
.hero { position: relative; min-height: min(92vh, 760px); display: grid; align-items: end; overflow: hidden; isolation: isolate; }
.hero-bg { position: absolute; inset: 0; z-index: -2; width: 100%; height: 100%; object-fit: cover; object-position: 50% 40%; transform: scale(1.04); }
.hero::after { content: ''; position: absolute; inset: 0; z-index: -1; background: radial-gradient(70% 55% at 50% 38%, transparent 0%, rgba(8, 7, 12, .35) 60%, rgba(8, 7, 12, .92) 100%), linear-gradient(180deg, rgba(8, 7, 12, .25) 0%, transparent 30%, rgba(8, 7, 12, .7) 66%, var(--bg) 100%); }
.hero-in { text-align: center; padding: 0 0 48px; }
.hero .logo { width: min(560px, 88%); margin: 0 auto; filter: drop-shadow(0 10px 40px rgba(0, 0, 0, .9)) drop-shadow(0 0 30px rgba(155, 107, 255, .25)); }
.hero .lead { font-size: clamp(1.1rem, 3.9vw, 1.35rem); max-width: 36rem; margin: 14px auto 0; text-shadow: 0 2px 10px #000; }
.cta { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin: 24px 0 14px; }
.store { display: inline-flex; flex-direction: column; align-items: flex-start; gap: 2px; min-width: 180px; padding: 11px 20px; border-radius: 14px; border: 1px solid rgba(229, 188, 98, .55); background: linear-gradient(180deg, rgba(58, 42, 18, .92), rgba(28, 20, 9, .92)); color: var(--ink); text-decoration: none; box-shadow: 0 8px 24px rgba(0, 0, 0, .5); }
.store small { font-size: .74rem; color: var(--muted); letter-spacing: .06em; text-transform: uppercase; }
.store b { font: 700 1.08rem/1.1 'Cinzel', Georgia, serif; color: var(--gold2); letter-spacing: .04em; }
.promise { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin: 0; padding: 0; list-style: none; }
.promise li { border: 1px solid var(--line); background: rgba(19, 17, 26, .7); border-radius: 999px; padding: 6px 14px; font-size: .95rem; }
/* sections */
.sec { padding: 64px 0; }
.sec + .sec { border-top: 1px solid rgba(229, 188, 98, .1); }
.split { display: grid; gap: 28px; align-items: center; }
.split > * { min-width: 0; }
@media (min-width: 820px) { .split { grid-template-columns: 1fr 1fr; gap: 48px; } .split.rev > :first-child { order: 2; } }
.split p { margin: 0 0 12px; }
.ticks { list-style: none; padding: 0; margin: 14px 0 0; display: grid; gap: 8px; }
.ticks li { padding-left: 28px; position: relative; }
.ticks li::before { content: ''; position: absolute; left: 4px; top: .55em; width: 10px; height: 10px; transform: rotate(45deg); background: var(--gold); box-shadow: 0 0 10px rgba(229, 188, 98, .6); }
/* cartes en éventail */
.fan { position: relative; height: clamp(260px, 62vw, 400px); }
.fan { --sp: 34%; }
@media (max-width: 600px) { .fan { --sp: 19%; } }
.fan img { transform: translateX(calc(-50% + var(--i) * var(--sp))) rotate(calc(var(--i) * 7deg)); }
.fan img { position: absolute; left: 50%; bottom: 0; width: clamp(110px, 25vw, 170px); aspect-ratio: 5 / 7; object-fit: cover; border-radius: 12px; border: 2px solid rgba(229, 188, 98, .7); box-shadow: 0 14px 30px rgba(0, 0, 0, .7); transform-origin: 50% 120%; }
.realms { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 6px; margin-top: 22px; }
.realms figure { margin: 0; text-align: center; }
.realms img { width: 100%; max-width: 54px; margin: 0 auto; }
.realms figcaption { font-size: .72rem; color: var(--muted); margin-top: 4px; }
/* gardiens */
.bosses { display: flex; justify-content: center; align-items: center; container-type: inline-size; position: relative; padding: 18px 0 34px; }
.bosses::before { content: ''; position: absolute; left: 6%; right: 6%; bottom: 0; height: 50%; background: radial-gradient(60% 100% at 50% 100%, rgba(200, 40, 40, .28), transparent 70%); }
.bosses img { position: relative; width: min(26cqi, 190px); height: auto; aspect-ratio: 5 / 7; margin: 0 -4cqi; border-radius: 10px; border: 2px solid #c9a24d; box-shadow: 0 12px 28px rgba(0, 0, 0, .75), 0 0 0 1px rgba(0, 0, 0, .6); transform: rotate(calc(var(--i) * 6deg)) translateY(calc(var(--a) * 14px)); }
.bosses img[style*="--i: 0;"] { transform: scale(1.12); border-color: #e0bd63; box-shadow: 0 14px 34px rgba(0, 0, 0, .8), 0 0 26px rgba(200, 40, 40, .45); }
/* jeux */
.games { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 15.5rem), 1fr)); gap: 14px; margin-top: 22px; }
.game { overflow: hidden; padding: 0; }
.game img { width: 100%; aspect-ratio: 900 / 297; object-fit: cover; }
.game div { padding: 12px 16px 16px; }
.game p { margin: 0; color: var(--muted); font-size: .97rem; }
.banner { border-radius: 16px; border: 1px solid var(--line); box-shadow: 0 14px 34px rgba(0, 0, 0, .55); }
.packs { display: flex; justify-content: center; align-items: flex-end; gap: 4%; }
.packs img { width: 40%; max-width: 210px; filter: drop-shadow(0 16px 26px rgba(0, 0, 0, .8)); }
.packs img:first-child { transform: rotate(-6deg); }
.packs img:last-child { transform: rotate(6deg) translateY(-8px); }
/* captures */
.shots { display: flex; gap: 14px; overflow-x: auto; scroll-snap-type: x mandatory; padding: 6px 2px 16px; -webkit-overflow-scrolling: touch; scrollbar-width: thin; }
.shots figure { flex: 0 0 min(60vw, 250px); margin: 0; scroll-snap-align: center; }
.shots img { border-radius: 22px; border: 1px solid var(--line); box-shadow: 0 10px 26px rgba(0, 0, 0, .6); }
.shots figcaption { color: var(--muted); font-size: .9rem; text-align: center; margin-top: 8px; }
.center { text-align: center; }
.pledge { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 13rem), 1fr)); gap: 12px; margin-top: 20px; }
.pledge .card b { display: block; color: var(--gold2); font-family: 'Cinzel', Georgia, serif; margin-bottom: 4px; }
.pledge .card { font-size: .96rem; color: var(--muted); }
/* pages de texte */
details { background: var(--panel); border: 1px solid var(--line); border-radius: 14px; padding: 4px 16px; margin: 0 0 10px; }
summary { cursor: pointer; padding: 12px 0; font-weight: 700; color: var(--ink); min-height: 44px; }
details[open] summary { color: var(--gold); }
table { width: 100%; border-collapse: collapse; font-size: .95rem; }
th, td { text-align: left; vertical-align: top; padding: 8px 6px; border-bottom: 1px solid rgba(255, 255, 255, .08); }
th { color: var(--gold); }
.tw { overflow-x: auto; }
main { padding-bottom: 20px; }
main.text { max-width: 46rem; }
main.text h2 { font-size: 1.2rem; margin: 30px 0 8px; }
footer { margin-top: 40px; border-top: 1px solid var(--line); padding: 24px 0 max(30px, env(safe-area-inset-bottom)); color: var(--muted); font-size: .92rem; text-align: center; }
footer a { color: var(--muted); margin: 0 6px; }
@media (max-width: 700px) { .hero { min-height: 0; display: block; padding-top: 0; } .hero-bg { position: relative; inset: auto; height: auto; aspect-ratio: 1024 / 572; transform: none; z-index: -2; -webkit-mask-image: linear-gradient(180deg, #000 70%, transparent); mask-image: linear-gradient(180deg, #000 70%, transparent); } .hero::after { display: none; } .hero-in { margin-top: -18vw; padding-bottom: 36px; } .hero .logo { width: min(420px, 82%); } }
@media (prefers-reduced-motion: no-preference) { .hero-bg { animation: heroIn 2.4s ease-out both; } @keyframes heroIn { from { transform: scale(1.12); opacity: 0; } to { transform: scale(1.04); opacity: 1; } } }
"""
NAV = [('index.html', 'Accueil'), ('aide.html', 'Aide'), ('confidentialite.html', 'Confidentialité')]
def page(fname, title, desc, body, text=True):
    nav = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{n}</a>' for h, n in NAV)
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#08070C">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://abyssal-game.fr/img/partage.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="stylesheet" href="fonts.css">
<link rel="stylesheet" href="site.css">
</head>
<body>
<header class="top"><div class="wrap"><a class="brand" href="index.html"><img src="img/embleme.webp" alt="" width="36" height="36"><span>ABYSSAL</span></a><nav aria-label="Pages du site">{nav}</nav></div></header>
{body if not text else f'<main class="wrap text">{body}</main>'}
<footer><div class="wrap">ABYSSAL — Le Bestiaire interdit · © 2026<br><a href="aide.html">Aide</a>·<a href="confidentialite.html">Confidentialité</a>·<a href="mentions-legales.html">Mentions légales</a>·<a href="mailto:contact@abyssal-game.fr">contact@abyssal-game.fr</a></div></footer>
</body>
</html>
"""
open(f'{OUT}/site.css', 'w').write(STYLE.strip() + '\n')

# ——— Accueil ———
n = len(CREA)
fan = ''.join(f'<img src="img/cartes/{cid}.webp" alt="{nm} ({fl})" width="360" height="504" loading="lazy" style="--i: {i - (n - 1) // 2}; z-index: {10 - abs(i - 3)}">' for i, (f, fl, cid, nm) in enumerate(CREA))
realms = ''.join(f'<figure><img src="img/royaumes/{f}.webp" alt="" width="96" height="96" loading="lazy"><figcaption>{fl}</figcaption></figure>' for f, fl, _, _ in CREA)
bosses = ''.join(f'<img src="img/gardiens/{k}.webp" alt="{nm}, {fl}" width="360" height="504" loading="lazy" style="--i: {i - 2}; --a: {abs(i - 2)}; z-index: {10 - abs(i - 2)}">' for i, (k, nm, fl) in enumerate(BOSSES))
games = ''.join(f'<article class="card game"><img src="img/jeux/{k}.webp" alt="" width="900" height="297" loading="lazy"><div><h3>{t}</h3><p>{d}</p></div></article>' for k, t, d in GAMES)
shots = ''.join(f'<figure><img src="img/shots/{k}.webp" alt="{c}" width="{shot_w}" height="{shot_h}" ><figcaption>{c}</figcaption></figure>' for k, c in SHOTS)
home = f"""<section class="hero"><img class="hero-bg" src="img/hero.webp" alt="" width="1024" height="572">
<div class="wrap hero-in">
  <h1 style="position:absolute;left:-9999px">ABYSSAL — Le Bestiaire interdit</h1>
  <img class="logo" src="img/titre.webp" alt="ABYSSAL — Le Bestiaire interdit">
  <p class="lead">Un jeu de cartes à collectionner dark fantasy. Ouvre des boosters, rassemble plus de 500 créatures tirées des mythes et descends dans l’Abysse, étage après étage.</p>
  <div class="cta"><span class="store"><small>Bientôt sur</small><b>iPhone</b></span><span class="store"><small>Bientôt sur</small><b>Android</b></span></div>
  <ul class="promise"><li>Gratuit</li><li>Sans publicité</li><li>Toutes les cartes se gagnent en jouant</li></ul>
</div></section>
<main>
<section class="sec"><div class="wrap split">
  <div><p class="kick">La collection</p><h2>Plus de 500 créatures, sept royaumes</h2>
  <p>Démons, anges déchus, dieux oubliés, dragons primordiaux, automates et spectres : chaque créature a son illustration, son histoire et son rôle au combat.</p>
  <ul class="ticks"><li>6 raretés, de la Commune à la Secrète</li><li>Cinq finitions à collectionner, de l’Argentée à la Prismatique</li><li>Un booster gratuit chaque jour</li></ul>
  <div class="realms">{realms}</div></div>
  <div class="fan" aria-label="Sept créatures, une par royaume">{fan}</div>
</div></section>
<section class="sec"><div class="wrap split rev">
  <div><p class="kick">La Descente</p><h2>100 étages, 20 gardiens</h2>
  <p>Le Bestiaire interdit a été déchiré, et ses pages sont tombées dans l’Abysse. Toi seul sais encore lire les sceaux : descends chapitre après chapitre pour les refermer. Chaque chapitre est gardé par un rêve de l’Abysse, un gardien unique avec ses règles et sa Furie.</p>
  <ul class="ticks"><li>Une équipe de 5 créatures, chacune avec son rôle</li><li>Pare au bon moment, brise les défenses, enchaîne les coups : le talent compte autant que tes cartes</li><li>Une créature tombée reste à terre : rallume-la avec une Braise de vie</li><li>Au fond, l’Abysse t’attend… et ce qui rêve derrière elle</li></ul></div>
  <div class="bosses">{bosses}</div>
</div></section>
<section class="sec"><div class="wrap">
  <p class="kick center">Le Cercle de l’Abysse</p><h2 class="center">Quatre jeux de cartes dans le jeu</h2>
  <p class="center muted" style="max-width:38rem;margin:0 auto">Huit adversaires par jeu, un défi chaque jour, des salles aux règles différentes.</p>
  <div class="games">{games}</div>
</div></section>
<section class="sec"><div class="wrap split">
  <div><p class="kick">En ligne</p><h2>Joue contre d’autres joueurs</h2>
  <p>Les Duels des Sceaux, le Pacte et les Enchères se jouent aussi contre de vrais joueurs ; les Cryptes, entre amis.</p>
  <ul class="ticks"><li>Partie rapide (30 secondes par coup) ou partie lente (12 heures par coup)</li><li>Le Choc des Boosters : chacun ouvre ses boosters face à l’autre et garde ses cartes, le meilleur tirage gagne un butin offert par le jeu</li><li>Des amis, leurs collections, leurs exploits et des classements</li></ul></div>
  <img class="banner" src="img/jeux/enligne.webp" alt="" width="900" height="297" loading="lazy">
</div></section>
<section class="sec"><div class="wrap split rev">
  <div><p class="kick">Chaque jour</p><h2>Boosters, Épreuves et coffres</h2>
  <p>Un booster gratuit, trois Épreuves du jour (les mêmes pour tous), des missions, une offrande et des coffres à ouvrir.</p></div>
  <div class="packs"><img src="img/standard3.webp" alt="Booster standard" loading="lazy"><img src="img/abysse2.webp" alt="Booster de l’Abysse" loading="lazy"></div>
</div></section>
<section class="sec"><div class="wrap split">
  <div><p class="kick">Bientôt</p><h2>L’Échoppe et le Codex de l’Abîme</h2>
  <p>Pour soutenir le jeu, une boutique uniquement d’apparence : cadres de profil vivants, dos de cartes animés, sachets de booster, plaques de pseudo, tapis de jeu, fonds de profil et réactions pour tes parties en ligne.</p>
  <ul class="ticks"><li>Le Codex de l’Abîme : une saison par mois, 30 paliers, une voie gratuite et une voie enluminée aux cosmétiques exclusifs</li><li>Saison I, La Nuit des Âmes, à partir du 1er décembre 2026</li><li>Jamais de cartes, de monnaie de jeu ni de puissance à acheter</li></ul></div>
  <img class="banner" src="img/jeux/echoppe.webp" alt="" width="900" height="297" loading="lazy">
</div></section>
<section class="sec"><div class="wrap">
  <p class="kick center">Le jeu en images</p><h2 class="center">Aperçu</h2>
  <div class="shots" aria-label="Captures d’écran du jeu">{shots}</div>
</div></section>
<section class="sec"><div class="wrap">
  <h2 class="center">Notre promesse</h2>
  <div class="pledge"><div class="card"><b>Gratuit</b>Le jeu entier se joue sans payer.</div><div class="card"><b>Sans publicité</b>Aucune publicité, aucun pistage.</div><div class="card"><b>Jamais plus fort en payant</b>Toutes les cartes se gagnent en jouant. L’Échoppe et le Codex ne vendent que des objets d’apparence.</div></div>
  <p class="center" style="margin-top:28px">Une question ? Consulte l’<a href="aide.html">Aide</a> ou écris-nous à <a href="mailto:contact@abyssal-game.fr">contact@abyssal-game.fr</a>.</p>
</div></section>
</main>"""
open(f'{OUT}/index.html', 'w').write(page('index.html', 'ABYSSAL — Le Bestiaire interdit', 'ABYSSAL, jeu de cartes à collectionner dark fantasy : plus de 500 créatures, 100 étages, 20 gardiens, quatre jeux de cartes et des parties en ligne. Gratuit, sans publicité.', home, text=False))

# ——— Aide ———
FAQ = [
  ('Faut-il un compte pour jouer ?', 'Oui. Au premier lancement, crée ton compte (adresse e-mail, mot de passe, puis pseudo). Ta partie y est liée et sauvegardée en ligne : tu la retrouves sur n’importe quel téléphone en te connectant.'),
  ('J’ai oublié mon mot de passe', 'Sur l’écran Compte, touche « Mot de passe oublié ? » et entre ton adresse e-mail. Tu reçois un lien pour choisir un nouveau mot de passe. Pense à regarder dans tes courriers indésirables.'),
  ('Changer mon mot de passe', '<b>Sanctuaire → Compte → Changer mon mot de passe</b>. Il doit compter 8 caractères au moins, avec une majuscule, une minuscule, un chiffre et un symbole.'),
  ('Puis-je changer mon pseudo ?', 'Non : le pseudo est définitif une fois choisi, c’est grâce à lui que tes amis te trouvent. Seule exception : un pseudo masqué après des signalements peut être remplacé une fois.'),
  ('J’ai changé de téléphone', 'Installe le jeu et connecte-toi avec ton compte : ta partie revient telle que tu l’as laissée.'),
  ('Ajouter un ami', '<b>Sanctuaire → Amis</b>, puis tape son pseudo. Tu peux aussi toucher le pseudo d’un joueur (classement, partie en ligne) pour ouvrir son profil et l’ajouter. Une fois la demande acceptée, vous voyez mutuellement vos collections complètes.'),
  ('Comment jouer contre d’autres joueurs ?', '<b>Aventure → Jeux</b>, choisis un jeu puis « Contre un joueur ». Partie rapide : 30 secondes par coup. Partie lente : 12 heures par coup. Si le temps est dépassé, la partie est perdue. Les Cryptes se jouent seulement entre amis.'),
  ('Le Choc des Boosters, c’est quoi ?', 'Un défi entre deux joueurs : chacun achète les mêmes boosters au prix de la boutique, ils s’ouvrent face à face, et <b>chacun garde toujours ses cartes</b>. Le meilleur tirage reçoit un butin offert par le jeu : la copie d’une carte de son choix parmi celles de l’adversaire, et des éclats. Le perdant ne perd rien.'),
  ('Les Torches, c’est quoi ?', 'Chaque combat de la Descente brûle une Torche, qu’il soit gagné ou perdu. Tu en as <b>5 par jour</b> : elles se rallument à minuit. Sans Torche, ton équipe se repose et ton chapitre t’attend jusqu’au lendemain. Les Épreuves du jour, le Cercle de l’Abysse, les boosters et la Fournaise ne demandent pas de Torche.'),
  ('Signaler ou masquer un joueur', 'Touche son pseudo pour ouvrir son profil, puis « Signaler ou masquer ce joueur ». Un pseudo signalé par plusieurs joueurs est masqué pour tout le monde.'),
  ('Recevoir les rappels sur mon téléphone', 'Dans l’application, <b>Réglages → Jeu → Notifications</b> : booster gratuit du jour, offrande du soir, Tirage des Ombres, « à toi de jouer » dans une partie lente, défis et demandes d’ami.'),
  ('Dans quelles langues peut-on jouer ?', 'En six langues : français, English, español, Deutsch, italiano et português. <b>Réglages → Jeu → Langue</b>.'),
  ('Supprimer mon compte', '<b>Sanctuaire → Compte → Supprimer mon compte</b> : ton profil, ta sauvegarde en ligne et tes scores sont effacés. Tu n’as plus l’application ? Écris-nous depuis l’adresse e-mail de ton compte, objet « Suppression de compte ».'),
  ('Y a-t-il des achats dans le jeu ?', 'Le jeu est gratuit et sans publicité, et toutes les cartes se gagnent en jouant. Bientôt, l’Échoppe proposera des objets <b>uniquement d’apparence</b> (cadres de profil, dos de cartes, sachets, plaques, tapis, fonds de profil, réactions), achetés avec des obsidiennes, ainsi que le Codex enluminé et le Pack du Fondateur : jamais rien qui rende plus fort. Les paiements passent par l’App Store ou Google Play.'),
  ('Qu’est-ce que le Codex de l’Abîme ?', 'Le pass de saison du jeu : une saison par mois, 30 paliers à franchir en jouant. La voie gratuite donne des éclats, des cendres, des coffres et des boosters ; la voie enluminée, achetée une fois par saison, donne à chaque palier un objet d’apparence exclusif. Première saison : La Nuit des Âmes, à partir du 1er décembre 2026.'),
  ('J’ai changé de téléphone : retrouver mes achats', 'Tes achats sont liés à ton compte ABYSSAL : connecte-toi et ils reviennent. Dans l’Échoppe, « Restaurer mes achats » vérifie à nouveau tes paiements auprès de l’App Store ou de Google Play.'),
  ('Le jeu n’a pas de son', 'Vérifie le volume dans <b>Réglages → Jeu</b>. Dans l’application, le son fonctionne même quand le téléphone est en mode silencieux.'),
]
aide = '<h1>Aide</h1><p class="muted">Les réponses aux questions les plus fréquentes. Tu ne trouves pas ? Écris-nous.</p>' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + '''
<h2 id="contact">Nous contacter</h2>
<div class="card"><p style="margin-top:0">Une question, un bug, une idée ? Écris-nous à <a href="mailto:contact@abyssal-game.fr?subject=ABYSSAL%20%E2%80%94%20aide">contact@abyssal-game.fr</a>.</p>
<p class="muted" style="margin-bottom:0">Pour un bug, indique ton modèle de téléphone, la version du jeu (<b>Réglages → À propos</b>) et, si possible, une capture d’écran. Nous répondons en général sous quelques jours.</p></div>'''
open(f'{OUT}/aide.html', 'w').write(page('aide.html', 'Aide — ABYSSAL', 'Aide et contact d’ABYSSAL — Le Bestiaire interdit : compte, mot de passe, amis, suppression du compte.', aide))

# ——— Confidentialité (reprise de la page du jeu) ———
src = open(f'{G}/confidentialite.html').read()
m = re.search(r'<main>(.*?)</main>', src, re.S)
body = m.group(1)
body = re.sub(r'<header>.*?</header>', '', body, flags=re.S)
body = re.sub(r'<footer>.*?</footer>', '', body, flags=re.S)
hd = re.search(r'<header>(.*?)</header>', m.group(1), re.S).group(1)
hd = re.sub(r'<img[^>]*>', '', hd)
body = hd.replace('<h1>', '<h1>', 1) + body
open(f'{OUT}/confidentialite.html', 'w').write(page('confidentialite.html', 'Confidentialité — ABYSSAL', 'Politique de confidentialité d’ABYSSAL — Le Bestiaire interdit : quelles données le jeu utilise, pourquoi, et comment les supprimer.', body))

# ——— Mentions légales ———
ml = '''<h1>Mentions légales</h1>
<h2>Éditeur</h2>
<p class="card">ABYSSAL — Le Bestiaire interdit, site et jeu édités par <b>Alexis Seguin</b>, entrepreneur individuel (micro-entreprise), nom commercial ABYSSAL.<br>Siège : Clermont-Ferrand (63), France.<br>Immatriculé au Registre national des entreprises (RNE) : SIREN 132 021 338 — SIRET 132 021 338 00018.<br>TVA non applicable, article 293 B du Code général des impôts.<br>Directeur de la publication : Alexis Seguin.<br>Contact : <a href="mailto:contact@abyssal-game.fr">contact@abyssal-game.fr</a></p>
<h2>Hébergement</h2>
<p class="card">Site : GitHub, Inc. (GitHub Pages), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis (+1 877 448 4820).<br>Comptes et sauvegardes du jeu : Supabase, Inc., hébergement en Union européenne.<br>Nom de domaine : OVH SAS, 2 rue Kellermann, 59100 Roubaix, France (+33 9 72 10 10 07).</p>
<h2>Propriété</h2>
<p>Les textes, illustrations, musiques et sons d’ABYSSAL sont la propriété de leur éditeur. Les polices Cinzel et Alegreya Sans sont distribuées sous licence SIL Open Font License 1.1.</p>
<h2>Données personnelles</h2>
<p>Voir la <a href="confidentialite.html">politique de confidentialité</a>.</p>'''
open(f'{OUT}/mentions-legales.html', 'w').write(page('mentions-legales.html', 'Mentions légales — ABYSSAL', 'Mentions légales du site abyssal-game.fr.', ml))
open(f'{OUT}/404.html', 'w').write(page('404.html', 'Page introuvable — ABYSSAL', 'Page introuvable.', '<h1>Page introuvable</h1><p>Cette page s’est perdue dans l’Abysse. <a href="index.html">Retour à l’accueil</a>.</p>'))
open(f'{OUT}/CNAME', 'w').write('abyssal-game.fr\n')
open(f'{OUT}/.nojekyll', 'w').write('')
open(f'{OUT}/README.md', 'w').write('# Site officiel d’ABYSSAL\n\nhttps://abyssal-game.fr — présentation, aide, politique de confidentialité, mentions légales.\nPages statiques servies par GitHub Pages (branche `main`, dossier racine). Généré depuis le dépôt du jeu.\n')
print('ok', sorted(os.listdir(OUT)))
