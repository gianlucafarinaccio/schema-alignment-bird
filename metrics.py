import json
import matplotlib.pyplot as plt

def calculate_metrics(data):
    # Inizializzare i dizionari per memorizzare i calcoli per db_id
    db_metrics = {}
    # Variabili globali per calcolare le metriche generali
    total_true_positives = 0
    total_false_positives = 0
    total_false_negatives = 0
    total_items = 0
    
    for key, value in data.items():
        true_set = set(value["true"])
        predicted_set = set(value["predicted"])
        db_id = value["db_id"]

        # Calcolare i veri positivi, falsi positivi e falsi negativi
        if true_set == predicted_set:
            true_positives = 1
            false_positives = 0
            false_negatives = 0
        else:
            true_positives = 0
            false_positives = len(predicted_set - true_set)
            false_negatives = len(true_set - predicted_set)
        
        # Aggiungere ai totali per il db_id
        if db_id not in db_metrics:
            db_metrics[db_id] = {'true_positives': 0, 'false_positives': 0, 'false_negatives': 0, 'count': 0}
        
        db_metrics[db_id]['true_positives'] += true_positives
        db_metrics[db_id]['false_positives'] += false_positives
        db_metrics[db_id]['false_negatives'] += false_negatives
        db_metrics[db_id]['count'] += 1
        
        # Aggiungere ai totali generali
        total_true_positives += true_positives
        total_false_positives += false_positives
        total_false_negatives += false_negatives
        total_items += 1
    
    # Calcolare le metriche per ciascun db_id
    db_results = {}
    for db_id, metrics in db_metrics.items():
        precision = metrics['true_positives'] / (metrics['true_positives'] + metrics['false_positives']) if (metrics['true_positives'] + metrics['false_positives']) > 0 else 0
        recall = metrics['true_positives'] / (metrics['true_positives'] + metrics['false_negatives']) if (metrics['true_positives'] + metrics['false_negatives']) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        db_results[db_id] = {'precision': precision, 'recall': recall, 'f1_score': f1_score}
    
    # Calcolare le metriche generali
    precision = total_true_positives / (total_true_positives + total_false_positives) if (total_true_positives + total_false_positives) > 0 else 0
    recall = total_true_positives / (total_true_positives + total_false_negatives) if (total_true_positives + total_false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Restituire i risultati
    return db_results, {'precision': precision, 'recall': recall, 'f1_score': f1_score}


def plot_metrics(db_results):
    # Estrazione dei valori per i vari db_id
    db_ids = list(db_results.keys())
    precision_values = [metrics['precision'] for metrics in db_results.values()]
    recall_values = [metrics['recall'] for metrics in db_results.values()]
    f1_values = [metrics['f1_score'] for metrics in db_results.values()]
    
    # Generare una lista di colori distinti
    colors = plt.cm.get_cmap('tab20', len(db_ids))  # Usa una mappa di colori per una lista di colori distinti
    
    # Creazione di un grafico per Precision
    plt.figure(figsize=(15, 5))

    # Precisione
    plt.subplot(131)
    plt.bar(db_ids, precision_values, color=colors(range(len(db_ids))))
    plt.xlabel('DB ID')
    plt.ylabel('Precision')
    plt.title('Precision per DB ID')
    plt.xticks(rotation=90)  # Ruotare le etichette sull'asse X per evitare sovrapposizioni

    # Recall
    plt.subplot(132)
    plt.bar(db_ids, recall_values, color=colors(range(len(db_ids))))
    plt.xlabel('DB ID')
    plt.ylabel('Recall')
    plt.title('Recall per DB ID')
    plt.xticks(rotation=90)  # Ruotare le etichette sull'asse X

    # F1
    plt.subplot(133)
    plt.bar(db_ids, f1_values, color=colors(range(len(db_ids))))
    plt.xlabel('DB ID')
    plt.ylabel('F1 Score')
    plt.title('F1 Score per DB ID')
    plt.xticks(rotation=90)  # Ruotare le etichette sull'asse X

    # Mostrare il grafico
    plt.tight_layout()
    plt.show()



with open('response_t.json','r') as f:
    data = json.load(f)

# Calcolare le metriche
db_results, overall_results = calculate_metrics(data)

# Stampare i risultati per db_id
print("Metrics for each db_id:")
for db_id, metrics in db_results.items():
    print(f"DB ID: {db_id}")
    print(f"  Precision: {metrics['precision']}")
    print(f"  Recall: {metrics['recall']}")
    print(f"  F1 Score: {metrics['f1_score']}")
    print()

# Stampare i risultati generali
print("Overall Metrics:")
print(f"Precision: {overall_results['precision']}")
print(f"Recall: {overall_results['recall']}")
print(f"F1 Score: {overall_results['f1_score']}")

plot_metrics(db_results)
