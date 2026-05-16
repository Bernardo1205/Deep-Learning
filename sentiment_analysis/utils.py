import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import Counter
from preprocessing import clean_text

# Configurar estilo de gráficos
def setup_plot_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)

# Visualizar distribución de sentimientos
def plot_sentiment_distribution(df):
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='airline_sentiment', order=['negative', 'neutral', 'positive'])
    plt.title("Sentiment Class Distribution")
    plt.ylabel("Count")
    plt.show()

# Visualizar longitud de tweets por sentimiento
def plot_tweet_length_distribution(df):
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x='word_count', hue='airline_sentiment', multiple="stack", bins=20)
    plt.title("Tweet Length (Words) by Sentiment")
    plt.xlabel("Words per Tweet")
    plt.show()

# Visualizar sentimientos por aerolínea
def plot_sentiment_per_airline(df):
    airline_sentiment = pd.crosstab(df['airline'], df['airline_sentiment'], normalize='index')
    airline_sentiment.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title("Sentiment Percentage per Airline")
    plt.ylabel("Proportion")
    plt.xticks(rotation=45)
    plt.legend(title="Sentiment", bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.show()

# Top palabras más frecuentes
def plot_top_words(df, top_n=15):
    all_words = [word for text in df['cleaned_text'] for word in text.split()]
    top_words = pd.DataFrame(Counter(all_words).most_common(top_n), columns=['Word', 'Count'])

    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_words, x='Count', y='Word', color='steelblue')
    plt.title(f"Top {top_n} Most Frequent Words (Cleaned)")
    plt.show()

# Valores faltantes
def plot_missing_values(df):
    miss = df.isnull().sum()
    miss = miss[miss > 0].sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    miss.plot(kind='barh', ax=ax, color='steelblue')
    ax.set_xlabel('Count of Missing Values')
    ax.set_title('Missing Values per Column')
    plt.tight_layout()
    plt.show()

# Resumen del dataset
def print_dataset_summary(df, vocab_size):
    print("\n" + "="*60)
    print("DATASET SUMMARY")
    print("="*60)
    print(f"Total tweets: {len(df)}")
    print(f"Unique airlines: {df['airline'].nunique()}")
    print(f"Unique users: {df['name'].nunique()}")
    print(f"Date range: {df['tweet_created'].min()} to {df['tweet_created'].max()}")
    print(f"Average tweet length: {df['word_count'].mean():.1f} words")
    print(f"Vocabulary size: {vocab_size}")
    print(f"\nSentiment distribution:")
    for sentiment, count in df['airline_sentiment'].value_counts().items():
        pct = (count / len(df)) * 100
        print(f"  {sentiment}: {count} ({pct:.1f}%)")
    print("="*60 + "\n")

# Guardar métricas en archivo
def save_metrics_to_file(test_results, filename='results.txt'):
    with open(filename, 'w') as f:
        f.write("MODEL EVALUATION RESULTS\n")
        f.write("="*50 + "\n\n")
        for model_name, metrics in test_results.items():
            f.write(f"{model_name}:\n")
            for metric, value in metrics.items():
                f.write(f"  {metric}: {value:.4f}\n")
            f.write("\n")

