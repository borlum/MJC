# MJC (Mechanical Journeying Construct)

Okay, vi prøver lige lidt igen(!).

Nyt forsøg på at få gang i MJC igen -- bare lidt. Største hurdle ved projektet? Afstand. Så prioritet nummer 1: simulator.

Har strikket en basic dynamisk model sammen.
*OBS:* **Parameter estimering mangler, men strukturen skulle være OK til vores behov. Der er selvfølgelig altid mulighed for at forfine det.**

Største mangler i den er: 

Motor-model
-----------
Pt. har jeg klasket noget sammen der bare antager første ordens dynamik mellem spænding og torque, med en tidskonstant vi kan skrue på. Tror vi kan nå langt med den, hvis vi lige få fin-tunet. Det kræver lige et par målinger(!).


Friktion
--------
Ja, var lige lidt på bar-bund for at få det igang, så antager lige nu friktions koefficienter på 1, både når det kommer til tranlation og rotation. Det er klart, at det er MEGET afhængig af overfladen -- men vi skal bare ha' valgt noget OK fornuftigt, og så er resten en forstyrrelse, som vi bare skal være robust overfor.