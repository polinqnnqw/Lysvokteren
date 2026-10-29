# 🧠 Egenvurdering — Lysvokteren

**Forfatter:** Polina Pashchenko

Jeg har jobbet med Lysvokteren over tre intensiver økter. Her er min ærlige refleksjon over resultatet, hva som fungerer, og hva jeg kunne gjort annerledes.

---

## 🎯 Hvor fornøyd er du med resultatet?
Jeg er veldig fornøyd og gir meg selv **9 av 10**. Jeg startet med en visjon om å lage noe annet enn en standard plattformspiller, og jeg føler at jeg har klart å skape et atmosfærisk spill med en unik sjel. Spillet ser bra ut, lyden fungerer utmerket (uten eksterne lydfiler!), og mekanikken med at oljen bare minker når lyset er på, gjør spillet overraskende taktisk og morsomt.

## ✅ Hva fungerer godt?
1. **Modulær kode:** Å dele spillet inn i filer som `ship.py`, `world.py` og `settings.py` var et genialt trekk. Det gjorde det utrolig lett å justere vanskelighetsgraden og fargene underveis uten å rote til hele koden.
2. **Dybde-perspektivet:** Da jeg innførte Z-aksen og fikk skipene til å bli mindre jo lenger bak de var, føltes spillet plutselig mye mer levende. Det ser ikke lenger ut som en flat 2D-skjerm, men som et ekte hav.
3. **Lydsyntese (NumPy):** Jeg er veldig stolt over at all lyden genereres i sanntid. Å slippe å laste ned filer og heller bruke sinusbølger i Python føles veldig profesjonelt.
4. **Olje-mekanikken:** Å skru lyset av og på for å spare olje, men samtidig risikere å miste grønne skip, er en veldig god spillmekanikk som jeg er stolt av å ha kommet på.

## ⚠️ Hva kunne vært bedre?
1. **Ytelse (FPS):** Bakgrunnen (nordlys, stjerner, fjell) tegnes på nytt hver eneste frame (60 ganger i sekundet). På en svak PC kan dette bli tungt. Med mer tid ville jeg "cachet" bakgrunnen slik at den bare tegnes én gang.
2. **Manglende meny:** Jeg rakk ikke å lage en pause-meny (Pause-skjerm) eller en innstillingsmeny. Akkurat nå må man trykke ESC for å lukke spillet helt.
3. **Fiendtlige skip:** Alle de røde skipene ser helt like ut. Det kunne vært morsomt med ulike varianter (f.eks. raske jegere eller store, trege krigsskip).

## 🚀 Hva ville du utviklet videre dersom du hadde mer tid?
- **Database for High Score:** I dag lagres high score i en enkel tekstfil. Jeg ville brukt SQLite for å lage en skikkelig database.
- **Historiedrevet kampanje:** I stedet for et endeløst spill, kunne jeg laget 10 nivåer med en fortelling og en sluttsekvens.
- **Mobilversjon:** Spillet ville passet perfekt på en iPad eller telefon med touch-kontroller. Jeg har lest om verktøyet BeeWare, som kan pakke Python-spill til iOS/Android, og det frister å prøve det.

## 🧗 Hvordan jobbet du når du møtte utfordringer?
Jeg møtte mange utfordringer, spesielt med vinkler og grafikk. Min strategi var:
1. **Les feilmeldingen nøye:** 90% av svaret står faktisk i den røde teksten i terminalen.
2. **Isoler problemet:** Hvis noe krasjet, lagde jeg en liten testfil for å se om jeg kunne få akkurat den tingen til å fungere alene.
3. **Bruk KI smart:** Jeg spurte om *hvorfor* noe skjedde, ikke bare *hvordan* jeg skulle fikse det. 
4. **Gi aldri opp:** Jeg satt fast i flere timer med den hvite firkanten, men ved å google, spørre KI og endre koden steg for steg, klarte jeg det til slutt.

## 🤖 Brukte du KI? Hvor nyttig var det?
Ja, jeg brukte KI (Copilot og ChatGPT). Det var veldig nyttig for å forstå trigonometri (vinkler) og for å finne ut hvorfor Python ikke ville installere Pygame. Men det var også utfordrende, fordi KI ofte ga meg kode som var utdatert eller som ikke fungerte i min versjon av Pygame. Jeg lærte at man aldri må kopiere kode blindt, men alltid lese den og forstå den selv først. KI er et hjelpemiddel, ikke en erstatning for egen tenking!