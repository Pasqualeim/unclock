# Le immagini dei post sul Raspberry Pi

Questo documento (uno dei flussi elencati in `AUTOMAZIONI.md`) spiega cosa è stato fatto il 29/10/2026 sul Raspberry Pi di casa, perché, e cosa controllare se un giorno smette di funzionare. La prima parte è a parole semplici; i dettagli tecnici sono in fondo.

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

1. Salva l'immagine o il video del post in `marketing/images/x/` o `marketing/video/x/`, con la data davanti al nome (es. `2026-10-28_niente_internet.png`).
2. Entro un'ora il Mac lo copia da solo sul Pi (vedi "Caricare i file").
3. Claude crea il post su Buffer con l'indirizzo `https://media.getunclock.app/<nome del file>`.
4. Buffer scarica il file e pubblica su X all'orario programmato.

## Caricare i file

Dal 29/10/2026 la copia è automatica. Ogni ora, e ogni volta che il Mac si accende, il Mac guarda le cartelle `marketing/images/x/` e `marketing/video/x/` e manda al Pi i file nuovi o cambiati (solo `.png`, `.jpg`, `.jpeg`, `.gif`, `.mp4`). Tutti i file finiscono nella stessa cartella `media`, senza sottocartelle.

- **Non cancella mai niente sul Pi.** Se togli un file dal Mac, sul Pi resta: può servire a un post già programmato su Buffer. Per toglierlo dal Pi va chiesto a Hermes.
- **Solo da casa.** SSH del Pi è raggiungibile solo dalla rete di casa (nessuna porta aperta sul router). Fuori casa la copia salta il giro senza errori e riprova l'ora dopo.
- **Due file con lo stesso nome** in immagini e video finirebbero uno sopra l'altro: la data e il nome diverso davanti lo evitano.

| Pezzo | Dove |
|---|---|
| Script | `tools/social/sync_media_pi.sh` (nel repo) |
| LaunchAgent (lo fa partire) | `~/Library/LaunchAgents/app.getunclock.syncmedia.plist` |
| Log | `~/Library/Logs/unclock-sync.log`: una riga quando copia qualcosa o quando il Pi non risponde; nessuna riga se non c'è niente di nuovo |
| Indirizzo del Pi in casa | `192.168.1.33` (`raspberrypi4.local`), utente `pasquale` |
| Accesso | chiave `~/.ssh/unclock_pi` (solo sul Mac), alias `unclock-pi` in `~/.ssh/config`: niente password |

La chiave sul Pi è limitata: in `~/.ssh/authorized_keys` del Pi la sua riga inizia con `command="/usr/bin/rrsync -wo /home/pasquale/media",restrict`. Con quella chiave si può solo scrivere dentro `media` con rsync: niente shell, niente lettura, niente altre cartelle. Per questo lo script usa `/` come destinazione (per `rrsync` è la cartella `media`). Copia della riga com'era prima: `~/.ssh/authorized_keys.bak-unclock` sul Pi.

Comandi (dal Terminale del Mac):

```bash
bash ~/Documents/Developer/NotificationBlocker/tools/social/sync_media_pi.sh
```

lancia la copia subito, senza aspettare l'ora.

```bash
launchctl bootout gui/$(id -u)/app.getunclock.syncmedia
```

la ferma (fino a quando non la riattivi);

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/app.getunclock.syncmedia.plist
```

la riattiva.

```bash
tail ~/Library/Logs/unclock-sync.log
```

mostra le ultime righe del log.

Se l'IP del Pi cambia (lo assegna il router), il log dirà "Pi non raggiungibile" anche a casa: aggiorna `HostName` nel blocco `unclock-pi` di `~/.ssh/config`. Per evitarlo, prenota l'indirizzo `192.168.1.33` per il Pi nelle impostazioni DHCP del router Vodafone.

### Verificare che la copia funzioni

1. Metti un'immagine qualsiasi in `marketing/images/x/`, per esempio `2026-10-29_prova.png`.
2. Lancia la copia a mano (comando sopra), oppure aspetta al massimo un'ora.
3. Apri `https://media.getunclock.app/2026-10-29_prova.png` dal telefono in 4G: deve comparire l'immagine.
4. In `~/Library/Logs/unclock-sync.log` deve esserci la riga "copiati 1 file".
5. Il file di prova resta sul Pi (la copia non cancella): per toglierlo, chiedi a Hermes (comandi sotto).

