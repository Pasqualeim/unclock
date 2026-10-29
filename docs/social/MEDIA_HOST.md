# Le immagini dei post sul Raspberry Pi

Questo documento spiega cosa è stato fatto il 29/10/2026 sul Raspberry Pi di casa, perché, e cosa controllare se un giorno smette di funzionare. La prima parte è a parole semplici; i dettagli tecnici sono in fondo.

## Il problema da risolvere

Buffer pubblica i post su X da solo, all'orario scelto. Per allegare un'immagine o un video, però, Buffer non accetta un file che sta sul Mac: vuole un **indirizzo internet** da cui scaricarlo, come `https://qualcosa/immagine.png`.

Serviva quindi un posto, raggiungibile da internet, dove mettere le immagini e i video dei post. Si è scelto il Raspberry Pi, che è già acceso in casa.

## L'idea, in una frase

Una cartella del Raspberry Pi è diventata visibile su internet all'indirizzo **https://media.getunclock.app/**: un file messo lì dentro si apre da qualsiasi parte del mondo aggiungendo il suo nome all'indirizzo.

Esempio: il file `niente_internet.png` nella cartella diventa `https://media.getunclock.app/niente_internet.png`. Quell'indirizzo è quello che si dà a Buffer.

## Cosa è stato fatto, passo per passo

Il lavoro l'ha fatto Hermes (l'agent che gira sul Pi), seguendo le istruzioni preparate in Cowork. Hermes non sa niente di Unclock e non gli serve: ha solo preparato il Pi.

1. **La cartella.** Sul Pi c'è ora la cartella `/home/pasquale/media`. È l'unica cosa del Pi che si vede da fuori: il resto del Pi (i tuoi file, Hermes, le impostazioni) resta privato.

2. **Il "distributore" dei file (Caddy).** È un piccolo programma che, quando qualcuno chiede un file, lo prende dalla cartella e lo consegna. È impostato in modo prudente:
   - consegna solo file che esistono e solo se si conosce il nome esatto;
   - non mostra mai l'elenco di cosa c'è nella cartella;
   - non permette di caricare, modificare o cancellare niente da fuori;
   - risponde solo dall'interno del Pi stesso: da solo non è raggiungibile né da internet né dagli altri apparecchi di casa.

3. **Il "corridoio" verso internet (tunnel Cloudflare).** Di solito, per rendere visibile un computer di casa, bisogna aprire una porta sul router: è scomodo e meno sicuro. Qui si è fatto il contrario: un programma sul Pi (`cloudflared`) apre **lui** un collegamento verso Cloudflare e lo tiene aperto. Quando qualcuno chiede un file a `media.getunclock.app`, Cloudflare passa la richiesta lungo quel collegamento, il Pi risponde dalla cartella, Cloudflare consegna il file. Risultato:
   - il router non è stato toccato, nessuna porta aperta;
   - chi scarica un file non vede l'indirizzo di casa tua, vede solo Cloudflare;
   - funziona anche se il tuo indirizzo internet di casa cambia.

4. **Il nome (`media.getunclock.app`).** Il dominio getunclock.app è già su Cloudflare (lo usa il sito). È stato aggiunto solo il "sotto-nome" `media`, che punta al corridoio del Pi. Il sito, la mail e il resto del dominio non sono stati toccati.

5. **Accensione automatica.** Il distributore e il corridoio partono da soli quando il Pi si accende: dopo un riavvio o un calo di corrente non serve fare niente.

6. **Le prove.** Fatte dal Pi e da fuori casa:
   - il file di prova `prova.txt` si apre e dice "ok";
   - l'indirizzo della cartella senza nome di file dà "non trovato", quindi l'elenco dei file non si vede;
   - un file che non esiste dà "non trovato".

### Il primo tentativo non andava

Al primo giro il file di prova arrivava vuoto. Era un errore nelle istruzioni preparate in Cowork, non del Pi né di Hermes: il distributore era impostato per rispondere solo a chi lo chiamava con il nome "interno" del Pi, mentre le richieste da internet arrivano con il nome `media.getunclock.app`. Davanti a un nome che non riconosceva rispondeva "ok, ecco a te" ma senza niente dentro. Cambiata una riga (vedi "Dettagli tecnici"), ha funzionato.

## Come si usa

1. Metti l'immagine o il video del post nella cartella `media` del Pi, con lo stesso nome che ha nel progetto (es. `2026-10-28_niente_internet.png`).
2. Claude crea il post su Buffer con l'indirizzo `https://media.getunclock.app/<nome del file>`.
3. Buffer scarica il file e pubblica su X all'orario programmato.

