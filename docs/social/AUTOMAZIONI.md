# Automazioni dei social: la mappa

Punto di partenza per qualunque problema sui post di X. Qui c'è l'elenco dei flussi automatici, dove sta ogni pezzo e quale documento lo spiega per intero. Messo in piedi il 29/10/2026.

Se un flusso si rompe, basta dire a Claude quale ("non è arrivato l'avviso", "il post non è uscito", "le immagini non sono sul Pi"): da qui sa dove guardare.

## I flussi in una riga

| # | Flusso | Quando | Dove gira | Documento |
|---|---|---|---|---|
| 1 | Copia dei media dal Mac al Raspberry Pi | ogni ora e all'accensione del Mac | Mac (LaunchAgent); se fallisce avvisa su Slack | `MEDIA_HOST.md` |
| 2 | Post su X della settimana: programma su Buffer la settimana prossima, prepara quella dopo, manda su Slack i programmati e l'anteprima dei preparati | venerdì alle 10:00 | Mac (pianificata dell'app Claude) | `PIANIFICATA_VENERDI.md` |
| 3 | Pubblicazione su X | all'ora di ogni post | Buffer (nel cloud) | `PIANIFICATA_VENERDI.md` |
| 4 | Controlli su Slack: post uscito o no, media dei prossimi 3 giorni raggiungibili, il venerdì post della settimana dopo programmati | feriali alle 11:30 | cloud Anthropic (routine) | `SLACK.md` |
| 5 | Cose da fare a mano: un promemoria per ogni riga in scadenza della lista Slack "Unclock: da fare a mano", ✅ = fatto | ogni giorno alle 9:30, avvisa solo se c'è qualcosa | cloud Anthropic (routine) | `SLACK.md` |

Come si legano: (2) scrive testi e media in `marketing/` → (1) porta i media sul Pi, che li espone su `https://media.getunclock.app/` → (2) programma su Buffer i post con quei link → (3) Buffer pubblica e scarica il media dal Pi all'ora del post → (4) controlla Buffer e avvisa su Slack.

Cosa deve restare acceso: il **Pi** sempre (Buffer prende i media da lì all'ora di uscita); il **Mac con l'app Claude aperta** il venerdì mattina (flusso 2) e, per la copia, quando ci sono media nuovi. Il flusso 4 non dipende dal Mac.

## Dove sta ogni pezzo

| Pezzo | Dove | Nel repo? |
|---|---|---|
| Script della copia | `tools/social/sync_media_pi.sh` | sì |
| LaunchAgent della copia | `~/Library/LaunchAgents/app.getunclock.syncmedia.plist` | no |
| Log della copia | `~/Library/Logs/unclock-sync.log` | no |
| Chiave SSH e alias del Pi | `~/.ssh/unclock_pi`, blocco `unclock-pi` in `~/.ssh/config` (Pi `192.168.1.33`) | no |
| Cartella pubblica sul Pi | `/home/pasquale/media` → `https://media.getunclock.app/<nome>` | no |
| Prompt della pianificata del venerdì | `~/.claude/scheduled-tasks/unclock-post-x-settimana/SKILL.md` (pagina Pianificate dell'app) | no |
| Script dei messaggi Slack del venerdì | `tools/social/slack_week_summary.py` | sì |
| Indirizzo del webhook Slack (segreto) | `~/.config/unclock/slack_webhook` | no |
| Routine cloud dell'avviso | https://claude.ai/code/routines/trig_01LG916LJiVKC3taXJ97s4go | no |
| Calendario dei post | `marketing/x/CALENDARIO.md` | no (`marketing/` è git-ignored) |
| Piani e testi | `marketing/x/AAAA-MM-GG_settimana-N.md` | no |
| Media | `marketing/images/x/`, `marketing/video/x/` | no |
| Script dei media | `marketing/tools/x_week<N>.py` (sul modello di `x_week1.py`) | no |
| Buffer | organizzazione "My Organization" (`69c8027e89cc374856f05767`), canale X `Pasquale_im` (`6ae38e932f1f5ed64812678d`), piano gratuito | — |
| Slack | workspace `pasqualeim`, canale #unclock-x, app "Unclock avvisi": vedi `SLACK.md` | — |

`marketing/` non è in git: calendario, piani e media non hanno storico né backup. Il resto della configurazione fuori dal repo è descritto qui e nei documenti collegati, così si può rifare.

## Segreti

Nessun segreto sta nel repo.

- **Chiave SSH del Pi:** solo sul Mac (`~/.ssh/unclock_pi`); sul Pi è limitata a scrivere con rsync dentro `media` (`MEDIA_HOST.md`).
- **Indirizzo del webhook Slack:** nel prompt della routine cloud e in `~/.config/unclock/slack_webhook` sul Mac. Come cambiarlo: `SLACK.md`.
- **Accessi a Buffer e Slack:** sono i connettori di claude.ai, legati all'account di Pasquale.

## Se qualcosa non va: da dove partire

| Sintomo | Flusso | Primo controllo |
|---|---|---|
| Un post non è uscito su X | 3 | Avviso ⚠️ in #unclock-x; il post su Buffer (stato `error`?); `PIANIFICATA_VENERDI.md` |
| Post uscito senza immagine | 1, 3 | `https://media.getunclock.app/<nome>` risponde 200? Pi acceso? `MEDIA_HOST.md` |
| Nessun avviso su Slack in un giorno con post | 4 | Ultima esecuzione della routine cloud; `SLACK.md` |
| Avviso nel canale ma niente notifica sul telefono | 4 | Pausa notifiche e pianificazione notifiche di Slack; `SLACK.md` |
| Venerdì nessun messaggio Slack né post nuovi | 2 | L'app Claude era aperta? Pagina Pianificate → ultima esecuzione; `PIANIFICATA_VENERDI.md` |
| ⚠️ "Media non raggiungibile" su Slack | 1, 4 | Pi acceso? HD montato? `cloudflared` attivo? `MEDIA_HOST.md` |
| ⚠️ "Nessun post su Buffer per la settimana prossima" | 2 | Apri l'app Claude e lancia la pianificata da Pianificate; `PIANIFICATA_VENERDI.md` |
| Media nuovi non sul Pi | 1 | `~/Library/Logs/unclock-sync.log`; `MEDIA_HOST.md` |
| Nessun promemoria alle 9:30 per una cosa in scadenza | 5 | La riga ha Scadenza e Fatto non spuntato? Ultima esecuzione della routine; `SLACK.md` |
| Due post nello stesso giorno | 2 | `marketing/x/CALENDARIO.md` contro Buffer; `PIANIFICATA_VENERDI.md` |

## Da ricordare

- **Ora legale (fine marzo 2027):** la routine cloud è in UTC (`30 10 * * 1-5`), quindi passerà alle 12:30 italiane; va spostata a `30 9 * * 1-5`. La pianificata del venerdì usa l'ora locale e non cambia.
- **Fine dicembre 2026:** rivedere com'è andata (la decisione del 29/10 era "almeno un paio di mesi").
- **IP del Pi:** conviene prenotarlo sul router Vodafone (`MEDIA_HOST.md`).
