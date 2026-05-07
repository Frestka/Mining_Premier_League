# Metriche di Validazione — Guida per l'Esame Orale
### Progetto: Mining Premier League

---

## Premessa: Cosa stiamo usando nel notebook?

Il notebook `Machine_Learning_Modeling.ipynb` valuta ogni modello con **tre strumenti**:

1. **Accuracy** — usata nel grafico di confronto principale
2. **Macro F1-Score** — affiancata all'Accuracy nel grafico doppio (sezione 5)
3. **Confusion Matrix** — plottata per ogni singolo modello
4. **Classification Report** — stampato per ogni modello (contiene Precision, Recall, F1 per classe)

---

## 1. Perché l'Accuracy da sola non basta?

### Il problema dello sbilanciamento delle classi

Il nostro dataset ha tre classi con frequenze diverse:
- **Win** (~37-38%)
- **Loss** (~37-38%)
- **Draw** (~25%)

I Draw sono meno frequenti. Questo crea un problema chiamato **"Class Imbalance"**, trattato esplicitamente nelle slide del corso.

### L'esempio che smonta l'Accuracy

Immagina un modello "stupido" che **predice sempre Win o Loss**, non indovinando mai un pareggio.

- Sui pareggi (25% dei casi) sbaglia sempre → 0% di correttezza su quella classe
- Su Win e Loss (75% dei casi) può andare benino

**Risultato paradossale**: questo modello può avere un'Accuracy del 55-65% pur non avendo mai previsto un solo pareggio correttamente. L'Accuracy non lo "punisce" abbastanza per questa lacuna, perché i pareggi sono la classe minoritaria.

**Conclusione**: L'Accuracy misura quante predizioni totali sono corrette, ma tratta tutte le classi con lo stesso peso implicito legato alla loro frequenza. In un dataset sbilanciato, è una metrica **ingannevole**.

---

## 2. Precision e Recall — Le fondamenta dell'F1

Prima di capire l'F1, bisogna capire Precision e Recall. Prendiamo come esempio la classe **Draw**:

### Precision (Precisione)
> "Di tutte le partite che il modello ha detto essere pareggi, quante lo erano davvero?"

```
Precision(Draw) = Veri Pareggi Previsti / Totale Pareggi Previsti
```

Un modello con Precision bassa sui pareggi fa molti **falsi allarmi**: dice "è un pareggio" quando non lo è.

### Recall (Sensibilità / Copertura)
> "Di tutte le partite che erano effettivamente pareggi, quante ne ha catturate il modello?"

```
Recall(Draw) = Veri Pareggi Previsti / Totale Pareggi Reali
```

Un modello con Recall bassa sui pareggi **se li lascia sfuggire**: non riesce a riconoscerli.

### Il trade-off
Un modello può aumentare la Precision sui pareggi essendo molto conservativo (predice "Draw" solo quando è sicurissimo) ma così facendo abbassa il Recall. L'F1-Score nasce per bilanciare questo trade-off.

---

## 3. F1-Score — La metrica bilanciata

### Formula

L'F1-Score è la **media armonica** di Precision e Recall:

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

La media armonica penalizza pesantemente i casi estremi: se Precision è alta ma Recall è bassissima (o viceversa), l'F1 crolla. Solo un buon equilibrio tra le due produce un F1 alto.

### F1 per singola classe
Ogni classe (Win, Draw, Loss) ha il suo F1-Score. Nel `classification_report` li trovi tutti e tre, riga per riga.

---

## 4. Macro F1-Score — La metrica della "giustizia"

### Cos'è
Il **Macro F1-Score** calcola l'F1 separatamente per Win, Draw e Loss, poi ne fa la **media aritmetica non pesata**.

```
Macro F1 = (F1_Win + F1_Draw + F1_Loss) / 3
```

### Perché è superiore all'Accuracy nel nostro caso

Il punto chiave è **"non pesata"**: la classe Draw (25%) pesa esattamente quanto Win (38%) nel calcolo finale.

Se il modello non riconosce i pareggi:
- F1_Draw → vicino a 0
- Macro F1 → crolla drasticamente

Anche se l'Accuracy rimane alta, il Macro F1 "smonta" il modello e mostra la sua lacuna reale.

**Esempio pratico**: Un modello con Accuracy 62% ma Macro F1 0.45 sta chiaramente fallendo su una o più classi. Un modello con Accuracy 58% ma Macro F1 0.56 è in realtà più equilibrato e affidabile.

### Frase per l'orale (imparare a memoria):
> *"Abbiamo scelto di affiancare all'Accuracy il Macro F1-Score perché il nostro dataset è sbilanciato: i pareggi rappresentano solo il 25% dei casi. L'Accuracy può essere gonfiata da un modello che ignora i pareggi, mentre il Macro F1 dà lo stesso peso a tutte e tre le classi, smascherando i modelli che non sanno classificare i Draw."*

---

## 5. Confusion Matrix — Capire la "logica" degli errori