Da Terminale, la stessa prova: `curl -s -o /dev/null -w "%{http_code}\n" https://media.getunclock.app/<nome>` deve dare `200`; con l'indirizzo senza nome di file deve dare `404`.

### Problemi della copia automatica

| Cosa vedi | Cosa vuol dire | Cosa fare |
|---|---|---|
| Nel log "Pi non raggiungibile" mentre sei a casa | Pi spento, o il suo IP è cambiato | Controlla che il Pi sia acceso; trova l'IP nuovo (app del router, o `arp -a` dal Mac: cerca `raspberrypi4`) e aggiornalo in `~/.ssh/config`; poi prenota l'IP sul router |
| Nel log "errore rsync: ... Permission denied (publickey)" | La chiave sul Pi è stata tolta o cambiata | Reinstallala dal Mac: `ssh-copy-id -i ~/.ssh/unclock_pi.pub -o PubkeyAuthentication=no -o PreferredAuthentications=password pasquale@192.168.1.33` (chiede la password del Pi), poi chiedi a Hermes di rimettere la limitazione (comandi sotto) |
| `ssh-copy-id` chiede la password e poi "Connection closed" | Il Mac prova prima le altre chiavi e il Pi chiude dopo troppi tentativi | Usa il comando della riga sopra: le due opzioni `-o` fanno provare solo la password (è successo il 29/10) |
| Nel log "errore rsync: ... rrsync" o "not allowed" | La riga della chiave sul Pi ha un percorso diverso da `/home/pasquale/media` | Chiedi a Hermes di mostrarti la riga e rimetterla come scritto sopra |
| Nessuna riga nel log da giorni, anche dopo file nuovi | Il LaunchAgent non gira | `launchctl print gui/$(id -u)/app.getunclock.syncmedia` deve rispondere; se dice "not found", riattivalo con il comando `bootstrap` sopra |
| Nel log "Operation not permitted" | macOS ha negato a `bash` la lettura di `Documents` (il 29/10 non succedeva) | Impostazioni di Sistema → Privacy e sicurezza → Accesso completo al disco → aggiungi `/bin/bash` |
| Il file c'è sul Pi ma l'indirizzo dà "Forbidden" | Permessi del file sbagliati | Chiedi a Hermes il `chmod 644` (sotto); la copia mette già 644, quindi succede solo a file messi a mano |

Nota: anche `x_banner_it.png` (il banner del profilo X) finisce sul Pi, perché è un `.png` in `images/x/`. È un'immagine già pubblica, va bene così.

### Comandi da dare a Hermes

Hermes lavora sul Pi; questi comandi si possono incollare a lui così come sono. Nessuno tocca Caddy o cloudflared.

Vedere cosa c'è nella cartella pubblica:

```
ls -la /home/pasquale/media
```

Togliere un file dalla cartella pubblica (solo se nessun post programmato su Buffer lo usa):

```
rm /home/pasquale/media/<nome del file>
```

Sistemare i permessi di tutti i file (errore "Forbidden"):

```
chmod 644 /home/pasquale/media/*
```

Vedere la riga della chiave del Mac (deve iniziare con `command="/usr/bin/rrsync -wo /home/pasquale/media",restrict` e finire con `unclock-sync@mac`):

```
grep unclock-sync@mac ~/.ssh/authorized_keys
```

Rimettere la limitazione alla chiave del Mac (dopo una reinstallazione con `ssh-copy-id`):

```
sed -i '/unclock-sync@mac$/{/^command=/!s|^ssh-ed25519|command="/usr/bin/rrsync -wo /home/pasquale/media",restrict ssh-ed25519|}' ~/.ssh/authorized_keys
```

Togliere del tutto l'accesso del Mac (la copia automatica si ferma, il sito dei media resta su):

```
sed -i '/unclock-sync@mac$/d' ~/.ssh/authorized_keys
```

Tornare alla copia di `authorized_keys` com'era prima della limitazione (il 29/10):

```
cp ~/.ssh/authorized_keys.bak-unclock ~/.ssh/authorized_keys
```

Controllare che `rrsync` esista (serve alla limitazione):

```
command -v rrsync    # /usr/bin/rrsync, dal pacchetto rsync
```

## Spostare i media sull'hard disk del Pi

Deciso il 30/10/2026, per non riempire la scheda SD dove gira il sistema del Pi: l'HD collegato al Pi ospita **solo i media dei post** (i contenuti generati per i post) (niente backup, niente file privati: tutto quello che c'è nella cartella è pubblico). L'idea: l'HD prende il posto della cartella, il percorso `/home/pasquale/media` resta uguale. Così Caddy, il tunnel, la chiave limitata del Mac e la copia automatica non cambiano.

