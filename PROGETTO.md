# Progetto Unclock

Quadro breve per il capo progetto e i subagenti. Il dettaglio resta in `docs/ROADMAP.md` (fonte di verità) e sulla bacheca Trello "Unclock" (vista rapida). Qui solo visione, decisioni e task che toccano più aree.

## Visione

Unclock zittisce le notifiche delle app di lavoro quando non lavori e conta il tempo che ti riprendi. La domanda: perché le app premiano solo il tempo di lavoro e concentrazione, e niente esiste per il tempo libero? Regole e checklist anti-stress: `docs/IDEA.md`.

Fase attuale: **test indipendente** (test chiuso su Play, 12 tester per 14 giorni). Il Play Store pubblico viene dopo.

## Aree e cartelle

| Area | Cartella | Subagente | Note |
|---|---|---|---|
| App | `~/Documents/Developer/NotificationBlocker` (`app/`, `docs/`, `tools/`) | `app-dev`, poi `android-reviewer` | Kotlin + Compose; regole in `CLAUDE.md` |
| Sito | `~/Documents/Developer/nook-site` | `sito-dev` | HTML statico su Netlify, https://getunclock.app; regole nel suo `CLAUDE.md` |
| Social | `NotificationBlocker/marketing/` (bozze in `marketing/bozze/`) | `social-manager` | Instagram; fuori dai commit (`.git/info/exclude`); pubblica solo Pasquale |

Legami tipici: una modifica visibile dell'app → screenshot e testi del sito (`tools/store/capture_screenshots.sh`), riga in `marketing/DEV_LOG.md`, bozza social. Un permesso o un flusso di dati nuovo → privacy del sito e `docs/store/LISTING.md`.

## Decisioni

- 2026-10-26: un capo progetto (sessione principale) e quattro subagenti (`app-dev`, `sito-dev`, `social-manager`, `android-reviewer`); `copywriter` e `docs-keeper` assorbiti (tono nei subagenti, allineamento dei fatti nel capo progetto). Modello `opus` per app, sito e review, `haiku` per il social.
- 2026-10-26: profilo Instagram con un nome diverso dall'app; personaggio in sospeso (vedi sotto).
- 2026-10-26: delega solo per lavoro vero (la prova di una bozza social è costata ~100k token): il capo progetto fa da sé domande, letture, modifiche piccole, analisi d'impatto e prove; il brief porta i fatti, gli agenti leggono il minimo; niente review per una stringa o una riga.
- Niente pubblicazioni (deploy, push, post, mail, Play Console) senza ok di Pasquale.

## Task

| Task | Area | Stato |
|---|---|---|
| Trovare 12 tester e far partire i 14 giorni del test chiuso | Social, sito | Da fare |
| Confermare l'approvazione del test chiuso su Play Console | Play | In attesa di Pasquale |
| Scegliere nome e personaggio del profilo Instagram | Social | In attesa di Pasquale |
| Prova completa da un altro account Google (pagina tester, gruppo, opt-in, installazione) | Sito, Play | Fatto (2026-10-26) |
| Struttura capo progetto + subagenti | Tutte | Fatto (2026-10-26) |

## Idee in sospeso

- Personaggio 8 bit per Instagram, dichiarato come personaggio (non una persona finta). Proposte del 2026-10-26: Pix il lucchetto del logo, Bit l'omino che posa la borsa, Ore la clessidra. Rimandato da Pasquale.
- Dopo il test: voci 2-4 della ROADMAP (haptic, splash, contatore nella card di stato...).
