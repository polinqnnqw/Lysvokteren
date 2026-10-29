# 📅 Prosess-logg og Arbeidsflyt — Lysvokteren

**Forfatter:** Polina Pashchenko
**Verktøy:** Python 3.14, Pygame-CE, NumPy
**Arbeidsform:** Individuelt, 3 økter (onsdager) på 4,5 timer hver.

I dette dokumentet beskriver jeg hele reisen min fra idé til ferdig spill, og hvordan jeg jobbet gjennom de tre øktene for å løse problemer og forbedre spillet.

---

## 🟢 Onsdag 14. oktober (4,5 timer) — Planlegging og det store installasjonsmarerittet

**Hva jeg gjorde:**
Denne dagen gikk med til idémyldring og oppsett. Jeg brukte god tid på å finne et konsept som føltes unikt. Inspirert av atmosfæriske spill som *Journey* og *Limbo* landet jeg på "Lysvokteren" — et spill hvor du ikke styrer en karakter, men selve lysstrålen. Jeg skrev en detaljert spillplan som ble godkjent av læreren i økt 2.

**Utfordringer og forbedringer:**
Det første store hinderet var teknisk. Da jeg skulle installere `pygame`, krasjet alt. Jeg fant ut at den vanlige `pygame`-pakken ikke støttet min Python-versjon (3.14) og prøvde å bygge seg selv, noe som feilet fordi jeg manglet C++-kompilator. 
Jeg måtte tenke kreativt. Løsningen ble å bytte til **Pygame-CE** (Community Edition), som er en mer oppdatert versjon. Jeg måtte også lære meg å bruke `python -m pip install` i stedet for bare `pip` for å sikre at pakkene ble installert i riktig Python-miljø. Dette lærte meg utrolig mye om hvordan virtuelle miljøer og avhengigheter fungerer i Python.

---

## 🟡 Onsdag 21. oktober (4,5 timer) — Kodekrig, grafikk og store feil

**Hva jeg gjorde:**
Nå startet den harde programmeringen. Jeg bygde spill-løkken (game loop), lagde startskjerm og begynte på skip og lys. Jeg delte koden opp i moduler (`ship.py`, `lighthouse.py`, `game.py` osv.) for å holde oversikten.

**Utfordringer og forbedringer:**
Her møtte jeg veggen skikkelig. Den første versjonen av lysstrålen og nordlyset ble en gigantisk, stygg hvit firkant som ødela hele skjermen. Jeg satt fast i flere timer.
Jeg brukte KI for å forstå problemet, og fant ut at feilen lå i noe som heter **Additive Blending** (`BLEND_RGBA_ADD`). Når jeg la sammen farger og alpha-kanaler, ble alt gjennomsiktig hvitt. 
**Forbedringen:** Jeg skrev om hele grafikk-koden. Jeg lærte at jeg måtte "pre-rendre" overflatene mine (Surfaces) med vanlig alfa-blending, og kun bruke additiv blending på bittesmå partikler. Jeg fikset også en matematisk feil med vinkler ved å skrive min egen `normalize_angle()`-funksjon, slik at lysstrålen ikke "hoppet" når den passerte 180 grader.

---

## 🔴 Onsdag 28. oktober (4,5 timer) — Polering, dybde og spillbalanse

**Hva jeg gjorde:**
Nå skulle spillet bli skikkelig kult. Jeg brukte denne økten på å legge til det siste visuelle og finpusse mekanikken.

**Utfordringer og forbedringer:**
- **Dybde-perspektiv:** I starten beveget skipene seg bare rett sidelengs som i Space Invaders. Jeg ville at de skulle seile i et ekte hav. Jeg introduserte en Z-akse (dybde). Jeg lagde en `scale`-egenskap slik at skip som var langt bak ble mindre, og skip som kom mot meg ble større. Dette krevde mye testing for å få fartsfølelsen riktig.
- **Spillbalanse (Oljen):** I den opprinnelige koden minket oljen konstant, uansett om lyset var på eller av. Etter å ha testet spillet selv, innså jeg at dette var kjedelig og stressende. **Jeg forbedret dette** ved å programmere det slik at oljen *kun* minker når lyset faktisk er på. Dette tvang spilleren til å ta taktiske valg (skru av lyset for å spare olje, men risikere å miste venner).
- **Dokumentasjon:** Til slutt skrev jeg denne dokumentasjonen, ryddet i koden og lastet alt opp til GitHub.

---

## 🎓 Hva jeg sitter igjen med
Gjennom disse tre øktene lærte jeg at spillutvikling er 20% koding og 80% feilsøking. Jeg lærte hvordan vektormatematikk og trigonometri faktisk brukes i praksis, og at små visuelle detaljer (som partikler og skjermristing) er det som gjør et spill morsomt å spille.