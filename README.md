# Android Root Assistant (ARA) - Wersja 1.0.41 - Darknet Edition

Ten projekt zawiera skrypt Python dla Android Root Assistant (ARA), wersja 1.0.41, w ulepszonej edycji Darknet. ARA to narzędzie zaprojektowane do pomagania użytkownikom w zarządzaniu, diagnozowaniu i potencjalnym rootowaniu urządzeń z systemem Android, oferujące interfejs graficzny w stylu terminala.

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

ARA 1.0.41 to rozbudowane narzędzie do zarządzania urządzeniami z systemem Android, zbudowane w oparciu o Python i Tkinter. Oferuje intuicyjny interfejs użytkownika przypominający terminal, umożliwiający wykrywanie urządzeń, zbieranie informacji systemowych, analizę bezpieczeństwa, przeglądanie logów `logcat` w czasie rzeczywistym oraz dostęp do potencjalnych metod rootowania. Jest to "Enhanced Darknet Edition", co odzwierciedla jego estetykę interfejsu oraz potencjalnie zaawansowane funkcje.

## Funkcje

-   **Wykrywanie Urządzeń Android:** Automatyczne wykrywanie podłączonych urządzeń Android za pomocą ADB (Android Debug Bridge).
-   **Szczegółowe Informacje o Urządzeniu:** Zbieranie i wyświetlanie kluczowych informacji o urządzeniu, takich jak model, producent, wersja Androida, SDK, architektura i identyfikator kompilacji.
-   **Analiza Statusu Roota:** Sprawdzanie, czy urządzenie jest zrootowane, oraz wykrywanie obecności Magisk.
-   **Skanowanie Bezpieczeństwa:** Podstawowa analiza zainstalowanych pakietów w poszukiwaniu podejrzanych aplikacji.
-   **Wyszukiwanie Metod Rootowania:** Dynamiczne sugerowanie potencjalnych metod rootowania w oparciu o wykryte informacje o urządzeniu (np. Magisk, Odin dla Samsunga, Mi Unlock dla Xiaomi, KingRoot dla starszych urządzeń).
-   **Strumień Logcat w Czasie Rzeczywistym:** Wyświetlanie i zapisywanie logów systemowych Androida (`logcat`) w czasie rzeczywistym.
-   **Zarządzanie Logami:** Możliwość zapisywania i czyszczenia logów systemowych oraz logów `logcat`.
-   **Zintegrowany Terminal Techniczny:** Umożliwia użytkownikowi wykonywanie niestandardowych poleceń `adb` lub `shell` bezpośrednio z aplikacji.
-   **Funkcje Rootowania (Placeholdery):** Przyciski i sekcje dla funkcji takich jak "Auto Root", "Choose Method", "Unlock Bootloader" i "Magisk Wizard", które są placeholderami do przyszłej implementacji lub wymagają ręcznej interwencji.
-   **Interfejs w Stylu Terminala:** Atrakcyjny interfejs graficzny (GUI) oparty na Tkinter, stylizowany na terminal, z ciemnym schematem kolorów i wyraźnymi czcionkami.

## Wymagania systemowe

-   **System operacyjny:** Windows (aplikacja korzysta z `subprocess` do wywoływania poleceń `adb` i `logcat`).
-   **Python:** Wersja 3.x (testowano z nowszymi wersjami Pythona 3).
-   **ADB (Android Debug Bridge):** Musi być zainstalowany i dostępny w zmiennych środowiskowych systemu (PATH).
-   **Urządzenie Android:** Fizyczne urządzenie z systemem Android z włączonym trybem debugowania USB, podłączone do komputera.

## Instalacja

1.  **Sklonuj repozytorium (lub pobierz skrypt):**
    ```bash
    git clone https://github.com/twoja-nazwa-uzytkownika/android-root-assistant.git
    cd android-root-assistant
    ```
    (Uwaga: Zastąp `https://github.com/twoja-nazwa-uzytkownika/android-root-assistant.git` rzeczywistym adresem URL repozytorium, jeśli ten skrypt jest częścią większego projektu.)

