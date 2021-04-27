# Učenje akustičkih modela govora za raspoznavanje pomoću alata Wav2letter

## Instalacija

- Radno okruženje je Arch Linux OS sa CUDA 11.1 (NVIDIA 1060 6gb GPU)

- Pri izvršavanju alata koristim Docker image omogućen od strane autora alata, instalirao sam prateći upute na A https://github.com/flashlight/flashlight/tree/master/.docker.

- Nakon preuzimanja i instalacije Docker image-a, pokrećem naredbu `docker run --privileged --gpus all -itd --ipc=host --name flashlight flml/flashlight:cuda-latest` radi pokretanja Docker container-a te naredbu `docker exec -it flashlight bash` radi ulaska u container putem komandne linije.

## Ulazne datoteke

Kako bi se model mogao uspješno trenirati putem wav2etter/flashlight_asr alata, potrebni su ulazni podaci u točno određenom formatu. Pratio sam upute na https://github.com/flashlight/flashlight/tree/master/flashlight/app/asr gdje je opisano koje datoteke su potrebne za treniranje modela. U ovom dijelu sam se dosta namučio, s obzirom da nemam nikakva iskustva s alatom niti s treniranjem modela za prepoznavanje govora. 
Potrebne datoteke su sljedeće:

- `train.lst`, `val.lst`, `test.lst` koji predstavljaju "manifest" datoteke sa putanjama do izvornih audio datoteka. Predstavljaju trening, validation i test podatke (ja sam ih podijelio prema distribuciji 80/10/10 gdje je 80% podataka korišteno za trening set, 10% za validacijski set podataka te 10% za test set podataka). Datoteke se nalaze na ovom repozitoriju tako da ih slobodno možete pogledati.

- `tokens.txt` - datoteka sa svim mogućim znakovima, uključujući i posebne izraze. Pretpostavljam da sam dobro kreirao tu datoteku, možete je otvoriti i pogledati jer to u redu.

- `lexicon.txt` - datoteka sa svim mogućim riječima. Prema uputama na repozitoriju alata (link gore), ova datoteka mora biti u određenom formatu. Kreirao sam vlastite Python skripte kako bih pretvorio riječi u traženi oblik. Ovu datoteku isto možete pogledati na ovom repozitoriju.

' `***.arch` - datoteka koja sadrži strukturu samog modela. Način kako se kreiraju ove datoteke su autori alata opisali na https://github.com/flashlight/flashlight/tree/master/flashlight/app/asr#writing-architecture-files. No iz tih uputa ja i dalje nisam baš shvatio kako se to radi niti ne znam kako bih kreirao kvalitetan model za treniranje VEPRAD baze podataka. `.arch` file koji se nalazi na ovom repozitoriju (`am_conformer_ctc_stride3_letters_25Mparams_distill.arch`) je zapravo preuzet sa https://github.com/flashlight/wav2letter/tree/master/recipes/rasr, gdje se nudi par `.arch` datoteka - ja sam odabrao onu sa najmanje parametara (28 mil.). Ovdje mi je najveći problem što ne znam kako kreirati vlastiti model niti ne mogu pronaći primjer koji bi bio dobar za moj konkretan problem. Treniranje radi pomoću navedene preuzete `.arch` datoteke, no čini mi se da su rezultati previše loši (više o tome u nastavku).

- `flagsfile` - datoteka koja sadrži "flagove" koji specificiraju razne parametre za treniranje modela te putanje u kojima se nalaze ulazne datoteke. Ovdje specificiramo putanju `.lst`, `.arch` datoteka te možemo navesti razne parametre modela poput `--lr` što predstavlja learning rate modela, može se postaviti batch size te razni drugi parametri...

## Treniranje modela

`fl_asr_train` je naziv izvršne datoteke pomoću koje se pokreće treniranje modela. Način kako sam ja pokretao treniranje bilo je sa naredbom `./fl_asr_train train --flagsfile=/path/to/flagsfile` gdje kao parametar navodim ranije spomenuti flagsfile koji sadrži sve ostale parametre vezanih za treniranje. Pokretanjem naredbe pokreće se treniranje gdje se informacije ispisuju na `stdout/stderr` nakon svake iteracije, te se također iste informacije pohranjuju u log datoteku u `models` direktorij.

## Izlazne datoteke

- `models` direktorij - također se može naći na ovom repozitoriju. Sadrži `.bin` datoteke koji predstavljaju datoteke istreniranih modela (ne nalaze se u ovom repozitoriju jer zauzimaju previše memorije), sadrži `xxx_log` datoteke u kojima se nalaze informacije o treniranju modela (train WER, train TER, val WER, val TER, loss, val-loss...). U `models` direktoriju ovog repozitorija možete pronaći log datoteku u kojoj se nalaze ispisi pri treniranju preko 1500 iteracija. Ako pogledate metrike, primjetiti ćete kako se točnost ne povećava niti nakon velikog broja iteracija, prema čemu ja zaključujem da ili arhitektura modela nije dobra ili ulazni parametri modela nisu dobri. Kako nemam iskustva sa alatom niti sa treniranjem modela akustičkih modela za prepoznavanje govora, nemam ideju kako da riješim ovaj problem stoga tražim pomoć.

