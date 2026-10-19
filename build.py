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
Image.open(f'{G}/store/apple/icone-1024.png').convert('RGB').resize((512, 512), Image.LANCZOS).save(f'{OUT}/img/icone.webp', quality=86)
SHOTS = [('08-accueil', 'L’Accueil et tes objectifs du jour'), ('02-ouverture', 'L’ouverture d’un booster'), ('03-combat', 'Un combat contre un gardien'), ('05-collection', 'Ta collection de 500 créatures'), ('04-equipe', 'Ton équipe'), ('06-sceaux', 'Les Duels des Sceaux'), ('07-bestiaire', 'Le Bestiaire'), ('01-carte', 'Une carte en détail')]
for k, _ in SHOTS:
    im = Image.open(f'{G}/store/apple/{k}.png').convert('RGB'); w = 540
    im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(f'{OUT}/img/shots/{k}.webp', quality=78)
shot_w, shot_h = Image.open(f'{OUT}/img/shots/08-accueil.webp').size

STYLE = '''
:root { --bg: #0B0A10; --panel: #15131C; --panel2: #1C1826; --ink: #ECE4D2; --muted: #B3A890; --gold: #E2B860; --line: rgba(226, 184, 96, .28); --violet: #9B6BFF; color-scheme: dark; }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
body { margin: 0; background: radial-gradient(ellipse at top, #1E1830 0%, var(--bg) 62%) fixed, var(--bg); color: var(--ink); font: 400 1.04rem/1.6 'Alegreya Sans', system-ui, sans-serif; }
a { color: var(--gold); }
img { max-width: 100%; height: auto; display: block; }
.wrap { max-width: 64rem; margin: 0 auto; padding: 0 max(16px, env(safe-area-inset-left)); }
.top { position: sticky; top: 0; z-index: 10; background: rgba(11, 10, 16, .88); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border-bottom: 1px solid var(--line); padding-top: env(safe-area-inset-top); }
.top .wrap { display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 56px; }
.brand { display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--gold); font: 700 1.05rem/1 'Cinzel', Georgia, serif; letter-spacing: .08em; }
.brand img { width: 34px; height: 34px; border-radius: 50%; }
nav { display: flex; gap: 4px; flex-wrap: wrap; justify-content: flex-end; }
nav a { text-decoration: none; color: var(--ink); padding: 10px 10px; border-radius: 10px; font-size: .95rem; min-height: 44px; display: inline-flex; align-items: center; }
nav a[aria-current="page"] { color: var(--gold); background: rgba(226, 184, 96, .08); }
@media (max-width: 440px) { .brand span { display: none; } nav { flex-wrap: nowrap; gap: 0; } nav a { padding: 10px 8px; font-size: .9rem; } }
h1, h2, h3 { font-family: 'Cinzel', Georgia, serif; color: var(--gold); letter-spacing: .03em; text-wrap: balance; }
h1 { font-size: clamp(1.6rem, 6vw, 2.4rem); line-height: 1.15; margin: 28px 0 8px; }
h2 { font-size: clamp(1.2rem, 4.5vw, 1.6rem); line-height: 1.2; margin: 44px 0 12px; }
h3 { font-size: 1.05rem; margin: 0 0 6px; }
.muted { color: var(--muted); }
.card { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; padding: 16px 18px; }
.hero { text-align: center; padding: 36px 0 12px; }
.hero .logo { width: min(520px, 92%); margin: 0 auto; filter: drop-shadow(0 10px 40px rgba(155, 107, 255, .25)); }
.hero p.lead { font-size: clamp(1.08rem, 3.8vw, 1.3rem); max-width: 36rem; margin: 14px auto 0; }
.badges { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin: 22px 0 6px; }
.badge { display: inline-flex; align-items: center; gap: 10px; padding: 12px 18px; border-radius: 14px; border: 1px solid var(--line); background: var(--panel2); color: var(--ink); text-decoration: none; min-height: 48px; }
.badge b { color: var(--gold); font-family: 'Cinzel', Georgia, serif; letter-spacing: .04em; }
.badge.main { background: linear-gradient(180deg, #3A2A12, #241A0C); border-color: rgba(226, 184, 96, .6); }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 1fr)); gap: 12px; }
.shots { display: flex; gap: 12px; overflow-x: auto; scroll-snap-type: x mandatory; padding: 4px 2px 14px; -webkit-overflow-scrolling: touch; }
.shots figure { flex: 0 0 min(62vw, 260px); margin: 0; scroll-snap-align: start; }
.shots img { border-radius: 18px; border: 1px solid var(--line); }
.shots figcaption { color: var(--muted); font-size: .9rem; text-align: center; margin-top: 6px; }
.promise { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin: 8px 0 0; padding: 0; list-style: none; }
.promise li { border: 1px solid var(--line); border-radius: 999px; padding: 6px 14px; font-size: .95rem; color: var(--ink); }
details { background: var(--panel); border: 1px solid var(--line); border-radius: 14px; padding: 4px 16px; margin: 0 0 10px; }
summary { cursor: pointer; padding: 12px 0; font-weight: 700; color: var(--ink); min-height: 44px; }
details[open] summary { color: var(--gold); }
table { width: 100%; border-collapse: collapse; font-size: .95rem; }
th, td { text-align: left; vertical-align: top; padding: 8px 6px; border-bottom: 1px solid rgba(255, 255, 255, .08); }
th { color: var(--gold); }
.tw { overflow-x: auto; }
main { padding-bottom: 20px; }
main.text { max-width: 44rem; }
footer { margin-top: 48px; border-top: 1px solid var(--line); padding: 20px 0 max(28px, env(safe-area-inset-bottom)); color: var(--muted); font-size: .92rem; text-align: center; }
footer a { color: var(--muted); margin: 0 6px; }
'''
NAV = [('index.html', 'Accueil'), ('aide.html', 'Aide'), ('confidentialite.html', 'Confidentialité')]
def page(fname, title, desc, body, text=True):
    nav = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{n}</a>' for h, n in NAV)
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0B0A10">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://abyssal-game.fr/img/icone.webp">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="stylesheet" href="fonts.css">
<link rel="stylesheet" href="site.css">
</head>
<body>
<header class="top"><div class="wrap"><a class="brand" href="index.html"><img src="img/embleme.webp" alt="" width="34" height="34"><span>ABYSSAL</span></a><nav aria-label="Pages du site">{nav}</nav></div></header>
<main class="wrap{" text" if text else ""}">
{body}
</main>
<footer><div class="wrap">ABYSSAL — Le Bestiaire interdit · © 2026<br><a href="aide.html">Aide</a>·<a href="confidentialite.html">Confidentialité</a>·<a href="mentions-legales.html">Mentions légales</a>·<a href="mailto:contact@abyssal-game.fr">contact@abyssal-game.fr</a></div></footer>
</body>
</html>
'''
open(f'{OUT}/site.css', 'w').write(STYLE.strip() + '\n')

# ——— Accueil ———
FEAT = [
  ('500 créatures à collectionner', 'Démons, anges déchus, dieux oubliés, dragons primordiaux, golems, spectres… 7 royaumes, 6 raretés, et des finitions Argentée, Enluminée et Abyssale.'),
  ('La Descente', '100 étages et 20 gardiens jusqu’au fond de l’Abysse. Chaque chapitre raconte une page du Bestiaire interdit.'),
  ('Des combats tactiques', 'Une équipe de 5 créatures, chacune avec son rôle. Pare au bon moment, brise les défenses, enchaîne les coups : le talent compte autant que tes cartes.'),
  ('La Salle des jeux', 'Les Duels des Sceaux, le Pacte, les Cryptes et les Enchères de Mammon : quatre jeux de cartes, huit adversaires, un défi par jour.'),
  ('Tes amis', 'Ajoute tes amis grâce à leur pseudo et découvre leur collection, leurs succès et leurs exploits.'),
  ('Épreuves du jour', 'Trois combats chaque jour, les mêmes pour tous, et un classement.'),
]
shots = ''.join(f'<figure><img src="img/shots/{k}.webp" alt="{c}" width="{shot_w}" height="{shot_h}" loading="lazy"><figcaption>{c}</figcaption></figure>' for k, c in SHOTS)
home = f'''<section class="hero">
  <h1 style="position:absolute;left:-9999px">ABYSSAL — Le Bestiaire interdit</h1>
  <img class="logo" src="img/titre.webp" alt="ABYSSAL — Le Bestiaire interdit">
  <p class="lead">Un jeu de cartes à collectionner dark fantasy. Ouvre des boosters, rassemble 500 créatures tirées des mythes et descends dans l’Abysse, étage après étage.</p>
  <div class="badges"><span class="badge main"><b>Bientôt sur iPhone</b></span></div>
  <ul class="promise"><li>Gratuit</li><li>Sans publicité</li><li>Toutes les cartes se gagnent en jouant</li><li>Aucun achat qui rend plus fort</li></ul>
