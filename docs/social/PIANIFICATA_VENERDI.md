# La pianificata del venerdì (post X della settimana dopo)

Deciso il 29/10/2026. Ogni venerdì Claude prepara da solo i post su X della settimana successiva: testi, immagini e video, e le bozze su Buffer. Pasquale le rilegge e le approva; niente esce senza il suo ok.

## Come funziona, in breve

1. **Venerdì, all'ora scelta** (le 10:00), parte una pianificata dell'app desktop di Claude sul Mac.
2. Claude legge il calendario (`marketing/x/CALENDARIO.md`), sposta i post saltati e, se servono, scrive i post nuovi fino a due settimane avanti in `marketing/x/AAAA-MM-GG_settimana-N.md` (3-4 post a settimana, mattine dei feriali 9-11, link sempre nella prima risposta), con testi passati da humanizer.
3. Crea immagini e video in `marketing/images/x/` e `marketing/video/x/`, con la **data di uscita** davanti al nome.
4. La copia automatica li porta sul Raspberry Pi (`docs/social/MEDIA_HOST.md`): la pianificata la lancia subito, senza aspettare l'ora.
5. Su Buffer crea **solo bozze** (`saveToDraft`), una per post non ancora su Buffer, con il media preso da `https://media.getunclock.app/<nome>`.
6. Pasquale, nel weekend o lunedì presto, apre Buffer, corregge se serve e programma lui le bozze all'orario scritto nel piano.

## Perché sul Mac e non nel cloud

- `marketing/` non è nel repo (è git-ignored): una pianificata nel cloud non vedrebbe né i piani né i media.
- Il Pi si raggiunge solo dalla rete di casa.
- Il venerdì Pasquale lavora da casa, quindi il Mac è acceso e in casa. Se un venerdì è spento, la pianificata salta quel giro: si lancia a mano dall'app.

