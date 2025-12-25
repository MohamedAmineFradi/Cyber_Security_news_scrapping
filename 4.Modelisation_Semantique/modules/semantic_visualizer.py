from typing import List, Dict, Tuple
import numpy as np
from sklearn.manifold import TSNE
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)


class SemanticVisualizer:
    def __init__(self, model: Word2Vec, perplexity: int = 30, random_state: int = 42):
        self.model = model
        self.wv = model.wv
        self.perplexity = perplexity
        self.random_state = random_state
        self.tsne_results = None
        self.top_words = None
    
    def prepare_visualization(self, n_words: int = 100) -> np.ndarray:
        logger.info(f"Sélection des {n_words} mots les plus fréquents...")
        self.top_words = self.wv.index_to_key[:n_words]
        vectors = np.array([self.wv[word] for word in self.top_words])
        
        logger.info(f"Réduction dimensionnelle t-SNE (perplexity={self.perplexity})...")
        tsne = TSNE(
            n_components=2,
            perplexity=self.perplexity,
            random_state=self.random_state,
            max_iter=1000,
            verbose=0
        )
        self.tsne_results = tsne.fit_transform(vectors)
        
        logger.info(f"Réduction terminée: {self.tsne_results.shape}")
        return self.tsne_results
    
    def plot_embedding(self, output_path: str = None, figsize: Tuple[int, int] = (16, 12)):
        if self.tsne_results is None or self.top_words is None:
            raise ValueError("Must call prepare_visualization first")
        
        logger.info("Création du graphique...")
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.scatter(self.tsne_results[:, 0], self.tsne_results[:, 1], 
                  alpha=0.6, s=50, c='steelblue', edgecolors='navy', linewidth=0.5)
        
        for i, word in enumerate(self.top_words):
            ax.annotate(word, 
                       xy=(self.tsne_results[i, 0], self.tsne_results[i, 1]),
                       xytext=(3, 3), textcoords='offset points',
                       fontsize=9, alpha=0.7)
        
        ax.set_xlabel('t-SNE 1', fontsize=12)
        ax.set_ylabel('t-SNE 2', fontsize=12)
        ax.set_title('Word2Vec Semantic Space (t-SNE Visualization)', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Graphique sauvegardé: {output_path}")
        
        plt.close()
    
    def plot_word_clusters(self, words_groups: Dict[str, List[str]], 
                          output_path: str = None, figsize: Tuple[int, int] = (14, 10)):
        if self.tsne_results is None or self.top_words is None:
            raise ValueError("Must call prepare_visualization first")
        
        logger.info("Création du graphique des clusters...")
        fig, ax = plt.subplots(figsize=figsize)
        
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
        
        ax.scatter(self.tsne_results[:, 0], self.tsne_results[:, 1], 
                  alpha=0.2, s=30, c='lightgray')
        
        for color_idx, (group_name, words) in enumerate(words_groups.items()):
            color = colors[color_idx % len(colors)]
            indices = [i for i, word in enumerate(self.top_words) if word in words]
            
            if indices:
                x = self.tsne_results[indices, 0]
                y = self.tsne_results[indices, 1]
                ax.scatter(x, y, alpha=0.8, s=100, c=color, label=group_name, edgecolors='black', linewidth=1)
                
                for idx in indices:
                    ax.annotate(self.top_words[idx],
                               xy=(self.tsne_results[idx, 0], self.tsne_results[idx, 1]),
                               xytext=(3, 3), textcoords='offset points',
                               fontsize=9, fontweight='bold')
        
        ax.set_xlabel('t-SNE 1', fontsize=12)
        ax.set_ylabel('t-SNE 2', fontsize=12)
        ax.set_title('Word2Vec Semantic Clusters', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Graphique clusters sauvegardé: {output_path}")
        
        plt.close()
    
    def get_visualization_data(self) -> Dict:
        if self.tsne_results is None or self.top_words is None:
            raise ValueError("Must call prepare_visualization first")
        
        return {
            'words': self.top_words,
            'coordinates': self.tsne_results.tolist(),
            'perplexity': self.perplexity
        }
