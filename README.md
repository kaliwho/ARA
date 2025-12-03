# Aquabot Reactive Agent (ARA) - Wersja 1.0.41

To repozytorium zawiera skrypt Python dla Aquabot Reactive Agent (ARA), wersja 1.0.41. ARA jest zaprojektowany do automatyzacji działań w zewnętrznym środowisku gry lub symulacji "Aquabot", działając jako inteligentny agent zdolny do wykrywania otoczenia, zarządzania swoim wewnętrznym stanem i wykonywania reaktywnych strategii.

## Spis treści
- [Opis](#opis)
- [Funkcje](#funkcje)
- [Wymagania systemowe](#wymagania-systemowe)
- [Instalacja](#instalacja)
- [Użycie](#użycie)
- [Konfiguracja](#konfiguracja)
- [Zależności](#zależności)
- [Jak to działa](#jak-to-działa)
- [Rozwiązywanie problemów](#rozwiązywanie-problemów)
- [Rozwój i Współpraca](#rozwój-i-współpraca)
- [Licencja](#licencja)

## Opis

ARA 1.0.41 to zaawansowany agent reaktywny opracowany do nawigowania, interakcji i podejmowania decyzji w czasie rzeczywistym w środowisku "Aquabot". Przetwarza informacje o stanie gry otrzymane za pośrednictwem komunikacji międzyprocesowej (IPC) i reaguje, symulując wprowadzanie danych z klawiatury i wykonując predefiniowane działania. Podstawową siłą agenta jest jego zdolność do zarządzania złożonymi stanami wewnętrznymi, stosowania algorytmów wyszukiwania ścieżek i strategicznego podejmowania decyzji w celu osiągnięcia celów, takich jak zbieranie zasobów, angażowanie wrogów lub unikanie zagrożeń.

## Funkcje

- **Zarządzanie stanem:** Utrzymuje kompleksową wewnętrzną reprezentację świata gry, w tym:
    - Aktualne współrzędne (X, Y, Z) i orientację.
    - Poziomy zdrowia, amunicji i pieniędzy.
    - Aktywne przedmioty i ekwipunek.
    - Szczegółowe informacje o mapie, w tym odkryte obszary, przeszkody i interesujące miejsca.
- **Komunikacja międzyprocesowa (IPC):** Komunikuje się z aplikacją "Aquabot" za pomocą nazwanego potoku Windows (`\\.\pipe\AquaWarSDK` do wysyłania poleceń i `\\.\pipe\FromAquaWarSDK` do odbierania danych).
- **Symulacja wprowadzania z klawiatury:** Wykorzystuje `pynput` do symulowania naciśnięć klawiszy, umożliwiając agentowi kontrolowanie działań Aquabota w grze.
- **Wyszukiwanie ścieżek:** Implementuje algorytm wyszukiwania A* dla efektywnej nawigacji, umożliwiając botowi znajdowanie optymalnych ścieżek, jednocześnie unikając przeszkód i znanych zagrożeń na mapie gry.
- **Reaktywne podejmowanie decyzji:** Zawiera solidny moduł podejmowania decyzji, który ocenia bieżący stan gry i wybiera odpowiednie działania w oparciu o zdefiniowany zestaw zasad i priorytetów (np. atak, jeśli w zasięgu, zbieranie przedmiotów, jeśli jest mało, ucieczka, jeśli jest krytycznie uszkodzony).
- **Wykonywanie akcji:** Obsługuje szeroki zakres działań, w tym:
    - Ruch (do przodu, do tyłu, obracanie się).
    - Atakowanie (strzelanie).
    - Użycie przedmiotów (np. apteczki, ulepszenia).
    - Eksploracja mapy.
- **Dynamiczne dostosowywanie strategii:** Dostosowuje swoją strategię w oparciu o zmiany w środowisku gry w czasie rzeczywistym, takie jak obecność wroga, dostępne zasoby i stan zdrowia.

## Wymagania systemowe

- **System operacyjny:** Windows (ze względu na użycie nazwanego potoku i zgodność `pynput`).
- **Python:** Wersja 3.x (testowano z nowszymi wersjami Pythona 3).
- **Zewnętrzna aplikacja "Aquabot":** Specyficzna gra lub symulacja "Aquabot", z którą ARA jest zaprojektowany do interakcji. Ta aplikacja musi być uruchomiona i poprawnie skonfigurowana do komunikacji za pośrednictwem określonych nazwanego potoków.

## Instalacja

1.  **Sklonuj repozytorium (lub pobierz skrypt):**
    ```bash
    git clone https://github.com/twoja-nazwa-uzytkownika/aquabot-ara.git
    cd aquabot-ara
    ```
    (Uwaga: Zastąp `https://github.com/twoja-nazwa-uzytkownika/aquabot-ara.git` rzeczywistym adresem URL repozytorium, jeśli ten skrypt jest częścią większego projektu.)

2.  **Zainstaluj zależności Python:**
    ```bash
    pip install pynput
    ```

## Użycie

1.  **Upewnij się, że aplikacja "Aquabot" jest uruchomiona:** Gra/symulacja musi być aktywna i gotowa do komunikacji za pośrednictwem nazwanego potoku.
2.  **Uruchom skrypt ARA:**
    ```bash
    python ARA_1.0.41.py
    ```

    Po uruchomieniu skrypt spróbuje nawiązać komunikację z aplikacją Aquabot, monitorować jej stan i autonomicznie rozpocznie wykonywanie działań.

## Konfiguracja

Większość konfiguracji jest zakodowana na stałe w skrypcie `ARA_1.0.41.py`. Kluczowe parametry obejmują:

-   **Ścieżki do nazwanego potoku:**
    -   `pipe_to_aquawarsdk_name = r'\\.\pipe\AquaWarSDK'`
    -   `pipe_from_aquawarsdk_name = r'\\.\pipe\FromAquaWarSDK'`
    Można je zmodyfikować, jeśli środowisko Aquabot używa innych nazw potoków.
-   **Stałe specyficzne dla gry:** Wartości takie jak `MAX_HEALTH`, `MAX_AMMO`, `MAP_SIZE`, identyfikatory przedmiotów i mapowania klawiszy akcji są zdefiniowane w skrypcie. Dostosuj je do konkretnej wersji lub konfiguracji gry "Aquabot", której używasz.
-   **Progi decyzyjne:** Parametry wpływające na zachowanie bota, takie jak kiedy uciekać, kiedy atakować lub które przedmioty priorytetyzować, są osadzone w logice.

W przypadku znaczących zmian wymagana jest bezpośrednia modyfikacja pliku `ARA_1.0.41.py`.

## Zależności

-   `pynput`: Używany do kontrolowania i monitorowania urządzeń wejściowych, w szczególności do symulowania naciśnięć klawiszy.

## Jak to działa

Agent działa w ciągłej pętli:
1.  **Odbieranie stanu:** Odczytuje bieżące dane stanu gry z `\\.\pipe\FromAquaWarSDK`.
2.  **Aktualizacja modelu wewnętrznego:** Analizuje odebrane dane i aktualizuje swój obiekt `State`, który obejmuje mapę, statystyki bota i lokalizacje wrogów.
3.  **Wyszukiwanie ścieżek (jeśli jest potrzebne):** Jeśli cel jest ustawiony (np. przedmiot do zebrania, wróg do ścigania), algorytm A* oblicza optymalną ścieżkę.
4.  **Podejmowanie decyzji:** Na podstawie zaktualizowanego stanu i bieżących celów agent określa najbardziej odpowiednie działanie (np. ruch, strzał, użycie przedmiotu, zmiana celu).
5.  **Wykonanie akcji:** Wysyła polecenia (symulowane naciśnięcia klawiszy) do aplikacji "Aquabot" za pośrednictwem `\\.\pipe\AquaWarSDK`.

Ten reaktywny cykl pozwala agentowi dynamicznie reagować na zmiany w świecie gry.

## Rozwiązywanie problemów

-   **Problemy z połączeniem potoku:** Upewnij się, że aplikacja "Aquabot" jest uruchomiona i że ścieżki nazwanego potoku w `ARA_1.0.41.py` odpowiadają tym używanym przez aplikację.
-   **Uprawnienia `pynput`:** W niektórych systemach Windows `pynput` może wymagać specjalnych uprawnień do symulowania wprowadzania z klawiatury. Uruchom terminal lub IDE jako administrator, jeśli napotkasz problemy.
-   **Nieprawidłowe zachowanie:** Jeśli bot zachowuje się nieoczekiwanie, sprawdź, czy stałe specyficzne dla gry (np. rozmiar mapy, identyfikatory przedmiotów, przypisania klawiszy) w skrypcie dokładnie odzwierciedlają środowisko "Aquabot".
-   **Wydajność:** Duże mapy lub złożone stany gry mogą wpływać na wydajność wyszukiwania ścieżek. W razie potrzeby rozważ optymalizację implementacji A* lub uproszczenie reprezentacji mapy.

## Rozwój i Współpraca

Ten projekt jest rozwijany jako oprogramowanie open source. Zachęcamy wszystkich do wnoszenia wkładu w jego rozwój! Oto kilka sposobów, w jakie możesz pomóc:

-   **Zgłaszanie błędów:** Jeśli znajdziesz błąd, proszę zgłoś go w sekcji Issues (jeśli repozytorium jest hostowane na platformie takiej jak GitHub/GitLab). Podaj jak najwięcej szczegółów, aby pomóc w jego odtworzeniu i naprawieniu.
-   **Sugestie dotyczące funkcji:** Masz pomysł na nową funkcję lub ulepszenie? Otwórz Issue, aby to omówić.
-   **Wysyłanie żądań zmian (Pull Requests):** Jeśli masz poprawkę błędu, nową funkcję lub ulepszenie kodu, które chciałbyś włączyć, prześlij Pull Request. Upewnij się, że Twój kod jest zgodny z istniejącym stylem projektu i zawiera odpowiednie testy (jeśli dotyczy).

Twoja pomoc w udoskonalaniu ARA jest bardzo mile widziana!

## Licencja

Niniejsze oprogramowanie jest objęte licencją MIT.

Copyright (c) 2025 [Twoje Imię/Nazwa Organizacji - Jeśli to jest Twój projekt, zastąp ten tekst]

Niniejszym udziela się bezpłatnie każdej osobie uzyskującej kopię tego oprogramowania i powiązanych plików dokumentacji (dalej "Oprogramowanie") prawa do korzystania z Oprogramowania bez ograniczeń, w tym między innymi do praw do używania, kopiowania, modyfikowania, łączenia, publikowania, rozpowszechniania, sublicencjonowania i/lub sprzedawania kopii Oprogramowania, oraz do zezwalania osobom, którym Oprogramowanie zostało dostarczone, na to samo, z zastrzeżeniem następujących warunków:

Powyższa informacja o prawach autorskich i niniejsza informacja o zezwoleniu zostaną zawarte we wszystkich kopiach lub istotnych częściach Oprogramowania.

OPROGRAMOWANIE JEST DOSTARCZANE "TAKIE, JAKIE JEST", BEZ JAKIEJKOLWIEK GWARANCJI, WYRAŹNEJ ANI DOROZUMIANEJ, W TYM MIĘDZY INNYMI GWARANCJI PRZYDATNOŚCI HANDLOWEJ, PRZYDATNOŚCI DO OKREŚLONEGO CELU ORAZ NIENARUSZALNOŚCI PRAW. W ŻADNYM WYPADKU AUTORZY LUB POSIADACZE PRAW AUTORSKICH NIE BĘDĄ ODPOWIEDZIALNI ZA JAKIEKOLWIEK ROSZCZENIA, SZKODY LUB INNE ZOBOWIĄZANIA, CZY TO W WYNIKU DZIAŁANIA UMOWY, CZYNÓW NIEDOZWOLONYCH LUB W INNY SPOSÓB, WYNIKAJĄCE Z OPROGRAMOWANIA LUB W ZWIĄZKU Z UŻYWANIEM LUB INNYMI TRANSAKCJAMI W OPROGRAMOWANIU.