2.  **Zainstaluj zależności Python:**
    ```bash
    pip install "pynput<1.0"
    pip install psutil
    ```
    (Skrypt używa `tkinter`, który jest zazwyczaj dołączany do standardowych instalacji Pythona na Windowsie.)

3.  **Upewnij się, że ADB jest zainstalowane i działa:**
    -   Pobierz pakiet SDK Platform-Tools ze strony dla deweloperów Androida.
    -   Rozpakuj go i dodaj ścieżkę do folderu `platform-tools` do zmiennych środowiskowych systemu PATH.
    -   Sprawdź, czy `adb` działa, otwierając wiersz polecenia i wpisując `adb devices`.

## Użycie

1.  **Podłącz urządzenie Android:** Podłącz telefon lub tablet z Androidem do komputera za pomocą kabla USB. Upewnij się, że debugowanie USB jest włączone w opcjach deweloperskich urządzenia.
2.  **Uruchom skrypt ARA:**
    ```bash
    python ARA_1.0.41.py
    ```
    Aplikacja uruchomi się, automatycznie sprawdzi połączenie ADB i spróbuje wykryć podłączone urządzenie.
3.  **Skanowanie Urządzenia:** Kliknij przycisk "🔍 SCAN", aby zebrać informacje o urządzeniu, statusie rootowania i dostępnych metodach.
4.  **Logcat:** Użyj przycisków w panelu "LIVE LOGCAT STREAM", aby uruchomić, zatrzymać, zapisać lub wyczyścić strumień logów Androida.
5.  **Terminal Techniczny:** Wpisz polecenia `adb` lub `shell` w polu tekstowym "TECHNICAL SHELL ACCESS" i naciśnij Enter lub kliknij "EXECUTE", aby wykonać je na urządzeniu.

## Konfiguracja

Większość konfiguracji jest wbudowana w kod źródłowy `ARA_1.0.41.py`. Użytkownik może edytować plik, aby:

-   Zmienić ścieżki katalogów roboczych (`WORK_DIR`, `DOWNLOADS_DIR`, `LOGS_DIR`).
-   Dostosować stałe interfejsu użytkownika, takie jak czcionki i schematy kolorów w sekcji `self.colors`.
-   Modyfikować logikę wykrywania metod rootowania w funkcji `detect_root_methods_advanced`.

## Zależności

-   `tkinter`: Standardowa biblioteka GUI dla Pythona (zazwyczaj wbudowana).
-   `subprocess`: Do uruchamiania poleceń systemowych (np. `adb`).
-   `threading`: Do operacji asynchronicznych (np. strumień `logcat`).
-   `pathlib`, `os`, `sys`, `shutil`: Standardowe moduły Pythona do operacji na plikach i systemie.
-   `datetime`: Do zarządzania czasem i datami.
-   `pynput` (wspomniane w wymaganiach instalacyjnych, chociaż w dostarczonym kodzie nie ma bezpośredniego użycia, co sugeruje, że mogło być przeznaczone do innych interakcji lub jest częścią niewykorzystanego kodu).

## Jak to działa

ARA działa jako aplikacja desktopowa z GUI:
1.  **Inicjalizacja:** Po uruchomieniu, aplikacja inicjuje interfejs użytkownika i automatycznie sprawdza obecność ADB oraz status połączenia urządzenia.
2.  **Skanowanie:** Po kliknięciu "SCAN", zbierane są informacje o urządzeniu za pomocą poleceń `adb shell getprop`, analizowany jest status rootowania (`which su`, `pm list packages | grep magisk`), a także przeprowadzana jest podstawowa analiza bezpieczeństwa.
3.  **Wykrywanie Metod Rootowania:** Na podstawie zebranych danych o urządzeniu, skrypt sugeruje potencjalne metody rootowania, takie jak Magisk, Odin czy KingRoot, przedstawiając ich kompatybilność i kroki.
4.  **Strumieniowanie Logcat:** Osobny wątek uruchamia `adb logcat` i w czasie rzeczywistym przesyła dane do okna tekstowego GUI.
5.  **Terminal Techniczny:** Umożliwia bezpośrednie wykonywanie poleceń `adb` i wyświetlanie wyników w osobnym panelu terminala.

