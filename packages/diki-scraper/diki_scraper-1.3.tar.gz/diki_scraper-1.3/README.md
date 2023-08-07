# diki_scraper: A Python library for generating diki.pl ENG-PL translations

`diki_scraper` pozwala na tłumaczenie słów z słownika ENG-PL diki.pl

## Instalacja
```
pip install diki_scraper
```


## Opis funkcji

Moduł zawiera funkcję `diki.translation(word, num = 5, ex_trans = 1)`

`word`, akceptuje string, który masz zamiar przetłumaczyć\
`num`, opcjonalnie akceptuje int (domyślnie 5), określający do ilu tłumaczeń (max) ma zwrócić funkcja \
`ex_trans`, opcjonalnie akceptuje int (domyślnie 1), określający czy funkcja ma zwrócić dokładne tłumaczenie słowa, np. czy dla słowa 'used' mają zostać wyświetlone tłumaczenia słowa 'use'


## Przykłady użycia



```python
from diki_scraper import diki

diki.translation('used')
```

```python
['używany', 'przyzwyczajony', 'przywykły']
```

```python
from diki_scraper import diki

diki.translation('used',10,0)
```

```python
['używany', 'przyzwyczajony', 'przywykły', 'używać', 'korzystać (np. z telefonu, toalety)', 'zużywać', 'wykorzystywać (np. kogoś do swoich celów)', 'używać (w mowie lub w piśmie)', 'używać', 'wykorzystywać (np. przewagę)']
```




