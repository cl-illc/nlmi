from collections import defaultdict


class Symbol:
    """
    A symbol in a grammar, this is an abstract class that does not do anything other than 
        to establish the minimum interface of terminals and nonterminals.
        
    A symbol is an object much like a python string, but we don't need operations such as concatenation 
     and other string operations. We just need to be able to compare symbols and check their identity. 
     
    Some of the methods below must be implemented in classes that inherit from Symbol. 
    """
    
    def __str__(self):
        """This method allows us to inspect the identity of the symbol"""
        raise NotImplementedError('Children classes must implement this method')

    def __hash__(self):
        """
        This returns a hash value, python needs this in order to 
        use a Symbol in hash-based containers such as sets and dictionaries
        """
        raise NotImplementedError('Children classes must implement this method')
    
    def __eq__(self, other):
        """This returns whether or not two symbols are the same"""
        raise NotImplementedError('Children classes must implement this method')
        
    def __lt__(self, other):
        """
        This is necessary so that python can sort symbols lexicographically.
        We just delegate this comparison function to python, since it knows how to 
            compare strings, we use the result of __str__ applied to each symbol.
        """
        return str(self) < str(other)
        
    def __repr__(self):
        """We just make __repr__ and __str__ return the same"""
        return str(self)


class Terminal(Symbol):
    """
    A type of Symbol that acts like a constant. 
    
    A terminal is simply a container for a python string which represents the actual symbol. 
    For example, a terminal symbol 'cat' simply contains the python string 'cat' in it.
    """
    
    def __init__(self, word: str):
        """
        word: a python string representing a word
        """
        self._word = word
        
    @property
    def word(self):
        return self._word
    
    def __str__(self):
        """
        We print terminals around single quotes, this gives a nice visual clue.
        If you need the underlying word (as a python string) and without the single quotes around it, 
        then you need to use the property Terminal.word.
        """
        return "'%s'" % self._word
    
    def __hash__(self):
        """This is necessary in order for python to be able to use Terminal objects in sets and dictionaries"""
        # Python knows how to compute hash values for basic types (str, tuple, etc.), so
        #  we delegate to python this job
        # This is a good idea since we don't really know how to write good hash functions
        #  and the team of python developers must have put quite some work into it
        return hash(self._word)
    
    def __eq__(self, other: Symbol):
        """This is necessary if order for python to be able to compare terminals symbols"""
        # Two symbols are the same if they are both terminals 
        #  and the words they stand for are also the same
        return isinstance(other, Terminal) and other._word == self._word


class Nonterminal(Symbol):
    """
    A type of Symbol that acts like a variable.

    A nonterminal is simply a container for a python string which represents the actual symbol.
    For example, a nonterminal symbol [NP] simply contains the python string 'NP' in it.
    """

    def __init__(self, category: str):
        """
        category: a python string representing a POS or phrasal category
        """
        self._category = category

    @property
    def category(self):
        return self._category

    def __str__(self):
        """
        We print nonterminals wrapped around squared brackets to make a visual clue.
        If you need the underlying category (as a python string) without the brackets around it,
         then you need to use the property Nonterminal.category.
        """
        return "[%s]" % self._category

    def __hash__(self):
        """Python can only hash objects that properly implement this method"""
        # Again we delegate to python the job of computing a hash value for our category
        return hash(self._category)

    def __eq__(self, other: Symbol):
        """Python needs this in order to compare nonterminal symbols"""
        # Two symbols are the same if they are both nonterminals
        #  and their categories are the same
        return isinstance(other, Nonterminal) and other._category == self._category


class Rule:
    """
    A Rule is just a container, in particular, a pair. 
    
    It stores a LHS nonterminal and a RHS sequence of symbols.
    
    In general, RHS could be empty, but we will not implement such grammars.
    We will restrict the RHS to containing at least one symbol.    
    
    """

    def __init__(self, lhs: Nonterminal, rhs: list):
        """
        Constructs a Rule: LHS -> RHS.
        
        We must validate that rules are well formed, that is, the LHS symbol is indeed a Nonterminal, 
            the RHS is *not* empty and only contains Symbol (i.e. Terminal or Nonterminal) objects.
        
        lhs: the LHS nonterminal
        rhs: a sequence of RHS symbols
        """
        if not isinstance(lhs, Nonterminal):
            raise ValueError('The LHS has to be a Nonterminal')
        if not all(isinstance(sym, Symbol) for sym in rhs):
            raise ValueError('The RHS can only contain instances of Symbol')
        self._lhs = lhs
        self._rhs = tuple(rhs)

    def __eq__(self, other: 'Rule'):
        """Two rules are the same if they have the same LHS and the same RHS"""
        return self._lhs == other._lhs and self._rhs == other._rhs

    def __hash__(self):
        """The hash value of the Rule is the hash value of the pair (LHS, RHS)"""
        # Once more we delegate the computation of the hash value to python
        return hash((self._lhs, self._rhs))

    def __str__(self):
        """We print rules using the notation LHS -> RHS"""
        return '%s -> %s' % (self._lhs, ' '.join(str(sym) for sym in self._rhs))
    
    def __repr__(self):
        return str(self)

    @property
    def lhs(self):
        """Returns the LHS nonterminal"""
        return self._lhs

    @property
    def rhs(self):
        """Returns the RHS sequence"""
        return self._rhs
    
    @property
    def arity(self):
        """Returns the arity (length of the RHS sequence)"""
        return len(self._rhs)