## Rozwiązywanie problemów

-   **"ADB: NOT FOUND":** Upewnij się, że ADB jest poprawnie zainstalowane, a ścieżka do folderu `platform-tools` jest dodana do zmiennych środowiskowych PATH.
-   **"DEVICE: OFFLINE" / Brak wykrycia urządzenia:**
    -   Sprawdź połączenie kablowe USB.
    -   Upewnij się, że debugowanie USB jest włączone w opcjach deweloperskich urządzenia Android.
    -   Spróbuj ponownie uruchomić `adb server` ręcznie: `adb kill-server`, a następnie `adb start-server`.
-   **Problemy z `logcat`:** Jeśli strumień `logcat` nie działa, upewnij się, że ADB jest połączone z urządzeniem i że urządzenie zezwoliło na debugowanie USB.
-   **Brak reakcji GUI:** Jeśli aplikacja przestanie odpowiadać, może to być spowodowane problemem z wątkami. Spróbuj ponownie uruchomić aplikację.

## Rozwój i Współpraca

Ten projekt jest rozwijany jako oprogramowanie open source. Zachęcamy wszystkich do wnoszenia wkładu w jego rozwój! Oto kilka sposobów, w jakie możesz pomóc:

-   **Zgłaszanie błędów:** Jeśli znajdziesz błąd, proszę zgłoś go w sekcji Issues (jeśli repozytorium jest hostowane na platformie takiej jak GitHub/GitLab). Podaj jak najwięcej szczegółów, aby pomóc w jego odtworzeniu i naprawieniu.
-   **Sugestie dotyczące funkcji:** Masz pomysł na nową funkcję lub ulepszenie? Otwórz Issue, aby to omówić.
-   **Wysyłanie żądań zmian (Pull Requests):** Jeśli masz poprawkę błędu, nową funkcję lub ulepszenie kodu, które chciałbyś włączyć, prześlij Pull Request. Upewnij się, że Twój kod jest zgodny z istniejącym stylem projektu i zawiera odpowiednie testy (jeśli dotyczy).

Twoja pomoc w udoskonalaniu ARA jest bardzo mile widziana!

## Licencja

Niniejsze oprogramowanie jest objęte licencją MIT.

Copyright (c) 2025 KaliWho & ZeroOne

Niniejszym udziela się bezpłatnie każdej osobie uzyskującej kopię tego oprogramowania i powiązanych plików dokumentacji (dalej "Oprogramowanie") prawa do korzystania z Oprogramowania bez ograniczeń, w tym między innymi do praw do używania, kopiowania, modyfikowania, łączenia, publikowania, rozpowszechniania, sublicencjonowania i/lub sprzedawania kopii Oprogramowania, oraz do zezwalania osobom, którym Oprogramowanie zostało dostarczone, na to samo, z zastrzeżeniem następujących warunków:

Powyższa informacja o prawach autorskich i niniejsza informacja o zezwoleniu zostaną zawarte we wszystkich kopiach lub istotnych częściach Oprogramowania.

OPROGRAMOWANIE JEST DOSTARCZANE "TAKIE, JAKIE JEST", BEZ JAKIEJKOLWIEK GWARANCJI, WYRAŹNEJ ANI DOROZUMIANEJ, W TYM MIĘDZY INNYMI GWARANCJI PRZYDATNOŚCI HANDLOWEJ, PRZYDATNOŚCI DO OKREŚLONEGO CELU ORAZ NIENARUSZALNOŚCI PRAW. W ŻADNYM WYPADKU AUTORZY LUB POSIADACZE PRAW AUTORSKICH NIE BĘDĄ ODPOWIEDZIALNI ZA JAKIEKOLWIEK ROSZCZENIA, SZKODY LUB INNE ZOBOWIĄZANIA, CZY TO W WYNIKU DZIAŁANIA UMOWY, CZYNÓW NIEDOZWOLONYCH LUB W INNY SPOSÓB, WYNIKAJĄCE Z OPROGRAMOWANIA LUB W ZWIĄZKU Z UŻYWANIEM LUB INNYMI TRANSAKCJAMI W OPROGRAMOWANIU.
