# Why Gradient Descent Works
and when does it not?

__This report is the theoretical basis of back propagation from the bottom up.__

## Definitions

### Limits

$$
\lim_{x \to c} f(x) = L
$$
This reads "the limit of $f(x)$ as $x$ approaches $c$ is $L$". It means that as $x$ gets closer and closer to $c$, $f(x)$ gets closer and closer to $L$. Formally, the above expressionis equivalent to

$$
(\forall \epsilon > 0)(\exists \delta > 0)(0 < |x - c| < \delta \implies |f(x) - L| < \epsilon)
$$

While it is easy to prove that $L$ must be unique shall it exist, it is important to note that such an $L$ may not exist. For our purposes, we will not dive deep into the corner cases.

### Continuity

A function $f(x)$ is continuous at $x = c$ if

$$
\lim_{x \to c} f(x) = f(c)
$$

A function $f(x)$ is continuous (everywhere) if:

$$
(\forall c\in \Reals)\Big(\lim_{x\to c} f(x) = f(c)\Big)
$$

### Derivatives

In order to run back propagation, we need the slope of the loss function (A.K.A the gradient) at specific points. The formal term for this is the derivative.

The derivative of a function $f(x)$ with respect to $x$ at $x = c$ is defined as

$$
f'(c) = \lim_{h \to 0} \frac{f(c + h) - f(c)}{h}
$$

A function is called "differentiable" if its derivative exists at every point.

## How it works

Let's say we have a neural network $f_\theta$, where $\theta$ is a vector representing all of the parameters in the network, including the weights and the biases. Our objective is to find the optimal parameters $\theta^{\star}$ such that the loss function is minimized. Let's use the mean squared error loss function as an example:

$$
\theta^{\star} = \argmin_{\theta} \frac{1}{n} \lvert y-f_\theta(X) \rvert^2
$$

where $X$ is the input data, $y$ is the labels, and $n$ is the number of data points.

### The principle
From the definition, we can see that the derivative of a function means that a very small increment in $x$ (from $x=c$ to $x=c+h$) will cause $f(x)$ to change by $f'(c)\times h$. Visually, the derivative is equal to the slope of the line tangent to the $f$ at $x=c$. This is why the derivative can tell us in which direction to move $x$ in order to result in a decrease in $f$. Partial derivatives are a lot harder to visualize in the same way, but the principle is the same. The partial derivative of the loss function with respect to each parameter tells us the direction we need to move each specific parameter in order to decrease the loss function.

Gradient descent works by repeatedly taking the derivative **of the loss function** and moving $x$ in the direction of the negative gradient, which, by definition (if the step we take is small enough), is guaranteed to reduce the loss function.

The size of the step we take is the magnitude of the gradient multiplied by a hyperparameter called "learning rate". The learning rate is a hyperparameter that controls how much we move in the direction of the gradient. If the learning rate is too high, we may overshoot the minimum. If the learning rate is too low, we may take too long to reach the minimum. This makes lr one of the most important hyperparameters to tune for in the training process.

$$
\theta = \theta - \eta \nabla_\theta L(\theta)
$$
where $\eta$ is the learning rate and $\nabla_\theta L(\theta)$ is the gradient of the loss function $L$.

### The algorithm

In order to calculate partial derivatives, we use an algorithm known as "back propagation". This algorithm starts by calculating the partial derivatives of the parameters on the outmost layer and the partial derivative of each node, then using those calculations to calculate the partial derivatives of the parameters on the next layer and so on until we reach the input layer.

The method used to calculate the gradients of the next layer using the gradients of the current layer is called "chain rule" in calculus. The chain rule states that the partial derivative of the loss function with respect to a parameter in a layer is equal to the partial derivative of the loss function with respect to the output of the layer multiplied by the partial derivative of the output of the layer with respect to the parameter.



We can easily calculate the partial derivative of the output of a single layer with respect to its parameters, and the partial derivative of the loss function with respect to each layer would be "back propagated" from the output layer to the input layer.