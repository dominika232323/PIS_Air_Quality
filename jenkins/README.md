do tego folderu będą wstawiane ważniejsze elementy związane z postawieniem jenkinsa np.:

- dockerfile

celem jest możliwość postawienia jenkinsa o tej samej konfiguracji na innym urządzeniu


jeśli ktoś z was chce / będzie musiał ustawić jenkinsa u siebie


korzystałem z tego poradnika:

https://www.youtube.com/watch?v=6YZvp2GwT0A



!!!zastrzeżenia:

- używałem najnowszej wersji jenkinsa - zmodyfikowany dockerfile w jenkins-master

- potrzebny jest własny agent jenkinsa - domyślny nie ma pythona, pokazany w filmie jest zbudowany na starej javie

    obraz agenta: krzysokol/pis_jekinks_agent:latest

    wstawić w pole docker-agent przy konfiguracji chmury, reszta jak w filmie
