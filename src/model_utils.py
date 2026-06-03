import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report


def plot_confusion_matrix(y_true, y_pred, title):
    """
    Genera due confusion matrix affiancate:
    - sinistra: conteggi interi
    - destra: normalizzata per riga (= recall per classe)
    """
    labels = ['Win', 'Draw', 'Loss']
    cm_raw  = confusion_matrix(y_true, y_pred, labels=labels)
    cm_norm = confusion_matrix(y_true, y_pred, labels=labels, normalize='true')

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    sns.heatmap(cm_raw, annot=True, fmt='d', cmap='Blues',
                xticklabels=labels, yticklabels=labels, ax=axes[0])
    axes[0].set_title(f'Confusion Matrix (conteggi) — {title}')
    axes[0].set_xlabel('Predicted')
    axes[0].set_ylabel('Actual')

    sns.heatmap(cm_norm, annot=True, fmt='.2%', cmap='Oranges',
                xticklabels=labels, yticklabels=labels, ax=axes[1])
    axes[1].set_title(f'Confusion Matrix (normalizzata) — {title}')
    axes[1].set_xlabel('Predicted')
    axes[1].set_ylabel('Actual')

    plt.tight_layout()
    plt.show()


def plot_per_class_heatmap(models_dict, X_test_scaled, y_test):
    """
    Genera una heatmap 3-pannelli (Precision | Recall | F1)
    per ogni modello nel dizionario.
    """
    labels = ['Win', 'Draw', 'Loss']
    rows = []

    for name, model in models_dict.items():
        y_pred = model.predict(X_test_scaled)
        report = classification_report(
            y_test, y_pred, labels=labels,
            target_names=labels, output_dict=True
        )
        for cls in labels:
            rows.append({
                'Modello':   name,
                'Classe':    cls,
                'Precision': report[cls]['precision'],
                'Recall':    report[cls]['recall'],
                'F1':        report[cls]['f1-score'],
            })

    df = pd.DataFrame(rows)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    for ax, metric in zip(axes, ['Precision', 'Recall', 'F1']):
        pivot = df.pivot(index='Modello', columns='Classe', values=metric)
        sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn',
                    vmin=0, vmax=1, ax=ax, linewidths=0.5)
        ax.set_title(f'{metric} per classe')
        ax.set_ylabel('Modello')
        ax.set_xlabel('Classe')

    plt.suptitle('Precision, Recall e F1 per Classe — Confronto Modelli',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()
