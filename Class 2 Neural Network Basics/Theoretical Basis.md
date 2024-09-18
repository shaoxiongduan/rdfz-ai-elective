# Why Gradient Descent Works
and when does it work best?

__This report is the theoretical basis of gradient descent from the bottom up.__

## Definitions

### Limits

$$
\lim_{x \to c} f(x) = L
$$

This reads "the limit of $f(x)$ as $x$ approaches $c$ is $L$". It means that as $x$ gets closer and closer to $c$, $f(x)$ gets closer and closer to $L$. Formally, the above expression is equivalent to

$$
(\forall \epsilon > 0)(\exists \delta > 0)(0 < |x - c| < \delta \implies |f(x) - L| < \epsilon)
$$

While it is easy to prove that $L$ must be unique shall it exist, it is important to note that such an $L$ may not exist. For our purposes, we will not dive deep into the corner cases.

__Some important principles of limits:__

We will be using these later on. These should be intuitive enough, but I do encourage you to at least ponder about how they can be proved.

1. $\displaystyle\lim_{x \to c} f(x) + \lim_{x \to c} g(x) = \lim_{x \to c} \Big(f(x) + g(x)\Big)$
2. $\displaystyle\lim_{x \to c} f(x) \cdot \lim_{x \to c} g(x) = \lim_{x \to c} \Big(f(x) \cdot g(x)\Big)$

### Continuity

A function $f(x)$ is continuous at $x = c$ if

$$
\lim_{x \to c} f(x) = f(c)
$$

A function $f(x)$ is continuous (everywhere) if:

$$
(\forall c\in \mathbb{R})\Big(\lim_{x\to c} f(x) = f(c)\Big)
$$

### Derivatives

In order to run back propagation, we need the slope of the loss function (A.K.A the gradient) at specific points. The formal term for this is the derivative.

The derivative of a function $f(x)$ with respect to $x$ at $x = c$ is defined as

$$
f'(c) = \lim_{h \to 0} \frac{f(c + h) - f(c)}{h}
$$

Also written as $\dot f(c)$, $\frac{d}{dx}f(x)\vert_{x=c}$ or $\frac{df}{dx}\vert_{x=c}$

A function is called "differentiable" if its derivative exists at every point.

### Partial Derivatives

Let $f$ be a function with many inputs, $x_0, x_1,\dots x_n$. The partial derivative of $f$ with respect to one of its inputs, $x_i$, at $(\forall j\in\{0,1,\dots n\})(x_j = c_j)$ is defined as:


$$
\frac{\partial f}{\partial x_i}(c_0, c_1, \dots, c_n) = \lim_{h \to 0} \frac{f(c_0, c_1, \dots, c_{i-1}, c_i + h, c_{i+1}, \dots, c_n) - f(c_0, c_1, \dots, c_{i-1}, c_i, c_{i+1}, \dots, c_n)}{h}
$$

## How it works

### The Loss Function

The loss function is a function to measure how well the neural network performs on the training data. It takes in all neural network parameters as inputs, and outputs a single number representing the loss, which represents the "error" of the neural network. A very common one to use is mean-squared error loss (MSE):

$$
L(\theta)=\frac{1}{n} \sum_{i=1}^n (y_i - f_\theta(x_i))^2
$$

where $x_i$ are the input data, $y_i$ are the labels, and $n$ is the number of data points in the training dataset.

We can also use $X$ to represent a vector  containing all the input data, and $y$ to represent a vector containing all the labels. This way, the MSE loss function can be written as:

$$
L(\theta)=\frac{1}{n} \lvert y-f_\theta(X) \rvert^2
$$

The MSE loss is most often used as the loss function for regression tasks. For classification tasks, it is more appropriate to use cross-entropy (CE) loss:

$$
L(\theta)=-\frac{1}{n} \sum_{i=1}^n\Big(\log f(x_i)_{y_i}\Big)
$$

Let's say we have a neural network $f_\theta$, where $\theta$ is a vector representing all of the parameters in the network, including the weights and the biases. Our objective is to find the optimal parameters $\theta^{\star}$ such that the loss function is minimized. Let's use the mean squared error loss function as an example:

$$
\theta^{\star} = \arg\min_{\theta} \frac{1}{n} \lvert y-f_\theta(X) \rvert^2
$$



