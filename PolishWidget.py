from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt5.uic.properties import QtGui


class PolishWidget(QWidget):
    def __init__(self, parent, img1, img2, img3):
        super(PolishWidget, self).__init__(parent)
        tab_layout = QVBoxLayout()

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)

        text_edit.textCursor().insertHtml('<center><h1> Instrukcja obsługi programu do analizy danych '
                                          'z kontroli położenia pacjenta v. 1.0 </h1>'
                                          'Alicja Przybyś, licencja open source Apache-2.0</center><br> ')
        text_edit.textCursor().insertHtml('<h2>Wczytywanie danych</h2> <br>')
        text_edit.textCursor().insertHtml('<p>To Aby wczytać dane należy wejść w menu File i wybrać '
                                          'Import→Multiple Patients→Select Multiple Files lub '
                                          'Import→Multiple Patients→Select Folder. Pierwsza z opcji pozwala na '
                                          'wybranie wielu plików z danego folderu – poprzez zaznaczenie tych plików '
                                          'myszką (przyciśnięcie Shift pozwala zaznaczyć wszystkie pliki w zakresie '
                                          'pomiędzy jednym wybranym plikiem a drugim, a przyciśnięcie Ctrl pozwala '
                                          'na wybór wielu plików w dowolnych miejscach w folderze) lub przez '
                                          'naciśnięcie Ctrl+A co zaznaczy wszystkie pliki dostępne w tym folderze. '
                                          'Druga natomiast wybierze do analizy wszystkie pliki z rozszerzeniem '
                                          '.odt znajdujące się w wybranym folderze. Program zakłada, że w każdym '
                                          'pliku dokonana została korekta zgodna z parametrami podanymi w okienku '
                                          'Preferences. Po wybraniu serii plików jedną z metod, program dokona '
                                          'odwrócenia tej korekty. Odwrócenie korekty nastąpi po określonej liczbie '
                                          'sesji. Liczba ta może być zmieniona w okienku Preferences.</p><br>')
        text_edit.textCursor().insertHtml('<p>Następnie program podliczy średnie i odchylenia standardowe dla każdej '
                                          'współrzędnej wektora przesunięcia ogniska padania wiązki od izocentrum '
                                          'a wyniki obliczeń przedstawi na tabeli oraz wykresie. Wartości podawane '
                                          'są w cm. Aby zobaczyć wyniki na wykresie dla danej wartości przesunięcia '
                                          'należy kliknąć w checkboxa przy odpowiedniej nazwie znajdującego się '
                                          'po prawej stronie wykresu.</p><br>')
        text_edit.textCursor().insertImage(img1)
        text_edit.textCursor().insertHtml('<br><p>Możliwy jest też podgląd wartości po dokonaniu odwrócenia korekty '
                                          'dla pojedynczego pliku. Aby to zrobić należy wybrać '
                                          'File→Import→Single Patient. Otworzy się nowe okno, w którym w tabeli '
                                          'podane będą wszystkie otrzymane wartości, pod spodem widoczne będą wyniki '
                                          'analizy oraz wykres z naniesionymi wartościami przesunięcia dla '
                                          'kolejnych dat przeprowadzonych badań. Aby wyświetlić te wartości należy '
                                          'kliknąć w checkboxy po prawej stronie.</p><br>')
        text_edit.textCursor().insertImage(img2)
        text_edit.textCursor().insertHtml('<br><h2>Zapisywanie danych</h2> <br>')
        text_edit.textCursor().insertHtml('<p>Program umożliwia zapisanie wyników analizy do pliku .csv '
                                          '(comma-separated values). Ten format umożliwia łatwą dalszą analizę '
                                          'w arkuszu obliczeniowym. Aby ładnie wyświetlić dane należy ustawić wartość '
                                          'separującą na spację oraz delimiter tekstu na znak cytowania (“). '
                                          'Aby zapisać w ten sposób dane należy wybrać File → Save... → data to '
                                          'a .csv file i w okienku, które się pojawi przenawigować do miejsca, '
                                          'w którym chce się zapisać plik. Następnie należy wpisać nazwę pliku, '
                                          'program sam doda odpowiednie rozszerzenie.</p><br>')
        text_edit.textCursor().insertHtml('<p>Możliwy jest też zapis wykresu do pliku. Aby to zrobić należy wybrać  '
                                          'File → Save... → plot i postąpić jak powyżej. Rozszerzenia, w jakich można '
                                          'zapisać wykres to: .png (portable network graphics), .pdf '
                                          '(portable document format), .svg (scalable vector graphics), .ps '
                                          '(PostScript) oraz .eps (encapsulated PostScript). Aby wybrać któryś '
                                          'z tych formatów wystarczy kliknąć na niego w liście na dole ekranu. '
                                          'Odpowiednie rozszerzenie dopisze się automatycznie do nazwy pliku. '
                                          'Można też samemu to rozszerzenie dopisać. Program zignoruje próby zapisu '
                                          'do pliku o rozszerzeniu innym niż z listy powyżej.</p><br>')
        text_edit.textCursor().insertHtml('<h2>Preferencje</h2> <br>')
        text_edit.textCursor().insertHtml('<p>Program pozwala na dostosowanie parametrów analizy. Po kliknięciu '
                                          'Edit → Preferences pojawi się niemodalne okno, w którym można dostosować '
                                          'trzy parametry.</p><br>')
        text_edit.textCursor().insertImage(img3)
        text_edit.textCursor().insertHtml('<br><p>Pierwszą z wartości jest próg, po którym stosowana jest korekta. '
                                          'Wartość domyślna progu to 0,3 cm.  Aby zmienić tę wartość należy nową '
                                          'wartość wpisać w pole tekstowe (pole tekstowe przyjmuje tylko wartości '
                                          'zmienno przecinkowe).</p><br>')
        text_edit.textCursor().insertHtml('<p>Drugą ze zmiennych jest liczba początkowych sesji medycznych pacjenta, '
                                          'które nie zostały objęte korektą. Domyślna wartość tej liczby to 3. '
                                          'Aby zmienić tę wartość należy nową wartość wpisać w pole tekstowe '
                                          '(pole tekstowe przyjmuje tylko wartości całkowite).</p><br>')
        text_edit.textCursor().insertHtml('<p>Trzecia ze zmiennych to liczba sesji medycznych branych do obliczania '
                                          'średniej i odchylenia standardowego. Wartość domyślna to wszystkie sesje '
                                          'w danym pliku. Aby zmienić tę wartość należy nową wartość wpisać '
                                          'w pole tekstowe (pole tekstowe przyjmuje tylko wartości całkowite). '
                                          'Aby wybrać wszystkie sesje w pliku należy wpisać 0.</p><br>')
        text_edit.textCursor().insertHtml('<p>Naciśnięcie Apply zmieni wartości, ale nie zamknie okienka. '
                                          'Naciśnięcie Ok zmieni wartości i zamknie okienko. Po zamknięciu okienka '
                                          'dane automatycznie odświeżą się z nowymi wartościami parametrów.</p><br>')
        text_edit.textCursor().insertHtml('<h2>Skróty klawiszowe</h2> <br>')
        text_edit.textCursor().insertHtml('<table>'
                                          '<tr>'
                                          '<th><br>			Skrót		</th>'
                                          '<th><br>			Akcja		</th>'
                                          '</tr>'
                                          '<tr>'
                                          '<td><br>			Ctrl + O		</td>'
                                          '<td><br>			Wczytaj dane z wybranych plików	</td>'
                                          '</tr>'
                                          '<tr>'
                                          '<td><br>			Ctrl + F<		</td>'
                                          '<td><br>		Wczytaj dane z wszystkich plików w folderze</td>'
                                          '</tr>'
                                          '<tr>'
                                          '<td><br>			Ctrl + A		</td>'
                                          '<td><br>			Wczytaj dane dla pojedynczego pacjenta		</td>'
                                          '</tr>'
                                          '<tr>'
                                          '<td><br>			Ctrl + S		</td>'
                                          '<td><br>			Zapisz dane do pliku .csv	</td>'
                                          '</tr>'
                                          '<tr>'
                                          '<td><br>			Ctrl + L		</td>'
                                          '<td><br>			Zapisz wykres	</td>'
                                          '</tr>'
                                          '<tr>'
                                          '<td><br>			Ctrl + H		</td>'
                                          '<td><br>			Pomoc		</td>'
                                          '</tr>'
                                          '<tr>'
                                          '<td><br>			Ctrl + P		</td>'
                                          '<td><br>			Otwórz okno preferencji		</td>'
                                          '</tr>'
                                          '</table>')
        text_edit.moveCursor(QTextCursor.Start)
        tab_layout.addWidget(text_edit)
        self.setLayout(tab_layout)