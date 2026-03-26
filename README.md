# MIP_1.praktiskais_darbs

## Projekta apraksts
Šī ir spēle “Cilvēks pret datoru”, kur spēles stāvokli veido:
- pašreizējais skaitlis,
- kopējie punkti,
- banka,
- gājiena kārta.

Spēlētāji pārmaiņus dala pašreizējo skaitli ar 3, 4 vai 5, ja dalīšana ir iespējama bez atlikuma.

## Noteikumi
1. Katrā gājienā drīkst izvēlēties tikai vienu no dalītājiem: 3, 4 vai 5.
2. Dalītāju drīkst izmantot tikai tad, ja pašreizējais skaitlis ar to dalās bez atlikuma.
3. Pēc dalīšanas:
   - ja iegūtais skaitlis ir pāra skaitlis, punktiem pieskaita +1,
   - ja nepāra, punktiem pieskaita -1.
4. Ja iegūtais skaitlis beidzas ar 0 vai 5, bankai pieskaita +1.
5. Spēle beidzas, kad vairs nav iespējams dalīt ar 3, 4 vai 5.
6. Gala rezultāts:
   - ja punktu summa ir pāra, gala punkti = punkti - banka,
   - ja punktu summa ir nepāra, gala punkti = punkti + banka.
7. Ja gala punkti ir pāra skaitlis, uzvar cilvēks.
   Ja gala punkti ir nepāra skaitlis, uzvar dators.

## Kā palaist
Nepieciešams Python 3.

Palaist terminālī:
```bash
python main.py
