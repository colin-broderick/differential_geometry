## TODO sort nForms by swapping.
## TODO Come up with a sensible representaiton for the zero form, or a way to omit them.


class sumForm:
    """
    A sumForm is a collection of Forms, or nForms, or a combination of both.
    """
    def __init__(self, indices, coefficients):
        self.coefficients = coefficients
        self.indices = indices
        self.simplify()


    def __xor__(self, other):
        if isinstance(other, Form):
            ## This always produces a sumForm.
            indices = [indices + [other.index] for indices in self.indices]
            coefficients = [coefficient * other.coefficient for coefficient in self.coefficients]
            return sumForm(indices, coefficients)

        elif isinstance(other, nForm):
            ## This always produces a sumForm.
            indices = [indices + other.indices for indices in self.indices]
            coefficients = [coefficient * other.coefficient for coefficient in self.coefficients]
            return sumForm(indices, coefficients)

        elif isinstance(other, sumForm):
            ## This always produces a sumForm.
            indices = [el1 + el2 for el2 in other.indices for el1 in self.indices]
            coefficients = [c1 * c2 for c2 in other.coefficients for c1 in self.coefficients]
            return sumForm(indices, coefficients)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return sumForm(self.indices, [coefficient*other for coefficient in self.coefficients])

    def __add__(self, other):
        if isinstance(other, Form):
            ## This always produces a sumForm.
            indices = self.indices + [[other.index]]
            coefficients = self.coefficients + [other.coefficient]
            return sumForm(indices, coefficients)

        elif isinstance(other, nForm):
            ## This always produces a sumForm.
            indices = self.indices + [other.indices]
            coefficients = self.coefficients + [other.coefficient]
            return sumForm(indices, coefficients)

        elif isinstance(other, sumForm):
            ## This always produces a sumForm.
            indices = self.indices + other.indices
            coefficients = self.coefficients + other.coefficients
            return sumForm(indices, coefficients)

    def simplify(self):
        ## TEST For each set of indices, if any two indices are the same, that set is a zero-form.
        for index in range(len(self.indices)):
            if len(set(self.indices[index])) != len(self.indices[index]):
                self.coefficients[index] = 0

        ## TODO TEST For remaining sets of indices, if any are identical, combine them.
        

    def __rmul__(self, other):
        return sumForm(self.indices, [coefficient*other for coefficient in self.coefficients])

    def __str__(self):
        if sum(self.coefficients) == 0:
            return "0"
        else:
            return " + ".join(nForm(a, b).__str__() for a, b in zip(self.indices, self.coefficients))



class nForm:
    """
    An nForm is a collection of Forms.
    """
    def __init__(self, indices, coefficient=1):
        self.coefficient = coefficient
        self.indices = indices
        self.simplify()

    def __xor__(self, other):
        if isinstance(other, Form):
            ## This always produces an nForm.
            coefficient = self.coefficient * other.coefficient
            indices = self.indices + [other.index]
            return nForm(indices, coefficient=coefficient)

        elif isinstance(other, nForm):
            ## This always producse an nForm.
            coefficient = self.coefficient * other.coefficient
            indices = self.indices + other.indices
            return nForm(indices, coefficient=coefficient)

        elif isinstance(other, sumForm):
            ## This always produces a sumForm.
            coefficients = [self.coefficient * coefficient for coefficient in other.coefficients]
            indices = [self.indices + indices for indices in other.indices]
            return sumForm(indices, coefficients)
        
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return nForm(self.indices, self.coefficient * other)

    def __add__(self, other):
        if isinstance(other, Form):
            ## This always produces a sumForm.
            indices = [self.indices, [other.index]]
            coefficients = [self.coefficient, other.coefficient]
            return sumForm(indices, coefficients)

        elif isinstance(other, nForm):
            ## This always produces a sumForm.
            indices = [self.indices, other.indices]
            coefficients = [self.coefficient, other.coefficient]
            return sumForm(indices, coefficients)

        elif isinstance(other, sumForm):
            ## This always produces a sumForm.
            indices = [self.indices] + other.indices
            coefficients = [self.coefficient] + other.coefficients
            return sumForm(indices, coefficients)

    def simplify(self):
        ## If any two indices are the same, this is a zero-form.
        if len(set(self.indices)) != len(self.indices):
            self.coefficient = 0

    def __rmul__(self, other):
        return nForm(self.indices, self.coefficient * other)

    def __str__(self):
        if self.coefficient == 0:
            return "0"
        elif self.coefficient == 1:
            return " ^ ".join(f"dx[{index}]" for index in self.indices)
        else:
            return f"{self.coefficient} * " + " ^ ".join(f"dx[{index}]" for index in self.indices)


class Form:
    """
    A Form is fully characterised by its index and coefficient.
    """
    def __init__(self, index, coefficient=1):
        self.index = index
        self.coefficient = coefficient
        self.simplify()

    def __xor__(self, other):
        if isinstance(other, Form):
            ## This always produces an nForm.
            coefficient = self.coefficient * other.coefficient
            indices = [self.index, other.index]
            return nForm(indices, coefficient=coefficient)

        elif isinstance(other, nForm):
            ## This always produces an nForm.
            coefficient = self.coefficient * other.coefficient
            indices = [self.index] + other.indices
            return nForm(indices, coefficient=coefficient)

        elif isinstance(other, sumForm):
            ## This always produces a sumForm.
            coefficients = [self.coefficient*coefficient for coefficient in other.coefficients]
            indices = [[self.index] + indices for indices in other.indices]
            return sumForm(indices, coefficients)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            ## This always produces a Form.
            return Form(self.index, self.coefficient * other)

    def __add__(self, other):
        if isinstance(other, Form):
            ## This always produces a sumForm.
            indices = [[self.index], [other.index]]
            coefficients = [self.coefficient, other.coefficient]
            return sumForm(indices, coefficients)

        elif isinstance(other, nForm):
            ## This always produces a sumForm.
            indices = [[self.index], other.indices]
            coefficients = [self.coefficient, other.coefficient]
            return sumForm(indices, coefficients)

        elif isinstance(other, sumForm):
            ## This always produces a sumForm
            indices = [[self.index]] + other.indices
            coefficients = [self.coefficient] + other.coefficients
            return sumForm(indices, coefficients)

    def __rmul__(self, other):
        return Form(self.index, self.coefficient * other)

    def simplify(self):
        pass

    def __str__(self):
        if self.coefficient == 1:
            return f"dx{self.index}"
        return f"{self.coefficient} * dx[{self.index}]"
