# La pianificata del venerdì (post X della settimana dopo)

Deciso il 29/10/2026. Ogni venerdì Claude prepara da solo i post su X della settimana successiva: testi, immagini e video, e le bozze su Buffer. Pasquale le rilegge e le approva; niente esce senza il suo ok.

## Come funziona, in breve

1. **Venerdì, all'ora scelta** (le 10:00), parte una pianificata dell'app desktop di Claude sul Mac.
2. Claude legge il piano e le regole, scrive il piano della settimana dopo in `marketing/x/AAAA-MM-GG_settimana-N.md` (3-4 post, mattine dei feriali 9-11, link sempre nella prima risposta), con testi passati da humanizer.
3. Crea immagini e video in `marketing/images/x/` e `marketing/video/x/`, con la **data di uscita** davanti al nome.
4. La copia automatica li porta sul Raspberry Pi (`docs/social/MEDIA_HOST.md`): la pianificata la lancia subito, senza aspettare l'ora.
5. Su Buffer crea **solo bozze** (`saveToDraft`), una per post, con il media preso da `https://media.getunclock.app/<nome>`.
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

## Prompt da dare a Cowork

Da incollare in Cowork per creare la pianificata. Cambia l'orario se scegli il pomeriggio.

```text
Crea una pianificata nell'app desktop di Claude sul mio Mac, nella scheda Code (Claude Code), non in Cowork: le serve la shell vera del Mac per raggiungere il Raspberry Pi di casa.

- Nome: Unclock: post X della settimana
- Quando: ogni venerdì alle 10:00 (ora italiana)
- Cartella di lavoro: /Users/pasqualeercolino/Documents/Developer/NotificationBlocker
- Modello: Opus
- Connettori: Buffer
- Prompt della pianificata: il testo tra le righe ===== qui sotto, così com'è.

=====
Sei il capo progetto di Unclock (leggi CLAUDE.md e PROGETTO.md). Oggi è venerdì: prepara i post su X (@Pasquale_im) della settimana prossima, da lunedì a venerdì. Non pubblicare e non programmare niente: su Buffer solo bozze.

1. Leggi: docs/IDEA.md, marketing/README.md, docs/social/PIANIFICATA_VENERDI.md, docs/social/MEDIA_HOST.md, marketing/DEV_LOG.md (novità dell'app), e i piani già fatti in marketing/x/ (il più recente per ultimo). Non ripetere temi o immagini già usati.
2. Scrivi marketing/x/<data di oggi>_settimana-<N>.md: 3 o 4 post (uno può essere un thread), mattine dei feriali tra 9 e 11 ora italiana, mai sera né weekend. Per ogni post: giorno e ora, nome del media, testo, prima risposta con il link (https://getunclock.app/it/prova o /en/try per l'inglese), una riga sul perché. Il link sta sempre nella prima risposta, mai nel post. Ogni testo passa dalla skill humanizer. Tono: una persona che condivide un'idea, niente vendita, mai "gratis".
3. Crea i media: immagini 1600x900 PNG in marketing/images/x/, video MP4 1920x1080 in marketing/video/x/, nome AAAA-MM-GG_slug con la data di uscita del post. Scrivi lo script marketing/tools/x_week<N>.py sul modello di marketing/tools/x_week1.py (riusa gli helper di tools/store/promo_video.py, stesso venv) e lancialo. Solo dati di esempio, mai notifiche vere. Guarda ogni immagine prima di andare avanti.
4. Manda i media sul Pi: bash tools/social/sync_media_pi.sh. Poi, per ogni media: curl -s -o /dev/null -w "%{http_code}" https://media.getunclock.app/<nome> deve dare 200. Se non dà 200, non mettere quel media su Buffer e scrivilo nel resoconto.
5. Su Buffer (connettore Buffer): get_account, list_channels, prendi il canale X di @Pasquale_im. Per ogni post crea una bozza con create_post, saveToDraft: true, schedulingType automatic, testo del post, media da https://media.getunclock.app/<nome> (alt text in italiano per le immagini), e la prima risposta come secondo elemento di metadata.twitter.thread. Non usare mai shareNow, addToQueue, shareNext o customScheduled.
6. Aggiorna la tabella Task di PROGETTO.md (riga 0a: settimana pronta, in attesa dell'ok di Pasquale). marketing/ non è in git: non committare i media. Committa e pusha su main solo i file tracciati che hai cambiato.
7. Resoconto finale in italiano, breve: il piano (giorni, orari, titoli), i media creati, le bozze su Buffer, cosa non è andato. Ricorda a Pasquale che le bozze vanno approvate e programmate da lui.

Se qualcosa blocca un passo (Pi non raggiungibile, Buffer non risponde, uno script fallisce), non improvvisare: fai il resto e scrivilo nel resoconto.
=====

Dopo averla creata, dimmi il nome della pianificata, quando parte la prima volta e come lanciarla a mano.
```

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
