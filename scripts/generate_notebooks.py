#!/usr/bin/env python3
import os
import json

def create_notebook_structure(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

def make_markdown_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source]
    }

def make_code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source]
    }

def generate_attention_notebook():
    cells = [
        make_markdown_cell([
            "# 🧠 Multi-Head Attention From Scratch (PyTorch)",
            "",
            "This notebook implements the foundational component of the Transformer architecture: **Multi-Head Attention**, as introduced in the paper *'Attention Is All You Need'* (Vaswani et al., 2017).",
            "",
            "### The Self-Attention Formula",
            "Attention is calculated by mapping a query and a set of key-value pairs to an output:",
            "$$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V$$",
            "Where $d_k$ is the dimensionality of the keys."
        ]),
        make_markdown_cell([
            "## 1. Import Dependencies"
        ]),
        make_code_cell([
            "import math",
            "import torch",
            "import torch.nn as nn",
            "import torch.nn.functional as F",
            "",
            "print(f\"PyTorch Version: {torch.__version__}\")"
        ]),
        make_markdown_cell([
            "## 2. Scaled Dot-Product Attention",
            "This function performs the core Q, K, V attention computations. We include scaling by $1/\\sqrt{d_k}$ to prevent gradient saturation, and support an optional mask."
        ]),
        make_code_cell([
            "def scaled_dot_product_attention(q, k, v, mask=None):",
            "    # Get key dimensions",
            "    d_k = q.size(-1)",
            "    ",
            "    # Calculate attention scores",
            "    # q: [batch, heads, seq_len, d_k], k^T: [batch, heads, d_k, seq_len]",
            "    scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(d_k)",
            "    ",
            "    # Apply optional mask (e.g. for autoregressive causal decoding)",
            "    if mask is not None:",
            "        scores = scores.masked_fill(mask == 0, -1e9)",
            "        ",
            "    # Apply softmax to get attention probabilities",
            "    attention_weights = F.softmax(scores, dim=-1)",
            "    ",
            "    # Multiply by values",
            "    output = torch.matmul(attention_weights, v)",
            "    return output, attention_weights"
        ]),
        make_markdown_cell([
            "## 3. Multi-Head Attention Class",
            "Rather than performing single attention projection, we split our queries, keys, and values into multiple heads to allow the model to jointly attend to information from different representation subspaces at different positions."
        ]),
        make_code_cell([
            "class MultiHeadAttention(nn.Module):",
            "    def __init__(self, d_model, num_heads):",
            "        super().__init__()",
            "        assert d_model % num_heads == 0, \"d_model must be divisible by num_heads\"",
            "        ",
            "        self.d_model = d_model",
            "        self.num_heads = num_heads",
            "        self.d_k = d_model // num_heads",
            "        ",
            "        # Projections for Q, K, V",
            "        self.q_linear = nn.Linear(d_model, d_model)",
            "        self.k_linear = nn.Linear(d_model, d_model)",
            "        self.v_linear = nn.Linear(d_model, d_model)",
            "        ",
            "        # Final output projection",
            "        self.out_linear = nn.Linear(d_model, d_model)",
            "        ",
            "    def split_heads(self, x, batch_size):",
            "        # x shape: [batch, seq_len, d_model] -> [batch, seq_len, num_heads, d_k] -> [batch, num_heads, seq_len, d_k]",
            "        x = x.view(batch_size, -1, self.num_heads, self.d_k)",
            "        return x.transpose(1, 2)",
            "        ",
            "    def forward(self, q, k, v, mask=None):",
            "        batch_size = q.size(0)",
            "        ",
            "        # 1. Project Q, K, V",
            "        q = self.q_linear(q)",
            "        k = self.k_linear(k)",
            "        v = self.v_linear(v)",
            "        ",
            "        # 2. Split into heads",
            "        q = self.split_heads(q, batch_size)",
            "        k = self.split_heads(k, batch_size)",
            "        v = self.split_heads(v, batch_size)",
            "        ",
            "        # 3. Apply Scaled Dot-Product Attention",
            "        output, attention_weights = scaled_dot_product_attention(q, k, v, mask)",
            "        ",
            "        # 4. Concatenate heads back",
            "        # output shape: [batch, num_heads, seq_len, d_k] -> [batch, seq_len, num_heads, d_k] -> [batch, seq_len, d_model]",
            "        output = output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)",
            "        ",
            "        # 5. Final output projection",
            "        return self.out_linear(output), attention_weights"
        ]),
        make_markdown_cell([
            "## 4. Verify & Test the Implementation"
        ]),
        make_code_cell([
            "# Instantiate Multi-Head Attention module",
            "d_model = 64",
            "num_heads = 8",
            "mha = MultiHeadAttention(d_model, num_heads)",
            "",
            "# Create mock batch input: [batch_size=2, seq_len=5, d_model=64]",
            "x = torch.randn(2, 5, d_model)",
            "",
            "# Forward pass",
            "output, attn_weights = mha(x, x, x)",
            "",
            "print(\"Execution Successful!\")",
            "print(f\"Input Shape:  {x.shape}\")",
            "print(f\"Output Shape: {output.shape}\")",
            "print(f\"Attention weights shape: {attn_weights.shape}\")"
        ])
    ]
    return create_notebook_structure(cells)

