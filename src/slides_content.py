"""Slide content for the 4-paper review deck.

Rendered to PDF by make_slides.py and to PPTX by make_pptx.py, so both outputs
stay in sync. The deck is meant to be read, not presented, so each slide carries
the concrete numbers from the paper rather than headline keywords.
"""

P1 = "1 | Mersani et al. 2025"
P2 = "2 | Roshani et al. 2023"
P3 = "3 | Lu et al. 2025"
P4 = "4 | Nielsen et al. 2022"


def build(d):
    # ============================================================ 1. TITULAS
    d.title_slide(
        "Intelektualieji metodai fazinių gardelių antenų projektavime",
        "Keturių mokslinių straipsnių apžvalga",
        ["Paulius Černiauskas, PEPfm-26",
         "Magistro tiriamasis darbas: 6×6 fazinės gardelės Ku ruožo antenos projektavimas ir tyrimas",
         "Intelektualiosios sistemos · Referatas · 2026",
         ],
    )

    # ============================================================ 2. APŽVALGA
    d.slide(
        "Keturi straipsniai — keturi antenos gyvavimo ciklo etapai",
        [("p", "Straipsniai parinkti taip, kad apimtų visą 6×6 Ku gardelės kūrimo eigą ir skirtingas "
               "intelektualiųjų metodų šeimas — nuo prižiūrimosios regresijos iki evoliucinio optimizavimo."),
         ("gap", 6),
         ("table",
          ["#", "Etapas", "Straipsnis", "Intelektualusis metodas"],
          [["1", "**Elemento projektavimas**\nS11 prognozė", "Mersani, Mekki, Ncibi (2025)\n*Indian J. of Science and Technology*",
            "7 ML regresijos modeliai:\nKNN, MLP, XGBoost, RF, SVR, LR, Ridge"],
           ["2", "**Tarpelementinė sąveika**\nizoliacijos didinimas", "Roshani, Koziel, Yahya et al. (2023)\n*Sensors* 23(16), 7089",
            "Atvirkštinis MLP surogatas,\napmokytas dalelių spiečiaus algoritmu (PSO)"],
           ["3", "**Gardelės topologija**\nšoninių lapelių mažinimas", "Lu, Maman, Earls, Boag, Baldi (2025)\narXiv:2504.17073",
            "Neuroninis tinklas kaip diferencijuojama\nkainos funkcija + gradientinis nusileidimas"],
           ["4", "**Eksploatacija**\ngedimų diagnostika", "Nielsen, Zhang, Shen et al. (2022)\n*IEEE Trans. Antennas Propag.* 70(7)",
            "Gilusis neuroninis tinklas (klasifikacija)\niš baseband I/Q signalų"],
           ],
          [22, 128, 210, 230]),
         ],
        kicker="Apžvalga",
    )

    # ============================================================ STRAIPSNIS 1
    d.slide(
        "Sprendžiama problema ir keliami uždaviniai",
        [("kv", [
            ("Kontekstas", "Kompaktiška 2,4 GHz ISM juostos mikrojuostelinė (patch) antena su dviem plyšiais, "
                           "skirta IoT ir nešiojamiems įrenginiams."),
            ("Pagrindinė problema", "Pilnabangis EM modeliavimas yra tikslus, bet lėtas. Autorių atliktas parametrinis "
                                    "skenavimas užtruko **daugiau nei 15 valandų**, o gautos žinios negeneralizuojamos "
                                    "neištirtoms konfigūracijoms."),
            ("Uždavinys 1", "Sukurti tikslų modelį, prognozuojantį atspindžio koeficientą S11 iš geometrinių "
                            "matmenų ir dažnio."),
            ("Uždavinys 2", "Palyginti šešis (lentelėje — septynis) ML algoritmus ir nustatyti tinkamiausią."),
            ("Uždavinys 3", "Realizuoti atvirkštinį projektavimą: iš norimos charakteristikos gauti matmenis."),
         ]),
         ("note", "Kodėl šis straipsnis",
          "Tai tas pats straipsnis, kurio eksperimentus atkartojau Namų darbe Nr. 2, todėl jo rezultatai "
          "toliau pateikiami kartu su mano paties patikrinimu."),
         ],
        kicker=P1, tag="Mersani et al., IndJST 18(33): 2715–2728, 2025",
    )

    d.slide(
        "Taikomi intelektualieji metodai",
        [("b", "**Surogatinio modelio idėja.** Vietoj CST sprendiklio naudojama ML funkcija: įėjime — 10 geometrinių "
               "matmenų ir dažnis, išėjime — S11 (dB). Atsakymas gaunamas per milisekundes, ne minutes."),
         ("b", "**Palyginti septyni modeliai**, apimantys keturias skirtingas šeimas:"),
         ("sub", "Atvejais grįsti: **KNN** (k artimiausių kaimynų)"),
         ("sub", "Neuroniniai tinklai: **MLP** (daugiasluoksnis perceptronas)"),
         ("sub", "Ansambliniai medžiai: **Random Forest**, **XGBoost**"),
         ("sub", "Branduoliniai ir tiesiniai: **SVR**, **tiesinė** ir **Ridge** regresija"),
         ("b", "**Duomenų apdorojimo grandinė:** normalizavimas → atsitiktinis 80/20 skaidymas → vertinimas "
               "pagal MAE, RMSE ir R²."),
         ("note", "Metodinė spraga",
          "Straipsnyje nenurodyti **nė vieno** modelio hiperparametrai, nors 3.5 skyriuje teigiama, kad "
          "„kiekvienam modeliui buvo pritaikytas sistemingas hiperparametrų derinimas“."),
         ],
        kicker=P1, tag="Mersani et al., IndJST 18(33): 2715–2728, 2025",
    )

    d.slide(
        "Eksperimentų duomenys ir vertinimo būdas",
        [("kv", [
            ("Duomenų šaltinis", "Autorių sukurtas rinkinys, sugeneruotas **CST Microwave Studio** parametriniais "
                                 "skenavimais. Paskelbtas Zenodo (DOI 10.5281/zenodo.15866821, CC BY 4.0)."),
            ("Apimtis", "**55 053 mėginiai**, 12 stulpelių: 10 geometrinių matmenų + dažnis → S11 (dB)."),
            ("Medžiagos", "FR4 pagrindas (εr = 4,3, tanδ = 0,02), storis 1,6 mm; PEC lopinėlis 42 × 29,3 mm."),
            ("Dažnių ruožas", "1,8–2,8 GHz, 1001 taškas (žingsnis 1 MHz)."),
            ("Metrikos", "MAE, RMSE (dB) ir R²; papildomai Pearson koreliacijos matrica ir Random Forest "
                         "požymių svarbos analizė."),
         ]),
         ("note", "Ką parodė mano auditas (ND2)",
          "„55 053 mėginiai“ iš tikrųjų yra **tik 53 unikalios geometrijos**, kiekviena nuskenuota per 1001 dažnio "
          "tašką. Be to, **3 iš 11 įėjimo požymių yra konstantos**. Nė vieno iš šių faktų straipsnyje nėra."),
         ],
        kicker=P1, tag="Mersani et al., IndJST 18(33): 2715–2728, 2025",
    )

    d.slide(
        "Palyginimas su alternatyvomis ir gauti rezultatai",
        [("p", "Straipsnio 2 lentelė — septyni modeliai, lyginami tarpusavyje. Dešinėje — mano atkartojimo "
               "rezultatai (Namų darbas Nr. 2)."),
         ("gap", 4),
         ("table",
          ["Modelis", "MAE", "RMSE", "R²", "Mano RMSE", "Skirtumas"],
          [["KNN (k = 5)", "0,0495", "**0,4216**", "**0,9866**", "0,4213", "−0,0003"],
           ["MLP", "0,1795", "0,5110", "0,9803", "0,5317", "+0,0207"],
           ["Random Forest", "0,0600", "0,5380", "0,9782", "0,5389", "+0,0009"],
           ["XGBoost", "0,1329", "0,5855", "0,9742", "**0,4570**", "**−0,1285**"],
           ["SVR (RBF)", "1,2276", "3,3202", "0,1690", "3,3202", "0,0000"],
           ["Tiesinė regresija", "1,9968", "3,5244", "0,0637", "3,5244", "0,0000"],
           ["Ridge regresija", "1,9968", "3,5244", "0,0637", "3,5244", "0,0000"],
           ],
          [150, 80, 90, 90, 100, 100]),
         ("b", "**Straipsnio išvada:** KNN ir MLP pranoksta ansamblinius metodus; tiesiniai modeliai ir SVR "
               "netinka, nes ryšys tarp geometrijos ir S11 yra stipriai netiesinis (R² ≈ 0,06 ir 0,17)."),
         ("b", "**Lyginama ir su literatūra** (3 lentelė): ankstesni darbai pasiekė R² = 0,75–0,90 prie RMSE "
               "0,50–2,02, naudodami 243–2106 mėginių rinkinius."),
         ],
        kicker=P1, tag="Mersani et al., IndJST 18(33): 2715–2728, 2025",
    )

    d.slide(
        "Autorių išvados ir mano patikrinimas",
        [("b", "**Autorių išvados:** surogatinis modelis sutrumpina projektavimą „nuo valandų iki sekundžių“; "
               "KNN pasiekia R² = 0,9866; galutinė antena rezonuoja ties 2,45 GHz su S11 < −40 dB; "
               "įtakingiausi parametrai — lopinėlio plotis ir maitinimo linijos ilgis."),
         ("gap", 2),
         ("table",
          ["Autorių teiginys", "Mano patikrinimo rezultatas"],
          [["KNN: RMSE 0,4216 / R² 0,9866",
            "**Atkartota tiksliai.** Penki iš septynių modelių sutampa iki 3–4 skaitmens po kablelio."],
           ["„Sistemingas hiperparametrų derinimas“",
            "**Nepagrįsta.** Penki modeliai atkartoti su `scikit-learn` numatytaisiais parametrais; "
            "viena XGBoost derinimo iteracija davė **22 % pagerėjimą**."],
           ["KNN ir MLP pranoksta ansamblinius metodus",
            "**Galioja tik jų parametrams.** Suderintas XGBoost (0,457) pralenkia MLP ir Random Forest."],
           ["R² = 0,9866 rodo aukštą tikslumą",
            "**Pervertinta.** Skaidant pagal geometrijas (ne eilutes), RMSE auga 0,42 → **1,26 dB**, "
            "R² krenta iki 0,872, o modelių skirtumai išnyksta."],
           ["Įtakingiausi: lopinėlio plotis, maitinimo linijos ilgis",
            "**Iš dalies.** Maitinimo linijos ilgis — taip, bet lopinėlio plotis yra priešpaskutinis (0,0018)."],
           ],
          [230, 460]),
         ],
        kicker=P1, tag="Mersani et al., IndJST 18(33): 2715–2728, 2025",
    )

    # ============================================================ STRAIPSNIS 2
    d.slide(
        "Sprendžiama problema ir keliami uždaviniai",
        [("kv", [
            ("Kontekstas", "Dviejų elementų 2,45 GHz mikrojuostelinė gardelė ant Rogers RO4003C pagrindo, "
                           "elementai išdėstyti itin arti — **0,05–0,07 λ** tarpas tarp kraštų (5,8 mm)."),
            ("Pagrindinė problema", "Glaudžiai išdėstyti elementai stipriai sąveikauja. Pradinė izoliacija tėra "
                                    "**≈ 9 dB**, o tai gadina spinduliavimo diagramą, mažina naudingumo koeficientą "
                                    "ir MIMO kanalų nepriklausomumą."),
            ("Uždavinys 1", "Sukurti naują atskiriantįjį rezonatorių, įterpiamą tarp elementų."),
            ("Uždavinys 2", "Sukurti **atvirkštinį** dirbtinio neuronų tinklo surogatą, kuris iš norimų "
                            "S parametrų tiesiogiai duotų rezonatoriaus matmenis."),
            ("Uždavinys 3", "Pagaminti prototipą ir patvirtinti rezultatus matavimais."),
         ]),
         ("note", "Kodėl tai aktualu 6×6 Ku gardelei",
          "Ku ruože (12–18 GHz) elementų žingsnis yra ~10 mm, todėl elementai fiziškai negali būti toli vienas "
          "nuo kito. Tarpelementinė sąveika yra viena pagrindinių 36 elementų gardelės projektavimo kliūčių."),
         ],
        kicker=P2, tag="Roshani et al., Sensors 23(16): 7089, 2023",
    )

    d.slide(
        "Taikomi intelektualieji metodai",
        [("b", "**Atvirkštinis (inverse) surogatinis modelis** — pagrindinė straipsnio naujovė. Skirtingai nuo "
               "įprasto modelio (geometrija → S parametrai), čia veikia priešinga kryptis:"),
         ("sub", "**Įėjimas (2 neuronai):** norima izoliacija S21 ir norimas atspindys S11"),
         ("sub", "**Išėjimas (3 neuronai):** rezonatoriaus matmenys LR, LT1, LT2"),
         ("sub", "**Architektūra:** MLP su dviem paslėptais sluoksniais po 10 neuronų, aktyvacija *tansig*"),
         ("b", "**Tinklas apmokomas ne atgaliniu sklidimu, o dalelių spiečiaus algoritmu (PSO):** "
               "500 dalelių, 2000 iteracijų, C1 = C2 = 2."),
         ("b", "**Kodėl PSO, o ne backpropagation?** Autorių argumentas: atgalinis sklidimas yra lokalus "
               "gradientinis metodas ir įstringa lokaliuose minimumuose, o PSO tyrinėja visą paieškos erdvę."),
         ("gap", 2),
         ("b", "**Praktinė nauda:** projektuotojui nereikia iteratyvaus EM optimizavimo — įvedus norimą "
               "izoliaciją, modelis iškart grąžina matmenis."),
         ],
        kicker=P2, tag="Roshani et al., Sensors 23(16): 7089, 2023",
    )

    d.slide(
        "Eksperimentų duomenys ir vertinimo būdas",
        [("kv", [
            ("Duomenų generavimas", "EM modeliavimas **ADS 2022** aplinkoje, keičiant rezonatoriaus geometrijos "
                                    "parametrus; ANN mokymas ir PSO realizuoti **MATLAB R2021b**."),
            ("Rinkinio apimtis", "Straipsnyje **nenurodyta** — tai vienas iš darbo trūkumų."),
            ("Varijuojami parametrai", "LR (rezonatoriaus ilgis), LT1 ir LT2 (dantukų ilgiai); WR = 4,7 mm fiksuotas."),
            ("Modelio vertinimas", "Vidutinė santykinė paklaida (MRE) atskirai mokymo ir testavimo aibėms."),
            ("Galutinis vertinimas", "**Pagamintas prototipas** ir išmatuoti S parametrai — nepriklausomas "
                                     "patikrinimas, kurio 1-ajame straipsnyje nėra."),
         ]),
         ("gap", 4),
         ("table",
          ["Prognozuojamas dydis", "MRE mokymo aibėje", "MRE testavimo aibėje"],
          [["LR — rezonatoriaus ilgis", "1,28 %", "**1,27 %**"],
           ["LT1 — pirmo dantuko ilgis", "3,34 %", "4,24 %"],
           ["LT2 — antro dantuko ilgis", "8,60 %", "**11,85 %**"],
           ],
          [280, 190, 190]),
         ("b", "Paklaida labai nevienoda: pagrindinį matmenį modelis prognozuoja tiksliai, o smulkiausią "
               "detalę — beveik 12 % paklaida."),
         ],
        kicker=P2, tag="Roshani et al., Sensors 23(16): 7089, 2023",
    )

    d.slide(
        "Palyginimas su alternatyviais sprendimais",
        [("p", "Straipsnio 3 lentelė lygina siūlomą sprendimą su vienuolika ankstesnių darbų. Žemiau — "
               "charakteringiausi."),
         ("gap", 4),
         ("table",
          ["Šaltinis", "Dažnis", "Metodas", "Tarpas", "Izoliacijos pagerėjimas", "Galutinė izoliacija"],
          [["[1]", "3,94 GHz", "I formos sekcija", "0,15 λ", "30 dB", "—"],
           ["[24]", "4,8 GHz", "Vingiuota linija", "0,11 λ", "16 dB", "22 dB"],
           ["[72]", "2,2–2,7 GHz", "ANN + rezonatorius", "—", "5,6 dB", "25,3 dB"],
           ["[82]", "2,45 GHz", "3D metamedžiaga", "0,13 λ", "18 dB", "35 dB"],
           ["[84]", "5,8 GHz", "Sunertos linijos", "0,07 λ", "24 dB", "23 dB"],
           ["**Siūlomas**", "**2,45 GHz**", "**Rezonatorius + atvirkštinis ANN**", "**0,05 λ**",
            "**37,2 dB**", "**46,2 dB**"],
           ],
          [70, 95, 220, 75, 130, 115]),
         ("b", "Siūlomas sprendimas vienu metu pasiekia **didžiausią izoliaciją** ir **mažiausią tarpą** tarp "
               "elementų. Ypač iškalbingas palyginimas su [72] — taip pat ANN pagrindu, bet tik 5,6 dB pagerėjimas."),
         ],
        kicker=P2, tag="Roshani et al., Sensors 23(16): 7089, 2023",
    )

    d.slide(
        "Rezultatai ir autorių išvados",
        [("table",
          ["Rodiklis", "Be rezonatoriaus", "Su rezonatoriumi (modeliuota)", "Prototipo matavimas"],
          [["Izoliacija S21 ties 2,45 GHz", "≈ 9 dB", "**46,2 dB**", "**38 dB**"],
           ["Atspindys S11", "—", "26 dB", "19 dB"],
           ["Juostos plotis (S11 < −10 dB)", "30 MHz", "**50 MHz** (+66 %)", "—"],
           ["Stiprinimas ties 2,45 GHz", "5,95 dB", "6,15 dB (+0,2 dB)", "—"],
           ],
          [230, 140, 180, 150]),
         ("gap", 2),
         ("b", "**Autorių išvados:** paviršiaus srovės tarp elementų beveik visiškai panaikinamos; atvirkštinis "
               "ANN-PSO modelis leidžia gauti projektą be iteratyvaus EM optimizavimo; spinduliavimo diagrama "
               "praktiškai nepakinta."),
         ("b", "**Autorių nurodyti ribotumai:** metodo pritaikymas kitiems dažnių ruožams ir antenų tipams dar "
               "netirtas; planuojama išplėsti į plačiajuostes gardeles ir išbandyti hibridinius optimizavimo algoritmus."),
         ("note", "Mano pastaba",
          "Modeliuota izoliacija 46,2 dB, o išmatuota — 38 dB, t. y. **8 dB skirtumas**. Straipsnis šio skirtumo "
          "plačiau neanalizuoja, nors būtent jis rodo realų metodo tikslumą gamyboje."),
         ],
        kicker=P2, tag="Roshani et al., Sensors 23(16): 7089, 2023",
    )

    # ============================================================ STRAIPSNIS 3
    d.slide(
        "Sprendžiama problema ir keliami uždaviniai",
        [("kv", [
            ("Kontekstas", "Didelės aktyviai skenuojamos gardelės (AESA) su **retintu (sparse)** elementų "
                           "išdėstymu — iki **1024 elementų**."),
            ("Pagrindinė problema", "Periodinis išdėstymas sukuria **difrakcinius lapelius** (grating lobes). "
                                    "Aperiodinis išdėstymas juos slopina, bet projektavimo laisvės laipsnių "
                                    "skaičius tampa milžiniškas, o kainos funkcija — nekonveksi ir "
                                    "nediferencijuojama."),
            ("Kodėl klasikiniai metodai netinka", "Pilna paieška neįmanoma dėl konfigūracijų skaičiaus; "
                                                  "stochastiniai metodai (atkaitinimo imitavimas, GA) yra lėti "
                                                  "ir skaičiavimo požiūriu brangūs didelėms gardelėms."),
            ("Uždavinys", "Pakeisti nekonveksią kainos funkciją **diferencijuojama** neuroninio tinklo "
                          "aproksimacija ir optimizuoti elementų koordinates gradientiniu nusileidimu."),
         ]),
         ],
        kicker=P3, tag="Lu, Maman, Earls, Boag, Baldi — arXiv:2504.17073, 2025",
    )

    d.slide(
        "Taikomi intelektualieji metodai",
        [("b", "**1. Uždavinio supaprastinimas.** Gardelės faktorius perrašomas iš penkių kintamųjų į du "
               "(uy, uz), o gardelė sudaroma iš periodinių **sub-masyvų** — taip sumažinamas laisvės laipsnių skaičius."),
         ("b", "**2. Neuroninis tinklas kaip surogatinė kainos funkcija.** Tinklas mokomas prognozuoti "
               "pagrindinio ir šoninių lapelių energijos santykį iš elementų koordinačių. Lygintos dvi architektūros:"),
         ("sub", "**FNN** — 4 pilnai sujungti sluoksniai, įėjimas 2048 (1024 elementų Y ir Z koordinatės), "
                 "paslėpti 20 ir 12 neuronų, ReLU; 1000 epochų, Adam, η = 1e-5"),
         ("sub", "**Set Transformer** — dėmesio mechanizmas, invariantiškas elementų eiliškumui; "
                 "2 galvos, paslėptas matmuo 32, η = 1e-3"),
         ("b", "**3. Optimizavimas gradientiniu nusileidimu.** Kadangi tinklas yra tolydus ir diferencijuojamas, "
               "elementų koordinatės tiesiogiai optimizuojamos Adam algoritmu (PyTorch)."),
         ("b", "**4. Fizikinių apribojimų baudos funkcija.** Logaritminė bauda už per mažą atstumą tarp elementų "
               "(riba θ = 0,5 λ) — taip netiesiogiai ribojama ir tarpelementinė sąveika."),
         ("b", "**Hiperparametrai parinkti automatiškai** įrankiu SHERPA (tinklelio paieška)."),
         ],
        kicker=P3, tag="Lu, Maman, Earls, Boag, Baldi — arXiv:2504.17073, 2025",
    )

    d.slide(
        "Eksperimentų duomenys ir vertinimo būdas",
        [("kv", [
            ("Duomenų kilmė", "**Sintetiniai** — gardelių konfigūracijos generuojamos sub-masyvų metodu, "
                              "kainos funkcija skaičiuojama analiziškai iš gardelės faktoriaus."),
            ("Įėjimo formatas", "Kiekviena gardelė — koordinačių porų aibė, papildyta iki 1024 elementų."),
            ("Kainos funkcija", "Pagrindinio lapelio ir šoninių lapelių energijos santykis su norma p = 4 — "
                                "didesnė bauda už aukštus pavienius pikus."),
            ("Eksperimento apimtis", "Optimizuotos **10 konfigūracijų su mažiausia pradine kaina**; "
                                     "viena optimizacija trunka **apie 1 minutę**."),
            ("Vertinimo rodikliai", "Kainos funkcijos pokytis, pirmojo ir antrojo šoninio lapelio lygis (SLL), "
                                    "pusės galios pluošto plotis, minimalus atstumas tarp elementų."),
         ]),
         ("note", "Ko rinkinyje nėra",
          "Straipsnyje nenurodytas mokymo rinkinio dydis (kiek gardelių konfigūracijų sugeneruota tinklui "
          "apmokyti). Kodas paskelbtas GitHub'e, todėl atkartoti įmanoma."),
         ],
        kicker=P3, tag="Lu, Maman, Earls, Boag, Baldi — arXiv:2504.17073, 2025",
    )

    d.slide(
        "Palyginimas ir gauti rezultatai",
        [("p", "Lyginamos dvi tinklo architektūros ir optimizavimas su baudos funkcija bei be jos."),
         ("gap", 4),
         ("table",
          ["Konfigūracija", "1-as SLL (uy, uz)", "2-as SLL (uy, uz)", "Vid. kainos pokytis"],
          [["**FNN + baudos funkcija**", "**−17,46 / −15,72 dB**", "**−20,03 / −17,22 dB**", "**552 %**"],
           ["Set Transformer (be baudos)", "−14,42 / −14,06 dB", "−15,27 / −14,93 dB", "66 %"],
           ["FNN be baudos", "−13,54 / −13,42 dB", "−13,86 / −14,41 dB", "59 %"],
           ],
          [220, 180, 180, 130]),
         ("gap", 2),
         ("b", "**Pusės galios pluošto plotis nepakito** nė viename variante (ζ3dB = 0,78°) — vadinasi, šoniniai "
               "lapeliai sumažinti nepabloginant pagrindinio pluošto."),
         ("b", "**Baudos funkcija pasirodė esminė.** Be jos optimizavimas stumia elementus iki pat minimalaus "
               "leistino atstumo (0,501 λ), o su bauda vidutinis minimalus atstumas padidėja iki 0,508 λ ir "
               "kartu pagerėja pati kaina — abu tikslai pasiekiami vienu metu."),
         ("b", "**Lyginama netiesiogiai** su klasikiniais metodais (atkaitinimo imitavimu, genetiniais algoritmais "
               "retinimui) — autoriai juos aptaria kaip lėtus ir brangius, bet **tiesioginio skaitinio palyginimo "
               "nepateikia**."),
         ],
        kicker=P3, tag="Lu, Maman, Earls, Boag, Baldi — arXiv:2504.17073, 2025",
    )

    d.slide(
        "Autorių išvados ir kritinis vertinimas",
        [("b", "**Autorių išvados:** neuroninis tinklas sėkmingai pakeičia nekonveksią kainos funkciją "
               "diferencijuojama aproksimacija; metodas veikia greitai (≈1 min. vienai gardelei) ir yra "
               "lygiagretinamas; jis apibendrinamas kitoms gardelėms, įskaitant neplanines; tinka tolesniam "
               "taikymui fazės nuosvyrai, pluošto formavimui ir gardelių retinimui."),
         ("gap", 4),
         ("note", "Kritinė pastaba dėl rezultatų pateikimo",
          "Teiginys apie **„552 % kainos sumažinimą“** yra matematiškai keistas — sumažinti dydį daugiau nei "
          "100 % neįmanoma. Iš lentelių matyti, kad kalbama apie neigiamos kainos funkcijos reikšmės pokytį "
          "(pvz. nuo −40 464 iki −287 802), t. y. apie **pagerėjimą kartais**, o ne procentinį sumažinimą. "
          "Tai apsunkina rezultatų lyginimą su kitais darbais."),
         ("gap", 2),
         ("b", "**Antra silpnoji vieta:** SLL vertės (−13…−17 dB) nėra ypač geros retintoms gardelėms — klasikiniai "
               "metodai pasiekia −20…−25 dB. Straipsnio stiprybė yra **greitis ir mastelis** (1024 elementai per "
               "minutę), o ne absoliutus spinduliavimo diagramos kokybės rekordas."),
         ],
        kicker=P3, tag="Lu, Maman, Earls, Boag, Baldi — arXiv:2504.17073, 2025",
    )

    # ============================================================ STRAIPSNIS 4
    d.slide(
        "Sprendžiama problema ir keliami uždaviniai",
        [("kv", [
            ("Kontekstas", "Aktyviosios fazinės gardelės (APA) 5G ir 6G įrenginiuose bei palydoviniame ryšyje. "
                           "Kiekvienas kanalas turi stiprintuvą ir fazės sukiklį, kurie gali sugesti."),
            ("Pagrindinė problema", "Įprasta diagnostika matuoja **spinduliavimo diagramą** beaidėje kameroje, "
                                    "naudojant kelis griežtai pozicionuotus zondus. Tai lėta, brangu ir "
                                    "neįmanoma atlikti eksploatacijos vietoje."),
            ("Uždavinys 1", "Diagnozuoti gedimus iš **baseband I/Q signalų**, naudojant tik **vieną zondą** "
                            "viename matavimo taške."),
            ("Uždavinys 2", "Atpažinti ne tik neveikiančius spinduliuotuvus, bet ir **stiprintuvų amplitudės** "
                            "bei **fazės sukiklių** nuokrypius."),
            ("Uždavinys 3", "Įvertinti atsparumą triukšmui ir gedimų grupėms."),
         ]),
         ("note", "Kuo šis straipsnis išsiskiria rinkinyje",
          "Tai vienintelis iš keturių darbų, dirbantis su **realios komercinės gardelės išmatuotais duomenimis**, "
          "o ne modeliavimo rezultatais."),
         ],
        kicker=P4, tag="Nielsen et al., IEEE Trans. Antennas Propag. 70(7): 5044–5053, 2022",
    )

    d.slide(
        "Taikomi intelektualieji metodai",
        [("b", "**Uždavinio tipas — klasifikavimas, ne regresija.** Tai svarbus skirtumas nuo kitų trijų "
               "straipsnių: tinklas priskiria matavimą vienai iš 50 klasių (49 gedimų scenarijai + „be gedimo“)."),
         ("b", "**Gilaus neuroninio tinklo architektūra:**"),
         ("sub", "4 pilnai sujungti sluoksniai po **500 neuronų**, iš viso **5 549 147 mokomi parametrai**"),
         ("sub", "Kiekviename sluoksnyje: paketinis normalizavimas (Batch Norm) + ReLU"),
         ("sub", "Išėjime softmax, nuostolių funkcija — kryžminė entropija, optimizatorius SGD"),
         ("sub", "Apmokytas modelis užima **22,3 MB**"),
         ("b", "**Įėjimo vektorius:** 5000 I ir 5000 Q atskaitų, sujungtų į **10 000 matmenų** vektorių. "
               "Tinklas pats išmoksta gedimo požymius, glūdinčius baseband signale — jų nereikia "
               "apibrėžti rankomis."),
         ("gap", 2),
         ("b", "**Esminė metodinė idėja:** gedimas keičia ne tik spinduliavimo diagramą, bet ir priimto "
               "signalo I/Q struktūrą, todėl pakanka vieno stebėjimo taško."),
         ],
        kicker=P4, tag="Nielsen et al., IEEE Trans. Antennas Propag. 70(7): 5044–5053, 2022",
    )

    d.slide(
        "Eksperimentų duomenys ir matavimų aplinka",
        [("kv", [
            ("Tiriamas objektas", "Komercinė **AMOTECH A0404** aktyvioji fazinė gardelė, **4 × 4 = 16 elementų**, "
                                  "28 GHz, su keturiais Anokiwave AWMF-0158 pluošto formavimo lustais."),
            ("Signalas", "3 GHz LTE OFDM, perkeltas į 28 GHz; piko ir vidutinės galios santykis 10,6 dB."),
            ("Matavimo schema", "**Viena** ruporinė antena 42 bangos ilgių (44 cm) atstumu."),
            ("Duomenų apimtis", "Kiekvienai klasei — **10 matavimų po 5 mln. atskaitų**, diskretizavimo "
                                "dažnis 10 kHz. Skaidymas 70 % / 30 %."),
            ("Gedimų scenarijai", "16 klasių — išjungtas spinduliuotuvas; 16 klasių — 0,5 dB slopinimas; "
                                  "16 klasių — 5° fazės poslinkis; papildomai iki 6 vienalaikių gedimų."),
         ]),
         ("gap", 4),
         ("b", "**Testavimui naudoti nepriklausomi nauji matavimai**, o ne atidėta mokymo duomenų dalis — "
               "metodologiškai griežčiau nei 1-ajame straipsnyje."),
         ],
        kicker=P4, tag="Nielsen et al., IEEE Trans. Antennas Propag. 70(7): 5044–5053, 2022",
    )

    d.slide(
        "Palyginimas su alternatyvomis ir rezultatai",
        [("table",
          ["Metodas", "Tikslumas", "Reikia beaidės kameros", "Matavimo taškų", "Aptinka aktyviųjų dalių gedimus"],
          [["REV (sukamojo vektoriaus)", "100 %", "Taip", "Daug", "Ne"],
           ["EM atvirkštinis uždavinys (ISP/EIP)", "—", "Taip", "Keli zondai", "Ne"],
           ["Ankstesni DNT iš spinduliavimo diagramų", "80 %", "Taip", "Keli", "Ne"],
           ["**Siūlomas DNT iš I/Q**", "**99 %**", "**Ne**", "**1**", "**Taip**"],
           ],
          [190, 85, 130, 100, 180]),
         ("gap", 4),
         ("table",
          ["Scenarijus", "Rezultatas"],
          [["Pavienis gedimas, švarus signalas", "**99 %** (atskiroms klasėms 88–99 %)"],
           ["Iki 6 vienalaikių gedimų", "**80 %**"],
           ["Triukšmas: SNR ≥ 4 dB", "Išlaikoma **> 90 %**"],
           ["Triukšmas: SNR ≤ 0 dB", "Modelis sugriūva — prognozuoja vieną klasę"],
           ["Diagnozės trukmė", "**6 ms** vienam matavimui (NVIDIA TITAN RTX)"],
           ],
          [260, 430]),
         ],
        kicker=P4, tag="Nielsen et al., IEEE Trans. Antennas Propag. 70(7): 5044–5053, 2022",
    )

    d.slide(
        "Autorių išvados ir nurodyti ribotumai",
        [("b", "**Autorių išvados:** metodas pašalina poreikį turėti kelis matavimo taškus ir brangią beaidę "
               "kamerą; diagnozė trunka milisekundes, todėl tinka naudoti eksploatacijos vietoje; aptinkami ne tik "
               "antenos elementų, bet ir stiprintuvų bei fazės sukiklių gedimai — to klasikiniai metodai nedaro."),
         ("gap", 4),
         ("table",
          ["Autorių nurodytas ribotumas", "Ką tai reiškia praktiškai"],
          [["Neatpažįsta gedimų tipų, kurių nebuvo mokymo aibėje",
            "Reikia iš anksto numatyti visus scenarijus — nauja gedimo rūšis bus priskirta klaidingai"],
           ["Daugybinių gedimų klasifikavimas riboja ties ~6",
            "Signalo matmenų nepakanka daugiau vienalaikių gedimų atskirti"],
           ["Prie SNR < 4 dB modelis sugriūva",
            "Reikia mokymo su triukšmu papildytais duomenimis"],
           ["Modelis pririštas prie konkrečios 28 GHz gardelės",
            "Perkėlimas į kitą gardelę reikalauja mokymo iš naujo — **tai svarbu perkeliant į Ku ruožą**"],
           ["Zondo padėties jautrumas neištirtas",
            "Praktikoje matavimo geometrija gali skirtis"],
           ],
          [300, 390]),
         ],
        kicker=P4, tag="Nielsen et al., IEEE Trans. Antennas Propag. 70(7): 5044–5053, 2022",
    )

    # ============================================================ PALYGINIMAS
    d.slide(
        "Visų keturių straipsnių palyginimas — uždavinys, metodas, duomenys",
        [("table",
          ["", "1 | Mersani 2025", "2 | Roshani 2023", "3 | Lu 2025", "4 | Nielsen 2022"],
          [["**Uždavinio tipas**", "Regresija\n(surogatas)", "Atvirkštinė regresija\n(projektavimo sintezė)",
            "Optimizavimas\n(surogatas + gradientas)", "Klasifikavimas\n(diagnostika)"],
           ["**Intelektualusis metodas**", "KNN, MLP, XGBoost,\nRF, SVR, LR, Ridge",
            "MLP, apmokytas **PSO**", "FNN ir Set Transformer\n+ Adam", "Gilusis NT\n(4 × 500, 5,5 mln. par.)"],
           ["**Objektas**", "1 patch elementas\n2,4 GHz", "2 elementų gardelė\n2,45 GHz",
            "Iki 1024 elementų\nAESA", "4 × 4 gardelė\n28 GHz"],
           ["**Duomenys**", "55 053 eilutės iš CST\n(**tik 53 geometrijos**)", "ADS modeliavimas\n(apimtis nenurodyta)",
            "Sintetinės konfigūracijos\n(apimtis nenurodyta)", "**Išmatuoti** I/Q\n10 × 5 mln. atskaitų / klasei"],
           ["**Duomenys vieši**", "**Taip** (Zenodo, CC BY)", "Ne", "Kodas GitHub'e", "Ne"],
           ["**Fizinis patikrinimas**", "Ne", "**Taip** — prototipas", "Ne", "**Taip** — komercinė gardelė"],
           ],
          [110, 145, 145, 145, 145]),
         ],
        kicker="Palyginimas I",
    )

    d.slide(
        "Visų keturių straipsnių palyginimas — palyginimo bazė ir rezultatai",
        [("table",
          ["", "1 | Mersani 2025", "2 | Roshani 2023", "3 | Lu 2025", "4 | Nielsen 2022"],
          [["**Lyginama su**", "6 kitais ML modeliais\n+ 3 literatūros darbais",
            "**11 ankstesnių darbų**\n(metamedžiagos, DGS, ANN)", "Klasikiniais metodais —\ntik aprašomai",
            "REV, ISP/EIP,\nankstesniais DNT"],
           ["**Pagrindinis rezultatas**", "KNN: RMSE 0,42\nR² 0,9866", "Izoliacija **46,2 dB**\n(+37,2 dB)",
            "SLL −17,5 dB,\n≈1 min. gardelei", "**99 %** pavieniams,\n80 % daugybiniams; 6 ms"],
           ["**Pranašumas prieš\nalternatyvas**", "Didesnis rinkinys nei\nankstesniuose darbuose",
            "**Geriausia izoliacija**\nprie mažiausio tarpo", "Greitis ir mastelis\n(1024 elementai)",
            "**Vienas zondas**, be\nbeaidės kameros"],
           ["**Kur silpniau**", "Tikslumas pervertintas;\nhiperparametrai nenurodyti",
            "Modeliuota 46 dB vs\nišmatuota 38 dB", "SLL nėra rekordinis;\n„552 %“ klaidina",
            "Sugriūva prie SNR < 4 dB;\nnepernešamas į kitą gardelę"],
           ["**Vertinimo griežtumas**", "Silpnas — nutekėjimas\ntarp aibių", "Vidutinis — yra matavimai",
            "Vidutinis — tik 10 konfig.", "**Griežčiausias** — nauji\nnepriklausomi matavimai"],
           ],
          [110, 145, 145, 145, 145]),
         ],
        kicker="Palyginimas II",
    )

    d.slide(
        "Metodų įvertinimas: kas tinka 6×6 Ku ruožo gardelei",
        [("table",
          ["Metodas", "Kam tiktų mano darbe", "Įvertinimas"],
          [["**Surogatinė regresija**\n(1 straipsnis)",
            "Greitai atrinkti gardelės elemento matmenis vietoj ilgo CST skenavimo",
            "**Tinka su išlygomis.** Mano atkartojimas parodė, kad tikslumas priklauso nuo to, kaip "
            "suplanuotas duomenų rinkinys ir kaip skaidomos aibės"],
           ["**Atvirkštinis ANN + PSO**\n(2 straipsnis)",
            "Tarpelementinės sąveikos mažinimas — Ku ruože elementų žingsnis ~10 mm, sąveika neišvengiama",
            "**Tinkamiausias.** Sprendžia tikrą 36 elementų gardelės problemą ir duoda matmenis tiesiogiai "
            "iš norimos izoliacijos"],
           ["**NT surogatas + gradientas**\n(3 straipsnis)",
            "Elementų išdėstymo optimizavimas, šoninių lapelių mažinimas",
            "**Perteklinis šiam masteliui.** Metodo nauda atsiranda ties šimtais elementų; 36 elementų "
            "gardelei pakaktų klasikinio optimizavimo"],
           ["**Gilusis NT klasifikavimui**\n(4 straipsnis)",
            "Pagamintos gardelės patikra: ar visi 36 kanalai veikia",
            "**Vertinga, bet vėlesniam etapui.** Reikalauja veikiančio prototipo ir matavimų"],
           ],
          [150, 250, 290]),
         ],
        kicker="Išvados",
    )

    d.slide(
        "Rekomendacija magistro tiriamajam darbui",
        [("b", "**1. Pradėti nuo surogatinio elemento modelio** (1 straipsnio metodika), bet ištaisius jos trūkumus, "
               "kuriuos nustačiau atkartodamas:"),
         ("sub", "duomenis skaidyti **pagal geometrijas, ne pagal eilutes** — kitaip tikslumas pervertinamas ~3 kartus"),
         ("sub", "vertinti **rezonansinį dažnį, rezonanso gylį ir juostos plotį**, ne bendrą RMSE"),
         ("sub", "kiekvienam geometriniam parametrui numatyti **bent 4–5 reikšmes**"),
         ("sub", "pagal mokymosi kreivę **~25 pilnų EM skaičiavimų** pakanka surogatui sukurti"),
         ("b", "**2. Pagrindinis dėmesys — tarpelementinei sąveikai** (2 straipsnio metodika). Tai kritinė 6×6 "
               "gardelės vieta Ku ruože, o atvirkštinis surogatas leidžia projektuoti nuo norimos izoliacijos."),
         ("b", "**3. Gardelės sintezei pakanka klasikinių metodų.** 36 elementų gardelei gilaus mokymosi "
               "optimizavimas (3 straipsnis) neatsiperka — PSO ar GA su tiesioginiu gardelės faktoriaus "
               "skaičiavimu bus paprasčiau ir skaidriau."),
         ("b", "**4. Diagnostiką numatyti kaip galimą darbo tęsinį** (4 straipsnio metodika) — ji tampa aktuali "
               "tik turint pagamintą prototipą."),
         ("gap", 2),
         ("note", "Bendra metodinė pamoka iš visų keturių",
          "Vertingiausi rezultatai gauti ten, kur modelis buvo patikrintas **nepriklausomai** — pagamintu prototipu "
          "(2) arba naujais matavimais (4). Silpniausias vertinimas — ten, kur remtasi vien atsitiktiniu "
          "duomenų skaidymu (1)."),
         ],
        kicker="Išvados",
    )

    d.slide(
        "Šaltiniai",
        [("b", "**[1]** A. Mersani, K. Mekki, O. Ncibi, „AI-Powered S11 Prediction for a Compact 2.4 GHz Patch "
               "Antenna“, *Indian Journal of Science and Technology*, t. 18, nr. 33, p. 2715–2728, 2025. "
               "DOI: 10.17485/IJST/v18i33.1326"),
         ("sub", "Duomenų rinkinys: Zenodo, DOI 10.5281/zenodo.15866821, CC BY 4.0"),
         ("b", "**[2]** S. Roshani, S. Koziel, S. I. Yahya, M. A. Chaudhary, Y. Y. Ghadi, S. Roshani, L. Golunski, "
               "„Mutual Coupling Reduction in Antenna Arrays Using Artificial Intelligence Approach and Inverse "
               "Neural Network Surrogates“, *Sensors*, t. 23, nr. 16, str. 7089, 2023. DOI: 10.3390/s23167089"),
         ("b", "**[3]** D. L. Y. Lu, L. Maman, J. Earls, A. Boag, P. Baldi, „Sparse Phased Array Optimization "
               "Using Deep Learning“, arXiv:2504.17073 [cs.LG], 2025."),
         ("sub", "Kodas: github.com/david5010/Optimization-of-Antenna-Arrays"),
         ("b", "**[4]** M. H. Nielsen ir kt., „Robust and Efficient Fault Diagnosis of mm-Wave Active Phased "
               "Arrays Using Baseband Signal“, *IEEE Transactions on Antennas and Propagation*, t. 70, nr. 7, "
               "p. 5044–5053, 2022. Preprintas: arXiv:2306.04360"),
         ("gap", 6),
         ("p", "Straipsnio [1] eksperimentai atkartoti Namų darbe Nr. 2; atkartojimo kodas, rezultatai ir "
               "ataskaita pateikti atskirai."),
         ],
        kicker="Literatūra",
    )
