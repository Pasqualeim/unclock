# Slack: avvisi e riepiloghi dei post su X e Reddit

Configurato il 29/10/2026. Slack è il canale unico per tutto quello che è utile a Pasquale sapere: post su X (cosa succede), post da pubblicare a mano, esito di ogni controllo automatico ed errori (regola del 30/10/2026: ogni nuovo controllo o automazione avvisa qui). Mappa di tutti i flussi: `AUTOMAZIONI.md`.

## In breve: due tipi di post, due tipi di avviso

- **Post da pubblicare a mano** (Reddit, e domani feddit o altri canali): l'avviso arriva **prima**, la mattina del giorno del post, entro le 9:30. Dice dove e in quale file c'è il testo; Pasquale pubblica quando vuole in giornata.
- **Post su X pubblicati in automatico** (Buffer, di solito 9-10 dei feriali): niente avviso prima, Pasquale non deve fare niente. Arriva **dopo**: alle 11:30 "uscito" col link (per rispondere ai commenti) o "non uscito" col motivo. In più, il venerdì, l'elenco dei post della settimana dopo e l'anteprima di quella successiva.

Regole di Pasquale (30/10/2026): ogni avviso di cosa pubblicare a mano arriva la mattina, entro le 9:30, mai il pomeriggio; nessun post va sul suo Google Calendar, nemmeno quelli Reddit da fare a mano: basta Slack (il calendario resta per le cose personali; eventi Reddit cancellati la sera del 30/10).

## Cosa arriva e quando

Tutto nel canale privato **#unclock-x**, sempre con la menzione di Pasquale:

| Messaggio | Quando | Chi lo manda |
|---|---|---|
| ✅ **Uscito su X:** inizio del post (ora) link | feriali verso le 11:30, se quel giorno c'era un post | routine cloud |
| ⚠️ **Post X non uscito:** inizio del post (ora). Motivo | come sopra, se il post è in errore o ancora in coda | routine cloud |
| ❌ **Controllo post X non riuscito:** errore | come sopra, se la routine non riesce a leggere Buffer | routine cloud |
| ⚠️ **Media non raggiungibile:** file, post, codice | feriali alle 11:30, se un'immagine o un video dei post dei prossimi 3 giorni non risponde su `media.getunclock.app` (Pi, HD o Cloudflare giù) | routine cloud |
| ⚠️ **Nessun post su Buffer per la settimana prossima** | venerdì alle 11:30, se la pianificata delle 10 non ha programmato niente (Mac spento o app chiusa) | routine cloud |
| 📝 **Da pubblicare oggi su Reddit:** comunità e sezione di `marketing/forum/PIANO_REDDIT.md` col testo | alle 9:30 dei giorni con un post Reddit | routine cloud Reddit |
| ❌ **Copia dei media sul Pi non riuscita:** errore | al primo errore di una serie (non ogni ora), se il Pi è raggiungibile ma la copia fallisce | `tools/social/sync_media_pi.sh` sul Mac |
| 📅 **Programmati: settimana …** (post della settimana prossima, già su Buffer: testi, prime risposte, immagini) | venerdì dopo le 10 | pianificata del venerdì |
| 🗓️ **In preparazione: settimana …** (anteprima dei post preparati quel giorno, che verranno programmati il venerdì dopo: c'è una settimana per chiedere modifiche) | venerdì dopo le 10 | pianificata del venerdì |

Nei giorni senza post non arriva niente. I due messaggi del venerdì sono solo da guardare: non c'è niente da approvare. Se qualcosa non va, Pasquale lo dice a Claude in una sessione del progetto.

**Scrivere in #unclock-x non serve:** l'app sa solo mandare messaggi, nessuno legge il canale in automatico. Claude lo legge (connettore Slack) solo quando glielo si chiede. In futuro si può aggiungere Claude dentro Slack, ma quel Claude girerebbe nel cloud: vede Buffer e Slack, non il Mac né il Pi.

## Com'è fatto

| Pezzo | Valore |
|---|---|
| Workspace | `pasqualeim` (piano gratuito: messaggi visibili per 90 giorni), id `T0CCVNTBL4X`, solo Pasquale |
| Pasquale | utente `U0CDER0KVRS` (proprietario e admin); nel profilo il fuso è Europe/Amsterdam, stessa ora di Roma |
| Canale | **#unclock-x**, privato, id `C0CD989A1K8`; un messaggio fissato "Come funziona questo canale" che spiega i tipi di avviso (rifatto il 30/10 con Reddit, media e controlli del venerdì; va aggiornato quando cambia un avviso) e la descrizione del canale |
| App | **Unclock avvisi**, id `A0CD51K5GH1`, icona: il lucchetto di Unclock (da `docs/store/icon-512.png`); gestione su api.slack.com/apps (accesso con l'account Slack di Pasquale) |
| Permesso dell'app | uno solo: `incoming-webhook` sul canale #unclock-x. Non legge niente e non vede altri canali |
| Connettore Slack di claude.ai | per leggere il canale e come strada di riserva; scrive come Pasquale, quindi **senza notifica** |
| Canali da archiviare | `#social`, `#nuovo-canale`, `#tutta-pasqualeim`: creati da Slack all'apertura, non usati |

### Perché un'app e perché la menzione

Due cose scoperte con le prove del 29/10:

1. **Slack non notifica mai i messaggi scritti da te.** Il connettore di claude.ai scrive a nome di Pasquale, quindi quei messaggi non suonano. Per questo c'è l'app "Unclock avvisi": scrive lei, e il messaggio arriva da un'app.
2. **Senza menzione non suona comunque.** Con le impostazioni di base Slack notifica solo le menzioni e i messaggi diretti. Per questo ogni messaggio inizia con `<@U0CDER0KVRS>`; nell'app compare tra le Attività come "Tag".

### L'indirizzo del webhook

È un link `https://hooks.slack.com/services/T0CCVNTBL4X/B0CCVSVCZV5/...`: chi lo conosce può scrivere in #unclock-x (solo lì). È **segreto**: sta solo nel prompt della routine cloud e nel file `~/.config/unclock/slack_webhook` del Mac (permessi 600), letto da `tools/social/slack_week_summary.py`; mai nel repo né nei documenti.

Per cambiarlo (se finisce in giro o smette di funzionare): api.slack.com/apps → Unclock avvisi → Incoming Webhooks → "Add New Webhook" sul canale #unclock-x, poi rimuovere quello vecchio; quindi chiedere a Claude di mettere il nuovo indirizzo nel prompt della routine cloud e nel file `~/.config/unclock/slack_webhook`.

## I mittenti

- **Routine cloud "Unclock: avviso post X (cloud)"**: https://claude.ai/code/routines/trig_01LG916LJiVKC3taXJ97s4go. Feriali, cron `30 10 * * 1-5` in UTC = 11:30 italiane (con l'ora legale, da fine marzo, diventa 12:30: va spostata a `30 9 * * 1-5`). Modello Sonnet, strumenti Read e Bash, connettori solo Buffer e Slack. Legge da Buffer (organizzazione `69c8027e89cc374856f05767`, canale `6ae38e932f1f5ed64812678d`) i post di oggi e manda l'avviso con il webhook; se il webhook non risponde "ok", scrive con il connettore (senza notifica). Non tocca Buffer né X. Gira anche col Mac spento. Si cambia dalla pagina della routine o chiedendo a Claude (strumento delle routine).
- **Routine cloud "Unclock: avviso post Reddit da pubblicare (cloud)"**: https://claude.ai/code/routines/trig_01TPcFPZqj5TXoc8483dvj7L. Creata il 30/10/2026. Ogni giorno, cron `30 8 * * *` in UTC = 9:30 italiane (con l'ora legale diventa 10:30: va spostata a `30 7 * * *`). Regola di Pasquale (30/10): ogni avviso di cosa pubblicare a mano arriva la mattina, entro le 9:30. Modello Sonnet, solo Bash, nessun connettore. Le date dei post Reddit (che Pasquale pubblica a mano) stanno **nel prompt della routine**, perché nel cloud non vede `marketing/`: quando cambia il calendario di `PIANO_REDDIT.md`, Claude aggiorna anche il prompt. Nei giorni fuori lista non manda niente; l'ultimo giorno ricorda di chiedere i post successivi. Le date dei post non vanno mai sul Google Calendar di Pasquale.
- **Pianificata del venerdì** (`PIANIFICATA_VENERDI.md`): a fine giro lancia due volte `tools/social/slack_week_summary.py <piano> "<titolo>" "<nota>"`, che legge il piano in `marketing/x/` e lo manda con il webhook: i post programmati della settimana prossima e l'anteprima di quelli appena preparati. In fondo al calendario scrive "Riepilogo Slack: <settimana> mandato" e "Anteprima Slack: <settimana> mandata", così non li rimanda. `--check <piano>` legge il piano senza mandare niente.

La prima versione dell'avviso era una pianificata locale (`unclock-avviso-post-x`, feriali 11:15) che scriveva come Pasquale: dipendeva dal Mac e non notificava, cancellata il 30/10 (il suo vecchio prompt resta in `~/.claude/scheduled-tasks/unclock-avviso-post-x/SKILL.md`).

## Se non arriva la notifica

| Cosa vedi | Cosa vuol dire | Cosa fare |
|---|---|---|
| Nessun messaggio in #unclock-x in un giorno con post | La routine cloud non è partita o non ha raggiunto Buffer/Slack | Aprire la routine (link sopra) e guardare l'ultima esecuzione; ricollegare Buffer o Slack da claude.ai → Connettori |
| Il messaggio c'è ma senza notifica | Impostazioni di notifica | In Slack: foto profilo → la "z" vuol dire notifiche in pausa → riattivale; nella stessa voce, la **pianificazione** delle notifiche (es. solo 9-18 feriali: le prove serali del 29/10 non suonavano per questo). Sul telefono: Impostazioni → Notifiche → Slack attivo. Sul Mac: Impostazioni di Sistema → Notifiche → Slack |
| Suona sul Mac ma non sul telefono | Slack manda al telefono solo se non sei attivo sul Mac | Normale; per provare, chiudi Slack sul Mac |
| Il messaggio c'è, scritto da "Pasquale Ercolino" e non dall'app | Il webhook non ha risposto e la routine ha usato la riserva | Provare il webhook (vedi sotto); se è stato rimosso, crearne uno nuovo |
| Il messaggio non ha l'icona del lucchetto | Messaggio scritto dal connettore, non dall'app | Come sopra |

Prova manuale del webhook (da Claude, che ha l'indirizzo nei prompt): un POST JSON `{"text":"<@U0CDER0KVRS> prova"}` all'indirizzo deve rispondere `ok` e far comparire il messaggio in #unclock-x.

## Storico del 29/10/2026

Connettore Slack autorizzato; messaggio di prova in DM; canale #unclock-x creato; app creata da Claude nel browser integrato (accesso fatto da Pasquale) con il manifest precompilato; webhook provato 7 volte: le prime non notificavano (niente menzione, poi notifiche in pausa e fuori orario), con menzione e notifiche attive arrivano; icona caricata. I messaggi di prova in #unclock-x e nel DM li cancella Pasquale (Claude non cancella messaggi).
