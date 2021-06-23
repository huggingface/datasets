---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- pl
licenses:
- cc-by-3.0
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- summarization
paperswithcode_id: null
---

# Dataset Card for polsum

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** http://zil.ipipan.waw.pl/PolishSummariesCorpus
- **Repository:** http://zil.ipipan.waw.pl/PolishSummariesCorpus
- **Paper:** http://nlp.ipipan.waw.pl/Bib/ogro:kop:14:lrec.pdf
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Mateusz Kopeć](http://zil.ipipan.waw.pl/MateuszKopec)

### Dataset Summary

The Corpus contains a large number of manual summaries of news articles,
with many independently created summaries for a single text. Such approach is supposed to overcome the annotator bias, which is often described as a problem during the evaluation of the summarization algorithms against a single gold standard.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Polish

## Dataset Structure

### Data Instances

See below an example from the dataset. Detailed descriptions of the fields are provided in the following section.

```
{'authors': 'Krystyna Forowicz',
 'body': "ROZMOWA\n\nProf. Krzysztof  Ernst, kierownik Zakładu Optyki Instytutu Fizyki Doświadczalnej Uniwersytetu Warszawskiego\n\nLidarowe oczy\n\nRYS. MAREK KONECKI\n\nJutro w Instytucie  odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar? \n\nPROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Nazywane też jest radarem laserowym.\n\nCzy to kosztowne urządzenie będzie służyło tylko naukowcom?\n\nTego typu lidar jest rzeczywiście drogi, kosztuje około  miliona marek niemieckich. Jest to najnowsza generacja tego typu lidarów.  DIAL - lidar absorbcji różnicowej  jest urządzeniem inteligentnym, to znaczy potrafi rozróżnić, co  mierzy. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen. Z lidara korzyść mamy potrójną: użyteczną, bo przy jego pomocy wykonujemy pomiary skażeń atmosferycznych, korzyść naukową - rozwijamy badania nad tym urządzeniem, staramy się m.in. rozszerzyć jego zastosowanie także na inne substancje występujące w atmosferze.  I korzyść dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska. Nad lidarem pracują specjaliści od laserów i od komputerów. Współpracujemy z doskonałym laboratorium prof. Ludgera Wöste z Freie Universitat Berlin rozwijającym m.in. problematykę lidarową. Pakiet software'u   wzbogacamy o nowe algorytmy, które potrafią lepiej i dokładniej rozszyfrowywać sygnał lidarowy, a w konsekwencji skażenia.  Żeby przetworzyć tzw. sygnał lidarowy, czyli to co wraca po rozproszeniu światła do układu, i otrzymać rozsądne dane dotyczące rozkładu koncentracji - trzeba dokonać skomplikowanych operacji. \n\nBadania, które prowadzimy, są zainicjowane i finansowane  przez Fundację Współpracy Polsko-Niemieckiej, dzięki której ten lidar u nas zaistniał i dla której w ramach naszych zobowiązań  wykonujemy pomiary zanieczyszczeń nad naszą wspólną granicą.  Zasadniczy koszt jego budowy pokryła uzyskana od Fundacji dotacja.  Część pieniędzy przekazał też Narodowy Fundusz Ochrony Środowiska i Gospodarki Wodnej oraz Komitet Badań Naukowych.\n\nCzy wszystkie zanieczyszczenia będzie można wykryć za pomocą lidaru?\n\nNie ma takiego jednostkowego urządzenia, które by wykrywało i mierzyło wszystkie szkodliwe gazy w atmosferze łącznie z dostarczeniem informacji o ich rozkładzie. Ale np. obecnie prowadzimy badania mające na celu rozszerzenie możliwości lidaru o taką substancję jak fosgen.  Tym szkodliwym gazem może być  skażone  powietrze  w  miastach, w których zlokalizowane są zakłady chemiczne, np. w Bydgoszczy pewne ilości fosgenu emitują Zakłady Chemiczne Organika- Zachem. \n\nLidar typu DIAL jest oparty na pomiarze absorbcji różnicowej, czyli muszą być zastosowane dwie wiązki laserowe o dwóch różnych długościach fali, z których jedna jest absorbowana, a druga nie jest absorbowana przez substancję, którą chcemy wykryć. Cząsteczki, które wykrywamy mają pasma absorbcji w bliskim nadfiolecie. Możemy np. badać zawartość ozonu w troposferze. Okazuje się bowiem, że o ile brak tego gazu w wysokich warstwach atmosfery powoduje groźny efekt cieplarniany, to jego nadmiar tuż nad Ziemią jest szkodliwy. Groźne są też substancje gazowe, jak np. tlenki azotu, będące następstwem spalin samochodowych. A samochodów przybywa.\n\nCzy stać nas będzie na prowadzenie pomiarów ozonu w miastach? \n\nKoszt jednego dnia kampanii pomiarowej firmy zachodnie szacują na kilka tysięcy DM. Potrzebne są pieniądze na utrzymanie lidaru, na prowadzenie badań. Nasze przedsięwzięcie nie ma charakteru komercyjnego. Koszt pomiarów będzie znacznie niższy.  Chcemy np. mierzyć w Warszawie rozkłady  koncentracji tlenków azotu, ich ewolucję czasową nad różnymi arteriami miasta. Chcielibyśmy rozwinąć tutaj współpracę z państwowymi i wojewódzkimi służbami ochrony środowiska. Tego typu badania były prowadzone np. w Lyonie. Okazało się,  że najwięcej tlenków azotu występuje niekoniecznie  tam gdzie są one produkowane, to znaczy nie przy najruchliwszych ulicach, jeśli są one dobrze wentylowane a gromadzą się one  w małych uliczkach. Przede wszystkim jednak do końca tego roku zamierzamy zakończyć pomiary  skażeń atmosferycznych nad granicą polsko-niemiecką. Koncentrujemy się głównie na Czarnym Trójkącie - obszarze u zbiegu trzech granic: Polski, Niemiec i Czech, do niedawna uważanym za najbardziej zdegradowany region w Europie. Prowadziliśmy pomiary w samym Turowie, gdzie elektrownia Turoszowska jest głównym  źródłem emisji. W planie mamy Bogatynię, zagłębie miedziowe.   \n\nW Czarnym Trójkącie istnieje wiele stacjonarnych stacji monitoringowych.\n\nNasz lidar ma większe możliwości niż stacje monitoringowe. Mierzy zanieczyszczenia nie tylko lokalnie, ale też ich rozkład w przestrzeni, z wysoką rozdzielczością przestrzenną i na odległość kilku kilometrów.  Możemy zatem śledzić ewolucję rozprzestrzeniania się tych zanieczyszczeń, ich kierunek i zmiany spowodowane m.in. warunkami atmosferycznymi. Wyniki naszych pomiarów porównujemy z  danymi uzyskanymi ze stacji monitoringowych.  \n\nJak wypadł Czarny Trójkąt?\n\nKiedy występowaliśmy  o finansowanie tego projektu do Fundacji Współpracy Polsko-Niemieckiej zanieczyszczenie powietrza w Czarnym Trójkącie było dużo większe niż obecnie i wszystko wskazuje na to, że będzie dalej spadać. Obecnie stężenie dwutlenku siarki jest na granicy naszych możliwości pomiarowych. Dla regionu Turoszowskiego to dobra wiadomość i dla stosunków polsko-niemieckich też.\n\nTypów lidarów jest wiele  \n\nTen lidar pracuje w obszarze bliskiego nadfioletu i promieniowania widzialnego, które jest wynikiem wykorzystania drugiej lub trzeciej harmonicznej lasera szafirowego, pracującego na granicy czerwieni i podczerwieni. DIAL jest tym typem lidara, który dzisiaj ma zdecydowanie największe wzięcie w ochronie środowiska. Z lidarów korzysta meteorologia. W Stanach Zjednoczonych lidary umieszcza się na satelitach (program NASA). Określają na przestrzeni kilkudziesięciu kilometrów rozkłady temperatury, wilgotności, ciśnienia, a także prędkości wiatru. Wykrywają pojawianie się huraganów, a nawet mogą określać rozmiary oka tajfunu.\n\nIle takich urządzeń jest w Europie?\n\n- W Europie takich lidarów jak nasz jest zaledwie kilka. Większość z nich mierzy ozon, dwutlenek siarki i tlenek azotu. Wykrywanie toluenu i benzenu jest oryginalnym rozwiązaniem. Długość fali dla benzenu jest już na skraju możliwości widmowych.  Nasz lidar typu DIAL jest najnowocześniejszym w Polsce. Ponadto jest lidarem ruchomym, zainstalowanym na samochodzie.  Ale  historia lidarów w naszym kraju jest dłuższa i zaczęła się na początku lat 60. Pierwsze próby  prowadzone były w stacji geofizycznej PAN  w Belsku, niedługo po skonstruowaniu pierwszego w świecie lasera  rubinowego. Potem powstał lidar stacjonarny, również typu DIAL, w Gdańsku, a w Krakowie sodary - urządzenia oparte na falach akustycznych, wygodne np. do pomiarów szybkości wiatru. Lidar umieszczony na samochodzie i zbudowany w latach 80  na Politechnice Poznańskiej w perspektywie miał być lidarem typu DIAL.\n\nFizycy dotychczas nie zajmowali się ochroną środowiska?\n\nTaka specjalizacja powstala na Wydziale Fizyki UW dwa lata temu. Gwarancją sukcesu naszego programu dydaktyczno-badawczego jest udział w nim zakładów należących do Instytutu Fizyki Doświadczalnej UW, Pracowni Przetwarzania Informacji (zdjęć satelitarnych) Instytutu Geofizyki i, co bardzo ważne, współpraca z Freie Universität Berlin. Mamy również na UW Międzywydziałowe Studia Ochrony Środowiska i studentom przekazujemy informacje o lidarze i fizycznych metodach badania środowiska. Nasze działania dydaktyczne bardzo efektywnie wspiera NFOŚ.\n\nRozmawiała Krystyna Forowicz",
 'date': '1997-04-21',
 'id': '199704210011',
 'section': 'Nauka i Technika',
 'summaries': {'author': ['I',
   'I',
   'I',
   'C',
   'C',
   'C',
   'K',
   'K',
   'K',
   'G',
   'G',
   'G',
   'J',
   'J',
   'J'],
  'body': ['Jutro w Instytucie  odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar?PROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Nazywane też jest radarem laserowym.Czy to kosztowne urządzenie będzie służyło tylko naukowcom? Z lidara korzyść mamy potrójną: użyteczną, bo przy jego pomocy wykonujemy pomiary skażeń atmosferycznych, naukową - rozwijamy badania nad tym urządzeniem. I korzyść dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska. Badania, które prowadzimy, są zainicjowane i finansowane  przez Fundację Współpracy Polsko-Niemieckiej, dzięki której ten lidar u nas zaistniał i dla której w ramach naszych zobowiązań  wykonujemy pomiary zanieczyszczeń nad naszą wspólną granicą.',
   'Jutro w Instytucie  odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar?PROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Nazywane też jest radarem laserowym.Czy to kosztowne urządzenie będzie służyło tylko naukowcom? Z lidara korzyść mamy potrójną: użyteczną, bo przy jego pomocy wykonujemy pomiary skażeń atmosferycznych, naukową - rozwijamy badania nad tym urządzeniem. I korzyść dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska. Badania, które prowadzimy, są zainicjowane i finansowane  przez Fundację Współpracy Polsko-Niemieckiej, dzięki której ten lidar u nas zaistniał i dla której w ramach naszych zobowiązań  wykonujemy pomiary zanieczyszczeń nad naszą wspólną granicą. Czy wszystkie zanieczyszczenia będzie można wykryć za pomocą lidaru?Nie ma takiego jednostkowego urządzenia, które by wykrywało i mierzyło wszystkie szkodliwe gazy w atmosferze łącznie z dostarczeniem informacji o ich rozkładzie. Możemy np. badać zawartość ozonu w troposferze. W Europie takich lidarów jak nasz jest zaledwie kilka. Większość z nich mierzy ozon, dwutlenek siarki i tlenek azotu. Fizycy dotychczas nie zajmowali się ochroną środowiska?Taka specjalizacja powstala na Wydziale Fizyki UW dwa lata temu. Gwarancją sukcesu naszego programu dydaktyczno-badawczego jest udział w nim zakładów należących do Instytutu Fizyki Doświadczalnej UW, Pracowni Przetwarzania Informacji Instytutu Geofizyki i współpraca z Freie Universität Berlin.',
   'Jutro w Instytucie  odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar?PROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Nazywane też jest radarem laserowym. Badania, które prowadzimy, są zainicjowane i finansowane  przez Fundację Współpracy Polsko-Niemieckiej, dzięki której ten lidar u nas zaistniał.',
   'Jutro odbędzie sie pokaz nowego polskiego lidara typu DIAL. lidar Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. DIAL - lidar absorbcji różnicowej  jest urządzeniem inteligentnym, to znaczy potrafi rozróżnić, co  mierzy. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen. Z lidara korzyść mamy potrójną: użyteczną, naukową I dydaktyczną. Żeby przetworzyć sygnał lidarowy, czyli to co wraca po rozproszeniu światła do układu, i otrzymać dane dotyczące rozkładu koncentracji - trzeba dokonać skomplikowanych operacji. muszą być zastosowane dwie wiązki laserowe o dwóch różnych długościach fali, z których jedna jest absorbowana, a druga nie jest absorbowana przez substancję, którą chcemy wykryć.',
   'Jutro odbędzie sie pokaz nowego polskiego lidara typu DIAL. lidar Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Nazywane też jest radarem laserowym. Jest to najnowsza generacja tego typu lidarów.  DIAL - lidar absorbcji różnicowej  jest urządzeniem inteligentnym, to znaczy potrafi rozróżnić, co  mierzy. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen. Z lidara korzyść mamy potrójną: użyteczną, bo przy jego pomocy wykonujemy pomiary skażeń atmosferycznych, korzyść naukową - rozwijamy badania nad tym urządzeniem.  I korzyść dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska. Żeby przetworzyć tzw. sygnał lidarowy, czyli to co wraca po rozproszeniu światła do układu, i otrzymać rozsądne dane dotyczące rozkładu koncentracji - trzeba dokonać skomplikowanych operacji. Badania, które prowadzimy, są zainicjowane i finansowane  przez Fundację Współpracy Polsko-Niemieckiej, dzięki której ten lidar u nas zaistniał i dla której w ramach naszych zobowiązań  wykonujemy pomiary zanieczyszczeń nad naszą wspólną granicą.  Zasadniczy koszt jego budowy pokryła uzyskana od Fundacji dotacja.  Część pieniędzy przekazał też Narodowy Fundusz Ochrony Środowiska i Gospodarki Wodnej oraz Komitet Badań Naukowych. Lidar typu DIAL jest oparty na pomiarze absorbcji różnicowej, czyli muszą być zastosowane dwie wiązki laserowe o dwóch różnych długościach fali, z których jedna jest absorbowana, a druga nie jest absorbowana przez substancję, którą chcemy wykryć.',
   'Jutro odbędzie sie pokaz nowego polskiego lidara typu DIAL. lidar Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. DIAL - lidar absorbcji różnicowej  jest urządzeniem inteligentnym, to znaczy potrafi rozróżnić, co  mierzy. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen. Z lidara korzyść mamy potrójną: użyteczną, naukową I dydaktyczną.',
   'Jutro w Instytucie  odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar? \nPROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Nazywane też jest radarem laserowym. DIAL - lidar absorbcji różnicowej  jest urządzeniem inteligentnym, to znaczy potrafi rozróżnić, co  mierzy. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen. Z lidara korzyść mamy potrójną: użyteczną, bo przy jego pomocy wykonujemy pomiary skażeń atmosferycznych, korzyść naukową - rozwijamy badania nad tym urządzeniem I korzyść dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.Nasz lidar ma większe możliwości niż stacje monitoringowe. Mierzy zanieczyszczenia nie tylko lokalnie, ale też ich rozkład w przestrzeni, z wysoką rozdzielczością przestrzenną i na odległość kilku kilometrów.',
   'Jutro w Instytucie  odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar? \nPROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Nazywane też jest radarem laserowym.Tego typu lidar jest drogi, kosztuje około  miliona marek niemieckich. DIAL - lidar absorbcji różnicowej  jest urządzeniem inteligentnym, to znaczy potrafi rozróżnić, co  mierzy. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen. Z lidara korzyść mamy potrójną: użyteczną, bo przy jego pomocy wykonujemy pomiary skażeń atmosferycznych, korzyść naukową - rozwijamy badania nad tym urządzeniem, staramy się m.in. rozszerzyć jego zastosowanie także na inne substancje występujące w atmosferze. I korzyść dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.Lidar typu DIAL jest oparty na pomiarze absorbcji różnicowej, czyli muszą być zastosowane dwie wiązki laserowe o dwóch różnych długościach fali, z których jedna jest absorbowana, a druga nie jest absorbowana przez substancję, którą chcemy wykryć. Cząsteczki, które wykrywamy mają pasma absorbcji w bliskim nadfiolecie.Nasz lidar ma większe możliwości niż stacje monitoringowe. Mierzy zanieczyszczenia nie tylko lokalnie, ale też ich rozkład w przestrzeni, z wysoką rozdzielczością przestrzenną i na odległość kilku kilometrów.  Możemy zatem śledzić ewolucję rozprzestrzeniania się tych zanieczyszczeń, ich kierunek i zmiany spowodowane m.in. warunkami atmosferycznymi. Wyniki naszych pomiarów porównujemy z  danymi uzyskanymi ze stacji monitoringowych.',
   'Jutro w Instytucie  odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar? \nPROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi.   Z lidara korzyść mamy potrójną: użyteczną, bo przy jego pomocy wykonujemy pomiary skażeń atmosferycznych, korzyść naukową i dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.',
   'Jutro odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar? \n\nPROF. KRZYSZTOF ERNST: urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi.\nto najnowsza generacja tego typu lidarów. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen.  korzyść mamy potrójną: użyteczną, przy jego pomocy wykonujemy pomiary skażeń atmosferycznych, naukową - rozwijamy badania nad urządzeniem I dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.\nNasze przedsięwzięcie nie ma charakteru komercyjnego. Chcemy np. mierzyć w Warszawie rozkłady koncentracji tlenków azotu. Koncentrujemy się głównie na Czarnym Trójkącie - obszarze u zbiegu granic: Polski, Niemiec i Czech, do niedawna uważanym za najbardziej zdegradowany region w Europie.',
   'Jutro odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar? \n\nPROF. KRZYSZTOF ERNST: urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi.\n\nto kosztowne urządzenie będzie służyło tylko naukowcom?\n\nlidar jest rzeczywiście drogi. to najnowsza generacja tego typu lidarów. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen.  korzyść mamy potrójną: użyteczną, przy jego pomocy wykonujemy pomiary skażeń atmosferycznych, naukową - rozwijamy badania nad tym urządzeniem I dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.\n\nCzy wszystkie zanieczyszczenia będzie można wykryć za pomocą lidaru?\n\nNie ma takiego jednostkowego urządzenia, które by wykrywało i mierzyło wszystkie szkodliwe gazy w atmosferze. Ale prowadzimy badania mające na celu rozszerzenie możliwości lidaru o taką substancję jak fosgen.\n\nstać nas będzie na prowadzenie pomiarów ozonu w miastach? \n\nNasze przedsięwzięcie nie ma charakteru komercyjnego. Chcemy np. mierzyć w Warszawie rozkłady koncentracji tlenków azotu, ich ewolucję czasową nad różnymi arteriami miasta. Koncentrujemy się głównie na Czarnym Trójkącie - obszarze u zbiegu granic: Polski, Niemiec i Czech, do niedawna uważanym za najbardziej zdegradowany region w Europie. zanieczyszczenie było dużo większe niż obecnie i wszystko wskazuje na to, że będzie dalej spadać.\nDIAL dzisiaj ma zdecydowanie największe wzięcie w ochronie środowiska. \n\nFizycy dotychczas nie zajmowali się ochroną środowiska?\n\nTaka specjalizacja powstala na Wydziale Fizyki UW dwa lata temu.',
   'Co to jest lidar? \n\nPROF. KRZYSZTOF ERNST: urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi.\nto najnowsza generacja tego typu lidarów. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen.  korzyść mamy potrójną: użyteczną, wykonujemy pomiary skażeń atmosferycznych, naukową - rozwijamy badania nad urządzeniem I dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.',
   'Co to jest lidar? \nPROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen. staramy się rozszerzyć jego zastosowanie na inne substancje występujące w atmosferze. Badania, które prowadzimy, są zainicjowane i finansowane  przez Fundację Współpracy Polsko-Niemieckiej. zamierzamy zakończyć pomiary  skażeń atmosferycznych nad granicą polsko-niemiecką. Nasz lidar ma większe możliwości niż stacje monitoringowe. Możemy śledzić ewolucję rozprzestrzeniania się zanieczyszczeń, ich kierunek i zmiany. Gwarancją sukcesu naszego programu dydaktyczno-badawczego jest udział w nim zakładów należących do Instytutu Fizyki Doświadczalnej UW, Pracowni Przetwarzania Informacji Instytutu Geofizyki i współpraca z Freie Universität Berlin.',
   "Co to jest lidar? \nPROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. DIAL - lidar absorbcji różnicowej potrafi rozróżnić, co  mierzy. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen. staramy się rozszerzyć jego zastosowanie także na inne substancje występujące w atmosferze. Pakiet software'u wzbogacamy o nowe algorytmy, które potrafią dokładniej rozszyfrowywać sygnał lidarowy, a w konsekwencji skażenia. Badania, które prowadzimy, są zainicjowane i finansowane  przez Fundację Współpracy Polsko-Niemieckiej. \n\nChcemy mierzyć w Warszawie rozkłady  koncentracji tlenków azotu, ich ewolucję czasową nad różnymi arteriami miasta. zamierzamy zakończyć pomiary  skażeń atmosferycznych nad granicą polsko-niemiecką. Nasz lidar ma większe możliwości niż stacje monitoringowe. Możemy śledzić ewolucję rozprzestrzeniania się zanieczyszczeń, ich kierunek i zmiany spowodowane m.in. warunkami atmosferycznymi. \n\nDIAL jest tym typem lidara, który dzisiaj ma największe wzięcie w ochronie środowiska. Z lidarów korzysta meteorologia. W Europie takich lidarów jak nasz jest zaledwie kilka. Nasz lidar jest najnowocześniejszym w Polsce. Ponadto jest lidarem ruchomym, zainstalowanym na samochodzie.  \n\nFizycy dotychczas nie zajmowali się ochroną środowiska?\nTaka specjalizacja powstala na Wydziale Fizyki UW dwa lata temu. Gwarancją sukcesu naszego programu dydaktyczno-badawczego jest udział w nim zakładów należących do Instytutu Fizyki Doświadczalnej UW, Pracowni Przetwarzania Informacji Instytutu Geofizyki i współpraca z Freie Universität Berlin.",
   'Co to jest lidar? \nPROF. KRZYSZTOF  ERNST: to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen. zamierzamy zakończyć pomiary  skażeń atmosferycznych nad granicą polsko-niemiecką. Nasz lidar ma większe możliwości niż stacje monitoringowe. Możemy śledzić ewolucję rozprzestrzeniania się zanieczyszczeń, ich kierunek i zmiany.'],
  'ratio': [10, 20, 5, 10, 20, 5, 10, 20, 5, 10, 20, 5, 10, 20, 5],
  'spans': [{'end': [244, 396, 457, 867, 922, 1022, 1103, 1877],
    'span_text': ['Jutro w Instytucie  odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar?',
     'PROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Nazywane też jest radarem laserowym.',
     'Czy to kosztowne urządzenie będzie służyło tylko naukowcom?',
     'Z lidara korzyść mamy potrójną: użyteczną, bo przy jego pomocy wykonujemy pomiary skażeń atmosferycznych,',
     'naukową - rozwijamy badania nad tym urządzeniem',
     '.',
     'I korzyść dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.',
     'Badania, które prowadzimy, są zainicjowane i finansowane  przez Fundację Współpracy Polsko-Niemieckiej, dzięki której ten lidar u nas zaistniał i dla której w ramach naszych zobowiązań  wykonujemy pomiary zanieczyszczeń nad naszą wspólną granicą.'],
    'start': [153, 247, 398, 760, 875, 1020, 1023, 1631]},
   {'end': [244,
     396,
     457,
     867,
     922,
     1022,
     1103,
     1878,
     2132,
     2296,
     2969,
     6225,
     6985,
     7047,
     7282,
     7326,
     7383],
    'span_text': ['Jutro w Instytucie  odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar?',
     'PROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Nazywane też jest radarem laserowym.',
     'Czy to kosztowne urządzenie będzie służyło tylko naukowcom?',
     'Z lidara korzyść mamy potrójną: użyteczną, bo przy jego pomocy wykonujemy pomiary skażeń atmosferycznych,',
     'naukową - rozwijamy badania nad tym urządzeniem',
     '.',
     'I korzyść dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.',
     'Badania, które prowadzimy, są zainicjowane i finansowane  przez Fundację Współpracy Polsko-Niemieckiej, dzięki której ten lidar u nas zaistniał i dla której w ramach naszych zobowiązań  wykonujemy pomiary zanieczyszczeń nad naszą wspólną granicą.',
     'Czy wszystkie zanieczyszczenia będzie można wykryć za pomocą lidaru?',
     'Nie ma takiego jednostkowego urządzenia, które by wykrywało i mierzyło wszystkie szkodliwe gazy w atmosferze łącznie z dostarczeniem informacji o ich rozkładzie.',
     'Możemy np. badać zawartość ozonu w troposferze.',
     'W Europie takich lidarów jak nasz jest zaledwie kilka. Większość z nich mierzy ozon, dwutlenek siarki i tlenek azotu.',
     '',
     'Fizycy dotychczas nie zajmowali się ochroną środowiska?',
     'Taka specjalizacja powstala na Wydziale Fizyki UW dwa lata temu. Gwarancją sukcesu naszego programu dydaktyczno-badawczego jest udział w nim zakładów należących do Instytutu Fizyki Doświadczalnej UW, Pracowni Przetwarzania Informacji',
     'Instytutu Geofizyki i',
     'współpraca z Freie Universität Berlin.'],
    'start': [153,
     247,
     398,
     760,
     875,
     1020,
     1023,
     1631,
     2064,
     2134,
     2921,
     6108,
     6984,
     6992,
     7049,
     7304,
     7344]},
   {'end': [244, 396, 1103, 1774, 1877],
    'span_text': ['Jutro w Instytucie  odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar?',
     'PROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Nazywane też jest radarem laserowym.',
     '',
     'Badania, które prowadzimy, są zainicjowane i finansowane  przez Fundację Współpracy Polsko-Niemieckiej, dzięki której ten lidar u nas zaistniał',
     '.'],
    'start': [153, 247, 1102, 1631, 1876]},
   {'end': [159,
     227,
     243,
     360,
     804,
     882,
     1025,
     1044,
     1103,
     1454,
     1540,
     1629,
     2848],
    'span_text': ['Jutro',
     'odbędzie sie pokaz nowego polskiego lidara typu DIAL.',
     'lidar',
     'Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi.',
     'DIAL - lidar absorbcji różnicowej  jest urządzeniem inteligentnym, to znaczy potrafi rozróżnić, co  mierzy. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen. Z lidara korzyść mamy potrójną: użyteczną,',
     'naukową',
     'I',
     'dydaktyczną',
     '.',
     'Żeby przetworzyć',
     'sygnał lidarowy, czyli to co wraca po rozproszeniu światła do układu, i otrzymać',
     'dane dotyczące rozkładu koncentracji - trzeba dokonać skomplikowanych operacji.',
     'muszą być zastosowane dwie wiązki laserowe o dwóch różnych długościach fali, z których jedna jest absorbowana, a druga nie jest absorbowana przez substancję, którą chcemy wykryć.'],
    'start': [153,
     173,
     238,
     270,
     591,
     875,
     1022,
     1033,
     1101,
     1437,
     1459,
     1549,
     2670]},
   {'end': [159, 227, 243, 396, 922, 1103, 1629, 2062, 2582, 2848],
    'span_text': ['Jutro',
     'odbędzie sie pokaz nowego polskiego lidara typu DIAL.',
     'lidar',
     'Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Nazywane też jest radarem laserowym.',
     'Jest to najnowsza generacja tego typu lidarów.  DIAL - lidar absorbcji różnicowej  jest urządzeniem inteligentnym, to znaczy potrafi rozróżnić, co  mierzy. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen. Z lidara korzyść mamy potrójną: użyteczną, bo przy jego pomocy wykonujemy pomiary skażeń atmosferycznych, korzyść naukową - rozwijamy badania nad tym urządzeniem',
     '.  I korzyść dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.',
     'Żeby przetworzyć tzw. sygnał lidarowy, czyli to co wraca po rozproszeniu światła do układu, i otrzymać rozsądne dane dotyczące rozkładu koncentracji - trzeba dokonać skomplikowanych operacji.',
     'Badania, które prowadzimy, są zainicjowane i finansowane  przez Fundację Współpracy Polsko-Niemieckiej, dzięki której ten lidar u nas zaistniał i dla której w ramach naszych zobowiązań  wykonujemy pomiary zanieczyszczeń nad naszą wspólną granicą.  Zasadniczy koszt jego budowy pokryła uzyskana od Fundacji dotacja.  Część pieniędzy przekazał też Narodowy Fundusz Ochrony Środowiska i Gospodarki Wodnej oraz Komitet Badań Naukowych.',
     '',
     'Lidar typu DIAL jest oparty na pomiarze absorbcji różnicowej, czyli muszą być zastosowane dwie wiązki laserowe o dwóch różnych długościach fali, z których jedna jest absorbowana, a druga nie jest absorbowana przez substancję, którą chcemy wykryć.'],
    'start': [153, 173, 238, 270, 542, 1020, 1437, 1631, 2581, 2602]},
   {'end': [159, 227, 243, 360, 804, 882, 1025, 1044, 1102],
    'span_text': ['Jutro',
     'odbędzie sie pokaz nowego polskiego lidara typu DIAL.',
     'lidar',
     'Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi.',
     'DIAL - lidar absorbcji różnicowej  jest urządzeniem inteligentnym, to znaczy potrafi rozróżnić, co  mierzy. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen. Z lidara korzyść mamy potrójną: użyteczną,',
     'naukową',
     'I',
     'dydaktyczną',
     '.'],
    'start': [153, 173, 238, 270, 591, 875, 1022, 1033, 1101]},
   {'end': [246, 396, 922, 1102, 4763],
    'span_text': ['Jutro w Instytucie  odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar?',
     'PROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Nazywane też jest radarem laserowym.',
     'DIAL - lidar absorbcji różnicowej  jest urządzeniem inteligentnym, to znaczy potrafi rozróżnić, co  mierzy. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen. Z lidara korzyść mamy potrójną: użyteczną, bo przy jego pomocy wykonujemy pomiary skażeń atmosferycznych, korzyść naukową - rozwijamy badania nad tym urządzeniem',
     'I korzyść dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.',
     'Nasz lidar ma większe możliwości niż stacje monitoringowe. Mierzy zanieczyszczenia nie tylko lokalnie, ale też ich rozkład w przestrzeni, z wysoką rozdzielczością przestrzenną i na odległość kilku kilometrów.'],
    'start': [153, 247, 590, 1022, 4555]},
   {'end': [246, 396, 480, 542, 1021, 1102, 2920, 4989],
    'span_text': ['Jutro w Instytucie  odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar?',
     'PROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi. Nazywane też jest radarem laserowym.',
     'Tego typu lidar jest',
     'drogi, kosztuje około  miliona marek niemieckich.',
     'DIAL - lidar absorbcji różnicowej  jest urządzeniem inteligentnym, to znaczy potrafi rozróżnić, co  mierzy. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen. Z lidara korzyść mamy potrójną: użyteczną, bo przy jego pomocy wykonujemy pomiary skażeń atmosferycznych, korzyść naukową - rozwijamy badania nad tym urządzeniem, staramy się m.in. rozszerzyć jego zastosowanie także na inne substancje występujące w atmosferze.',
     'I korzyść dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.',
     'Lidar typu DIAL jest oparty na pomiarze absorbcji różnicowej, czyli muszą być zastosowane dwie wiązki laserowe o dwóch różnych długościach fali, z których jedna jest absorbowana, a druga nie jest absorbowana przez substancję, którą chcemy wykryć. Cząsteczki, które wykrywamy mają pasma absorbcji w bliskim nadfiolecie.',
     'Nasz lidar ma większe możliwości niż stacje monitoringowe. Mierzy zanieczyszczenia nie tylko lokalnie, ale też ich rozkład w przestrzeni, z wysoką rozdzielczością przestrzenną i na odległość kilku kilometrów.  Możemy zatem śledzić ewolucję rozprzestrzeniania się tych zanieczyszczeń, ich kierunek i zmiany spowodowane m.in. warunkami atmosferycznymi. Wyniki naszych pomiarów porównujemy z  danymi uzyskanymi ze stacji monitoringowych.'],
    'start': [153, 247, 459, 493, 590, 1022, 2602, 4555]},
   {'end': [246, 360, 626, 883, 920, 1102],
    'span_text': ['Jutro w Instytucie  odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar?',
     'PROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi.',
     '',
     'Z lidara korzyść mamy potrójną: użyteczną, bo przy jego pomocy wykonujemy pomiary skażeń atmosferycznych, korzyść naukową',
     'i',
     'dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.'],
    'start': [153, 247, 625, 760, 919, 1032]},
   {'end': [158,
     262,
     271,
     359,
     397,
     590,
     761,
     803,
     867,
     907,
     922,
     1025,
     1102,
     3311,
     3516,
     3595,
     3623,
     3675,
     4226,
     4332],
    'span_text': ['Jutro',
     'odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar? \n\nPROF. KRZYSZTOF',
     'ERNST:',
     'urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi.',
     '',
     'to najnowsza generacja tego typu lidarów.',
     'Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen.',
     'korzyść mamy potrójną: użyteczną,',
     'przy jego pomocy wykonujemy pomiary skażeń atmosferycznych,',
     'naukową - rozwijamy badania nad',
     'urządzeniem',
     'I',
     'dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.',
     '',
     'Nasze przedsięwzięcie nie ma charakteru komercyjnego.',
     'Chcemy np. mierzyć w Warszawie rozkłady',
     'koncentracji tlenków azotu',
     '.',
     'Koncentrujemy się głównie na Czarnym Trójkącie - obszarze u zbiegu',
     'granic: Polski, Niemiec i Czech, do niedawna uważanym za najbardziej zdegradowany region w Europie.'],
    'start': [153,
     172,
     263,
     279,
     396,
     548,
     699,
     769,
     806,
     875,
     911,
     1022,
     1033,
     3310,
     3462,
     3556,
     3596,
     3674,
     4158,
     4233]},
   {'end': [158,
     262,
     271,
     359,
     398,
     459,
     498,
     543,
     590,
     761,
     803,
     867,
     922,
     1025,
     1102,
     2242,
     2300,
     2406,
     3247,
     3311,
     3516,
     3595,
     3675,
     4226,
     4333,
     5130,
     5241,
     5439,
     5661,
     5756,
     7113],
    'span_text': ['Jutro',
     'odbędzie sie pokaz nowego polskiego lidara typu DIAL. Co to jest lidar? \n\nPROF. KRZYSZTOF',
     'ERNST:',
     'urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi.',
     '',
     'to kosztowne urządzenie będzie służyło tylko naukowcom?',
     'lidar jest rzeczywiście drogi',
     '.',
     'to najnowsza generacja tego typu lidarów.',
     'Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen.',
     'korzyść mamy potrójną: użyteczną,',
     'przy jego pomocy wykonujemy pomiary skażeń atmosferycznych,',
     'naukową - rozwijamy badania nad tym urządzeniem',
     'I',
     'dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.',
     'Czy wszystkie zanieczyszczenia będzie można wykryć za pomocą lidaru?\n\nNie ma takiego jednostkowego urządzenia, które by wykrywało i mierzyło wszystkie szkodliwe gazy w atmosferze',
     '. Ale',
     'prowadzimy badania mające na celu rozszerzenie możliwości lidaru o taką substancję jak fosgen.',
     '',
     'stać nas będzie na prowadzenie pomiarów ozonu w miastach?',
     'Nasze przedsięwzięcie nie ma charakteru komercyjnego.',
     'Chcemy np. mierzyć w Warszawie rozkłady',
     'koncentracji tlenków azotu, ich ewolucję czasową nad różnymi arteriami miasta.',
     'Koncentrujemy się głównie na Czarnym Trójkącie - obszarze u zbiegu',
     'granic: Polski, Niemiec i Czech, do niedawna uważanym za najbardziej zdegradowany region w Europie.',
     'zanieczyszczenie',
     'było dużo większe niż obecnie i wszystko wskazuje na to, że będzie dalej spadać.',
     '',
     'DIAL',
     'dzisiaj ma zdecydowanie największe wzięcie w ochronie środowiska.',
     'Fizycy dotychczas nie zajmowali się ochroną środowiska?\n\nTaka specjalizacja powstala na Wydziale Fizyki UW dwa lata temu.'],
    'start': [153,
     172,
     263,
     279,
     396,
     402,
     469,
     541,
     548,
     699,
     769,
     806,
     875,
     1022,
     1033,
     2062,
     2294,
     2312,
     3245,
     3251,
     3462,
     3556,
     3596,
     4158,
     4233,
     5114,
     5160,
     5438,
     5656,
     5690,
     6990]},
   {'end': [262, 271, 359, 397, 590, 761, 803, 807, 867, 907, 922, 1025, 1102],
    'span_text': ['Co to jest lidar? \n\nPROF. KRZYSZTOF',
     'ERNST:',
     'urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi.',
     '',
     'to najnowsza generacja tego typu lidarów.',
     'Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen.',
     'korzyść mamy potrójną: użyteczną,',
     '',
     'wykonujemy pomiary skażeń atmosferycznych,',
     'naukową - rozwijamy badania nad',
     'urządzeniem',
     'I',
     'dydaktyczną - szkolimy studentów zainteresowanych ochroną środowiska.'],
    'start': [227,
     263,
     279,
     396,
     548,
     699,
     769,
     806,
     824,
     875,
     911,
     1022,
     1033]},
   {'end': [245,
     360,
     761,
     936,
     971,
     1022,
     1733,
     1878,
     4159,
     4614,
     4772,
     4818,
     4860,
     4906,
     7283,
     7326,
     7383],
    'span_text': ['Co to jest lidar?',
     'PROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi.',
     'Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen.',
     'staramy się',
     'rozszerzyć jego zastosowanie',
     'na inne substancje występujące w atmosferze.',
     'Badania, które prowadzimy, są zainicjowane i finansowane  przez Fundację Współpracy Polsko-Niemieckiej',
     '.',
     'zamierzamy zakończyć pomiary  skażeń atmosferycznych nad granicą polsko-niemiecką.',
     'Nasz lidar ma większe możliwości niż stacje monitoringowe.',
     'Możemy',
     'śledzić ewolucję rozprzestrzeniania się',
     'zanieczyszczeń, ich kierunek i zmiany',
     '.',
     'Gwarancją sukcesu naszego programu dydaktyczno-badawczego jest udział w nim zakładów należących do Instytutu Fizyki Doświadczalnej UW, Pracowni Przetwarzania Informacji',
     'Instytutu Geofizyki i',
     'współpraca z Freie Universität Berlin.'],
    'start': [227,
     246,
     699,
     924,
     942,
     977,
     1631,
     1876,
     4076,
     4555,
     4765,
     4778,
     4823,
     4904,
     7114,
     7305,
     7344]},
   {'end': [245,
     360,
     625,
     761,
     936,
     1022,
     1311,
     1357,
     1436,
     1733,
     1878,
     3247,
     3311,
     3563,
     3676,
     4159,
     4614,
     4772,
     4818,
     4906,
     5410,
     5439,
     5701,
     5789,
     6163,
     6364,
     6472,
     7048,
     7283,
     7326,
     7383],
    'span_text': ['Co to jest lidar?',
     'PROF. KRZYSZTOF  ERNST: Jest to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi.',
     'DIAL - lidar absorbcji różnicowej',
     'potrafi rozróżnić, co  mierzy. Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen.',
     'staramy się',
     'rozszerzyć jego zastosowanie także na inne substancje występujące w atmosferze.',
     "Pakiet software'u",
     'wzbogacamy o nowe algorytmy, które potrafią',
     'dokładniej rozszyfrowywać sygnał lidarowy, a w konsekwencji skażenia.',
     'Badania, które prowadzimy, są zainicjowane i finansowane  przez Fundację Współpracy Polsko-Niemieckiej',
     '.',
     '',
     '',
     'Chcemy',
     'mierzyć w Warszawie rozkłady  koncentracji tlenków azotu, ich ewolucję czasową nad różnymi arteriami miasta.',
     'zamierzamy zakończyć pomiary  skażeń atmosferycznych nad granicą polsko-niemiecką.',
     'Nasz lidar ma większe możliwości niż stacje monitoringowe.',
     'Możemy',
     'śledzić ewolucję rozprzestrzeniania się',
     'zanieczyszczeń, ich kierunek i zmiany spowodowane m.in. warunkami atmosferycznymi.',
     '',
     '',
     'DIAL jest tym typem lidara, który dzisiaj ma',
     'największe wzięcie w ochronie środowiska. Z lidarów korzysta meteorologia.',
     'W Europie takich lidarów jak nasz jest zaledwie kilka.',
     'Nasz lidar',
     'jest najnowocześniejszym w Polsce. Ponadto jest lidarem ruchomym, zainstalowanym na samochodzie.',
     'Fizycy dotychczas nie zajmowali się ochroną środowiska?',
     'Taka specjalizacja powstala na Wydziale Fizyki UW dwa lata temu. Gwarancją sukcesu naszego programu dydaktyczno-badawczego jest udział w nim zakładów należących do Instytutu Fizyki Doświadczalnej UW, Pracowni Przetwarzania Informacji',
     'Instytutu Geofizyki i',
     'współpraca z Freie Universität Berlin.'],
    'start': [227,
     246,
     591,
     668,
     924,
     942,
     1293,
     1313,
     1366,
     1631,
     1876,
     3246,
     3310,
     3556,
     3567,
     4076,
     4555,
     4765,
     4778,
     4823,
     5409,
     5438,
     5656,
     5714,
     6108,
     6353,
     6374,
     6990,
     7049,
     7305,
     7344]},
   {'end': [245, 271, 360, 761, 4159, 4614, 4772, 4818, 4860, 4905],
    'span_text': ['Co to jest lidar?',
     'PROF. KRZYSZTOF  ERNST:',
     'to urządzenie pozwalające wyznaczać zanieczyszczenia atmosfery metodami optycznymi.',
     'Wykrywa ozon, dwutlenek siarki, tlenki azotu, benzen, toluen.',
     'zamierzamy zakończyć pomiary  skażeń atmosferycznych nad granicą polsko-niemiecką.',
     'Nasz lidar ma większe możliwości niż stacje monitoringowe.',
     'Możemy',
     'śledzić ewolucję rozprzestrzeniania się',
     'zanieczyszczeń, ich kierunek i zmiany',
     '.'],
    'start': [227, 246, 276, 699, 4076, 4555, 4765, 4778, 4823, 4904]}],
  'type': ['extract',
   'extract',
   'extract',
   'extract',
   'extract',
   'extract',
   'extract',
   'extract',
   'extract',
   'extract',
   'extract',
   'extract',
   'extract',
   'extract',
   'extract']},
 'title': 'Lidarowe oczy'}
```

### Data Fields

- `id`: a `string` example identifier
- `date`: date of the original article (`string`)
- `title`: title of the original article (`string`)
- `section`: the section of the newspaper the original article belonged to (`string`)
- `authors`: original article authors (`string`)
- `body`: original article body (list of `string`s)
- `summaries`: a dictionary feature containing summaries of the original article with the following attributes:
  - `ratio`: ratio of summary - percentage of the original article (list of `int32`s)
  - `type`: type of summary - extractive (`extract`) or abstractive (`abstract`) (list of `string`s)
  - `author`: acronym of summary author (list of `string`)
  - `body`: body of summary (list of `string`)
  - `spans`:  a list containing spans for extractive summaries (empty for abstractive summaries):
    - `start`: start of span (`int32`)
    - `end`: end of span (`int32`)
    - `span_text`: span text (`string`)

### Data Splits

Single train split

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information
```
@inproceedings{
    ogro:kop:14:lrec,
    author = "Ogrodniczuk, Maciej and Kopeć, Mateusz",
    pdf = "http://nlp.ipipan.waw.pl/Bib/ogro:kop:14:lrec.pdf",
    title = "The {P}olish {S}ummaries {C}orpus",
    pages = "3712--3715",
    crossref = "lrec:14"
}
@proceedings{
    lrec:14,
    editor = "Calzolari, Nicoletta and Choukri, Khalid and Declerck, Thierry and Loftsson, Hrafn and Maegaard, Bente and Mariani, Joseph and Moreno, Asuncion and Odijk, Jan and Piperidis, Stelios",
    isbn = "978-2-9517408-8-4",
    title = "Proceedings of the Ninth International {C}onference on {L}anguage {R}esources and {E}valuation, {LREC}~2014",
    url = "http://www.lrec-conf.org/proceedings/lrec2014/index.html",
    booktitle = "Proceedings of the Ninth International {C}onference on {L}anguage {R}esources and {E}valuation, {LREC}~2014",
    address = "Reykjavík, Iceland",
    key = "LREC",
    year = "2014",
    organization = "European Language Resources Association (ELRA)"
}
```
### Contributions

Thanks to [@kldarek](https://github.com/kldarek) for adding this dataset.