# La pianificata del venerdì (post su X in automatico)

Deciso il 29/10/2026 da Pasquale: i post su X (@Pasquale_im) li prepara **e li programma su Buffer Claude, da solo**, ogni venerdì. Pasquale non rilegge, non approva e non programma niente. Durata: almeno un paio di mesi (fino a fine dicembre 2026), poi si guarda com'è andata.

## Il ciclo

Ogni venerdì alle 10:00 (parte verso le 10:10) una pianificata dell'app desktop di Claude, sul Mac:

1. **Programma su Buffer i post della settimana prossima**, che sono già pronti dal venerdì prima.
2. **Prepara i post della settimana dopo ancora** (testi, immagini, video), che programmerà il venerdì successivo.

Esempio: venerdì 30/10 i post del 02-06/11 sono già programmati (li ha programmati Claude il 29/10), quindi prepara quelli del 09-13/11. Venerdì 06/11 programma quelli del 09-13/11 e prepara quelli del 16-20/11. E così via.

In ogni giro, nell'ordine:

1. Legge il calendario `marketing/x/CALENDARIO.md`, aggiorna gli stati da Buffer (uscito, errore) e riprogramma i post saltati.
2. Programma su Buffer i post pronti della settimana prossima (`customScheduled`, data e ora del calendario), con il media da `https://media.getunclock.app/<nome>` e la prima risposta col link come secondo post del thread.
3. Scrive i post della settimana dopo in `marketing/x/AAAA-MM-GG_settimana-N.md` (3-4 post, mattine dei feriali 9-11, link sempre nella prima risposta), testi passati da humanizer.
4. Crea immagini e video in `marketing/images/x/` e `marketing/video/x/`, con la **data di uscita** davanti al nome, e li manda sul Raspberry Pi (`docs/social/MEDIA_HOST.md`) controllando che rispondano 200.
5. Aggiorna calendario e tabella Task di `PROGETTO.md`, scrive un resoconto breve in italiano.

## Perché sul Mac e non nel cloud

- `marketing/` non è nel repo (è git-ignored): una pianificata nel cloud non vedrebbe né i piani né i media.
- Il Pi si raggiunge solo dalla rete di casa.
- Il venerdì Pasquale lavora da casa, quindi il Mac è acceso. Se l'app è chiusa alle 10, la pianificata parte appena si riapre.

Per questo è stata creata da Claude Code (scheda **Code**), non da Cowork: la shell di Cowork passa da una lista di siti consentiti e non raggiunge il Pi.

## Il calendario e le regole contro gli accavallamenti

Tutto parte da un **calendario unico**, `marketing/x/CALENDARIO.md` (non in git, come tutto `marketing/`): una riga per post con data, ora, media, piano, stato e id del post su Buffer. Stati: `pianificato` (pronto, non su Buffer) → `programmato` (su Buffer) → `uscito`; `saltato` se la data è passata senza uscire.

Regole a ogni giro, anche se un venerdì salta o la pianificata parte due volte:

- un post per giorno feriale al massimo, 4 a settimana (lun-ven), ore 9-11;
- prima di programmare controlla Buffer e il calendario: se il post c'è già, non lo ricrea;
- un post non uscito con la data passata (o in errore su Buffer) va al primo giorno feriale libero da domani in poi, modificando il post Buffer esistente, mai creandone un altro;
- i post nuovi vanno solo dopo l'ultimo post già nel calendario, mai a riempire buchi prima;
- mai preparare oltre la settimana dopo la prossima; un venerdì saltato si recupera al giro dopo (prepara e programma la settimana che manca);
- al massimo 10 post programmati su Buffer (piano gratuito); con 3-4 a settimana se ne usano 3-4;
- i post usciti non si toccano.

## Regole sui contenuti

- Contenuti secondo `docs/IDEA.md` (tempo libero, mai riposo come premio, mai il lavoro che manca); tono da persona che condivide un'idea, niente vendita, mai "gratis".
- Ogni testo passa da humanizer. Link sempre nella prima risposta, mai nel post.
- Schermate solo con dati di esempio, mai notifiche vere; se l'immagine mostra dati di esempio lo dice.
- Grafica e video su Opus. Mai pubblicare subito (`shareNow`): solo post programmati. Niente Telegram, Reddit, email.

## Il prompt

Il prompt valido è uno solo: `~/.claude/scheduled-tasks/unclock-post-x-settimana/SKILL.md`. Si legge e si cambia dalla pagina Pianificate dell'app, o chiedendo a Claude. Contiene il ciclo e le regole qui sopra, con il canale Buffer (`6ae38e932f1f5ed64812678d`). Modalità Auto: gira senza chiedere conferme.

## Slack

