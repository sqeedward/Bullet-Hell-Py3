# Numele Proiectului Petru Griffon x Ghiu Simulator
## Descriere

Proiectul nostru este un joc Python bazat pe Pygame, oferind o experiență captivantă de acțiune și aventură. Jucătorii se pot bate cu diversi inamici cunoscuti ca fiind celebritati. 

## Cuprins

1. [Instrucțiuni](#instrucțiuni)
2. [Cum să rulezi jocul](#cum-să-rulezi-jocul)
3. [Structura Proiectului](#structura-proiectului)
4. [Contribuții](#contributii)

## Cum să rulezi jocul
```
pip install pygame
```

```
python3 main.py
```

## Structura Proiectului

### `main.py`

În fișierul `main.py`, am implementat crearea meniului folosind biblioteca `pygame_menu`. Meniul include o imagine de fundal sugestivă a ceea ce se întâmplă în joc și butoane pentru a personaliza experiența utilizatorului.  O scurtă descriere a butoanelor:

- **Dificultate (Hard/Easy):** Permite jucătorului să aleagă nivelul de dificultate al jocului.
- **Selectare Nume Utilizator:** Permite utilizatorului să introducă un nume pentru a personaliza experiența de joc.
- **Play:** Butonul care direcționează jucătorul către începerea jocului propriu-zis.
- **Quit:** Butonul care închide jocul.

### `gameengine.py`

Clasa `GameStates` este utilizată pentru a monitoriza starea jocului, inclusiv pauza (`pause`), desfășurare (`running`) și oprire (`quit`).

Clasa GameEngine inițializează caracteristicile jocului prin constructor, stabilind:
- Caracteristicile caracterului principal (înălțime, grosime, animație).
- Caracteristicile proiectilului utilizat de caracterul principal.
- Caracterul inamic.
- Fereastra jocului.
- Camera.

Metoda `handle_events`:
-Această metodă gestionează evenimentele jocului, cum ar fi apăsările de taste (W, A, S, D) pentru mișcarea caracterului principal, mișcarea mouse-ului pentru a trage în inamici, și butonul de pauză (`P`) pentru a controla stările `RUNNING`, `PAUSE`, și `QUIT`.

### `tools/animations.py`

Această clasă generează o suprafață dintr-o imagine de tip array. Necesită dimensiunile fiecărei imagini și numărul de imagini pe foaie de animație. O foaie de animație reprezintă un vector de imagini concatenate pentru a forma o imagine mai mare. Specificați numărul de imagini de preluat și indexul animației curente dorite.

Constructor pentru foaia de animație: Parametrul `animations` reprezintă o matrice de animații, fie sub formă de imagine, listă sau np.array. `width` și `height` se referă la dimensiunea fiecărei imagini (de exemplu, o animație cu width = 64, height = 64). `pictures_per_line` indică câte imagini sunt pe fiecare linie (de exemplu, prima animație poate avea 8, a doua doar 4, astfel avem `pictures_per_line = [8, 4]`). `count` reprezintă numărul de imagini, iar `current` este animația curentă. `scales` sunt utilizate pentru dimensiuni.

Metode:
- `add_animation_sheet`: Permite adăugarea de noi animații la obiectul existent.
- `select_animation`: Permite selectarea unei anumite animații și a unei poziții în cadrul acelei animații.
- `cutImageFromSheet`: Extrage o imagine specifică dintr-un set de animații și o redimensionează.
- `nextAnimation`: Trece la următoarea imagine dintr-o animație.

Această clasă este o extensie a clasei `AnimationSheet`, adăugând funcționalități specifice pentru gestionarea animațiilor în jocuri. Constructorul `__init__` primește un șir de caractere `path` ca argument, reprezentând calea către fișierul de imagine, și îl convertește într-o matrice de culori pentru utilizare ulterioară. Metoda `update` actualizează animația la fiecare cadru, ținând cont de ratele de cadre și timpul petrecut în joc. Metoda `tickUpdate` este similară cu `update`, dar primește direct numărul de cadre trecute și actualizează animația în consecință. Metoda `nextAnimation` trece la următoarea animație, dacă este disponibilă.

### `tools/assetsloader.py`

Dictionarul `paths`:
Acest dicționar conține chei care reprezintă numele resurselor (sprite-urilor), iar valorile asociate sunt căile către fișierele de imagine asociate acestor resurse. Căile sunt definite relativ la directorul sursă al proiectului.

Dictionarul `loaded`:
Acest dicționar va stoca sprite-urile deja încărcate pentru a evita încărcarea duplicată a acelorași resurse.

Metoda `getImage`:
Această metodă returnează un obiect imagine (`pygame.Surface`) asociat numelui dat ca parametru. Dacă imaginea este deja încărcată, se va returna imaginea din dicționarul `loaded`, altfel se va încărca imaginea folosind calea din dicționarul `paths` și se va salva în dicționarul `loaded` pentru a o putea accesa mai rapid data viitoare.

Metoda `getSprite`:
Această metodă apelează `getImage` pentru a obține o imagine asociată numelui dat. Apoi, se creează un obiect `pygame.Surface` pentru o anumită regiune (rectangulară) a imaginii, specificată prin parametrul `rectangle`. Această regiune va fi extrasă din imaginea originală și va fi setată ca imagine a unui obiect `pygame.sprite.Sprite`. Opțiunea de `colorkey` este folosită pentru a trata un anumit culoare ca transparent în imaginea rezultată. Dacă nu este specificat, nu se va aplica nicio transparență.

### `tools/builder.py`

Variabile de clasă:
- `tile_size`: Dimensiunea fiecărei țigle în pixeli.
- `tiles_set`: Un set care va stoca pozițiile țiglelor existente.
- `imgs`: O listă care va stoca informații despre tipul de țiglă de la fiecare poziție.
- `build_mode`: Un indicator al modului de construire (0 pentru modul de construire simplu, diferit de zero pentru modul de construire extins).
- `block_list`: O listă care pare să nu fie utilizată în codul furnizat.
- `tiles`: O listă de chei pentru a accesa sprite-urile din AssetLoader.
- `tiles_indx`: Un indice care indică care dintre sprite-urile din lista tiles este selectat în mod curent.

Metoda `__init__`:
Constructorul primește o cameră și o stochează pentru a fi utilizată ulterior.

Metoda `initSpawnPos`:
Inițializează o poziție specificată cu un tip de țiglă dată. Creează o instanță a clasei BackgroundTile și adaugă informații relevante în `tiles_set` și `imgs`.

Metoda `spawnAtPos`:
Verifică dacă o țiglă există deja la o anumită poziție și, în caz negativ, o inițializează folosind `initSpawnPos`.

Metoda `spawnBlocks`:
Spawn-ează țigle la o poziție dată în funcție de modul de construire (`build_mode`). Dacă modul este 0, se spawn-ează doar o țiglă la poziția curentă. În caz contrar, se spawn-ează un set extins de țigle în jurul poziției.

Metoda `change_tile`:
Schimbă tipul de țiglă selectată la următorul în lista `tiles`.

Metoda `eventHandler`:
Gestionează evenimentele de la tastatură și mouse. În cazul apăsării butonului stâng al mouse-ului, se apelează `spawnBlocks`. Alte evenimente sunt gestionate în funcție de tastele apăsate.

Metoda `save_map`:
Salvează harta într-un fișier numit "map.txt". Informațiile salvate includ pozițiile și tipurile de țigle.

Metoda `load_map`:
Încarcă o hartă salvată anterior dintr-un fișier specificat.

### `tools/camera.py`

Metoda `__init__`:
Constructorul primește două argumente, `pos` și `size`, care reprezintă poziția și dimensiunea camerei. Se calculează `center` ca fiind mijlocul camerei, iar un obiect de tip `pygame.rect.Rect` este creat pentru reprezentarea dreptunghiului camerei.

Metoda `setCenter`:
Setează centrul camerei la poziția specificată.

Metoda `getCenter` și `getRealCenter`:
`getCenter` returnează centrul camerei, iar `getRealCenter` returnează centrul în coordonatele reale (fără a ține cont de dimensiunea camerei).

Metoda `setPos`:
Setează poziția camerei la locația specificată și actualizează `center` și dreptunghiul camerei.

Metoda `getPos`:
Returnează poziția camerei.

Metoda `draw`:
Desenează un obiect (presupus a fi o instanță a clasei `GameObject`) pe ecran, ținând cont de poziția și dimensiunile camerei. Verifică dacă obiectul este vizibil în cadrul camerei (verificând coliziunea dreptunghiurilor). Dacă nu este vizibil, nu îl desenează.

Metoda `draw_raw`:
Desenează o imagine direct pe ecran la o anumită poziție, fără a lua în considerare obiecte de tip `GameObject`. Această metodă nu efectuează verificări de coliziune și desenează imaginea indiferent de poziția camerei.

### `tools/spritesheet.py`

Metoda `__init__`:
Constructorul clasei. Primește trei argumente: `path` (calea către sprite sheet), `state_count` (numărul total de stări ale sprite-ului, implicit 1) și `sprite_counts` (o listă care conține numărul de sprite-uri pentru fiecare stare). Calea (`path`) și sprite sheet-ul (`Spritesheet`) sunt stocate ca atribute ale obiectului, iar numărul total de sprite-uri (`sprite_count`) este inițializat.

### `entities/enemy.py`

Constantă `SPAWN_DISTANCE`:
Reprezintă distanța la care inamicul este plasat inițial în afara ecranului.

Clasa `Enemy` și Constructorul (`__init__`):

Constructorul primește mai mulți parametri: `sprite` (imaginea inamicului), `player` (obiectul jucătorului), `speed` (viteza inamicului), `health` (viața inamicului), `pos` (poziția inițială), `randomPos` (opțiunea de a alege o poziție aleatoare), și `animation` (animatie pentru inamic).
Inițializează clasa de bază (`Entity`) cu parametrii specificați.
Setează statistici pentru inamic (viteza și viața).
Dacă este specificată opțiunea `randomPos`, plasează inamicul în afara ecranului la o distanță aleatoare.

Metoda `setEnemyStats`:
Setează viteza și viața inamicului.

Metoda `damage`:
Scade viața inamicului cu o anumită cantitate de daună. Dacă viața ajunge la zero sau mai mică, inamicul este eliminat (`__del__`).

Metoda `moveToPosSimplified`:
Face ca inamicul să se miște direct spre poziția jucătorului, fără a ține cont de obstacole.

Metoda `randomSpawnRelativeToScreen`:
Plasează inamicul în afara ecranului la o distanță specificată (`SPAWN_DISTANCE`) într-o zonă aleatoare.

Metoda `onTick`:
Implementează logica pentru acțiunile inamicului în fiecare cadru (`frame`).

Metoda `onCollision`:
Se ocupă de logica coliziunilor. Dacă inamicul intră în coliziune cu un proiectil, îi scade viața în funcție de daunele proiectilului.

Metoda `onBlit`:
Implementează logica de afișare a animației în funcție de direcția mișcării.

### `entities/entity.py`

Clasa `Entity` și Constructorul (`__init__`):
Constructorul primește parametri precum `pos` (poziția entității), `sprite` (imaginea entității), `animation` (opțional, animația entității), și `hitbox` (opțional, zona de coliziune a entității).
Dacă `hitbox` nu este furnizat, se creează unul implicit folosind poziția entității (`pos`) și dimensiuni (10x10).
Inițializează clasa de bază (`Collidable`) cu parametrii specificați.
Inițializează `vel` (viteza) și `acc` (accelerația) cu vectori de tipul `geo.v2(0, 0)`.
Adaugă entitatea la lista `Entity.members` (o listă statică care conține toate entitățile).

Metoda `setVel`:
Setează viteza entității la o valoare specificată.

Metoda `addVel`:
Adaugă o valoare specificată la viteza entității.

Metoda `setAcc`:
Setează accelerația entității la o valoare specificată.

Metoda `getSprite`:
Returnează obiectul sprite al entității.

Metoda `setHp`:
Setează punctele de viață (`hp`) ale entității.

Metoda `onTick`:
Implementează logica pentru acțiunile entității în fiecare cadru (`frame`).

Metoda `move`:
Mută entitatea cu un vector specificat.

Metoda `move_to`:
Setează poziția entității la o anumită valoare.

Metoda `updatePos`:
Actualizează poziția entității pe baza vitezei și accelerației într-un interval de timp dat (`dt`).

Metoda `updateAnimation`:
Actualizează imaginea sprite-ului entității în funcție de animația asociată.

Metoda `onBlit`:
Implementează logica de afișare a animației în funcție de durata de timp specificată (60 cadre pe secundă și 0.3 secunde pentru fiecare animație).

Metoda `__del__`:
În momentul distrugerii entității, aceasta este eliminată din lista `Entity.members`. Se folosește și metoda `__del__` a clasei de bază (`Collidable`).

### `entities/gameobject.py`

Clasa `GameObject`:
Constructor (`__init__`):
Initializează un obiect de joc cu o poziție (`pos`) și un sprite specificat.

Metoda `move(vect)`:
Mută obiectul de joc cu un vector specificat.

Metoda `getPos()`:
Returnează poziția obiectului de joc.

Metoda `setPos(posv)`:
Setează poziția obiectului de joc la o valoare specificată.

Metoda `onBlit()`:
O metodă goală care poate fi suprascrisă în clasele derivate pentru a implementa logica specifică afișării.

Clasa `Collidable` (derivată din `GameObject`):
Atribut static `members`:
O listă statică care conține toate obiectele colizibile create.

Constructor (`__init__`):
Inițializează un obiect colizibil cu o poziție (`pos`), un sprite și o zonă de coliziune (`hitbox`) specificate.
Adaugă obiectul colizibil la lista statică `Collidable.members`.

Metoda `updateHitboxPos(newPos)`:
Actualizează poziția zonei de coliziune la o nouă poziție specificată.

Metoda `onCollision(other)`:
O metodă pe care trebuie să o suprascrieți în clasele derivate pentru a gestiona comportamentul la coliziune cu alte obiecte.

Metoda `checkCollision()`:
Verifică coliziunile cu toate celelalte obiecte colizibile. Dacă se detectează o coliziune, se apelează met

### `entities/player.py`

Clasa `Player` reprezintă jucătorul în joc și moștenește de la clasa `Entity`, care, la rândul său, este derivată din clasa `Collidable`. Acest lanț de moștenire indică că un jucător este un obiect colizibil cu altele din joc și are o anumită logică de mișcare și comportament.

Principalele aspecte ale clasei `Player` includ:
Arme și Selecția Armelor:
Există o listă de arme (`weapons`) și un indice pentru arma curent selectată (`weapon_pos`).
Jucătorul poate adăuga arme la lista sa și poate schimba între ele.

Logica de Mișcare:
Jucătorul se mișcă pe ecran în funcție de input-ul utilizatorului și are animații asociate mișcării.
Atunci când se ciocnește cu un obiect de tip `Border`, se evită coliziunea ajustând poziția jucătorului.

Focul cu Arma:
Jucătorul poate trage cu arma curent selectată, determinând unghiul de tragere.

Gestiona Coliziunile:
Metoda `onCollision` gestionează reacția jucătorului la coliziuni. Dacă se ciocnește cu un obiect de tip `Border`, ajustează poziția.

Animații:
Există animații asociate mișcării și direcției jucătorului.

### `entities/projectile.py`

Clasa `Projectile`:
Aceasta moștenește de la clasa `Entity` și are adăugate câteva funcționalități specifice proiectilelor.
Proiectilul are un timp de viață (`seconds_alive`), un contor (`cnt`) și un daune (`dmg`).
Constructorul primește parametri precum poziția, imaginea și daunele, inițializând și animația proiectilului cu o imagine specifică (`fireball`).
Metoda `getDamage` returnează valoarea daunelor.
`onCollision` asigură că proiectilele nu se ciocnesc între ele și nu au interacțiuni cu jucătorul (`Player`), iar în caz contrar proiectilul se distruge (`__del__`).
Metoda `onTick` gestionează durata de viață a proiectilului și îl distruge dacă a depășit acest timp.

Clasa `Pellet` și `Bullet`:
Acestea sunt subclase ale clasei `Projectile` și sunt specializate pentru a crea proiectile cu daune specifice (20 pentru `Pellet` și 100 pentru `Bullet`).
Constructorul apelează constructorul clasei părinte (`super()`) și specifică daunele corespunzătoare pentru fiecare subtip de proiectil.

## Contribuții

### Răzvan Andrei Rotaru
### Sebastian George Brumă
### Victor-Ioan Măndescu
### Ioana Ionescu