class CFG:
    """
    A CFG is a container for rules.
    
    Internally we maintain a few sets:
    * _terminals: the set of terminal symbols
    * _nonterminal: the set of all nonterminal symbols     
    * _preterminals: a subset of nonterminal symbols that correspond to POS categories
    
    We also maintain a set of rules: _rules
    
    We also maintain a dictionary whose keys are Nonterminal LHS symbols, and whose values are lists of rules.
    Thus, if X is a symbol, _rules_by_lhs[X] should return the list of rules that share that symbol as their
        LHS nonterminal.
    
    """

    def __init__(self, start_symbol: Nonterminal):
        if not isinstance(start_symbol, Nonterminal):
            raise ValueError('The start symbol must be a nonterminal')
        self._start = start_symbol
        # this should contain all rules of the grammar
        self._rules = set()
        # this should map a LHS symbol to a list of context-free rules rewriting that symbol
        self._rules_by_lhs = defaultdict(list)  
        # this should contain all terminals 
        self._terminals = set()
        # this should contain all nonterminals (including start symbol and preterminals)
        self._nonterminals = set()
        # this should contain only pre-terminals (that is, POS categories)
        self._preterminals = set()
        # length of the longest RHS
        self._arity = 0  

    def add(self, rule: Rule):
        """
        Add a rule to the ruleset, unless the rule is already known.
        This method also updates the sets of symbols with the symbols in this rule.
        """        
        if rule in self._rules:  # we do not add repeated rules
            return        
        # add rule to ruleset
        self._rules.add(rule)
        # also maps it for convenience
        self._rules_by_lhs[rule.lhs].append(rule)
        # the rule's LHS is now part of the nonterminal set
        self._nonterminals.add(rule.lhs)
        # and we should also add all other symbols in the rule
        for sym in rule.rhs:
            if isinstance(sym, Terminal):  # terminals
                self._terminals.add(sym)
            else:  # nonterminals
                self._nonterminals.add(sym)
        # a preterminal rule has arity 1 and rewrites to a terminal
        if rule.arity == 1 and isinstance(rule.rhs[0], Terminal):
            self._preterminals.add(rule.lhs)
        # here we update the arity of the grammar
        if rule.arity > self._arity:
            self._arity = rule.arity

    def update(self, rules):
        """Adds a collection of rules to the grammar"""
        for rule in rules:
            self.add(rule)
            
    @property
    def start(self):
        return self._start

    @property
    def nonterminals(self):
        return self._nonterminals
    
    @property
    def preterminals(self):
        return self._preterminals

    @property
    def terminals(self):
        return self._terminals
    
    @property
    def arity(self):
        """Returns the arity of the longest rule"""
        return self._arity

    def __len__(self):
        """The size of the grammar in number of rules"""
        return len(self._rules)

    def __getitem__(self, lhs: Nonterminal):
        """Returns rules for a certain LHS symbol"""
        return self._rules_by_lhs.get(lhs, frozenset())

    def get(self, lhs: Nonterminal, default=frozenset()):
        """Return rules whose LHS is the given symbol"""
        return self._rules_by_lhs.get(lhs, frozenset())

    def can_rewrite(self, lhs: Nonterminal):
        """
        Whether a given nonterminal can be rewritten. In other words, do we know a rule whose LHS is this
         symbol?
        """
        return len(self._rules_by_lhs.get(lhs, [])) > 0

    def __iter__(self):
        """Iterator over rules (in arbitrary order)"""
        return iter(self._rules)
    
    def items(self):
        """Iterator over pairs of the kind (LHS, rules rewriting LHS)"""
        return self._rules_by_lhs.items()
    
    def __str__(self):
        """Converts all rules to string"""
        lines = []
        # First rules for the start symbol
        for rule in self[self._start]:
            lines.append(str(rule))
        # Then other rules (except pre-terminal ones)
        for lhs, rules in sorted(self.items(), key=lambda pair: pair[0]):
            if lhs == self._start or lhs in self._preterminals:
                continue
            for rule in rules:
                lines.append(str(rule))
        # And finally the pre-terminal rules
        for pos in sorted(self._preterminals):
            for rule in self[pos]:
                lines.append(str(rule))
        # Now we concatenate them all
        return '\n'.join(lines)
    
    def __repr__(self):
        return 'CFG: start=%s n_terminals=%d n_nonterminals=%d n_rules=%d' % (
            self._start, len(self._terminals), len(self._nonterminals), len(self._rules)
        )

