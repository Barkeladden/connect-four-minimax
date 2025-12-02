# Connect Four AI (Minimax)

Dette prosjektet er en implementasjon av Fire på rad med en AI-motstander basert på minimax-algoritmen. Det ble gjort som et sideprosjekt på videregående.

## Om prosjektet

Prosjektet består av et spillbrett representert som en grid-struktur og en AI-spiller som evaluerer mulige trekk ved hjelp av:

* Minimax-algoritmen

* Alpha-beta pruning (for å redusere søkedybden og gjøre AI-en raskere)

* Heuristisk evalueringsfunksjon som vurderer stillinger basert på mønstre, trusler og potensielle fire på rad (regler definert av meg)

Spilleren kan velge kolonne, og AI-en responderer med det trekket som gir best forventet utfall innenfor gjeldende søkedybde. Brettet visualiseres med pygame.

## Hva jeg lærte

* Hvordan minimax fungerer i praksis

* Hvordan heuristikk påvirker spillstyrke

* Håndtering av rekursjon og state-evaluering

* Effektivisering med alpha-beta pruning