</section>
<h2>Le jeu en images</h2>
<div class="shots" aria-label="Captures d’écran du jeu">{shots}</div>
<h2>Ce qui t’attend</h2>
<div class="grid">{''.join(f'<div class="card"><h3>{t}</h3><p class="muted" style="margin:0">{d}</p></div>' for t, d in FEAT)}</div>
<h2>Une question ?</h2>
<p>Consulte la page <a href="aide.html">Aide</a>, ou écris-nous à <a href="mailto:contact@abyssal-game.fr">contact@abyssal-game.fr</a>.</p>'''
open(f'{OUT}/index.html', 'w').write(page('index.html', 'ABYSSAL — Le Bestiaire interdit', 'ABYSSAL, jeu de cartes à collectionner dark fantasy : 500 créatures, 100 étages, 20 gardiens. Gratuit, sans publicité.', home, text=False))

# ——— Aide ———
FAQ = [
  ('Comment créer un compte ?', 'Au lancement du jeu, touche « Créer un compte », ou plus tard : <b>Sanctuaire → Compte</b>. Le compte est facultatif : il sauvegarde ta partie en ligne pour la retrouver sur un autre téléphone, et te permet d’apparaître dans les classements et d’ajouter des amis.'),
  ('J’ai oublié mon mot de passe', 'Sur l’écran Compte, touche « Mot de passe oublié ? » et entre ton adresse e-mail. Tu reçois un lien pour choisir un nouveau mot de passe. Pense à regarder dans tes courriers indésirables.'),
  ('Changer mon mot de passe', '<b>Sanctuaire → Compte → Changer mon mot de passe</b>. Il doit compter 8 caractères au moins, avec une majuscule, une minuscule, un chiffre et un symbole.'),
  ('Puis-je changer mon pseudo ?', 'Non : le pseudo est définitif une fois choisi, c’est grâce à lui que tes amis te trouvent. Seule exception : un pseudo masqué après des signalements peut être remplacé une fois.'),
  ('Ajouter un ami', '<b>Sanctuaire → Amis</b>, puis tape son pseudo. Tu peux aussi toucher un joueur dans un classement. Une fois la demande acceptée, vous voyez mutuellement vos collections, vos succès et vos statistiques.'),
  ('J’ai changé de téléphone', 'Si tu as un compte : installe le jeu et connecte-toi, ta partie revient. Sans compte, la partie reste seulement sur l’ancien appareil ; tu peux en copier une sauvegarde depuis <b>Réglages → Jeu → Avancé</b> avant de changer.'),
  ('Signaler un joueur', 'Dans un classement, touche le pseudo d’un joueur : tu peux le signaler ou le masquer pour toi. Un pseudo signalé par plusieurs joueurs est masqué pour tout le monde.'),
  ('Supprimer mon compte', '<b>Sanctuaire → Compte → Supprimer mon compte</b> : ton profil, ta sauvegarde en ligne et tes scores sont effacés. Tu n’as plus l’application ? Écris-nous depuis l’adresse e-mail de ton compte, objet « Suppression de compte » : c’est fait sous 30 jours. Voir aussi la <a href="confidentialite.html#suppression">politique de confidentialité</a>.'),
  ('Y a-t-il des achats dans le jeu ?', 'Le jeu est gratuit et sans publicité, et toutes les cartes se gagnent en jouant. Plus tard, une boutique proposera des objets <b>uniquement cosmétiques</b> (cadres de profil, dos de cartes, finitions de prestige…) : ils changent l’apparence, jamais la force de tes créatures. Aucun booster, aucune monnaie du jeu ni aucun avantage en combat ne sera vendu.'),
  ('Le jeu n’a pas de son', 'Vérifie le volume dans <b>Réglages → Jeu</b>. Le son du jeu fonctionne même quand l’iPhone est en mode silencieux.'),
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
<p class="card">ABYSSAL — Le Bestiaire interdit<br>Site et jeu édités à titre personnel, sans activité commerciale.<br>Contact : <a href="mailto:contact@abyssal-game.fr">contact@abyssal-game.fr</a></p>
<h2>Hébergement</h2>
<p class="card">Site : GitHub, Inc. (GitHub Pages), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.<br>Comptes et sauvegardes du jeu : Supabase, Inc., hébergement en Union européenne.<br>Nom de domaine : OVH SAS, 2 rue Kellermann, 59100 Roubaix, France.</p>
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
