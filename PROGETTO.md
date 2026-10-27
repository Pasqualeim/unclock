# Progetto Unclock

Quadro breve per il capo progetto e i subagenti. Il dettaglio resta in `docs/ROADMAP.md` (fonte di verità). Qui visione, decisioni e **la lista dei punti da fare** (sezione Task): è l'unica, va tenuta aggiornata dopo ogni commit.

## Visione

Unclock zittisce le notifiche delle app di lavoro quando non lavori e conta il tempo che ti riprendi. La domanda: perché le app premiano solo il tempo di lavoro e concentrazione, e niente esiste per il tempo libero? Regole e checklist anti-stress: `docs/IDEA.md`.

Fase attuale: **test indipendente**: far provare l'app a più persone possibile, fino a 1.000, prima del Play Store pubblico. I 12 tester per 14 giorni chiesti da Google sono solo il minimo per poter pubblicare.

## Aree e cartelle

| Area | Cartella | Subagente | Note |
|---|---|---|---|
| App | `~/Documents/Developer/NotificationBlocker` (`app/`, `docs/`, `tools/`) | `app-dev`, poi `android-reviewer` | Kotlin + Compose; regole in `CLAUDE.md` |
| Sito | `~/Documents/Developer/nook-site` | `sito-dev` | HTML statico su Netlify, https://getunclock.app; regole nel suo `CLAUDE.md` |
| Social | `NotificationBlocker/marketing/` (bozze in `marketing/bozze/`) | `social-manager` | Instagram, X, Reddit, feddit.it, XDA; pubblica solo Pasquale |

Legami tipici: una modifica visibile dell'app → screenshot e testi del sito (`tools/store/capture_screenshots.sh`), riga in `marketing/DEV_LOG.md`, bozza social. Un permesso o un flusso di dati nuovo → privacy del sito e `docs/store/LISTING.md`.

## Mappa dei fatti

Ogni argomento ha un solo file padrone: lì il fatto è scritto per intero e aggiornato; altrove solo un rimando breve ("vedi X"). Se due file non sono d'accordo vince il codice, poi il padrone. Un argomento nuovo che compare in più file prende una riga qui. Controllo: `docs-auditor`.

