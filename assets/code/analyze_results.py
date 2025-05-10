import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from wordcloud import WordCloud
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics import confusion_matrix
import glob

def load_latest_results():
    """Load the most recent comparison results CSV file"""
    csv_files = glob.glob("comparison_results_*.csv")
    if not csv_files:
        raise FileNotFoundError("No comparison results CSV files found")
    
    # Sort by modification time (newest first)
    latest_file = max(csv_files, key=os.path.getmtime)
    print(f"Analyzing latest results file: {latest_file}")
    
    # Load the CSV file
    df = pd.read_csv(latest_file)
    
    # Convert similarity score to numeric
    df['similarity_score'] = pd.to_numeric(df['similarity_score'], errors='coerce')
    
    return df, latest_file

def basic_statistics(df):
    """Calculate basic statistics about the results"""
    total_comparisons = len(df)
    correct_identifications = df['ai_generated_correctly_identified'].value_counts().get('Yes', 0)
    accuracy = correct_identifications / total_comparisons if total_comparisons > 0 else 0
    
    avg_similarity = df['similarity_score'].mean()
    median_similarity = df['similarity_score'].median()
    
    print("\n=== BASIC STATISTICS ===")
    print(f"Total image pairs analyzed: {total_comparisons}")
    print(f"Correctly identified AI images: {correct_identifications} ({accuracy:.2%})")
    print(f"Average similarity score: {avg_similarity:.2f}/10")
    print(f"Median similarity score: {median_similarity}/10")
    
    # Create a contingency table of similarity score vs. correct identification
    contingency = pd.crosstab(
        df['similarity_score'], 
        df['ai_generated_correctly_identified'], 
        normalize='index'
    )
    
    print("\n=== IDENTIFICATION ACCURACY BY SIMILARITY SCORE ===")
    if not contingency.empty and 'Yes' in contingency.columns:
        for score, correct_pct in contingency['Yes'].items():
            count = len(df[df['similarity_score'] == score])
            print(f"Similarity {score}/10: {correct_pct:.2%} correct ({count} pairs)")

def create_visualizations(df, output_prefix):
    """Create visualizations of the results"""
    # Set the style
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8))
    
    # 1. Distribution of similarity scores
    plt.subplot(2, 2, 1)
    ax = sns.countplot(x='similarity_score', data=df, palette='viridis')
    plt.title('Distribution of Similarity Scores')
    plt.xlabel('Similarity Score (1-10)')
    plt.ylabel('Count')
    
    # Add count labels on top of bars
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha = 'center', va = 'bottom')
    
    # 2. Correct identification by similarity score
    plt.subplot(2, 2, 2)
    correct_by_score = df.groupby('similarity_score')['ai_generated_correctly_identified'].apply(
        lambda x: (x == 'Yes').mean()
    ).reset_index()
    correct_by_score.columns = ['similarity_score', 'accuracy']
    
    sns.barplot(x='similarity_score', y='accuracy', data=correct_by_score, palette='viridis')
    plt.title('Identification Accuracy by Similarity Score')
    plt.xlabel('Similarity Score (1-10)')
    plt.ylabel('Accuracy')
    plt.ylim(0, 1.1)  # Set y-axis to 0-100%
    
    # 3. Overall accuracy pie chart
    plt.subplot(2, 2, 3)
    accuracy_counts = df['ai_generated_correctly_identified'].value_counts()
    plt.pie(accuracy_counts, labels=accuracy_counts.index, autopct='%1.1f%%', colors=['#66b3ff', '#ff9999'])
    plt.title('AI Detection Accuracy')
    
    # 4. Word cloud of AI identification explanations
    plt.subplot(2, 2, 4)
    create_explanation_wordcloud(df, plt)
    
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_visualizations.png", dpi=300)
    print(f"Saved visualizations to {output_prefix}_visualizations.png")
    
    # Create a second figure for additional analysis
    plt.figure(figsize=(10, 8))
    analyze_explanation_text(df, output_prefix)
    
def create_explanation_wordcloud(df, plt):
    """Create a word cloud from the explanations"""
    # Combine all explanations
    text = ' '.join(df['explanation'].dropna().astype(str))
    
    # Clean the text
    text = re.sub(r'[^\w\s]', '', text.lower())
    
    # Remove common stopwords
    stopwords = {'the', 'and', 'is', 'in', 'it', 'to', 'that', 'of', 'for', 'image', 'this', 'with', 'as', 'on', 'are', 'be', 'has', 'more', 'also'}
    wordcloud = WordCloud(
        width=800, height=400,
        background_color='white',
        stopwords=stopwords,
        max_words=100,
        contour_width=3
    ).generate(text)
    
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Common Terms in AI Detection Explanations')

