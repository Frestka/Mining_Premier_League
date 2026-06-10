# To-Do List: Refactoring Grafici

- [ ] **Spostare il grafico di Confronto Modelli (Accuracy vs Macro F1)**
  - Creare la funzione `plot_model_comparison(results_acc, results_f1, dummy_acc, dummy_f1_mac)` in `src/model_utils.py`.
  - Sostituire il codice nella Cella 17 del notebook con il richiamo alla funzione.

- [ ] **Spostare il grafico delle Feature Importances**
  - Creare la funzione `plot_feature_importance(importances, feature_names, top_n=15)` in `src/model_utils.py`.
  - Sostituire il codice nella Cella 23 del notebook con il richiamo alla funzione.

- [ ] **Spostare i grafici dell'Analisi SHAP**
  - Creare la funzione `plot_shap_analysis(model, X_test_scaled, class_names)` in `src/model_utils.py` per gestire i dot plot e bar plot.
  - Sostituire il blocco di estrazione e plottaggio SHAP nella Cella 24 del notebook con il richiamo alla funzione.

- [ ] **Aggiornare gli import nel Notebook**
  - Assicurarsi di importare le tre nuove funzioni da `src.model_utils` all'inizio del notebook `Machine_Learning_Modeling.ipynb`.


  - aggiungere alla full pipeline trigger il notebbok di ML

  - serve metriche di validazione?

  - ssitemare insime il markdown di ML

  COSE DA CHIEDERE AL PROF

- la teoria(slide) vine chiesta all'orale?
- il progetto va consegnato? se si come e quando?
- 