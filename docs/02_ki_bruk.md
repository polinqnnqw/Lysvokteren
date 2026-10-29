# 🤖 Bruk av KI-verktøy — Lysvokteren

**Forfatter:** Polina Pashchenko

Læreren anbefalte å bruke KI i begrenset grad, først og fremst når man står fast. Jeg har fulgt dette rådet. Jeg har brukt **Microsoft Copilot** og **ChatGPT** som sparringpartnere i ca. 20-25 % av prosjektet. Jeg har ikke brukt KI til å generere ferdig spillkode, men heller til å forstå konsepter, finne feil og lære matematikk.

Her er en detaljert oversikt over hvordan jeg brukte KI, hvilke spørsmål jeg stilte, og hvordan jeg bearbeidet svarene.

---

## 💡 Eksempel 1: Feilsøking av grafikk (Additive Blending)

**Problemet mitt:** Skjermen ble fylt av en hvit, gjennomsiktig firkant når jeg prøvde å tegne lysstrålen og nordlyset.

**Prompt stilt til KI:** 
> *"Hvorfor blir grafikken min bare en stor hvit firkant når jeg bruker pygame.BLEND_RGBA_ADD for å tegne et lys?"*

**Svarene jeg fikk:** 
KI forklarte at `BLEND_RGBA_ADD` legger sammen både RGB-fargene og Alfa-kanalen. Når man legger sammen mange gjennomsiktige lag (som et nordlys eller en lysstråle), blir alpha-verdien til slutt 255 (helt hvit).

**Hvordan jeg bearbeidet og brukte svaret:** 
Jeg forsto *hvorfor* det skjedde, men KI ga meg ingen ferdig kode som passet mitt spill. Jeg gikk inn i koden min og endret strategi. Jeg sluttet å bruke `BLEND_RGBA_ADD` på store overflater. I stedet lagde jeg en egen `Surface` hvor jeg tegnet fargene med vanlig alfa-blending, og sendte den til skjermen. Jeg beholdt additiv blending kun for de små partiklene (eksplosjonene). **Læring:** Jeg lærte hvordan Pygame håndterer piksler og farger.

---

## 📐 Eksempel 2: Trigonometri og vinkler

**Problemet mitt:** Jeg trengte å sjekke om et skip var innenfor lysstrålen. Dette krevde vinkelmåling.

**Prompt stilt til KI:**
> *"Hvordan sjekker jeg om et punkt (x, y) er innenfor en vinkelsektor i Python? Jeg prøver å lage en lysstråle fra et fyrtårn."*

**Svarene jeg fikk:**
KI forklarte at jeg måtte bruke `math.atan2(dy, dx)` for å finne vinkelen fra fyrtårnet til skipet, og deretter sammenligne denne vinkelen med lysstrålens vinkel.

**Hvordan jeg bearbeidet og brukte svaret:**
KI sin kode fungerte greit, helt til vinkelen passerte 180 grader (overgangen fra pi til -pi). Da "hoppet" lyset over skjermen, og spillet krasjet. **Jeg forbedret koden** ved å skrive min egen funksjon `normalize_angle()` som sørget for at differansen mellom vinklene alltid var mellom -pi og pi. **Læring:** Jeg fikk en dyp forståelse for hvordan trigonometri og radianer fungerer i programmering.

---

## ⚙️ Eksempel 3: Installasjonsproblemer med Python 3.14

**Problemet mitt:** `pip install pygame` feilet med en stor rød feilmelding om at den manglet C++-kompilator.

**Prompt stilt til KI:**
> *"Pygame installeres ikke på Python 3.14. Jeg får 'Failed to build wheel'. Hva gjør jeg?"*

**Svarene jeg fikk:**
KI foreslo å installere Visual Studio Build Tools (noe som tar enormt mye plass), eller å bruke en annen versjon av Python.

**Hvordan jeg bearbeidet og brukte svaret:**
Jeg syntes ikke løsningen med kompilator var god nok, så jeg googlet videre og fant `pygame-ce` (Community Edition) som hadde ferdigbygde filer (wheels) for Python 3.14. Jeg brukte KI til å bekrefte at `pygame-ce` er en trygg erstatning, og at koden ville fungere likt. **Læring:** Jeg lærte at KI ikke alltid har den mest elegante løsningen, men det hjelper meg å forstå feilmeldingene slik at jeg kan finne bedre alternativer selv.

---

## 🤔 Hva jeg lærte av KI-hjelpen
- **KI er en sparringpartner, ikke en fasit:** KI tar ofte feil når det kommer til nyere Python-versjoner og spesifikke Pygame-funksjoner. 
- **Forståelse er nøkkelen:** Jeg måtte forstå *hvorfor* koden fungerte før jeg limte den inn, ellers ville jeg aldri klart å fikse det når det krasjet senere.
- **Læringseffekt:** KI hjalp meg mest med å forklare tung matematikk (som `atan2`), noe som sparte meg for mange timer med frustrasjon.