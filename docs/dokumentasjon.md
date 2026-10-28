# 📄 Dokumentasjon — Lysvokteren

**Prosjekt:** Lag ditt eget spill
**Verktøy:** Python 3.14, Pygame-CE, NumPy
**Forfatter:** Polina Pashchenko
**Dato:** 28.10.26

---

## 1. Idé og planlegging

Målet mitt var å lage et spill som føltes rolig, men krevende — inspirert av atmosfæriske spill som *Journey* og *Limbo*. I stedet for å styre en karakter, ville jeg styre selve lyset. Dette gir en unik spillmekanikk som passer perfekt til den mørke, norske fjord-settingen.

**Spillplan (godkjent av lærer i økt 2):**
- **Målgruppe:** 12–25 år, spillere som liker stemningsfulle og taktiske spill.
- **Mål i spillet:** Overlev så lenge som mulig ved å skille vennlige skip (grønne) fra fiendtlige skip (røde).
- **Mekanikker:** Roterende lysstråle (styres med mus), olje-ressurs, livssystem (3 liv), poengsystem og progressiv vanskelighetsgrad.
- **Visuelt:** Mørk bakgrunn, bi turquoise farger (Tiffany & Svart-estetikk), nordlys, stjerner og et simulert dybde-perspektiv på skipene.

## 2. Valg av verktøy

Jeg valgte **Python** med **Pygame-CE** fordi det gir full kontroll over 2D-grafikk og spill-løkker. 
- **Pygame-CE:** Jeg måtte bytte fra vanlig `pygame` til `pygame-ce` (Community Edition) fordi standardversjonen ikke hadde støtte for Python 3.14. Dette løste installasjonsproblemene.
- **NumPy:** Brukt for å syntetisere lyd i sanntid. Dette gjorde at jeg slapp å laste ned eksterne lydfiler.
- **VS Code:** Brukt som kodeeditor med integrert terminal.

## 3. Utviklingsprosess og utfordringer
![alt text](<Skjermbilde 2026-10-28 110147.png>)
<video controls src="20261028-1012-24.5871614.mp4" title=""></video>



Underveis støtte jeg på flere tekniske utfordringer som jeg måtte løse:

1. **Installasjonsproblemer:** Vanlig `pygame` ville ikke bygge på min versjon av Python. Løsningen var å bruke `pip install pygame-ce` og endre importene. Dette lærte meg mye om hvordan Python-pakker og avhengigheter fungerer.
2. **Grafiske bugs (Additive Blending):** Den første versjonen av lysstrålen og nordlyset ble en stor, stygg hvit flekk. Dette skjedde fordi `BLEND_RGBA_ADD` oppførte seg annerledes enn forventet i Pygame. Jeg løste dette ved å pre-rendre overflater (Surfaces) med vanlig alfa-blending, og heller bruke additiv blending kun på små partikler.
3. **Dybde-perspektiv:** For at skipene skulle se ut som de seilte i et hav (og ikke bare sidelengs), innførte jeg en Z-akse. Jeg lagde en `scale`-egenskap basert på Z, slik at skipene lenger bak ble mindre.
4. **Spillbalanse:** I starten minket oljen konstant. Etter testing fant jeg ut at det var morsommere og mer rettferdig om oljen *kun* minker når lyset faktisk er på. Dette tvang spilleren til å ta taktiske valg.

## 4. Hva jeg lærte

- **Teknisk:** Hvordan man bygger en robust spill-løkke med delta-tid, vektormatematikk for å sjekke vinkler (`math.atan2`), og hvordan man genererer sinus-bølger med NumPy for lydeffekter.
- **Struktur:** Viktigheten av modulær kode. Ved å dele spillet inn i `ship.py`, `world.py`, `game.py`, osv., ble det mye lettere å feilsøke.
- **Prosess:** At god "game feel" (spillfølelse) kommer fra små detaljer som skjermristing (screenshake), partikler og lydrespons.

## 5. Bruk av KI

Jeg har brukt **Microsoft Copilot** og **ChatGPT** som sparringpartnere, hovedsakelig ved feilsøking og idéutvikling. Jeg har ikke brukt KI til å generere hele spillet, men heller til å forstå konsepter.

