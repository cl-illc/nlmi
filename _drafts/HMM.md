---
layout: post
title: HMM FAQ
date:   2018-03-05
author: Wilker
categories: FAQ
mathjax: true
---

Hello everyone,

here we will answer some questions about HMMs.

# Transition vs Emission distributions

A transition **distribution** is a probability **distribution** over the possible classes (PoS tags) given a value for the previous class (itself a PoS tag). Thus, the transition **probability** is the chance to move from some tag $$c_{\text{prev}}$$ to some tag $$c$$.


Below is the transition distribution for `NOUN` obtained by maximum likelihood estimation using a portion of the Penn Treebank:

\begin{equation}
    P_{C|C_{\text{prev}} = \text{'noun'} }
\end{equation}

    # Transition from C_prev='NOUN'
    c_prev    c           prob
    --------  ----  ----------
    NOUN      NOUN  0.262119
    NOUN      .     0.245416
    NOUN      ADP   0.176698
    NOUN      VERB  0.144336
    NOUN      CONJ  0.0423475
    NOUN      PRT   0.0418482
    NOUN      X     0.030138
    NOUN      ADV   0.0181554
    NOUN      DET   0.0127996
    NOUN      ADJ   0.0108025
    NOUN      NUM   0.00939542
    NOUN      PRON  0.00535585 


An emission **distribution** is a probability **distribution** over words given a value for the current class. Thus, the emission **probability** is the chance to emit some word $$w$$ from some class $$c$$. Note that, there is no $$c_{\text{prev}}$$ in emission distributions.

Below is the first few entries in the emission distribution for `NOUN` obtained by maximum likelihood estimation using a portion of the Penn Treebank:

\begin{equation}
    P_{X|C=\text{'noun'}}
\end{equation}


    # emission from c:NOUN
    c     v                prob
    ----  ---------  ----------
    NOUN  %          0.00926912
    NOUN  company    0.00513559
    NOUN  year       0.0045093
    NOUN  market     0.00410221
    NOUN  new        0.00410221
    NOUN  president  0.00397695
    NOUN  program    0.00378906
    NOUN  trading    0.00356986
    NOUN  stock      0.0034446
    NOUN  years      0.0032254


# Terminology


\begin{equation}
(1) \qquad    P_{C|C_{\text{prev}}=c_{\text{prev}}}
\end{equation} 

(1)  is the probability **distribution** over classes given a class $$c_{\text{prev}}$$, we call this particular distribution a *transition distribution*

\begin{equation}
(2) \qquad    P_{C|C_{\text{prev}}}(c|c_{\text{prev}})
\end{equation}

(2) is the probability **value** for a class $$c$$ given a class $$c_{\text{prev}}$$, we call this particular value a *transition probability*


\begin{equation}
(3) \qquad    P_{C|C_{\text{prev}}}
\end{equation}
(3) refers to a set of probability distributions which we call *transition distributions*, in particular, there is one distribution for each possible value of the conditioning context (a class in this case)


\begin{equation}
(4) \qquad    P_{X|C=c}
\end{equation} 
(4) is the probability **distribution** over words given a class $$c$$, we call this particular distribution an *emission distribution*


\begin{equation}
(5) \qquad    P_{X|C}(x|c)
\end{equation}
(5) is the probability **value** for a word $$x$$ given a class $$c$$, we call this particular value an *emission probability*


\begin{equation}
(6) \qquad    P_{X|C}
\end{equation}
(6) refers to a set of probability distributions which we call *emission distributions*, in particular, there is one distribution for each possible value of the conditioning context (a class in this case)


# Cost of representation

We can use big-O-notation to express the cost of representing all probability distributions in the model. Recall that we have two types of distributions:

* transition distributions map from a class (in the previous position) to a class (in the current position)
* emission distributions maps from a class (in the current position) to a word (in the current position)

Consider that we have $$t$$ classes and $$v$$ words. Then the space of all possible *transition events* is something like `any possible tag followed by any possible tag` which amounts to $$t \times t$$ combinations.

Similarly, the space of all possible *emission events* is something like `any possible tag with any possible word` which amounts to $$t \times v$$ combinations.

We can then express the representation cost as $$O(t^2 + t \times v)$$, because:

* we have $$t$$ transition distributions (one for each class we may condition on), each of which is a Categorical distribution over $$t$$ classes (the class we may transit to), thus $$t^2$$ parameters (probability values) are necessary;
* we have $$t$$ emission distributions (one for each class we may condition on), each of which is a Categorical distribution over $$v$$ words (the words we may emit), thus $$t \times v$$ parameters (probability values) are necessary;