| Argomento | Padrone | Altrove solo un rimando |
|---|---|---|
| Stato e priorità (cosa è fatto, cosa manca) | `docs/ROADMAP.md` | PROGETTO.md (lista dei punti), `CLAUDE.md` "Priorities" |
| Visione, regole anti-stress | `docs/IDEA.md` | `CLAUDE.md`, agenti, `marketing/STRATEGY.md` |
| Architettura app, regola di blocco, chiavi delle preferenze | `CLAUDE.md` (app) | ROADMAP, `REDESIGN.md` (storico) |
| Colori, tipi, forme, tono dei testi, nome | `docs/DESIGN_SYSTEM.md` | `CLAUDE.md`, `nook-site/CLAUDE.md` |
| Animazioni e loro durate | `docs/MOTION.md` | `CLAUDE.md`, `nook-site/CLAUDE.md` (durate del sito) |
| Permessi e dati (cosa vede l'app, cosa esce dal telefono) | il codice (manifest) → `docs/store/LISTING.md` (Data safety) | privacy del sito, testi del sito, social |
| Informativa privacy | `nook-site/public/it/privacy`, `en/privacy` | `LISTING.md`, app (`privacy_policy_url`) |
| Pagina tester, mail di benvenuto, gruppo, Telegram | `nook-site/CLAUDE.md` | ROADMAP (riga 3, solo stato), `CLAUDE.md` app |
| Sito: aspetto, struttura, deploy, dominio | `nook-site/CLAUDE.md`, `nook-site/README.md` | `CLAUDE.md` app ("Website") |
| Play Console, test chiuso, passi manuali | `docs/PUBLISHING.md` | ROADMAP (stato) |
| Testi e grafica dello store | `docs/store/LISTING.md` | ROADMAP (stato) |
| Instagram: strategia, calendario, novità | `marketing/STRATEGY.md`, `CALENDAR.md`, `DEV_LOG.md` | `docs/social/INSTAGRAM.md` (storico), PROGETTO.md |
| Anteprima dei link (og-it/og-en: nome, icona, titolo) | `nook-site/tools/og_image.py` (rigenera le PNG) | `nook-site/CLAUDE.md` |
| Versione dell'app (versionName, versionCode) | `app/build.gradle.kts` | `docs/store/LISTING.md` (aggiornata a ogni rilascio), ROADMAP, `PUBLISHING.md` |
| Video promo e immagini dei post (testi, scene, ritmo) | `tools/store/promo_video.py` (rigenera `marketing/video/` e `marketing/images/post_*`) | bozze in `marketing/bozze/` |
| Capo progetto e subagenti | `CLAUDE.md` app ("Project lead", "Agents") | PROGETTO.md (decisioni) |

## Decisioni

- 2026-10-26: un capo progetto (sessione principale) e quattro subagenti (`app-dev`, `sito-dev`, `social-manager`, `android-reviewer`); `copywriter` e `docs-keeper` assorbiti (tono nei subagenti, allineamento dei fatti nel capo progetto). Modello `opus` per app, sito e review, `haiku` per il social.
- 2026-10-26: profilo Instagram con un nome diverso dall'app; personaggio in sospeso (vedi sotto).
- 2026-10-26: delega solo per lavoro vero (la prova di una bozza social è costata ~100k token): il capo progetto fa da sé domande, letture, modifiche piccole, analisi d'impatto e prove; il brief porta i fatti, gli agenti leggono il minimo; niente review per una stringa o una riga.
- 2026-10-26: contro i documenti incoerenti: hook git di graphify in entrambi i repo (grafo aggiornato a ogni commit e checkout, zero token), `docs-auditor` in sola lettura lanciato dopo un rilascio, un cambio di permessi o dati, o su richiesta (mai ogni N modifiche), e la "Mappa dei fatti" qui sopra. Sfoltire i doppioni si fa dopo, a pezzi.
- 2026-10-26: niente Trello (leggerlo e scriverlo costava troppi token). La lista dei punti è la sezione Task qui sotto, aggiornata dopo ogni commit in tutti e due i repo (hook `.claude/hooks/progetto-after-commit.py`); a inizio sessione il capo progetto la mette nel piano di Claude Code. Niente di fatto o deciso resta solo nella chat.
- 2026-10-26: Instagram in pausa; i canali per trovare tester sconosciuti sono BetaList e Reddit (punti 1-3 dei Task). Gli scambi tra sviluppatori (r/AndroidClosedTesting) danno al massimo i 12 di Google, non utenti veri; niente servizi a pagamento di tester e niente premi.
- Niente pubblicazioni (deploy, push, post, mail, Play Console) senza ok di Pasquale.

## Task

In ordine di priorità. Chi: [P] Pasquale, [C] Claude.

| # | Task | Chi | Stato |
|---|---|---|---|
| 1 | Reddit: account con un po' di storia (circa 50 di karma, commentando davvero), poi un post in inglese su r/SideProject e r/betatests (storia, screenshot, link, richiesta di riscontri; testo scritto con Claude, passato da humanizer); leggere prima le regole di ogni subreddit | P | Da fare |
| 2 | Prima di BetaList: controllare il percorso inglese del sito fino alla mail di benvenuto e il limite giornaliero di mail di Resend (un lancio può portare centinaia di iscritti in un giorno) | C | Da fare |
| 3 | Iscrivere Unclock su BetaList (coda gratuita di 2-3 mesi; saltarla costa circa 99-129 $, decide Pasquale); il giorno del lancio chiedere ai tester e su Telegram di commentare la scheda | P | Da fare |
| 4 | Confermare in Play Console l'approvazione del test chiuso (in revisione dal 22/10) | P | In attesa |
| 5 | Attivare la notifica email di Netlify Forms per il modulo `signup` | P | Da fare |
| 6 | Sfoltire i doppioni della Mappa dei fatti, prossimo il CLAUDE.md dell'app (ROADMAP 3, 3a, 3b fatte) | C | In corso |
| — | Obiettivo di fondo: far provare l'app a più persone possibile prima del Play Store (tappe 12, 100, oltre) | P, C | In corso |
| — | Ricorrente: a ogni cambio visibile dell'app, rifare screenshot e immagini del sito | C | Sempre |
| — | Dopo: controllare il limite mensile di Netlify Forms se le iscrizioni superano le 100 al mese | P | Dopo |

Fatto di recente: video promo in motion design IT/EN e 6 immagini per i post (27/10, `tools/store/promo_video.py`), testo dei post per Reddit, feddit e X (27/10, `marketing/bozze/`), prova da un altro account Google (26/10), struttura capo progetto con subagenti, auditor e mappa dei fatti (26/10), informativa e anteprime del sito corrette (26/10). Lo storico completo è nella ROADMAP e in `git log`.

## Idee in sospeso

- Instagram, fermo per scelta di Pasquale (2026-10-26): prima Reddit e BetaList. Quando riparte: aprire `@pasquale.builds` (Creator, nome "Pasquale", foto, bio, link getunclock.app/it/prova), annunciarlo alla rete personale, poi i testi delle prime 4 settimane passati da humanizer. Piano in `marketing/PIANO_INSTAGRAM.md`.

- Personaggio 8 bit per Instagram, dichiarato come personaggio (non una persona finta). Proposte del 2026-10-26: Pix il lucchetto del logo, Bit l'omino che posa la borsa, Ore la clessidra. Rimandato da Pasquale.
- Dopo il test: voci 2-4 della ROADMAP (haptic, splash, contatore nella card di stato...).