def analyze_explanation_text(df, output_prefix):
    """Analyze the explanation text for common patterns"""
    # Feature extraction
    explanations = df['explanation'].fillna('').astype(str)
    
    # Look for common phrases and techniques mentioned
    techniques = {
        'symmetry': r'symmetr(y|ical)',
        'skin texture': r'skin texture|texture|pores',
        'background': r'background',
        'lighting': r'lighting|light',
        'eyes': r'eye|pupils',
        'artifacts': r'artifact|glitch',
        'unnatural': r'unnatural|unrealistic',
        'too perfect': r'perfect|flawless',
        'hair': r'hair',
        'teeth': r'teeth|tooth',
        'ears': r'ear',
    }
    
    # Count occurrences of each technique
    technique_counts = {}
    for tech, pattern in techniques.items():
        count = explanations.str.contains(pattern, case=False).sum()
        technique_counts[tech] = count
    
    # Create bar chart of techniques
    plt.barh(list(technique_counts.keys()), list(technique_counts.values()))
    plt.title('Detection Techniques Mentioned in Explanations')
    plt.xlabel('Number of Mentions')
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_detection_techniques.png", dpi=300)
    print(f"Saved detection techniques analysis to {output_prefix}_detection_techniques.png")
    
    # Print the most common detection techniques
    print("\n=== MOST COMMON DETECTION TECHNIQUES ===")
    sorted_techniques = sorted(technique_counts.items(), key=lambda x: x[1], reverse=True)
    for technique, count in sorted_techniques:
        if count > 0:
            print(f"{technique}: mentioned in {count} explanations ({count/len(df):.1%})")

def analyze_by_correctly_identified(df):
    """Compare characteristics of correctly vs incorrectly identified images"""
    print("\n=== ANALYSIS BY IDENTIFICATION RESULT ===")
    
    # Group by whether AI was correctly identified
    grouped = df.groupby('ai_generated_correctly_identified')
    
    # Calculate average similarity for each group
    avg_similarity = grouped['similarity_score'].mean()
    
    for result, avg in avg_similarity.items():
        count = len(grouped.get_group(result))
        print(f"{result} identifications ({count} pairs): Average similarity score {avg:.2f}/10")