Il modo di fare il punto 1 è ancora **da decidere**: la shell che Claude usa sul Mac non riesce a raggiungere né il Pi né `media.getunclock.app` (la sua connessione passa da una lista di siti consentiti), quindi non può copiare i file da sola. Opzioni: li copi tu dal Mac (Finder o un comando pronto), oppure Hermes li scarica da un link.

## Regole

- **Nella cartella solo i media dei post.** Chi conosce il nome esatto di un file lo può aprire. Niente file privati, niente schermate con notifiche vere: solo dati di prova, come nei post.
- **Tieni il Pi acceso** finché i post programmati non sono usciti: non è ancora verificato se Buffer si salva una copia del file subito o lo riscarica all'ora di pubblicazione.
- Il sotto-nome `media` non raccoglie dati di nessuno: l'informativa privacy del sito non cambia.

## Se smette di funzionare

Prima prova: apri dal telefono, in 4G e non col Wi-Fi di casa, `https://media.getunclock.app/prova.txt`. Deve comparire "ok".

| Cosa vedi | Cosa vuol dire | Cosa fare |
|---|---|---|
| Pagina di errore di Cloudflare (1033 o 530) | Il corridoio è spento: Pi spento, senza internet, o `cloudflared` fermo | Controlla che il Pi sia acceso e online; poi chiedi a Hermes di riavviare `cloudflared` |
| Pagina bianca, nessun errore | Il distributore risponde a vuoto (è l'errore del primo tentativo) | Chiedi a Hermes di rimettere il Caddyfile scritto qui sotto e ricaricare Caddy |
| "Not found" su un file che hai messo | Nome diverso (maiuscole, estensione) o file nella cartella sbagliata | Controlla il nome esatto del file dentro `/home/pasquale/media` |
| "Forbidden" | Il file non è leggibile | Chiedi a Hermes di dare al file i permessi 644 |
| Buffer rifiuta il media | Indirizzo non raggiungibile o formato | Prova l'indirizzo in 4G; usa PNG/JPG per le immagini, MP4 per i video |

Puoi passare questa tabella e i "Dettagli tecnici" a Hermes o a Claude: c'è tutto quello che serve per capire e riparare.

## Stato

- 29/10/2026: configurato e provato, funziona.
- Da fare: riavviare il Pi e rifare la prova di `prova.txt` (verifica dell'accensione automatica); farsi dire da Hermes l'indirizzo del Pi nella rete di casa e se SSH è attivo solo in casa; decidere come si caricano i file.

---

## Dettagli tecnici

| Pezzo | Valore |
|---|---|
| Cartella pubblica | `/home/pasquale/media` (utente `pasquale`) |
| Distributore | Caddy, configurazione in `/etc/caddy/Caddyfile`, ascolta solo su `127.0.0.1:8080` |
| Corridoio | cloudflared 2026.10.6 (repo ufficiale Cloudflare), tunnel `unclock-media`, UUID `1481ffda-ac84-486b-87a0-78313bca8176` |
| Configurazione del corridoio | `/etc/cloudflared/config.yml` |
| Chiave del corridoio | `/etc/cloudflared/1481ffda-ac84-486b-87a0-78313bca8176.json`: è segreta, resta sul Pi, non va mai copiata altrove |
| Nome | record CNAME `media` → tunnel, zona `getunclock.app` su Cloudflare |
| Avvio automatico | servizi systemd `caddy` e `cloudflared` |

`/etc/caddy/Caddyfile`:

```
http://:8080 {
    bind 127.0.0.1
    root * /home/pasquale/media
    file_server
}
```

La riga che ha risolto l'errore è la prima: `http://:8080` accetta qualunque nome; la versione sbagliata era `http://127.0.0.1:8080`. `bind 127.0.0.1` lo rende raggiungibile solo dal Pi stesso; l'assenza di `browse` toglie l'elenco dei file.

`/etc/cloudflared/config.yml`:

```
tunnel: 1481ffda-ac84-486b-87a0-78313bca8176
credentials-file: /etc/cloudflared/1481ffda-ac84-486b-87a0-78313bca8176.json
ingress:
  - hostname: media.getunclock.app
    service: http://127.0.0.1:8080
  - service: http_status:404
```

Comandi di controllo sul Pi:

```
systemctl status caddy cloudflared       # entrambi "active"
sudo ss -ltnp | grep 8080                # solo 127.0.0.1:8080
curl -s http://127.0.0.1:8080/prova.txt  # "ok": se questo va e l'indirizzo pubblico no, il guasto è nel corridoio
journalctl -u cloudflared -n 50          # ultimi messaggi del corridoio
```

Da fuori casa:

```
curl -s https://media.getunclock.app/prova.txt                                       # ok
curl -s -o /dev/null -w "%{http_code}\n" https://media.getunclock.app/                # 404
curl -s -o /dev/null -w "%{http_code}\n" https://media.getunclock.app/nonesiste.png   # 404
```
