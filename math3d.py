class VectorN(object):
    """ This is a class which will be used to represent a vector (or a point
        in n-dimensional space. It is basically acts as a python list (of
        floats), but with extra vector operations that python lists don't
        have. """


    def __init__(self, p):
        """ The constructor.  p can be one of these type of objects:
            an integer: the dimension this vector exist in (in which case,
                 this vector is initialized to a p-dimensional zero vector)
            a sequence-like object: the values of the vector (we infer
                 the dimension based on the length of the sequence.  The values
                 are copied to this VectorN (and converted to floats)) """
        if isinstance(p, int):
            self.mDim = p
            self.mData = [0.0] * p
        elif hasattr(p, "__len__") and hasattr(p, "__getitem__"):
            # Note: We're using len(p) and p[i], so we need the above
            #   two methods.
            self.mDim = len(p)
            self.mData = []
            for i in range(len(p)):
                self.mData.append(float(p[i]))
        else:
            raise TypeError("Invalid parameter.  You must pass a sequence or an integer")


    def __str__(self):
        """ Returns a string representation of this VectorN (self) """
        s = "<Vector" + str(self.mDim) + ": "
        s += str(self.mData)[1:-1]
        s += ">"
        return s


    def __len__(self):
        """ Returns the dimension of this VectorN when a VectorN is passed to
           the len function (which is built into python) """
        return self.mDim


    def __getitem__(self, index):
        """ Returns an element of mData """
        return self.mData[index]


    def __setitem__(self, index, value):
        """ Sets the value of self.mData[index] to value """
        self.mData[index] = float(value)    # Could fail with an invalid index
                                            # error, but we'll let python handle
                                            # it.
    def copy(self):
        """ Returns an identical (but separate) VectorN """
        # Note: This works because our VectorN has a __len__ and __getitem__
        #     method (which is what the constructor expects)
        return VectorN(self.mData)


    def __eq__(self, rhs):
        """ Returns True if this VectorN (self) is of the same type (VectorN)
            and dimension of rhs and all the values in self are the same as the
            values in rhs """
        if isinstance(rhs, VectorN) and self.mDim == rhs.mDim:
            for i in range(self.mDim):
                if self.mData[i] != rhs.mData[i]:
                    return False
            return True
        return False


    def iTuple(self):
        """ Returns a tuple with the values of this vector, converted to integers """
        L = []
        for val in self.mData:
            L.append(int(val))
        return tuple(L)     # Converts the *list* L to a tuple and returns it


    def __neg__(self):
        """ Returns a vector with all the element's signs flipped """
        x = VectorN(self.mDim)
        for i in range(self.mDim):
            x.mData[i] = -self.mData[i]
        return x

    def __add__(self, other):
        """ Adds elements of the same position of the two vectors and returns a new vector with the new elements"""
        if not isinstance(other, VectorN):
            raise TypeError("Can only add another Vector" + str(self.mDim) + " to this Vector" + str(self.mDim))
        if self.mDim != other.mDim:
            raise TypeError("Can only add another Vector" + str(self.mDim) + " to this Vector" + str(self.mDim))
        x = VectorN(self.mDim)
        for i in range(self.mDim):
            x.mData[i] = self.mData[i] + other.mData[i]
        return x


    def __sub__(self, other):
        """ Subtracts elements of the same position of the two vectors and returns a new vector with the new elements"""
        if not isinstance(other, VectorN):
            raise TypeError("Can only subtract another Vector" + str(self.mDim) + " from this Vector" + str(self.mDim))
        if self.mDim != other.mDim:
            raise TypeError("Can only subtract another Vector" + str(self.mDim) + " from this Vector" + str(self.mDim))
        x = VectorN(self.mDim)
        for i in range(self.mDim):
            x.mData[i] = self.mData[i] - other.mData[i]
        return x

    def __mul__(self, other):
        """ Multiplies the vectors elements by the given scalar individually"""
        if not isinstance(other, int) and not isinstance(other, float):
            raise TypeError("Can only multiply a Vector" + str(self.mDim) + " by a scalar")
        x = VectorN(self.mDim)
        for i in range(self.mDim):
                x.mData[i] = self.mData[i] * other
        return x


    def __rmul__(self, other):
        """ Mul but with the vector on the right side of the operator"""
        return self * other


    def __truediv__(self, other):
        """ Divides the vectors elements by the given scalar individually"""
        if not isinstance(other, int) and not isinstance(other, float):
            raise TypeError("Can only divide a Vector" + str(self.mDim) + " by a scalar")
        x = VectorN(self.mDim)
        for i in range(self.mDim):
            x.mData[i] = self.mData[i] / other
        return x


    def __rtruediv__(self, other):
        """ truediv but with the vector on the right side of the operator"""
        raise TypeError("You cannot divide anything by a Vector")


    def isZero(self):
        """ Checks if all elements of a vector are 0.0 and returns true/false"""
        for i in self.mData:
            if i != 0.0:
                return False
        return True


    def magnitude(self):
        """ Finds the magnitude of the vector"""
        x = 0
        for i in self.mData:
            x += i ** 2
        return x ** 0.5

    def normalized_copy(self):
        """returns a normalized copy of the vector"""

        if self.isZero():
            return self.copy()

        return self / self.magnitude()


    def dot(self, otherVector):
        """
        Computes the dot product between self and another VectorN of the same length.

        :param otherVector: another VectorN of the same length as self, raises an error if this is not the case.
        :return: None.
        """
        if not isinstance(otherVector, VectorN):
            raise Exception(TypeError("dot product must be with a VectorN"))

        if self.mDim != otherVector.mDim:
            raise Exception(TypeError("dot product must be with a Vector" + str(self.mDim)))

        dotProduct = 0.0
        for i in range(self.mDim):
            dotProduct += self.mData[i] * otherVector.mData[i]

        return dotProduct