def generate_resnet_notebook():
    cells = [
        make_markdown_cell([
            "# 🖼️ ResNet Residual & Bottleneck Blocks (PyTorch)",
            "",
            "This notebook implements the architectural blocks that revolutionized deep computer vision: **Residual Blocks** and **Bottleneck Blocks**, introduced in the landmark paper *'Deep Residual Learning for Image Recognition'* (He et al., 2015).",
            "",
            "### The Residual Concept",
            "Instead of hoping stacked layers fit a desired underlying mapping $H(x)$, we let these layers fit a residual mapping $F(x) = H(x) - x$. The original mapping is recast into $F(x) + x$, achieved via a shortcut connection (identity mapping)."
        ]),
        make_markdown_cell([
            "## 1. Import Dependencies"
        ]),
        make_code_cell([
            "import torch",
            "import torch.nn as nn",
            "",
            "print(f\"PyTorch Version: {torch.__version__}\")"
        ]),
        make_markdown_cell([
            "## 2. Basic Residual Block (ResNet-18 & ResNet-34)",
            "Composed of two $3\\times3$ convolutional layers. If the dimension changes (due to stride), we project the identity shortcut using a $1\\times1$ convolution."
        ]),
        make_code_cell([
            "class BasicBlock(nn.Module):",
            "    expansion = 1",
            "    ",
            "    def __init__(self, in_planes, planes, stride=1):",
            "        super().__init__()",
            "        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)",
            "        self.bn1 = nn.BatchNorm2d(planes)",
            "        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)",
            "        self.bn2 = nn.BatchNorm2d(planes)",
            "        ",
            "        self.shortcut = nn.Sequential()",
            "        # If spatial size changes or input channels don't match output channels",
            "        if stride != 1 or in_planes != self.expansion * planes:",
            "            self.shortcut = nn.Sequential(",
            "                nn.Conv2d(in_planes, self.expansion * planes, kernel_size=1, stride=stride, bias=False),",
            "                nn.BatchNorm2d(self.expansion * planes)",
            "            )",
            "            ",
            "    def forward(self, x):",
            "        out = torch.relu(self.bn1(self.conv1(x)))",
            "        out = self.bn2(self.conv2(out))",
            "        # Add the identity shortcut mapping",
            "        out += self.shortcut(x)",
            "        out = torch.relu(out)",
            "        return out"
        ]),
        make_markdown_cell([
            "## 3. Bottleneck Block (ResNet-50, 101, & 152)",
            "For deeper networks, a three-layer bottleneck structure is used: $1\\times1$, $3\\times3$, and $1\\times1$ convolutions. The $1\\times1$ layers are responsible for reducing and restoring dimensions, leaving the $3\\times3$ layer a bottleneck with smaller input/output dimensions."
        ]),
        make_code_cell([
            "class BottleneckBlock(nn.Module):",
            "    expansion = 4",
            "    ",
            "    def __init__(self, in_planes, planes, stride=1):",
            "        super().__init__()",
            "        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1, bias=False)",
            "        self.bn1 = nn.BatchNorm2d(planes)",
            "        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)",
            "        self.bn2 = nn.BatchNorm2d(planes)",
            "        self.conv3 = nn.Conv2d(planes, self.expansion * planes, kernel_size=1, bias=False)",
            "        self.bn3 = nn.BatchNorm2d(self.expansion * planes)",
            "        ",
            "        self.shortcut = nn.Sequential()",
            "        if stride != 1 or in_planes != self.expansion * planes:",
            "            self.shortcut = nn.Sequential(",
            "                nn.Conv2d(in_planes, self.expansion * planes, kernel_size=1, stride=stride, bias=False),",
            "                nn.BatchNorm2d(self.expansion * planes)",
            "            )",
            "            ",
            "    def forward(self, x):",
            "        out = torch.relu(self.bn1(self.conv1(x)))",
            "        out = torch.relu(self.bn2(self.conv2(out)))",
            "        out = self.bn3(self.conv3(out))",
            "        # Add shortcut link",
            "        out += self.shortcut(x)",
            "        out = torch.relu(out)",
            "        return out"
        ]),
        make_markdown_cell([
            "## 4. Test the Architectures"
        ]),
        make_code_cell([
            "# Generate dummy tensor representing a batch of 2 RGB images of size 64x64",
            "dummy_input = torch.randn(2, 64, 64, 64)",
            "",
            "# Instantiate Blocks",
            "basic = BasicBlock(in_planes=64, planes=64)",
            "bottleneck = BottleneckBlock(in_planes=64, planes=16, stride=2) # 16*4 = 64 channels out, strides down",
            "",
            "out_basic = basic(dummy_input)",
            "out_bottleneck = bottleneck(dummy_input)",
            "",
            "print(\"Blocks Run Successfully!\")",
            "print(f\"Input shape:      {dummy_input.shape}\")",
            "print(f\"Basic output:      {out_basic.shape}\")",
            "print(f\"Bottleneck output: {out_bottleneck.shape}\")"
        ])
    ]
    return create_notebook_structure(cells)