### Cos'è
La Confusion Matrix è una tabella 3×3 (nel nostro caso) che mostra, per ogni classe reale, come il modello ha distribuito le sue predizioni.

```
                  Predicted
                Win   Draw   Loss
Actual  Win  [ TW    e1     e2  ]
        Draw [ e3    TD     e4  ]
        Loss [ e5    e6     TL  ]
```
(TW = True Win, TD = True Draw, TL = True Loss; e1..e6 = errori)

### Perché è fondamentale: la gravità degli errori

Nel calcio, **non tutti gli errori sono uguali**:

| Errore | Tipo | Gravità |
|--------|------|---------|
| Prevede Win, era Draw | Errore di "misura" | 🟡 Medio — la partita era comunque in bilico |
| Prevede Draw, era Win | Errore di "misura" | 🟡 Medio — l'esito era incerto |
| Prevede Win, era Loss | Errore di "logica" | 🔴 Alto — il modello ha letto la partita al contrario |
| Prevede Loss, era Win | Errore di "logica" | 🔴 Alto — il modello ha letto la partita al contrario |

Un modello che confonde **classi adiacenti** (Win ↔ Draw, Draw ↔ Loss) dimostra comunque di aver catturato qualcosa della dinamica tattica: sa che la partita era incerta. Un modello che confonde **classi opposte** (Win ↔ Loss) non ha capito nulla del dominio.

### Come usarla all'orale
Guardando la Confusion Matrix del vostro modello migliore, potete commentare:
- *"Gli errori principali si concentrano tra Win e Draw, non tra Win e Loss. Questo dimostra che il modello ha compreso la logica dominante della partita, ma fatica sull'incertezza tipica dei pareggi, che per natura sono le partite più difficili da prevedere."*

---

## 6. Il DummyClassifier — Il punto di partenza

### Cos'è
Il `DummyClassifier` con `strategy='most_frequent'` ignora completamente le feature e predice sempre la classe più frequente nel training set.

### Perché è indispensabile
Senza una baseline triviale, dire "il nostro Random Forest ha fatto 60% di Accuracy" non significa nulla. Con la baseline:

- Se Dummy fa 38% → RF fa 60% → c'è un guadagno reale di +22 punti percentuali ✅
- Se Dummy fa 38% → RF fa 40% → il modello non sta quasi imparando nulla ❌

Lo stesso vale per il Macro F1: il Dummy avrà un Macro F1 molto basso (vicino a 0) perché non prevede mai Draw né Loss. Qualsiasi nostro modello reale dovrebbe superarlo ampiamente.

---

## 7. Il grafico doppio nel notebook — Come leggerlo

Nella sezione 5 del notebook c'è un grafico con **due pannelli affiancati**:

- **Pannello sinistro (blu)** → Accuracy di ogni modello
- **Pannello destro (verde)** → Macro F1-Score di ogni modello
- **Linea rossa tratteggiata** → baseline del DummyClassifier

### Cosa cercare nel grafico

1. **Distanza dalla linea rossa**: più il modello è lontano dalla baseline, più sta realmente imparando.
2. **Differenza tra i due pannelli**: se un modello ha Accuracy alta ma Macro F1 basso, significa che è "pigro" — ottimizza per le classi maggioritarie e ignora i Draw.
3. **Il modello migliore** non è necessariamente quello con Accuracy più alta, ma quello con il miglior Macro F1.

---

## 8. Riepilogo Metriche — Schema per l'Esame

| Metrica | Formula semplificata | Cosa misura | Limite |
|---------|---------------------|-------------|--------|
| **Accuracy** | Corretti / Totale | Correttezza globale | Ingannevole con classi sbilanciate |
| **Precision** | Veri Positivi / Previsti Positivi | Affidabilità delle predizioni positive | Ignora i falsi negativi |
| **Recall** | Veri Positivi / Positivi Reali | Capacità di trovare tutti i casi | Ignora i falsi positivi |
| **F1-Score** | Media armonica di P e R | Bilanciamento P e R | Tratta F.P. e F.N. allo stesso modo |
| **Macro F1** | Media di F1 per classe (non pesata) | Equità tra tutte le classi | Può essere troppo severo se una classe è intrinsecamente difficile |
| **Confusion Matrix** | Tabella TN/TP/FN/FP per classe | Distribuzione e gravità degli errori | Non sintetizza in un numero unico |

---

## 9. Verdetto finale sulle metriche

**La gerarchia corretta per il nostro progetto è:**

1. 🥇 **Macro F1-Score** → metrica principale per confrontare i modelli (equa, non ingannata dallo sbilanciamento)
2. 🥈 **Confusion Matrix** → per analizzare la qualità e la gravità degli errori del modello migliore
3. 🥉 **Accuracy** → per comunicare i risultati in modo semplice e confrontarli con la baseline Dummy

Questo approccio dimostra padronanza delle metriche di validazione superiore alla media universitaria e risponde direttamente alla critica più comune che un professore di Data Mining può fare: *"Ma l'Accuracy non è sufficiente su dataset sbilanciati!"*