La pianificata deve girare in una sessione con la shell vera del Mac (la scheda **Code** dell'app desktop, cartella `NotificationBlocker`). La shell di Cowork passa da una lista di siti consentiti e non raggiunge né il Pi né `media.getunclock.app` (`MEDIA_HOST.md`): se la pianificata girasse lì, i media non arriverebbero sul Pi in tempo e Buffer non li troverebbe.

## Regole che la pianificata rispetta

- **Mai pubblicare, mai programmare.** Su Buffer solo bozze; niente `shareNow`, `addToQueue`, `customScheduled`. Niente Telegram, Reddit, email.
- Contenuti secondo `docs/IDEA.md` (tempo libero, mai riposo come premio, mai il lavoro che manca); tono da persona che condivide un'idea, niente vendita, mai "gratis".
- Ogni testo passa da humanizer. Link sempre nella prima risposta, mai nel post.
- Schermate solo con dati di esempio, mai notifiche vere; se l'immagine mostra dati di esempio lo dice.
- Grafica e video su Opus.
- Alla fine aggiorna la tabella Task di `PROGETTO.md` e scrive un resoconto breve in italiano.

## Il calendario e le regole contro gli accavallamenti

Deciso il 29/10/2026, quando la settimana 1 è stata spostata di 7 giorni. Tutto parte da un **calendario unico**, `marketing/x/CALENDARIO.md` (non in git, come tutto `marketing/`): una riga per post con data, ora, media, piano, stato (`pianificato` → `bozza` → `programmato` → `uscito`, oppure `saltato`) e id della bozza su Buffer. La pianificata lo legge per primo e lo aggiorna per ultimo.

Regole che valgono a ogni giro, anche se un venerdì salta o la pianificata parte due volte:

- un post per giorno feriale al massimo, 4 a settimana (lun-ven), ore 9-11;
- prima di creare una bozza controlla Buffer e il calendario: se il post c'è già, non lo ricrea;
- un post non uscito con la data passata diventa `saltato` e va al primo giorno libero da domani in poi; la sua bozza su Buffer si aggiorna, non se ne crea un'altra;
- i post nuovi vanno solo dopo l'ultimo post già nel calendario, mai a riempire buchi prima;
- orizzonte: il calendario copre fino al venerdì della settimana dopo la prossima, non oltre; un venerdì saltato si recupera al giro dopo, sempre entro l'orizzonte;
- al massimo 10 post programmati su Buffer (piano gratuito);
- i post `programmato` e `uscito` non si toccano.

**Cosa fa Pasquale:** quando programma una bozza o pubblica a mano, cambia lo stato nel calendario (o lo chiede a Claude). Se non lo fa, la pianificata vede la bozza su Buffer e non la duplica, ma potrebbe spostarla come `saltato` se la data è passata.

## Il prompt

La pianificata è stata creata da Claude Code (non da Cowork) con lo strumento delle attività pianificate. Il prompt valido è uno solo: `~/.claude/scheduled-tasks/unclock-post-x-settimana/SKILL.md`. Si legge e si cambia dalla pagina Pianificate dell'app (o chiedendo a Claude). Contiene le regole qui sopra e i passi: post saltati, post nuovi con testi da humanizer, media, copia sul Pi con controllo 200, bozze su Buffer (canale `6ae38e932f1f5ed64812678d`), PROGETTO.md, resoconto.

## Se qualcosa va storto

| Cosa vedi | Cosa vuol dire | Cosa fare |
|---|---|---|
| Venerdì nessun resoconto | Mac spento o app chiusa all'ora della pianificata | Lancia la pianificata a mano dall'app |
| Le bozze su Buffer non hanno l'immagine | Il media non era sul Pi quando Buffer l'ha cercato | Controlla `~/Library/Logs/unclock-sync.log` e la tabella dei problemi in `MEDIA_HOST.md`; poi aggiungi il media alla bozza da Buffer con l'indirizzo `https://media.getunclock.app/<nome>` |
| Il resoconto dice "Pi non raggiungibile" | La pianificata gira senza accesso alla rete di casa (es. in Cowork) o il Pi è spento | Verifica che la pianificata sia nella scheda Code; poi la tabella dei problemi in `MEDIA_HOST.md` |
| Su Buffer un post risulta programmato, non bozza | La pianificata non ha rispettato la regola | Rimettilo in bozza da Buffer e segnalalo: va corretto il prompt qui sopra |

## Stato

- 29/10/2026: creata dalla sessione Code con lo strumento delle attività pianificate (non da Cowork): "Unclock: post X della settimana", venerdì alle 10:00 (parte verso le 10:10; spostata dalle 9:00 il 29/10), modalità Auto. Il prompt è in `~/.claude/scheduled-tasks/unclock-post-x-settimana/SKILL.md` (uguale a quello qui sopra, con i percorsi assoluti); orario e prompt si cambiano dalla pagina Pianificate dell'app. Primo giro venerdì 30/10: controllare il resoconto e le bozze su Buffer.
- 29/10/2026: Buffer controllato dal connettore: account pasquale.ercolino98, organizzazione "My Organization", fuso Europe/Rome, piano gratuito (3 canali, 10 post programmati alla volta). Canale X collegato lo stesso giorno: `Pasquale_im` (service `twitter`, id `6ae38e932f1f5ed64812678d`), attivo.
- 29/10/2026: prova riuscita. Una bozza con immagine da `https://media.getunclock.app/2026-10-28_niente_internet.png` e una risposta in thread è stata accettata da Buffer (stato `draft`, immagine letta 1600x900 PNG), poi cancellata. Nella bozza Buffer tiene l'indirizzo del Pi come anteprima, non una copia sua: il Pi deve restare acceso finché i post non sono usciti (regola in `MEDIA_HOST.md`).
- 29/10/2026: settimana 1 spostata di 7 giorni (si parte giovedì 05/11; media rinominati con le date nuove e copiati sul Pi, 200), tolto l'obbligo dei 30-45 minuti online, aggiunti calendario unico e regole contro gli accavallamenti. Il giro di venerdì 30/10 deve solo fare le bozze dei 4 post e al massimo 2 post nuovi per l'11-13/11.
