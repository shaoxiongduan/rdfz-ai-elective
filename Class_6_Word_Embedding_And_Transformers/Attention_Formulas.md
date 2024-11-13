# [Self Attention Mechanism](https://arxiv.org/abs/1706.03762)
~~~
Incorporating context into sequences.
~~~

We have a sequence of embeddings $a_1, a_2, \cdots, a_n$. Each $a_i$ is an embedding with $m$ dimensions. We want to compute $a_1', a_2', \cdots, a_n'$, where $a_i'$ represents the meaning of $a_i$ in the context of the entire sequence. In practice, $a_i'$ is a weighted sum of all the embeddings in the sequence.

## Down-Projecting Embeddings

Each word has a query, key and value, calculated by projecting the embedding vectors with learnable matrices $W_Q$, $W_K$ and $W_V$.

$$
Q_i = a_i W_Q\\
K_i = a_i W_K\\
V_i = a_i W_V
$$

## Calculating Attention Scores

First, we calculate the attention scores $s_{ij}$ for each pair of embeddings $a_i$ and $a_j$. This measures how much the meaning of $a_j$ affects the meaning $a_i$.


$$
S_{ij} = Q_i \cdot K_j
$$

The dot product of the query and key vectors is a measure of how similar the two vectors are. A larger dot product indicates a stronger relationship between the two words.


## Calculating Attention Weights

Next, we apply softmax to the attention score to calculate attention weights $w_{ij}$ for each pair of embeddings $a_i$ and $a_j$. These weights represent the importance of $a_j$ in the context of $a_i$.

$$
w_{ij} = \frac{\exp(S_{ij})}{\sum_{k=1}^n \exp(S_{ik})}
$$

Recall that this is the same softmax function we used in classification. This turns the attention scores into a probabilistic distribution.

## Calculating the Contextualized Embedding

Now that we know the attention weights, we can calculate the contextualized embedding $a_i'$ for each word $a_i$ simply by taking a weighted sum of all the values of the embeddings in the sequence according to attention weights.

$$
a_i' = \sum_{j=1}^n w_{ij} V_j
$$

## Matrix Representation

$$
Q=aW_Q\\
K=aW_K\\
V=aW_V\\
S=QK^T\\
w=\text{softmax}(S)\\
a'=wV
$$

Simply, each self-attention layer achieves the following:
$$
\text{softmax}(QK^T)V
$$


## Up-Projecting Embeddings

Finally, we up-project the contextualized embeddings $a_i'$ back to the original embedding size with a learnable matrix $W_O$ to obtain the final output embeddings $o_i$.

$$
o_i = a_i' W_O
$$

or

$$
o = a' W_O
$$

## Dimension Analysis

- $a \in \mathbb{R}^{n \times m}$
- $W_Q \in \mathbb{R}^{m \times d_k}$
- $W_K \in \mathbb{R}^{m \times d_k}$
- $W_V \in \mathbb{R}^{m \times d_v}$
- $W_O \in \mathbb{R}^{d_v \times m}$
- $Q \in \mathbb{R}^{n \times d_k}$, $K \in \mathbb{R}^{n \times d_k}$, $V \in \mathbb{R}^{n \times d_v}$
- $S \in \mathbb{R}^{n \times n}$
- $w \in \mathbb{R}^{n \times n}$
- $a' \in \mathbb{R}^{n \times d_v}$
- $o \in \mathbb{R}^{n \times m}$

# Resources
[The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)