def analyze_similarity_vs_accuracy(df, output_prefix):
    """
    Analyze the relationship between similarity scores and detection accuracy
    including confusion matrix-style analysis
    """
    print("\n=== SIMILARITY SCORE VS DETECTION ACCURACY ANALYSIS ===")
    
    # Create a new figure
    plt.figure(figsize=(15, 12))
    
    # 1. Line plot showing accuracy by similarity score
    plt.subplot(2, 2, 1)
    correct_by_score = df.groupby('similarity_score')['ai_generated_correctly_identified'].apply(
        lambda x: (x == 'Yes').mean()
    ).reset_index()
    correct_by_score.columns = ['similarity_score', 'accuracy']
    
    # Add trend line
    sns.regplot(x='similarity_score', y='accuracy', data=correct_by_score, 
                scatter=True, ci=None, line_kws={"color": "red"})
    plt.title('Detection Accuracy vs Similarity Score with Trend')
    plt.xlabel('Similarity Score (1-10)')
    plt.ylabel('Accuracy')
    plt.ylim(0, 1.1)
    
    # Calculate correlation
    correlation = df['similarity_score'].corr(df['ai_generated_correctly_identified'].map({'Yes': 1, 'No': 0}))
    plt.annotate(f'Correlation: {correlation:.2f}', xy=(0.05, 0.95), xycoords='axes fraction')
    
    print(f"Correlation between similarity score and detection accuracy: {correlation:.2f}")
    
    # 2. Confusion matrix for high vs low similarity
    plt.subplot(2, 2, 2)
    
    # Create high/low similarity categories
    median_score = df['similarity_score'].median()
    df['similarity_category'] = df['similarity_score'].apply(
        lambda x: 'High Similarity' if x >= median_score else 'Low Similarity'
    )
    
    # Create confusion matrix data
    confusion_data = pd.crosstab(
        df['similarity_category'],
        df['ai_generated_correctly_identified'],
        rownames=['Similarity'],
        colnames=['Correctly Identified']
    )
    
    # Plot heatmap of confusion matrix
    sns.heatmap(confusion_data, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title('Confusion Matrix: Similarity vs Detection Accuracy')
    
    # Print the confusion matrix data
    print("\nConfusion Matrix (counts):")
    print(confusion_data)
    
    # Calculate percentages for each similarity category
    confusion_pct = pd.crosstab(
        df['similarity_category'],
        df['ai_generated_correctly_identified'],
        normalize='index'
    ) * 100
    
    print("\nConfusion Matrix (percentages by row):")
    print(confusion_pct.round(1))
    
    # 3. Accuracy by binned similarity scores
    plt.subplot(2, 2, 3)
    
    # Create similarity bins (1-3, 4-6, 7-10)
    bins = [0, 3, 6, 10]
    labels = ['Low (1-3)', 'Medium (4-6)', 'High (7-10)']
    df['similarity_bin'] = pd.cut(df['similarity_score'], bins=bins, labels=labels, right=True)
    
    # Calculate accuracy for each bin
    bin_accuracy = df.groupby('similarity_bin')['ai_generated_correctly_identified'].apply(
        lambda x: (x == 'Yes').mean()
    ).reset_index()
    bin_accuracy.columns = ['similarity_bin', 'accuracy']
    
    # Count samples in each bin
    bin_counts = df['similarity_bin'].value_counts().sort_index()
    
    # Create bar chart
    ax = sns.barplot(x='similarity_bin', y='accuracy', data=bin_accuracy, palette='viridis')
    plt.title('Detection Accuracy by Similarity Score Range')
    plt.xlabel('Similarity Score Range')
    plt.ylabel('Accuracy')
    plt.ylim(0, 1.1)
    
    # Add count labels on top of bars
    for i, p in enumerate(ax.patches):
        ax.annotate(f'n={bin_counts[i]}', 
                   (p.get_x() + p.get_width() / 2., p.get_height() + 0.05),
                   ha = 'center')
    
    # Print binned accuracy stats
    print("\nAccuracy by Similarity Score Range:")
    for i, row in bin_accuracy.iterrows():
        bin_name = row['similarity_bin']
        accuracy = row['accuracy']
        count = bin_counts[bin_name]
        print(f"{bin_name}: {accuracy:.2%} accuracy ({count} pairs)")
    
    # 4. Detailed heatmap of all similarity scores vs correct identification
    plt.subplot(2, 2, 4)
    
    # Create a cross-tabulation of similarity scores vs correct identification
    heatmap_data = pd.crosstab(
        df['similarity_score'],
        df['ai_generated_correctly_identified'],
        normalize='index'
    )
    
    # Make sure both 'Yes' and 'No' columns exist
    if 'Yes' not in heatmap_data.columns:
        heatmap_data['Yes'] = 0
    if 'No' not in heatmap_data.columns:
        heatmap_data['No'] = 0
    
    # Extract only the 'Yes' column for the heatmap
    yes_data = heatmap_data[['Yes']].reset_index()
    yes_data.columns = ['similarity_score', 'accuracy']
    
    # Convert to wide format for heatmap
    pivot_data = yes_data.pivot_table(
        values='accuracy', 
        index=[0], 
        columns='similarity_score'
    ).fillna(0)
    
    # Plot heatmap
    sns.heatmap(pivot_data, annot=True, fmt='.2%', cmap='RdYlGn', vmin=0, vmax=1)
    plt.title('Accuracy Heatmap by Similarity Score')
    plt.xlabel('Similarity Score')
    plt.ylabel('')
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_similarity_analysis.png", dpi=300)
    print(f"Saved similarity analysis to {output_prefix}_similarity_analysis.png")

def main():
    try:
        # Load the data
        df, latest_file = load_latest_results()
        
        # Generate output prefix from the CSV filename
        output_prefix = os.path.splitext(latest_file)[0]
        
        # Basic stats
        basic_statistics(df)
        
        # Create visualizations
        create_visualizations(df, output_prefix)
        
        # Analysis by correct identification
        analyze_by_correctly_identified(df)
        
        # New confusion matrix and similarity analysis
        analyze_similarity_vs_accuracy(df, output_prefix)
        
        print("\nAnalysis complete! See the generated visualization files for details.")
        
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main() 