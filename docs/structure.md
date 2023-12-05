## Flowchart

```mermaid
flowchart TD
    subgraph subsim [Simulation variables]
        direction LR
        set[assets/settings.json] --> sim[simulation.py]
    end
    subgraph subent [entities]
        ent[entities.py]
    end
    subgraph sublvl [level objects]
        direction LR
        lvls[assets/levels/level**.json] --> lvl[level.py]
    end
    subsim --> subent
    subent --> sublvl
    sublvl --> player[player.py]
    menu[menu.py] --> main
    player --> main[main.py]
```

## Legenda

Każdy plik poniżej importuje wszystkie pliki powyżej
* settings.json - ustawienia, które mogą być zmienione przez użytkownika
* [simulation.py](#simulation.py) - parametry symulacji, wczytuje plik settings oraz zawiera informacje o klawiszach czy ilości klatek na sekundę itp (ważne ustawienie devMode = True, tylko do testowania)
* entities.py - klasa ogólna dla bytów, jak i zawiera przeciwników (może rodzielić bossów w przyszłości), zawiera też przedmioty
* level.py - wczytuje poziomy z plików, jak i definuje obiekty, które znajdują się w poziomie
* player.py - zawiera wszystkie akcje związane w graczem sterowanym, jego ekwipunek, umiejętności
* main.py - główna pętla programu

## simulation.py
* [variables](#variables)
* [get_current_scale()](#get_current_scale())
* [gameObjects](#gameobjects)
* [gameEntities](#gameentities)
* [GameObjects](#gameobjects)
* [settings](#settings)

### variables

Parametry gry
* max_velocity - maksymalna prędkość gracza
* movement_velocity - prędkość gracza przy poruszaniu się
* frame_rate - fps
* grid_size - ilość kratek na które jest podzielony poziom
* screen_size - wyjściowy rozmiar ekranu
* current_offset - offset wyświetlanej gry od ekranu, bo są rózne proporcje ekranu
* current_scale - skala obecnego ekranu od wyjściowego rozmiaru ekranu

### get_current_scale()

Mierzy obecną skalę między obecnym ekranem, a ekranem wyjściowym. Zapisuje ją w parametrach gry.

### gameObjects

Lista obiektów do wyświetlenia w grze.

### gameEntities

Lista bytów w grze.

### GameObjects

* init(object, isEntity: bool) - dodaje obiekt do listy gameObjects. Jeśli isEntity = True, to obiekt jest też w liście gameEntities
* delete(object) - usuwa obiekt z gameObjects i gameEntities
* get(name: str) - zwraca obiekt z listy gameObjects o danym imieniu
* update(collidables) - wywołuje update na każdym bycie z listy gameEntities
* blit(screen) - wywołuje blit na kązdym obiekcie z listy gameObjects

### settings
