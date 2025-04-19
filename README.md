# Micromouse
## A házi feladat formai és kivitelezési követelményei:
- [x] Ideálisan 3 fős csapatokban végzett projektmunka.
- [x] Házi feladatok választása a 4. hét végéig, bemutatás a 14. héten (5.20.)
- [ ] Projektterv készítése és nyomonkövetése, rendszeres konzultáció.
- [ ] Beadás GitHub-on, "rendes" commit history-val, érdemes használni a csapatmunka során a kollaborációs eszközöket (branch-ek, pull request-ek, gitflow, stb).
- [ ] A házi feladat működéséről egy (vagy több) legalább 1.5 - 2.5 perces bemutató Youtube-on.
- [ ] Dokumentáció markdown-ban a git repo readme-jében, nincs ppt, pdf, word doksi vagy bármi egyéb!

### Formai követelmények:
- [ ] Tartalomjegyzék linkekkel a header-ekre.
- [ ] Képek beágyazva (a fejlesztés lépéseiről és a végeredményről) és link a Youtube videóra.
- [ ] Link minden felhasznált ROS csomag (nav2, gazebo, rviz2, slam_toolnox) wiki oldalára, github repora, stb...

### Tartalmi követelmények:
- [ ] Dependency-k és teljes telepítési útmutató, hogy még én is fel tudjam tenni a csomagotokat (és el is tudjam indítani).
- [ ] Saját 3D modell, Collada mesh és abból URDF fájl készítése, ha meglévő robot modellből indultok ki, akkor valami saját komponens hozzáadása URDF-ben.
- [ ] A robot szenzorainak a szimulációja Gazebo-ban, minimum 1 kamera, ha meglévő modellből indultok ki, akkor 1 bármilyen plusz szenzor hozzáadása.
- [ ] Gazebo világ építése és szimulációja (pl. szoba, versenypálya, sakktábla, térképrészlet épületekkel, stb.)
- [ ] Minimum 1 saját fejlesztésű ROS node Pythonban vagy C++-ban.
- [ ] Jó tanács: beadás előtt próbáljátok ki egy üres colcon workspace-ben fordítani, ha ott megy nálam is fog.

## Feladatleírás:
- Micromouse jellegű labirintus készítése
- Átlós haladást lehetővé tevő szakasz is legyen benne
- Labirintus feltérképezése pl szimulált távolságmérő szenzorral
- Útvonaltervezés a labirintuson való végigvezetésre saját ROS node-dal