Come resta il Pi se l'HD è staccato: si accende lo stesso (`nofail`); `/home/pasquale/media` è una cartella vuota sulla SD, i link dei post danno "non trovato" finché l'HD non torna. La copia vecchia sulla SD resta in `/home/pasquale/media.sd-backup` finché la prova non è andata bene.

### Istruzioni da incollare a Hermes

L'HD è un Toshiba EXT da 932 GiB in **FAT32** (UUID `6747-1E19`), già pieno al 73% di file di Pasquale: **non si formatta** (decisione del 30/10). FAT32 non ha i permessi di Linux, quindi proprietario e permessi si danno al montaggio (`uid`, `gid`, `umask`; `quiet` fa passare senza errore il `chmod` della copia dal Mac). Limite: un file al massimo 4 GB (i video dei post sono molto più piccoli). I media vanno in una sola sottocartella, `unclock-media`: è l'unica parte dell'HD visibile da internet, il resto resta privato.

```
Devo spostare la cartella pubblica /home/pasquale/media sull'hard disk Toshiba EXT (sda1, FAT32, UUID 6747-1E19), senza cambiare il suo percorso. NON formattare l'HD e non toccare i file che ci sono già. Caddy (/etc/caddy/Caddyfile), cloudflared e ~/.ssh/authorized_keys NON vanno toccati.

1. Dimmi se qualcosa usa già il percorso "/media/pasquale/TOSHIBA EXT" (script, servizi, collegamenti): dopo questo lavoro l'HD si troverà in /mnt/unclock-hd. Se qualcosa lo usa, FERMATI e chiedimi.
2. Smonta il montaggio automatico: `udisksctl unmount -b /dev/sda1`.
   Crea /mnt/unclock-hd e aggiungi a /etc/fstab (prima una copia: /etc/fstab.bak-unclock), con uid e gid presi da `id -u pasquale` e `id -g pasquale`:
   UUID=6747-1E19  /mnt/unclock-hd  vfat  defaults,nofail,x-systemd.device-timeout=10s,uid=<uid>,gid=<gid>,umask=022,quiet,utf8  0  0
   Poi `sudo systemctl daemon-reload && sudo mount -a` e controlla con `findmnt /mnt/unclock-hd` e `ls /mnt/unclock-hd` (devono comparire i file di prima).
3. mkdir /mnt/unclock-hd/unclock-media
   cp -r --preserve=timestamps /home/pasquale/media/. /mnt/unclock-hd/unclock-media/
   Confronta: `ls /home/pasquale/media | wc -l` e `ls /mnt/unclock-hd/unclock-media | wc -l` devono dare lo stesso numero.
4. mv /home/pasquale/media /home/pasquale/media.sd-backup && mkdir /home/pasquale/media && chmod 755 /home/pasquale/media
   Aggiungi a /etc/fstab:
   /mnt/unclock-hd/unclock-media  /home/pasquale/media  none  bind,nofail,x-systemd.requires-mount-for=/mnt/unclock-hd  0  0
   Poi `sudo systemctl daemon-reload && sudo mount -a` e controlla con `findmnt /home/pasquale/media` e `ls -la /home/pasquale/media` (proprietario pasquale, file leggibili da tutti).
5. Prova: `curl -s https://media.getunclock.app/prova.txt` deve rispondere "ok"; `curl -sI https://media.getunclock.app/<un'immagine che c'è>` deve dare 200.
6. Riavvia il Pi (`sudo reboot`) e, quando è su, rifai i controlli dei punti 4 e 5.
7. Dimmi l'esito di ogni punto. Non cancellare /home/pasquale/media.sd-backup: lo tolgo io dopo qualche giorno.
```

Dopo la prova: un file nuovo da `marketing/images/x/` deve arrivare sull'HD entro un'ora (vedi "Verificare che la copia funzioni"); poi si toglie `media.sd-backup` chiedendolo a Hermes (`rm -r /home/pasquale/media.sd-backup`).

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
- 29/10/2026: copia automatica dal Mac attiva e provata (immagine e video rispondono 200, la radice 404).
- Da fare: spostare i media sull'HD del Pi (istruzioni per Hermes in "Spostare i media sull'hard disk del Pi").
- Da fare: riavviare il Pi e rifare la prova di `prova.txt` (verifica dell'accensione automatica); prenotare l'IP del Pi sul router.

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
