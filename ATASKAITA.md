# Namų darbas Nr. 2 — mokslinio straipsnio eksperimentų atkartojimas

**Studentas:** Paulius Černiauskas, PEPfm-26
**Magistro tiriamojo darbo tema:** 6×6 fazinės gardelės (phased array) Ku dažnių ruožo antenos projektavimas ir tyrimas
**Data:** 2026-09-25

Ši ataskaita atitinka `ND2_reproduction.ipynb` struktūrą: kiekvienas skyrius atitinka notebook'o dalį.

---

## 1. Pasirinktas straipsnis

**A. Mersani, K. Mekki, O. Ncibi, „AI-Powered S11 Prediction for a Compact 2.4 GHz Patch Antenna", *Indian Journal of Science and Technology*, 2025, 18(33): 2715–2728.**
DOI: 10.17485/IJST/v18i33.1326 · Open Access (CC BY)

Lydintysis duomenų straipsnis:
**„Parametric simulation dataset of a 2.4 GHz patch antenna with slot for AI-based S11 prediction", *Data in Brief*, 2025.**

Straipsnyje mikrojuostelinės antenos atspindžio koeficientas S11 prognozuojamas mašininio mokymosi modeliais — tai surogatinis modelis, keičiantis lėtą CST elektromagnetinį modeliavimą.

### 1.1. Kodėl būtent šis straipsnis

| Užduoties reikalavimas | Kaip tenkinamas |
|---|---|
| Taikomi intelektualieji metodai | Septyni mašininio mokymosi regresijos modeliai kaip surogatinis EM modeliavimo pakaitalas |
| Publikuota per pastaruosius 5 metus | 2025 m. rugsėjo 8 d. |
| Duomenys viešai prieinami | Taip — Zenodo, DOI 10.5281/zenodo.15866821, CC BY 4.0, 3,6 MB CSV. Atsisiųsta ir patikrinta |
| Kompiuterinių resursų pakanka | Taip — visi eksperimentai sukasi CPU, bendra trukmė ~12 min. |
| Ryšys su magistro darbu | 6×6 fazinės gardelės elementas yra mikrojuostelinė (patch) antena. Surogatinis S11 modelis pakeičia lėtą CST parametrinį skenavimą projektuojant elementą. Straipsnis nurodo, kad jų parametrinis skenavimas truko **daugiau nei 15 valandų** |

### 1.2. Kodėl atmesti artimesni straipsniai

Ieškota straipsnių tiesiogiai apie fazines gardeles. Artimiausias kandidatas — *„Robust and Efficient Fault Diagnosis of mm-Wave Active Phased Arrays using Baseband Signal"* (arXiv:2306.04360, 4×4 gardelė, 28 GHz) — naudoja išmatuotus komercinės AMOTECH A0404 gardelės duomenis, kurie **nepaskelbti**. Tas pats pasakytina apie daugumą fazinių gardelių ML straipsnių. Todėl pasirinktas straipsnis, kurio duomenų rinkinys realiai atsisiunčiamas.

---

## 2. Duomenų auditas