### The Principle
From the definition, we can see that the derivative of a function means that a very small increment in $x$ (from $x=c$ to $x=c+h$) will cause $f(x)$ to change by $f'(c)\times h$. Visually, the derivative is equal to the slope of the line tangent to the $f$ at $x=c$. This is why the derivative can tell us in which direction to move $x$ in order to result in a decrease in $f$.

Partial derivatives are a lot harder to visualize in the same way, but the principle is the same. When calculating a partial derivative with respect to a certain variable, all other variables are being "viewed as" constants. Therefore, the partial derivative tells us how much the function changes with a slight increment in the specific variable. The partial derivative of the loss function with respect to each parameter tells us the direction we need to move each specific parameter in order to decrease the loss function.

Gradient descent works by repeatedly taking the derivative **of the loss function** and moving $x$ in the direction of the negative gradient, which, by definition (if the step we take is small enough), is guaranteed to reduce the loss function.

The size of the step we take is the magnitude of the gradient multiplied by a hyperparameter called "learning rate". The learning rate is a hyperparameter that controls how much we move in the direction of the gradient. If the learning rate is too high, we may overshoot the minimum. If the learning rate is too low, we may take too long to reach the minimum. This makes learning rate one of the most important hyperparameters to tune for in the training process.

### The Algorithm

In order to calculate partial derivatives, we use an algorithm known as "back propagation". This algorithm starts by calculating the partial derivatives of the parameters on the outmost layer and the partial derivative of each node, then using those calculations to calculate the partial derivatives of the parameters on the next layer and so on until we reach the input layer.

The method used to calculate the gradients of the next layer using the gradients of the current layer is called "chain rule" in calculus. The chain rule states that the partial derivative of the loss function with respect to a parameter in a layer is equal to the partial derivative of the loss function with respect to the output of the layer multiplied by the partial derivative of the output of the layer with respect to the parameter.

____

__Here is a very simple (perhaps oversimplified) proof of the chain rule:__

An important condition for the chain rule to hold is that functions involved must be differentiable (the exact conditions are a lot more specific). Let $f$ be a function of $u$ (and other variables) and $u$ be a function of $x$ (and other variables). Given that both $f$ and $u$ are differentiable, we have:

$$
\frac{\partial}{\partial{u}}f = \lim_{k\to 0}\frac{f(u(x)+k)-f(u(x))}{k}
$$

Since we know that $u$ is differentiable, it must also be continuous (try to prove this yourself). This means $\displaystyle\lim_{l\to x}u(l)=u(x)$. Setting $h=l-x$ and rearranging gives: $\displaystyle\lim_{h\to 0}\Big(u(x+h)-u(x)\Big)=0$. Another way of writing this is $u(x+h)-u(x)\to 0$ as $h\to 0$.

Set $k=u(x+h)-u(x)$ in the previous equation:

$$
\frac{\partial}{\partial{u}}f = \lim_{u(x+h)-u(x)\to 0}\frac{f(u(x)+u(x+h)-u(x))-f(u(x))}{u(x+h)-u(x)}
$$

We know that $u(x+h)-u(x)$ will approach $0$ as $h\to 0$, so we can rewrite the equation as:

$$
\frac{\partial}{\partial{u}}f = \lim_{h\to 0}\frac{f(u(x+h))-f(u(x))}{u(x+h)-u(x)}
$$

By definition, we have

$$
\frac{\partial}{\partial{x}}u = \lim_{h\to 0}\frac{u(x+h)-u(x)}{h}
$$

Multiplying the above two equations gives:

$$
\frac{\partial f}{\partial u}\cdot\frac{\partial u}{\partial x} = \lim_{h\to 0}\frac{f(u(x+h))-f(u(x))}{u(x+h)-u(x)}\cdot\frac{u(x+h)-u(x)}{h}=\lim_{h\to 0}\frac{f(u(x+h))-f(u(x))}{h}=\frac{\partial f}{\partial x}
$$

**In the above proof, irrelevant variables for $f$ and $u$ were omitted**

____

We can easily calculate the partial derivative of the output of a single layer with respect to its parameters, and the partial derivative of the loss function with respect to each layer would be "back propagated" from the output layer to the input layer.

Each optimization step looks somewhat like this:

$$
\theta \leftarrow \theta - \eta \nabla_\theta L(\theta)
$$

where $\eta$ is the learning rate and $\nabla_\theta L(\theta)$ is the gradient of the loss function $L$. This is a very primitive optimization technique. Most optimizers used today apply a more complex function to the calculated gradient before using it to update the parameters, but the basic idea is similar.