Workspace `pasqualeim` (piano gratuito), solo Pasquale. Gli avvisi dei post vanno nel canale privato **#unclock-x** (id `C0CD989A1K8`, creato il 29/10/2026), che ha in cima un messaggio che spiega i tre tipi di avviso: :white_check_mark: uscito, :warning: non uscito, :x: controllo non riuscito. I canali `#social`, `#nuovo-canale` e `#tutta-pasqualeim` sono quelli creati da Slack all'apertura del workspace: non servono, si possono archiviare.

**Notifiche sul telefono:** i messaggi scritti tramite il connettore Slack risultano scritti da Pasquale stesso, e Slack non notifica mai i propri messaggi. Per questo il 29/10/2026 Claude ha creato l'app Slack **Unclock avvisi** (id `A0CD51K5GH1`, gestione su api.slack.com/apps) con un solo permesso: un Incoming Webhook che scrive in #unclock-x. La routine cloud scrive attraverso il webhook, quindi il messaggio arriva da un'app e il telefono suona; se il webhook non risponde, ripiega sul connettore Slack (messaggio senza notifica).

L'indirizzo del webhook è segreto (chi lo ha può scrivere in #unclock-x, solo lì): sta solo nel prompt della routine cloud, mai nel repo. Se finisse in giro: api.slack.com/apps → Unclock avvisi → Incoming Webhooks → rimuovi il webhook e creane uno nuovo, poi chiedi a Claude di aggiornare la routine.

## Se qualcosa va storto

| Cosa vedi | Cosa vuol dire | Cosa fare |
|---|---|---|
| Venerdì nessun resoconto | Mac spento o app chiusa all'ora della pianificata | Riapri l'app (parte da sola) o lanciala a mano da Pianificate |
| Un post su Buffer senza immagine o in errore | Il media non era sul Pi o il Pi era spento all'ora di uscita | `~/Library/Logs/unclock-sync.log` e la tabella dei problemi in `MEDIA_HOST.md`; il venerdì dopo la pianificata lo riprogramma da sola |
| Il resoconto dice "Pi non raggiungibile" | Pi spento, IP cambiato, o la pianificata gira senza rete di casa | Tabella dei problemi in `MEDIA_HOST.md` |
| Due post nello stesso giorno su X | Il calendario non era aggiornato | Dillo a Claude: sistema calendario e Buffer |
| Nessun messaggio Slack in un giorno con post | Routine cloud non partita o Slack/Buffer scollegati su claude.ai | Apri la routine (link in Stato) e guarda l'ultima esecuzione; ricollega i connettori da claude.ai |
| Un post esce con un testo che non va | Nessuno l'ha riletto (scelta del 29/10) | Cancellalo da X; dillo a Claude per correggere il prompt |

## Stato

- 29/10/2026: pianificata "Unclock: post X della settimana" creata da Claude Code, venerdì alle 10:00, modalità Auto. Buffer: account pasquale.ercolino98, organizzazione "My Organization", fuso Europe/Rome, piano gratuito (3 canali, 10 post programmati alla volta), canale X `Pasquale_im` collegato.
- 29/10/2026: prova riuscita con una bozza (immagine dal Pi letta 1600x900 PNG), poi cancellata. Buffer usa l'indirizzo del Pi, non una copia sua: il Pi deve restare acceso finché i post non sono usciti.
- 29/10/2026: la settimana 1 (prevista 29/10-03/11) spostata a lun 02/11 - ven 06/11 (lun 9:30, mar 10:00, gio 9:30, ven 9:00) e **programmata su Buffer da Claude**, video compreso. Tolto l'obbligo dei 30-45 minuti online: Pasquale risponde quando può. Primo giro della pianificata venerdì 30/10: prepara i post del 09-13/11.
- 29/10/2026: avviso su Slack quando un post esce, **nel cloud** (funziona anche col Mac spento): routine "Unclock: avviso post X (cloud)", https://claude.ai/code/routines/trig_01LG916LJiVKC3taXJ97s4go, feriali alle 11:30 ora italiana (cron `30 10 * * 1-5` in UTC: dall'ora legale, fine marzo, diventa le 12:30), connettori solo Buffer e Slack. Legge i post di oggi da Buffer e scrive a Pasquale in messaggio diretto su Slack (workspace pasqualeim, utente `U0CDER0KVRS`) "Uscito su X" con link o "Post X non uscito" con il motivo; senza post quel giorno non scrive niente; non tocca Buffer né X. La prima versione locale (`unclock-avviso-post-x`, feriali 11:15) è spenta: dipendeva dal Mac acceso. Lo stato "uscito" nel calendario lo aggiorna la pianificata del venerdì leggendo Buffer.
