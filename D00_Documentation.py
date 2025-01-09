
to do:
    1. to clear the code and standartize sintax 100%
    2. to add arm operating function and other 80%
    3. to develop position anti-fail system (accelerometer based) 30%
    4. to develop mission anti-fail system (optimalization in fail situations) 90%
    5. if time to experiment with multitasking 100%
    6. to develop ultrasonic locator 10%
    7. to create audiovisual manager 90%
    8. to create the best code ever!

Návod k použití:
    1) názvosloví souborů
        D ... documentation
        F ... source file - zde jsou uložené funkce pro navigaci robota a podobný bordel
        T ... testing file - tady je bordel po předchozích testech a slouží k testování
        M ... main program branch - tady je zapsáno vše o aktuálním ůkolu - Tady je jediné místo kde se píšou jízdy - nide jinde se nic nepřepisuje (pokud nejste sebevrach)
            Inicialization - tady jsou konkrétní inforamce o robotovi 
            R ... rides - tady jsou/budou konkrétní informace o jízdách - tady se definují jízdy i jednotlivé mise
            MManager - tady je spouštěcí sekvence - jediné co se upravuje zde jsou na začátku zdroje a je potřeba napsat všechny jízdy do lisu "rides"

    2) Použití
        1. Do souboru M01_inicialization se napíšou informace o robotovi (už vyplněno)
        2. Do souboru jízd se musí definovat jízdy
            eg:
                m11 = Mission(bot, 475, 595, 60, [85, 300]) -> začáteční stav
                def m11_body(): -> funkce kde je uloženo body
                    La.target(225)
                    bot.straight_position(300, 520, -1)
                    bot.straight_position(400, 860, 1)
                m11.add_body(m11_body) -> body je následně nezbytné přidat k misi
                m11.add_checkpoint(100, 100) -> k misi je též možné přidat checkpoint (místo kam robot zajede pokud tutu misi už splnil a robot byl po havárii puštěn znovu)
                r1 = Ride(Color.GREEN, m10, m11, m12, m13, m14, m15, m16) -> definice jízdy (barva, setup, mise...)
            možný obsah body:
                bot.straight_position(x, y, kdyz dopredu tak 1 dozadu je -1)
                kdyz chces jet na souradnice ^
                bot.straight_g(vzdalenost, konečná rychlost, True pokud chces pocatecni smer, pocatecni smer)
                kdyz chces jet jen rovne a dozadu ^
                La.run_target(rychlost 1000 max, pozice motoru 0 dole 225 nahorem, wait = false pokud chces prehravat naraz s dalsim radkem jinak nic sem nepis)
                zubata ruka ^
                Ra.run_angle(rychlost 1000 max, pozice motoru 100 je dole a 1300 nahore, wait = false pokud chces prehravat naraz s dalsim radkem jinak nic sem nepis)
                hak se snekem ^
                bot.turn(absolutni uhel, 0)
                toceni robota na miste ^
                absolutni uhel = 90° je vzdy ve smeru osy Y a 0° je vzdy ve smeru osy X
        3. Otevřít soubor M03_MManager, zkontrolovat zrojové soubory a jízdy v 'rides' (mají tam být minimálně všechny co chcete pouštět)
        4. pustit program a řídit se pokyny na robotovi
            jízda se vybere automaticky podle barvi na nádstavci (barvě jízdy - nastaveno v R souboru) 
            jízdu potvrdíme zmáčknutí prostředního tlačítka
            robot se rozjede
            v případě potřeby robota znehybníme opětovným zmáčknutím středního tlačítka - po dalším spuštění se robot vrátí na misi u které přestal
            robota zcela vypneme stačením bluetooth tlačítka