### Konkrete eksempler:

**Eksempel 1: Feilsøking av vinkler**
- **Prompt:** *"Hvordan sjekker jeg om et punkt (x, y) er innenfor en vinkelsektor i Python? Jeg prøver å lage en lysstråle."*
- **Svar:** KI forklarte at jeg måtte bruke `math.atan2(dy, dx)` for å finne vinkelen til punktet, og deretter sammenligne den med strålens vinkel.
- **Bearbeidelse:** KI sin kode sjekket ikke hva som skjedde når vinkelen passerte 180 grader (overgangen fra pi til -pi). Jeg måtte derfor skrive min egen hjelpefunksjon `normalize_angle()` for å sørge for at differansen alltid var mellom -pi og pi. Dette lærte jeg mye av.

**Eksempel 2: Feilsøking av grafikk**
- **Prompt:** *"Hvorfor blir grafikken min bare en stor hvit firkant når jeg bruker pygame.BLEND_RGBA_ADD?"*
- **Svar:** KI forklarte at additive blending legger sammen fargeverdiene, og at alfakanalen også blir lagt sammen, noe som fører til at alt blir gjennomsiktig hvitt.
- **Bearbeidelse:** Jeg brukte svaret til å isolere problemet. Jeg endret koden slik at bare de små partiklene bruker additiv blending, mens de store overflatene (som nordlyset) bruker vanlig alfa-blending. KI ga meg forståelsen, men jeg skrev koden selv.

**Refleksjon rundt KI-bruk:**
KI var utrolig nyttig for å forstå matematikken bak vinkler, men den tok ofte feil når det gjaldt spesifikke Pygame-funksjoner. Jeg lærte at man aldri må stole blindt på KI-kode, men alltid teste og forstå den selv før man bruker den.

## 6. Ressurser

- **Pygame Documentation:** https://www.pygame.org/docs/
- **Pygame-CE (Community Edition):** https://pyga.me/
- **NumPy Documentation:** https://numpy.org/doc/
- **Elevkanalen (Spillutvikling):** https://www.elevkanalen.no/fag/1002/produkt/2057/
- **MDN Web Docs (Trigonometri og atan2):** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/atan2
- **Inspirasjon:** Spillene *Journey* (Thatgamecompany) og *Return of the Obra Dinn* (Lucas Pope).

## 7. Egenvurdering

**Hvor fornøyd er du med resultatet?**
Jeg er veldig fornøyd (9/10). Spillet ser bra ut, lyden fungerer, og mekanikken med at oljen bare minker når lyset er på, gjør spillet taktisk og morsomt.

**Hva fungerer godt?**
- Den modulære koden gjør det lett å justere vanskelighetsgraden i `settings.py`.
- Overgangen til dybde-perspektiv (Z-akse) for skipene gjorde spillet mye mer levende.
- Lydsyntesen med NumPy fungerer feilfritt uten eksterne filer.

**Hva kunne vært bedre?**
- Ytelsen kunne vært bedre. Bakgrunnen tegnes på nytt hver frame, noe som kan bli tungt på svake PC-er.
- Jeg rakk ikke å lage en pause-meny.
- Fiendtlige skip kunne hatt flere varianter (f.eks. ulike størrelser).

**Hva ville du utviklet videre dersom du hadde mer tid?**
- En high-score-tavle som lagres i en database.
- Flere nivåer med en historie og en sluttsekvens.
- En mobilversjon tilpasset berøringsskjerm.

**Hvordan jobbet du når du møtte utfordringer?**
Jeg leste feilmeldingene nøye, isolerte problemet i små testfiler, og brukte KI til å forklare konseptene jeg satt fast på. Jeg ga meg ikke før jeg forsto *hvorfor* koden fungerte.

**Brukte du KI? I så fall hvordan, og hvor nyttig var det?**
Ja, som en sparringpartner. Det var veldig nyttig for å forstå matematikk og feilsøking, men jeg måtte bearbeide svarene mye selv for at de skulle passe mitt spill.