*(notebook'o 1 dalis · `src/01_inspect_data.py`)*

- **Šaltinis:** Zenodo, `Cleaned_DataSet.csv` (3,64 MB), CC BY 4.0
- **Apimtis:** 55 053 eilutės × 12 stulpelių (10 geometrinių matmenų + dažnis → S11)
- **Modeliavimas:** CST Microwave Studio, FR4 (εr = 4,3, tanδ = 0,02), h = 1,6 mm, PEC lopinėlis, 1,8–2,8 GHz

```
shape                : (55053, 12)
missing values       : 0
duplicated rows      : 0
unique geometries    : 53
rows per geometry    : min=1000, max=2002, mean=1038.7
frequency points     : 1001  (1.8 – 2.8 GHz)
Columns that never vary: width_imp_line_mm, substrate_height_mm, patch_height_mm
```

**Du dalykai, kurių straipsnyje nėra:**

1. „55 053 mėginiai" yra **tik 53 unikalios antenos geometrijos**, kiekviena nuskenuota per 1001 dažnio tašką. Tai nėra 55 tūkstančiai nepriklausomų projektų.
2. Trys iš vienuolikos įėjimo požymių yra **konstantos**: maitinimo linijos plotis (3 mm), pagrindo storis (1,6 mm) ir metalizacijos storis (0,035 mm).

Šios pastabos lemia visų tolesnių rezultatų interpretaciją.

---

## 3. Eksperimentas 1 — pažodinis straipsnio atkartojimas

*(notebook'o 2 dalis · `src/02_reproduce_paper.py`)*

Protokolas iš straipsnio 2.2 skyriaus ir autorių notebook'o, pridėto prie Zenodo įrašo: normalizavimas, atsitiktinis 80/20 skaidymas, metrikos MAE / RMSE / R². Hiperparametrai straipsnyje **nenurodyti** nė vienam modeliui; KNN (k=5) ir Random Forest (150 medžių) paimti iš autorių notebook'o, likusieji — `scikit-learn` numatytieji, išskyrus XGBoost ir MLP, kuriuos teko derinti patiems.

Palyginimas su straipsnio **2 lentele**:

| Modelis | MAE (mūsų) | MAE (straipsnio) | RMSE (mūsų) | RMSE (straipsnio) | R² (mūsų) | R² (straipsnio) | ΔRMSE |
|---|---|---|---|---|---|---|---|
| KNN (k=5) | 0,0495 | 0,0495 | **0,4213** | **0,4216** | 0,9866 | 0,9866 | −0,0003 |
| XGBoost | 0,0827 | 0,1329 | 0,4570 | 0,5855 | 0,9843 | 0,9742 | −0,1285 |
| MLP (128-64) | 0,1589 | 0,1795 | 0,5317 | 0,5110 | 0,9787 | 0,9803 | +0,0207 |
| Random Forest (150) | 0,0599 | 0,0600 | **0,5389** | **0,5380** | 0,9781 | 0,9782 | +0,0009 |
| SVR (RBF) | 1,2276 | 1,2276 | **3,3202** | **3,3202** | 0,1690 | 0,1690 | 0,0000 |
| Linear Regression | 1,9968 | 1,9968 | **3,5244** | **3,5244** | 0,0637 | 0,0637 | 0,0000 |
| Ridge Regression | 1,9968 | 1,9968 | **3,5244** | **3,5244** | 0,0637 | 0,0637 | 0,0000 |

**Išvada: penki iš septynių modelių atkartoti praktiškai tiksliai.** KNN, Random Forest, SVR, Linear ir Ridge sutampa iki trečio–ketvirto skaitmens, įskaitant MAE. Tai patvirtina, kad protokolas suprastas teisingai ir kad autorių naudoti hiperparametrai buvo numatytieji.

Skiriasi tik du modeliai, ir abiem atvejais dėl **nenurodytų hiperparametrų** — detalus paaiškinimas 8.3 skyriuje.

**Ridge Regression identiška Linear Regression** iki ketvirto skaitmens — atkartota lygiai taip, kaip straipsnyje. Priežastis: prie 44 tūkst. mokymo eilučių ir 11 požymių numatytoji reguliarizacija α = 1 yra nereikšminga.

### 3.1. Teiginys apie hiperparametrų derinimą

Straipsnio 3.5 skyriuje kaip viena iš trijų sėkmės priežasčių nurodoma: *„trečia, kiekvienam modeliui buvo pritaikytas sistemingas hiperparametrų derinimas, užtikrinantis optimalų veikimą"*.

Šis atkartojimas tam prieštarauja. Penki iš septynių modelių buvo paleisti su **`scikit-learn` numatytaisiais parametrais** (SVR: C=1, γ='scale'; Ridge: α=1; KNN: k=5; Random Forest: 150 medžių iš autorių notebook'o) ir davė **tas pačias reikšmes iki ketvirto skaitmens**. Jei modeliai būtų buvę sistemingai derinti, toks sutapimas su numatytaisiais parametrais būtų labai mažai tikėtinas.

Stipriausias įrodymas yra pats XGBoost: skirdamas jam vieną derinimo iteraciją gavau RMSE 0,4570 prieš straipsnio 0,5855. Sunkiai tikėtina, kad „sistemingas derinimas" būtų palikęs 22 % rezervą.

Tai svarbu ne tik metodologiškai: straipsnio pagrindinė išvada — kad KNN ir MLP pranoksta ansamblinius metodus — yra tiesioginė šio nederinimo pasekmė, o ne duomenų savybė.

---

## 4. Eksperimentas 2 — vertinimas pagal nematytas geometrijas

*(notebook'o 3 dalis · `src/03_grouped_split.py`)*

**Problema.** Kadangi rinkinyje tėra 53 geometrijos po 1001 dažnio tašką, atsitiktinis **eilučių** skaidymas patalpina tos pačios S11 kreivės gretimus taškus ir į mokymo, ir į testavimo aibę. Pvz., tos pačios geometrijos taškai ties 2,450 ir 2,452 GHz gali būti mokymo aibėje, o 2,451 GHz taškas — testavimo. Tai nėra naujos antenos prognozė, o paprasta interpoliacija jau matytoje kreivėje.

Realiai surogatinis modelis turi prognozuoti S11 geometrijai, kuri **niekada nebuvo modeliuota** — būtent tai straipsnis ir deklaruoja kaip tikslą (2.1.3 skyrius: „jie negeneralizuoja žinių neištirtoms konfigūracijoms").

`GroupKFold` (5 dalys) pagal geometrijos ID, konstantiniai stulpeliai pašalinti.

| Modelis | RMSE (atsitiktinis) | R² (atsitiktinis) | RMSE (nematyta geom.) | R² (nematyta geom.) |
|---|---|---|---|---|
| KNN (k=5) | 0,421 | 0,9866 | **1,257 ± 0,233** | **0,872** |
| Random Forest (150) | 0,539 | 0,9781 | **1,252 ± 0,246** | **0,875** |
| XGBoost | 0,457 | 0,9843 | **1,285 ± 0,352** | **0,867** |
| MLP (128-64) | 0,532 | 0,9787 | **1,303 ± 0,647** | **0,844** |
| SVR (RBF) | 3,320 | 0,169 | 3,280 | 0,166 |
| Linear / Ridge | 3,524 | 0,064 | 3,483 | 0,059 |

**Išvados:**

- Paklaida **išauga apie 3 kartus** (KNN: 0,42 → 1,26 dB), R² nukrinta nuo 0,987 iki 0,872. Straipsnyje paskelbtas R² = 0,9866 techniškai teisingas, bet **įvertina lengvesnę užduotį**, nei deklaruojamas tikslas.
- Nematytų geometrijų atveju visi keturi netiesiniai modeliai tampa **statistiškai neatskiriami** (1,25–1,30 dB, standartiniai nuokrypiai 0,23–0,65). Straipsnio pagrindinė išvada apie KNN pranašumą neišlieka.
- Tiesiniai modeliai ir SVR elgiasi vienodai abiem atvejais — jie nieko neišmoko nė vienoje versijoje. Tai naudinga kontrolė: jie neturėjo įsimintos kreivės, kurios sąžiningas skaidymas galėtų atimti.

---

## 5. Eksperimentas 3 — inžinerinės metrikos

*(notebook'o 4 dalis · `src/04_engineering_metrics.py`)*

Straipsnyje vertinama tik RMSE/R² decibelais. Projektuotojui rūpi trys dydžiai: rezonansinis dažnis `f_res`, rezonanso gylis `S11_min` ir −10 dB juostos plotis. Šis eksperimentas prognozuoja **visą S11(f) kreivę kiekvienai nematytai geometrijai** (53 geometrijos, GroupKFold).

| Modelis | f_res MAE (MHz) | f_res mediana (MHz) | f_res ≤ 10 MHz (%) | S11_min MAE (dB) | BW MAE (MHz) |
|---|---|---|---|---|---|
| KNN (k=5) | **6,77** | **2,0** | **86,8** | 6,32 | 7,38 |
| Random Forest (150) | 9,08 | 2,0 | 84,9 | **6,08** | 6,11 |
| XGBoost | 8,49 | 3,0 | 83,0 | 6,35 | **5,43** |

**Dydžių reikšmė:**

- **f_res MAE** — rezonansinio dažnio vidutinė paklaida. KNN atveju 6,77 MHz, t. y. 0,28 % nuo 2,45 GHz.
- **f_res mediana** — ta pati paklaida, bet mediana, kurios nesugadina pavieniai išsišokimai. **Čia slypi svarbiausia informacija:** vidurkis 6,77, o mediana tik 2,0 MHz. Tipinė paklaida yra 2 MHz, bet keletas geometrijų suklysta labai smarkiai. Blogiausias atvejis (geometrija #48) klysta 82 MHz.
- **f_res ≤ 10 MHz (%)** — patikimumo matas: ne „kokia vidutinė paklaida", o „kaip dažnai modeliu galima pasitikėti". KNN: 86,8 % ≈ 46 geometrijos iš 53; likusios ~7 nepataiko.
- **S11_min MAE** — rezonanso gylio paklaida. ~6 dB yra blogas rezultatas, nes pats dydis svyruoja nuo −10 iki −45 dB. Modelis negali atskirti gerai suderintos antenos (−25 dB) nuo vidutiniškai suderintos (−19 dB). Fizikinė priežastis: gylį lemia smulkus impedanso derinimas, kuris jautriau reaguoja į geometrijos pokyčius nei pats rezonansinis dažnis.
- **BW MAE** — −10 dB juostos pločio paklaida. 5–7 MHz; kadangi tokių antenų juosta paprastai yra keliasdešimt MHz, tai maždaug 10–20 % santykinė paklaida.

**Bendra išvada:** nė vienas modelis nelaimi — KNN geriausias pagal dažnį, Random Forest pagal gylį, XGBoost pagal juostos plotį, ir visi skirtumai telpa į triukšmo ribas. Modelis žino, *kur* bus rezonansas, bet ne *koks gilus*. Todėl surogatą galima naudoti kandidatams atrinkti, bet ne nuspręsti, kad projektas baigtas.

Iliustracija `figures/fig3_curves_unseen.png` rodo geriausią, medianinį ir blogiausią atvejį.

---

## 6. Eksperimentas 4 — straipsnio 4, 5 ir 6 paveikslų atkartojimas

*(notebook'o 5 dalis · `src/05_figures.py`)*

### 6.1. 4 pav. — parametrų svarba

Straipsnio teiginys: *„patch width ir feed line length yra įtakingiausi veiksniai"*. Straipsnyje nenurodyta, ar į svarbos diagramą įtrauktas dažnis, todėl suskaičiuoti abu variantai:

| Su dažniu | Svarba | | Tik geometrija | Svarba |
|---|---|---|---|---|
| frequency_GHz | 0,7995 | | length_imp_line_mm | 0,3418 |
| width_slot_mm | 0,0640 | | width_slot_mm | 0,3202 |
| length_imp_line_mm | 0,0503 | | length_slot_mm | 0,2564 |
| length_slot_mm | 0,0408 | | substrate_length_mm | 0,0428 |
| width_substrate_mm | 0,0211 | | width_substrate_mm | 0,0346 |
| substrate_length_mm | 0,0187 | | patch_length_mm | 0,0024 |
| patch_length_mm | 0,0047 | | **patch_width_mm** | **0,0018** |
| **patch_width_mm** | **0,0008** | | 3 konstantiniai | 0,0000 |

**Teiginys atkartotas tik iš dalies.** Maitinimo linijos ilgis (`length_imp_line_mm`) iš tikrųjų yra svarbiausias geometrinis parametras. Bet **lopinėlio plotis (`patch_width_mm`) yra priešpaskutinis su svarba 0,0018**, o ne vienas iš dviejų įtakingiausių; antroje ir trečioje vietose yra plyšio matmenys.

Pažymėtina, kad ir straipsnio 4 pav. grafike matosi, jog įtakingiausi yra `length_imp_line_mm` ir `width_slot_mm`, nors tekste teigiama, kad `patch_width_mm` ir `length_imp_line_mm`. Tai vidinis straipsnio prieštaravimas.

Įtraukus dažnį, jam tenka 80 % viso modelio „dėmesio" — modelis daugiausia mokosi S11 kreivės formos, o ne geometrijos įtakos. Trys konstantiniai požymiai gauna lygiai 0, nepriklausomai patvirtindami 2 skyriaus auditą.

Fizikiškai lopinėlio matmenys *turėtų* būti svarbūs. Priežastis, kodėl nėra: rinkinyje `patch_length_mm` įgyja tik **2 reikšmes** (28,0 ir 29,3), o `patch_width_mm` — 5 artimas (40–44 mm). Modelis negali išmokti to, kas duomenyse beveik nevarijuoja. Tai duomenų rinkinio planavimo trūkumas, ne modelio.

### 6.2. 6 pav. — Pearson koreliacijos matrica

Straipsnio teiginys: *„S11 rodo labai silpnas koreliacijas su visais įėjimo požymiais (maks. |r| ≈ 0,13)"*.

| Požymis | \|r\| su S11 |
|---|---|
| frequency_GHz | 0,1973 |
| width_slot_mm | **0,1258** |
| length_imp_line_mm | 0,1183 |
| width_substrate_mm | 0,1080 |
| length_slot_mm | 0,0731 |
| patch_length_mm | 0,0200 |
| substrate_length_mm | 0,0035 |
| patch_width_mm | 0,0014 |

**Teiginys patvirtintas.** Didžiausia geometrinio parametro koreliacija yra 0,1258 ≈ 0,13, lygiai kaip skelbiama. Trys konstantiniai stulpeliai duoda `NaN` (nulinė dispersija).

Pastaba dėl interpretacijos: Pearson *r* matuoja tik **tiesinį** ryšį. Viename geometrijos pjūvyje S11 yra visiškai determinuota dažnio funkcija, bet r(dažnis, S11) = −0,18 — nes rezonanso duobė simetriška ir kylanti bei krintanti pusės viena kitą kompensuoja. Todėl maža |r| reiškia „netiesinis", o ne „silpnas". Straipsnio išvada teisinga, bet geriau ją pagrindžia tas pats eksperimentas kitu būdu: Linear/Ridge R² = 0,064, o KNN R² = 0,987.

### 6.3. 5 pav. — prognozuota prieš modeliuota

Atkartota (`figures/fig2_pred_vs_true.png`). Sklaidos diagrama atitinka straipsnio aprašymą: taškai glaudžiai apie y = x liniją intervale nuo −25 iki 0 dB, su pastebimais nuokrypiais ties S11 < −30 dB.

### 6.4. Kur iš tikrųjų slypi paklaida

| S11 intervalas (dB) | Taškų sk. | % visų taškų | Vid. abs. paklaida (dB) | Maks. | **% kvadratų sumos (SSE)** |
|---|---|---|---|---|---|
| (−70, −30] | 10 | 0,1 | **7,090** | 25,07 | **34,4** |
| (−30, −20] | 68 | 0,6 | 1,045 | 16,98 | 15,8 |
| (−20, −10] | 409 | 3,7 | 0,323 | 10,28 | 8,4 |
| (−10, −5] | 670 | 6,1 | 0,280 | 16,86 | 31,1 |
| (−5, 0] | 9851 | **89,5** | **0,020** | 10,66 | 10,3 |

Paskutiniai du stulpeliai prieštarauja vienas kitam, ir tai yra esmė:

- **MAE iškraipo plokščioji sritis.** 89,5 % taškų yra ties S11 ≈ 0 dB su 0,02 dB paklaida, todėl bendra MAE = 0,060 dB neneša informacijos.
- **RMSE elgiasi teisingai.** Kvadratavimas veikia kaip turi: 0,1 % taškų (rezonanso sritis) sudaro **34,4 %** kvadratų sumos, o 89,5 % plokščiųjų taškų — tik 10,3 %. Sakyti, kad RMSE „nemato" didelių paklaidų, būtų neteisinga.
- **R² išpūstas dėl vardiklio.** R² = 1 − SSE/SST, o SST yra S11 dispersija (13,27), didelė **būtent dėl gilių rezonansų**. Modelis gauna kreditą už tos dispersijos „paaiškinimą", nors gylio nepataiko.

**Tikroji problema su RMSE yra ne ta, kad ji ignoruoja dideles paklaidas, o ta, kad matuoja jas decibelais.** Projektuotojo sprendimas priklauso nuo dažnio poslinkio:

| Modelis | RMSE (nematyta geom.) | f_res MAE (MHz) |
|---|---|---|
| Random Forest | **1,252** (geriausia) | **9,08** (blogiausia) |
| KNN | 1,257 | **6,77** (geriausia) |
| XGBoost | 1,285 (blogiausia) | 8,49 |

**RMSE rikiuoja modelius priešinga tvarka nei rezonansinio dažnio paklaida.** Optimizuodamas RMSE, neoptimizuoji to, kas svarbu.

Straipsnis pats pastebi simptomą (2.2 skyrius: „nedideli nuokrypiai atsiranda kraštuose, pavyzdžiui S11 < −30 dB"), bet iš to neišveda išvados apie metrikos tinkamumą.

---

## 7. Eksperimentas 5 — kiek EM modeliavimų reikia

*(notebook'o 6 dalis · `src/06_learning_curve.py`)*

Šio eksperimento straipsnyje nėra, bet perkeliant metodiką į savo projektą jis svarbiausias: kiekviena mokymo geometrija kainuoja vieną pilną CST skaičiavimą.

5 pakartojimai, fiksuota nematytų geometrijų testavimo aibė. Testavimo RMSE (dB):

| Modelis | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 42 |
|---|---|---|---|---|---|---|---|---|
| KNN (k=5) | 2,126 | 1,827 | 1,687 | 1,579 | 1,292 | 1,463 | 1,418 | 1,349 |
| Random Forest | 2,000 | 1,620 | 1,554 | 1,471 | 1,291 | 1,378 | 1,354 | 1,307 |
| XGBoost | 2,012 | 1,711 | 1,574 | 1,440 | 1,324 | 1,303 | 1,245 | **1,188** |

**Išvada:** kreivė įsisotina ties **20–25 geometrijomis**; nuo 25 iki 42 RMSE pagerėja vos ~8 %. Vadinasi, autorių surinktų 53 geometrijų yra daugiau nei pakanka, o panašų surogatinį modelį naujai antenai galima sukurti turint ~25 pilnus EM skaičiavimus.

**Metodologinė pastaba.** Minimumas ties n = 25 ir pablogėjimas ties n = 30 yra atrankos triukšmas, ne realus efektas — daugiau duomenų negali pakenkti. Grafiko ±1σ juostos persidengia. Sąžininga interpretacija yra „įsisotina po ~20–25", o ne „optimalu ties 25". Priežastis struktūrinė: 53 geometrijos yra maža imtis mokymosi kreivei, o testavimo aibėje telpa tik ~11 geometrijų.

---

## 8. Išvados

*(notebook'o 7 dalis)*

### 8.1. Naudota aplinka

**Aparatinė:** nešiojamasis kompiuteris, AMD Ryzen 5 7530U (6 branduoliai / 12 gijų), 5,8 GB RAM, integruota Radeon grafika. **GPU skaičiavimams nenaudotas** — visi eksperimentai sukasi vien CPU.

**Programinė:** Windows 11 Home (10.0.26200), Python 3.12.10, `numpy` 2.1.3, `pandas` 2.2.3, `scikit-learn` 1.5.2, `xgboost` 3.4.1, `matplotlib` 3.9.2, Jupyter Notebook 7.6.3.

**Trukmė:** viso notebook'o paleidimas nuo pradžios iki galo užtrunka ~12 min. Ilgiausiai trunka SVR mokymas (~55 s), MLP (~26 s) ir mokymosi kreivė (~4 min, 120 modelių mokymų). Visi kiti modeliai mokosi per kelias sekundes.

**Duomenys:** `Cleaned_DataSet.csv` (3,64 MB) iš Zenodo, DOI 10.5281/zenodo.15866821, licencija CC BY 4.0. Papildomų duomenų negeneruota.

### 8.2. Kuriuos eksperimentus pavyko atkartoti

Pagrindinis straipsnio rezultatas — 2 lentelės septynių modelių palyginimas — atkartotas sėkmingai: penki iš septynių modelių sutampa iki trečio–ketvirto skaitmens po kablelio, įskaitant MAE. Taip pat atkartotos abi likusios skaitinės iliustracijos. 5 pav. sklaidos diagrama atitinka straipsnio aprašymą: taškai glaudžiai išsidėstę apie y = x liniją intervale nuo −25 iki 0 dB, su pastebimais nuokrypiais ties S11 < −30 dB. 6 pav. koreliacijos matricos teiginys pasitvirtino tiksliai — didžiausia geometrinio parametro koreliacija yra 0,126, kai straipsnyje skelbiama ~0,13.

Iš dalies atkartotas tik 4 pav. — įėjimo parametrų svarba. Maitinimo linijos ilgis mūsų skaičiavimuose tikrai yra svarbiausias geometrinis parametras, kaip teigia straipsnis, bet lopinėlio plotis atsidūrė priešpaskutinėje vietoje (svarba 0,0018), o ne tarp dviejų įtakingiausių. Priežastis slypi duomenyse, ne modelyje: `patch_length_mm` rinkinyje įgyja vos dvi reikšmes, o `patch_width_mm` — penkias gretimas, todėl modelis šių matmenų įtakos išmokti tiesiog negali.

Neatkartotas liko atvirkštinio projektavimo karkasas, kurį straipsnis skelbia kaip trečiąją savo įžvalgą. Priežastis ne techninė: straipsnio tekste šiam karkasui neskirta nė vieno skyriaus — nenurodytas nei modelio tipas, nei įėjimai, nei rezultatų metrikos, tad paprasčiausiai nėra pagal ką atkartoti. Tai straipsnio spraga, o ne atkartojimo trūkumas.

Taip pat nepavyko atkartoti 2 ir 7 pav. — parametrinių skenavimų ir galutinio antenos projekto. Paskelbtame duomenų rinkinyje nėra nei galutinio projekto matmenų (1 lentelėje nurodyto maitinimo linijos ilgio 11 mm rinkinyje apskritai nėra, jis siekia tik 10 mm), nei visų straipsnio tekste cituojamų skenavimo reikšmių. Tikėtina, kad tos simuliacijos buvo atliktos atskirai ir į Zenodo įrašą neįtrauktos.

### 8.3. Rezultatų palyginimas su straipsniu

| Modelis | RMSE (mūsų) | RMSE (straipsnio) | R² (mūsų) | R² (straipsnio) | Skirtumas |
|---|---|---|---|---|---|
| KNN (k=5) | 0,4213 | 0,4216 | 0,9866 | 0,9866 | −0,0003 |
| XGBoost | 0,4570 | 0,5855 | 0,9843 | 0,9742 | **−0,1285** |
| MLP (128-64) | 0,5317 | 0,5110 | 0,9787 | 0,9803 | **+0,0207** |
| Random Forest (150) | 0,5389 | 0,5380 | 0,9781 | 0,9782 | +0,0009 |
| SVR (RBF) | 3,3202 | 3,3202 | 0,1690 | 0,1690 | 0,0000 |
| Linear Regression | 3,5244 | 3,5244 | 0,0637 | 0,0637 | 0,0000 |
| Ridge Regression | 3,5244 | 3,5244 | 0,0637 | 0,0637 | 0,0000 |

**Skirtumų paaiškinimas.** Straipsnis nenurodo **nė vieno modelio hiperparametrų**. KNN (k=5) ir Random Forest (150 medžių) paimti iš autorių `ML_PatchAntenna_.ipynb`; SVR, Ridge ir Linear paleisti su `scikit-learn` numatytaisiais. Visi penki sutapo. Skiriasi būtent tie du modeliai, kurių parametrų nebuvo iš kur paimti:

- **XGBoost (−0,1285, mūsų geriau).** Konfigūracija: 600 medžių, gylis 8, η = 0,05. Derinimas davė 22 % mažesnę RMSE nei paskelbta, tad straipsnio XGBoost greičiausiai paleistas su numatytaisiais parametrais. Pasekmė svarbi: **straipsnio pagrindinė išvada, kad KNN ir MLP pranoksta ansamblinius metodus, yra nederinimo pasekmė, o ne duomenų savybė** — suderintas XGBoost pralenkia ir MLP, ir Random Forest.
- **MLP (+0,0207, mūsų šiek tiek blogiau).** Nenurodytas nei sluoksnių skaičius, nei neuronų kiekis, nei aktyvacijos funkcija, nei optimizatorius. Pasirinkta 128-64, ReLU, Adam, early stopping. Bet kuris kitas pagrįstas pasirinkimas duotų kiek kitokį rezultatą, tad tikslus atkartojimas čia principiškai neįmanomas.

Atskirai pažymėtina, kad straipsnio 3.5 skyriuje teigiama, jog „kiekvienam modeliui buvo pritaikytas sistemingas hiperparametrų derinimas". Šis atkartojimas tam prieštarauja (žr. 3.1 skyrių).

### 8.4. Papildomi eksperimentai, kurių straipsnyje nėra

1. **Duomenų auditas.** 55 053 „mėginiai" yra tik **53 unikalios geometrijos** po 1001 dažnio tašką, o 3 iš 11 įėjimo požymių yra konstantos.
2. **Vertinimas pagal nematytas geometrijas.** Dėl pirmojo punkto atsitiktinis eilučių skaidymas praleidžia informaciją tarp aibių. Skaidant pagal geometrijas, RMSE išauga 3 kartus (0,42 → 1,26 dB), R² krenta iki 0,872, o **modelių skirtumai visiškai išnyksta**.
3. **Inžinerinės metrikos.** Rezonansinis dažnis prognozuojamas gerai (mediana 2 MHz, 87 % geometrijų ≤ 10 MHz), bet rezonanso gylis — blogai (~6 dB).
4. **Metrikų analizė.** MAE iškraipo plokščioji sritis; R² išpūstas dėl didelės S11 dispersijos; RMSE didelėms paklaidoms jautri teisingai, bet matuoja jas decibelais — ir rikiuoja modelius **priešinga tvarka** nei f_res paklaida.
5. **Mokymosi kreivė.** ~**25 pilnų EM skaičiavimų** pakanka surogatiniam modeliui.

### 8.5. Praktinė išvada magistro darbui

Perkeliant metodiką į 6×6 Ku ruožo fazinės gardelės elementą:

- **~25 pilnų EM skaičiavimų** pakanka surogatiniam S11 modeliui sukurti.
- Duomenis skaidyti **pagal geometrijas, ne eilutes** — kitaip tikslumas bus pervertintas 3 kartus.
- Vertinti **f_res, S11_min ir juostos plotį**, ne bendrą RMSE.
- Parametrų skenavimą planuoti taip, kad **kiekvienas geometrinis parametras įgytų bent 4–5 reikšmes** — priešingu atveju modelis fizikiškai svarbių matmenų įtakos neišmoks, kaip nutiko su `patch_length_mm` (tik 2 reikšmės).
- Surogatą naudoti **kandidatams atrinkti**, o atrinktus patikrinti pilnu CST skaičiavimu.

---

## 9. AI agento panaudojimas

| Etapas | Ką atliko agentas |
|---|---|
| Straipsnio paieška | Literatūros paieška, kandidatų atranka, **duomenų prieinamumo patikra** (atmestas arXiv:2306.04360 dėl nepaskelbtų matavimų) |
| Straipsnio analizė | Išanalizuotas pilnas straipsnio PDF, lydintysis *Data in Brief* straipsnis, Zenodo README ir autorių `.ipynb`; rekonstruotas eksperimento protokolas ir 2 lentelės atskaitos reikšmės |
| Eksperimentų paruošimas | Duomenų atsisiuntimas, struktūros auditas, **metodologinės problemos identifikavimas** (53 geometrijos, 3 konstantiniai požymiai) |
| Kodo kūrimas | 6 eksperimentų skriptai, bendras modulis ir savarankiškas Jupyter notebook'as; eksperimentų 2, 3 ir 5 sumanymas |
| Vykdymas ir rezultatai | Visi eksperimentai paleisti, sugeneruotos 6 iliustracijos ir CSV rezultatų failai, palyginta su paskelbtomis reikšmėmis |

Agento indėlio ribos: straipsnio pasirinkimą, darbo apimtį ir sprendimą atkartoti tik šį vieną straipsnį nustatė autorius. Ataskaitos ir notebook'o tekstą autorius redagavo ir papildė savo pastebėjimais (pvz., vidinis straipsnio prieštaravimas 4 pav.).

---

## 10. Atkartojimo instrukcija

Paprasčiausia — per naršyklę:

```bash
pip install -r requirements.txt
jupyter notebook
```

ir atidaryti `ND2_reproduction.ipynb`, tada `Run > Run All Cells`. Duomenys parsisiunčiami automatiškai.

Arba atskirais skriptais:

```bash
pip install -r requirements.txt
mkdir data
curl -L -o data/Cleaned_DataSet.csv "https://zenodo.org/records/15866865/files/Cleaned_DataSet.csv?download=1"
cd src
python 01_inspect_data.py
python 02_reproduce_paper.py
python 03_grouped_split.py
python 04_engineering_metrics.py
python 05_figures.py
python 06_learning_curve.py
```

Rezultatai — `results/`, iliustracijos — `figures/`.
