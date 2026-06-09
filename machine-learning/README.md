# 🧠 Machine Learning & Deep Learning Notes

A comprehensive guide from statistical machine learning foundations to deep neural architectures and state-of-the-art Generative AI (LLMs, RAG).

---

## 🗺️ Table of Contents
1. [Mathematics of Machine Learning](#1-mathematics-of-machine-learning)
2. [Classical Machine Learning Algorithms](#2-classical-machine-learning-algorithms)
3. [Deep Learning Foundations](#3-deep-learning-foundations)
4. [Generative AI & Large Language Models (LLMs)](#4-generative-ai--large-language-models-llms)

---

## 1. Mathematics of Machine Learning

Understanding the mathematics under the hood is critical for debugging model weights, loss divergence, and optimization paths.

### 📐 Linear Algebra
*   **Eigenvalues and Eigenvectors:** For a square matrix $A$, a non-zero vector $v$ satisfies:
    $$A v = \lambda v$$
    where $\lambda$ represents the eigenvalue. In PCA (Principal Component Analysis), eigenvectors represent the principal axes of variance.
*   **Matrix Decomposition (SVD):** Decomposes any matrix $A$ of dimensions $m \times n$ into three matrices:
    $$A = U \Sigma V^T$$
    Used in collaborative filtering recommendation engines and data compression.

### 📈 Calculus
*   **The Gradient ($\nabla f$):** The vector of partial derivatives pointing in the direction of steepest ascent:
    $$\nabla f(x_1, x_2, \dots, x_n) = \left[ \frac{\partial f}{\partial x_1}, \frac{\partial f}{\partial x_2}, \dots, \frac{\partial f}{\partial x_n} \right]$$
*   **Hessian Matrix:** The square matrix of second-order partial derivatives, denoting the local curvature of a function. Used in second-order optimization methods like Newton-Raphson (and XGBoost's custom objective expansions).

### 🎲 Probability & Estimation
*   **Bayes' Theorem:**
    $$P(A|B) = \frac{P(B|A)P(A)}{P(B)}$$
*   **Maximum Likelihood Estimation (MLE):** Estimates model parameters by maximizing the likelihood of the observed data:
    $$\theta_{\text{MLE}} = \arg\max_{\theta} \log P(X|\theta)$$
*   **Maximum A Posteriori (MAP):** Introduces a prior probability distribution $P(\theta)$ (acting as a regularizer):
    $$\theta_{\text{MAP}} = \arg\max_{\theta} \left[ \log P(X|\theta) + \log P(\theta) \right]$$

---

## 2. Classical Machine Learning Algorithms

### Linear and Logistic Regression
*   **Regularization Cost Functions:**
    *   **L1 Regularization (Lasso):** Introduces absolute penalty: $\lambda \sum |\theta_i|$. Generates sparse weights (forces coefficients to zero), acting as a built-in feature selector.
    *   **L2 Regularization (Ridge):** Introduces squared penalty: $\lambda \sum \theta_i^2$. Minimizes coefficients without forcing them to zero. Good for handling multicollinearity.
    *   **ElasticNet:** Linear combination of L1 and L2 penalties.

### Tree-Based Ensemble Methods
*   **Random Forests:** Bagging (Bootstrap Aggregation) technique. Trains multiple decision trees in parallel on bootstrap samples. Reduces variance without changing bias.
*   **Gradient Boosting Decision Trees (GBDT):** Boosting technique. Trains trees sequentially, with each tree fitting the residual errors of the previous ensemble. Highly optimized frameworks:
    *   **XGBoost:** Utilizes pre-sorted splitting, weighted quantile sketch, and Taylor expansion for custom loss functions.
    *   **LightGBM:** Employs Leaf-wise growth (instead of Level-wise) and GOSS (Gradient-based One-Side Sampling) for high speed on massive datasets.

---

## 3. Deep Learning Foundations

### Activation Functions
*   **ReLU:** $f(x) = \max(0, x)$. Mitigates vanishing gradient issues but can suffer from "dying ReLU" (inactive neurons).
*   **GELU (Gaussian Error Linear Unit):** $f(x) = x \cdot \Phi(x)$ (where $\Phi(x)$ is the cumulative distribution function of the standard normal distribution). Used in BERT, GPT, and modern transformer architectures.

### Optimization & Backpropagation
Modern neural networks adjust weights using the Chain Rule to propagate loss backward from the output layer:
$$\frac{\partial L}{\partial w_{ij}} = \frac{\partial L}{\partial a_j} \cdot \frac{\partial a_j}{\partial z_j} \cdot \frac{\partial z_j}{\partial w_{ij}}$$

#### Common Optimizers:
- **SGD (Stochastic Gradient Descent):** Updates weights based on mini-batches.
- **Adam (Adaptive Moment Estimation):** Tracks both first moment (momentum) and second moment (uncentered variance) of gradients to scale learning rate dynamically per parameter.
- **AdamW:** Corrects Adam's weight decay behavior by decoupling weight decay from the gradient update step.

---

## 4. Generative AI & Large Language Models (LLMs)

### The Transformer (Self-Attention)
Introduced in *Attention Is All You Need* (2017). Replaced recurrent networks (LSTMs) with self-attention, enabling massive parallelization.

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

where:
*   $Q$ (Query), $K$ (Key), $V$ (Value) are linear projections of input embeddings.
*   $\sqrt{d_k}$ is the scaling factor (dimension of keys) to prevent dot-products from growing too large in high dimensions (which drives softmax into flat gradients).

```
Input Tokens ➡️ Word Embeddings ➡️ Self-Attention Layer ➡️ Feed Forward ➡️ Logits ➡️ Next Token
```

### Parameter-Efficient Fine-Tuning (PEFT)
Fine-tuning models with billions of parameters requires substantial memory. PEFT reduces compute overhead.
*   **LoRA (Low-Rank Adaptation):** Keeps base model weights frozen. Injects trainable rank decomposition matrices ($A$ and $B$) into the attention layers.
    $$W_{\text{updated}} = W_{\text{frozen}} + \Delta W \quad \text{where} \quad \Delta W = B \cdot A$$
    If $W$ is $d \times d$, and rank $r \ll d$, the number of parameters drops from $d^2$ to $2 \cdot d \cdot r$.
*   **QLoRA (Quantized LoRA):** Compresses the base model to 4-bit NormalFloat (NF4) and uses Double Quantization to further reduce RAM usage during LoRA fine-tuning.

### Retrieval-Augmented Generation (RAG)
Augments LLMs with external, dynamic data sources without re-training.

```
                   ┌─────────────────┐
                   │  User Question  │
                   └────────┬────────┘
                            │
                            ▼
             ┌──────────────────────────────┐
             │ Vector Embeddings & Indexing  │
             └──────────────┬───────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   Retrieval Query     │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Vector Database Search│
                └───────────┬───────────┘
                            │ (Relevant Context Documents)
                            ▼
    ┌───────────────────────────────────────────────┐
    │ Augmentation (Inject System Prompt + Context) │
    └───────────────────────┬───────────────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │  LLM Engine │
                     └──────┬──────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Accurate Response │
                  └───────────────────┘
```
*   **Key Optimizations:**
    *   *Hierarchical Node Parsing:* Chunking documents into parent-child blocks.
    *   *Hybrid Search:* Combining semantic search (embeddings) with keyword search (BM25).
    *   *Reranking:* Re-scoring retrieved nodes using a cross-encoder model (e.g., Cohere Rerank) to prioritize top relevance.
