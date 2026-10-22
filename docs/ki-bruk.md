# Bruk av KI-verktøy

Jeg har brukt Microsoft Copilot og ChatGPT som sparringpartnere underveis, spesielt ved feilsøking og idéutvikling. Jeg har ikke brukt KI til å generere hele spillet, men heller til å forstå konsepter.

## Eksempel 1: Feilsøking av vinkler
**Prompt:** "Hvordan sjekker jeg om et punkt (x, y) er innenfor en vinkelsektor i Python? Jeg prøver å lage en lysstråle."
**Svar:** KI forklarte at jeg måtte bruke `math.atan2(dy, dx)` for å finne vinkelen til punktet, og deretter sammenligne den med strålens vinkel.
**Bearbeidelse:** KI sin kode sjekket ikke hva som skjedde når vinkelen passerte 180 grader (overgangen fra pi til -pi). Jeg måtte derfor skrive min egen hjelpefunksjon `normalize_angle()` for å sørge for at differansen alltid var mellom -pi og pi. Dette lærte jeg mye av.

## Eksempel 2: Idéutvikling
**Prompt:** "Jeg vil lage et atmosfærisk spill i Python. Har du forslag til mekanikker som ikke er for kompliserte å kode, men som føles unike?"
**Svar:** KI foreslo en rekke mekanikker, blant annet "lyskontroll".
**Bearbeidelse:** Jeg tok idéen om lyskontroll og utviklet den videre selv til konseptet "Lysvokteren", hvor man må balansere lys og mørke, samt administrere en olje-ressurs.

## Refleksjon rundt KI-bruk
KI var utrolig nyttig for å forstå matematikken bak vinkler, men den tok ofte feil når det gjaldt spesifikke Pygame-funksjoner (som `BLEND_RGBA_ADD`). Jeg lærte at man aldri må stole blindt på KI-kode, men alltid teste og forstå den selv før man bruker den.