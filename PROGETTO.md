# Progetto Unclock

Quadro breve per il capo progetto e i subagenti. Il dettaglio resta in `docs/ROADMAP.md` (fonte di verità) e sulla bacheca Trello "Unclock" (vista rapida). Qui solo visione, decisioni e task che toccano più aree.

## Visione

Unclock zittisce le notifiche delle app di lavoro quando non lavori e conta il tempo che ti riprendi. La domanda: perché le app premiano solo il tempo di lavoro e concentrazione, e niente esiste per il tempo libero? Regole e checklist anti-stress: `docs/IDEA.md`.

Fase attuale: **test indipendente**: far provare l'app a più persone possibile, fino a 1.000, prima del Play Store pubblico. I 12 tester per 14 giorni chiesti da Google sono solo il minimo per poter pubblicare.

## Aree e cartelle

| Area | Cartella | Subagente | Note |
|---|---|---|---|
| App | `~/Documents/Developer/NotificationBlocker` (`app/`, `docs/`, `tools/`) | `app-dev`, poi `android-reviewer` | Kotlin + Compose; regole in `CLAUDE.md` |
| Sito | `~/Documents/Developer/nook-site` | `sito-dev` | HTML statico su Netlify, https://getunclock.app; regole nel suo `CLAUDE.md` |
| Social | `NotificationBlocker/marketing/` (bozze in `marketing/bozze/`) | `social-manager` | Instagram; fuori dai commit (`.git/info/exclude`); pubblica solo Pasquale |

Legami tipici: una modifica visibile dell'app → screenshot e testi del sito (`tools/store/capture_screenshots.sh`), riga in `marketing/DEV_LOG.md`, bozza social. Un permesso o un flusso di dati nuovo → privacy del sito e `docs/store/LISTING.md`.

## Mappa dei fatti

Ogni argomento ha un solo file padrone: lì il fatto è scritto per intero e aggiornato; altrove solo un rimando breve ("vedi X"). Se due file non sono d'accordo vince il codice, poi il padrone. Un argomento nuovo che compare in più file prende una riga qui. Controllo: `docs-auditor`.

| Argomento | Padrone | Altrove solo un rimando |
|---|---|---|
| Stato e priorità (cosa è fatto, cosa manca) | `docs/ROADMAP.md` | PROGETTO.md (task fra le aree), Trello, `CLAUDE.md` "Priorities" |
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
| Capo progetto e subagenti | `CLAUDE.md` app ("Project lead", "Agents") | PROGETTO.md (decisioni) |

## Decisioni

- 2026-10-26: un capo progetto (sessione principale) e quattro subagenti (`app-dev`, `sito-dev`, `social-manager`, `android-reviewer`); `copywriter` e `docs-keeper` assorbiti (tono nei subagenti, allineamento dei fatti nel capo progetto). Modello `opus` per app, sito e review, `haiku` per il social.
- 2026-10-26: profilo Instagram con un nome diverso dall'app; personaggio in sospeso (vedi sotto).
- 2026-10-26: delega solo per lavoro vero (la prova di una bozza social è costata ~100k token): il capo progetto fa da sé domande, letture, modifiche piccole, analisi d'impatto e prove; il brief porta i fatti, gli agenti leggono il minimo; niente review per una stringa o una riga.
- 2026-10-26: contro i documenti incoerenti: hook git di graphify in entrambi i repo (grafo aggiornato a ogni commit e checkout, zero token), `docs-auditor` in sola lettura lanciato dopo un rilascio, un cambio di permessi o dati, o su richiesta (mai ogni N modifiche), e la "Mappa dei fatti" qui sopra. Sfoltire i doppioni si fa dopo, a pezzi.
- 2026-10-26: Trello si aggiorna dopo ogni commit, in tutti e due i repo (hook `.claude/hooks/trello-after-commit.py`); niente di fatto o deciso resta solo nella chat.
- Niente pubblicazioni (deploy, push, post, mail, Play Console) senza ok di Pasquale.

## Task

| Task | Area | Stato |
|---|---|---|
| Far provare l'app fino a 1.000 tester (tappe: 12, 100, 1.000) | Social, sito | In corso |
| Reggere 1.000 iscrizioni: limiti di Netlify Forms, Resend e il tetto di 50 mail al giorno | Sito | Da fare (Claude) |
| Confermare l'approvazione del test chiuso su Play Console | Play | In attesa di Pasquale |
| Aprire (o rinominare) il profilo `@pasquale.builds` e seguire `marketing/PIANO_INSTAGRAM.md` | Social | Da fare (Pasquale) |
| Prova completa da un altro account Google (pagina tester, gruppo, opt-in, installazione) | Sito, Play | Fatto (2026-10-26) |
| Attivare la notifica email di Netlify Forms per il modulo `signup` | Sito | Da fare (Pasquale) |
| Sfoltire i doppioni indicati dalla Mappa dei fatti | Tutte | In corso: ROADMAP righe 3, 3a, 3b fatte (26/10/2026); il resto a pezzi |
| Struttura capo progetto + subagenti, auditor, mappa dei fatti | Tutte | Fatto (2026-10-26) |

## Idee in sospeso

- Personaggio 8 bit per Instagram, dichiarato come personaggio (non una persona finta). Proposte del 2026-10-26: Pix il lucchetto del logo, Bit l'omino che posa la borsa, Ore la clessidra. Rimandato da Pasquale.
- Dopo il test: voci 2-4 della ROADMAP (haptic, splash, contatore nella card di stato...).
