import json
import matplotlib.pyplot as plt
import argparse

# Create the parser
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument("-n","--name", type=str, help="name of your benchmark",required=True)

# Parse the arguments
args = parser.parse_args()

benchmark_name = args.name



def calculate_metrics(data):
    db_metrics = {}
    total_true_positives = 0
    total_false_positives = 0
    total_false_negatives = 0
    total_items = 0
    
    for key, value in data.items():
        true_set = set(value["true"])
        predicted_set = set(value["predicted"])
        db_id = value["db_id"]


        if true_set == predicted_set:
            true_positives = 1
            false_positives = 0
            false_negatives = 0
        else:
            true_positives = 0
            false_positives = len(predicted_set - true_set)
            false_negatives = len(true_set - predicted_set)
        

        if db_id not in db_metrics:
            db_metrics[db_id] = {'true_positives': 0, 'false_positives': 0, 'false_negatives': 0, 'count': 0}
        
        db_metrics[db_id]['true_positives'] += true_positives
        db_metrics[db_id]['false_positives'] += false_positives
        db_metrics[db_id]['false_negatives'] += false_negatives
        db_metrics[db_id]['count'] += 1
        
        total_true_positives += true_positives
        total_false_positives += false_positives
        total_false_negatives += false_negatives
        total_items += 1
    

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
    

    return db_results, {'precision': precision, 'recall': recall, 'f1_score': f1_score}


def plot_metrics(db_results, output_folder="."):
    db_ids = list(db_results.keys())
    precision_values = [metrics['precision'] for metrics in db_results.values()]
    recall_values = [metrics['recall'] for metrics in db_results.values()]
    f1_values = [metrics['f1_score'] for metrics in db_results.values()]
    
    colors = plt.cm.get_cmap('tab20', len(db_ids))
    
    # Precision
    plt.figure(figsize=(10, 5))
    plt.bar(db_ids, precision_values, color=colors(range(len(db_ids))))
    plt.xlabel('DB ID')
    plt.ylabel('Precision')
    plt.title('Precision')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/precision.png")
    plt.close()
    
    # Recall
    plt.figure(figsize=(10, 5))
    plt.bar(db_ids, recall_values, color=colors(range(len(db_ids))))
    plt.xlabel('DB ID')
    plt.ylabel('Recall')
    plt.title('Recall')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/recall.png")
    plt.close()
    
    # F1 Score
    plt.figure(figsize=(10, 5))
    plt.bar(db_ids, f1_values, color=colors(range(len(db_ids))))
    plt.xlabel('DB ID')
    plt.ylabel('F1 Score')
    plt.title('F1 Score')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/f1_score.png")
    plt.close()



with open(f'output_{benchmark_name}/output_completed.json','r') as f:
    data = json.load(f)

db_results, overall_results = calculate_metrics(data)

with open(f'output_{benchmark_name}/metrics.txt','w') as f:
    f.write("Metrics for each db_id:\n")
    for db_id, metrics in db_results.items():
        f.write(f"DB ID: {db_id}\n")
        f.write(f"  Precision: {metrics['precision']}\n")
        f.write(f"  Recall: {metrics['recall']}\n")
        f.write(f"  F1 Score: {metrics['f1_score']}\n")
        f.write("\n")

    f.write("Overall Metrics:\n")
    f.write(f"Precision: {overall_results['precision']}\n")
    f.write(f"Recall: {overall_results['recall']}\n")
    f.write(f"F1 Score: {overall_results['f1_score']}\n")

plot_metrics(db_results, f"output_{benchmark_name}")