def generate_rag_notebook():
    cells = [
        make_markdown_cell([
            "# 🔍 Zero-Dependency Vector Search & RAG Pipeline",
            "",
            "This notebook implements a simple, zero-dependency **Retrieval-Augmented Generation (RAG)** vector search mechanism. We chunk textual documents, represent them using basic tf-idf/token counting vectors, index them in a simple Vector DB, query them using cosine similarity, and build a prompt for generation."
        ]),
        make_markdown_cell([
            "## 1. Import Modules"
        ]),
        make_code_cell([
            "import math",
            "import re",
            "from collections import Counter",
            "",
            "print(\"Standard modules imported successfully!\")"
        ]),
        make_markdown_cell([
            "## 2. Text Processor & Embedding Simulation",
            "Since we are not calling external LLM APIs, we will build a simple TF-IDF vectorizer that converts text blocks into sparse bag-of-words coordinate arrays."
        ]),
        make_code_cell([
            "def tokenize(text):",
            "    text = text.lower()",
            "    return re.findall(r'\\w+', text)",
            "",
            "def calculate_cosine_similarity(vec1, vec2):",
            "    # dot product / (norm1 * norm2)",
            "    intersection = set(vec1.keys()) & set(vec2.keys())",
            "    dot_product = sum(vec1[x] * vec2[x] for x in intersection)",
            "    ",
            "    sum1 = sum(vec1[x]**2 for x in vec1.keys())",
            "    sum2 = sum(vec2[x]**2 for x in vec2.keys())",
            "    ",
            "    denominator = math.sqrt(sum1) * math.sqrt(sum2)",
            "    if not denominator:",
            "        return 0.0",
            "    return float(dot_product) / denominator"
        ]),
        make_markdown_cell([
            "## 3. The Vector Database Index",
            "Here, we implement a simple `VectorDB` to store document strings and query them based on semantic/cosine similarity."
        ]),
        make_code_cell([
            "class VectorDB:",
            "    def __init__(self):",
            "        self.documents = []",
            "        ",
            "    def add_document(self, doc_id, text):",
            "        tokens = tokenize(text)",
            "        vector = Counter(tokens)",
            "        self.documents.append({",
            "            \"id\": doc_id,",
            "            \"text\": text,",
            "            \"vector\": vector",
            "        })",
            "        ",
            "    def query(self, query_text, top_k=1):",
            "        query_tokens = tokenize(query_text)",
            "        query_vector = Counter(query_tokens)",
            "        ",
            "        results = []",
            "        for doc in self.documents:",
            "            score = calculate_cosine_similarity(query_vector, doc[\"vector\"])",
            "            results.append((doc, score))",
            "            ",
            "        # Sort by similarity score descending",
            "        results.sort(key=lambda x: x[1], reverse=True)",
            "        return results[:top_k]"
        ]),
        make_markdown_cell([
            "## 4. Run the RAG Pipeline",
            "We populate the index, search for coordinates, extract the top-matching context, and build a structured prompt."
        ]),
        make_code_cell([
            "db = VectorDB()",
            "",
            "# 1. Add knowledge chunks",
            "db.add_document(\"doc1\", \"SQL execution order is FROM -> JOIN -> WHERE -> GROUP BY -> SELECT.\")",
            "db.add_document(\"doc2\", \"Python generators use lazy evaluation to save memory, yielding items one by one.\")",
            "db.add_document(\"doc3\", \"Transformers use causal self-attention mechanisms with scaled dot products for language modeling.\")",
            "db.add_document(\"doc4\", \"Polars is written in Rust, utilizing parallel CPU scheduling and lazy evaluation query plans.\")",
            "",
            "# 2. Query the Vector DB",
            "query = \"How does Polars run data operations so quickly?\"",
            "hits = db.query(query, top_k=1)",
            "best_match, score = hits[0]",
            "",
            "print(f\"Query: {query}\")",
            "print(f\"Best Match ({score:.2f}% similarity): {best_match['text']}\\n\")",
            "",
            "# 3. Build RAG Prompt",
            "prompt = f\"\"\"Context: {best_match['text']}",
            "",
            "Question: {query}",
            "Answer utilizing the context provided above:\"\"\"",
            "",
            "print(\"--- RAG PROMPT SENT TO GENERATOR ---\")",
            "print(prompt)"
        ])
    ]
    return create_notebook_structure(cells)

def main():
    notebooks_dir = "notebooks"
    os.makedirs(notebooks_dir, exist_ok=True)
    
    # Generate Attention Notebook
    with open(os.path.join(notebooks_dir, "attention_from_scratch.ipynb"), "w", encoding="utf-8") as f:
        json.dump(generate_attention_notebook(), f, indent=1)
    print("Notebook compiled: notebooks/attention_from_scratch.ipynb")
    
    # Generate ResNet Notebook
    with open(os.path.join(notebooks_dir, "resnet_block_from_scratch.ipynb"), "w", encoding="utf-8") as f:
        json.dump(generate_resnet_notebook(), f, indent=1)
    print("Notebook compiled: notebooks/resnet_block_from_scratch.ipynb")
    
    # Generate RAG Notebook
    with open(os.path.join(notebooks_dir, "simple_rag_vector_search.ipynb"), "w", encoding="utf-8") as f:
        json.dump(generate_rag_notebook(), f, indent=1)
    print("Notebook compiled: notebooks/simple_rag_vector_search.ipynb")

if __name__ == "__main__":
    main()
