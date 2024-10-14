Date: 2024-10-11 10:44 pm
Tags: misc
Authors: Sharath Gururaj
Title: Notes on the rank theorem in linear algebra
disqus_identifier: notes-on-the-rank-theorem-in-linear-algebra

I have always been fascinated by the rank theorem in linear algebra. It is known sometimes by other names:

1. The rank-nullity theorem
2. Fundamental theorem of linear algebra (part 1)

Stated simply, The rank theorem asserts that in any matrix, the row rank is equal to the column rank.

The result of the theorem always seems a bit magical to me (as I will explain later). It is as if someone told me the following - In a room, close your eyes and randomly throw a crumpled ball of paper. It will always land in the waste paper bin!

So naturally, I have put quite a bit of effort to understand the proof, but most proofs seem like "rabbit-out-of-a-hat". And yet, it is a fundamental theorem that is used ubiquitously in linear algebra.

In this post, I hope to give an intuitive understanding of the rank theorem. The structure of this post is as follows:

1. Cover some basic definitions and theorems to get everyone on the same page
1. Show just how profound and non-obvious is the result of the theorem
1. Illustrate an intuitive way of thinking about the theorem
1. Explore some other common proofs of the theorem

The target audience for this post is people who already have a decent understanding of the matrix-oriented proofs, as well as the more abstract proofs, and who are looking for a more intuitive explanation of the result.

Although I try to cover most of the basic facts for the sake of completeness and as a refresher, It is by no means sufficient as an introduction to someone who is not aware of the subject.

In particular, familiarity with the following two books will be immensely helpful

1. [Linear algebra and its applications - by Gilbert Strang](https://www.amazon.com/Introduction-Linear-Algebra-Gilbert-Strang/dp/1733146679/ref=sr_1_1?crid=1JW0E99JN5SKE&dib=eyJ2IjoiMSJ9.F5NXQBUERLV6mEXR0WvWdC1VIo5KtbzV8WZcVUP2Dg4cb4i4DR40XDLNrVXwixRol38MYo6BTvYpyNTQVQ0gImwXuiqCQ59piMxv2_tRyE44IAugYBc4-ZNbbapORHJvxiCa1y1Dmv2TKy9e3Ss9FNH_k5b179BLKOjRGpHcSZiTDj5njPwn8N8jmqDIILP_SJ-OGLVSjZwqkUiOw5K5xa7fM9dhW9Yd2ITMbkE1hR4.ea-vft9gJC1k1gLg1yAzgwQ31yIYCgzAnEuQE1JHUwo&dib_tag=se&keywords=introduction+to+linear+algebra+gilbert+strang&qid=1728671128&s=books&sprefix=introduction+to+linear+algebra+gilbert+strang%2Cstripbooks%2C277&sr=1-1). This book is more of an application oriented introductory textbook for undergrads
1. [Linear algebra and its applications - by Peter Lax](https://www.amazon.com/Linear-Algebra-Its-Applications-Peter/dp/0471751561/ref=sr_1_1?crid=3DTKAMQYELAH8&dib=eyJ2IjoiMSJ9.QS-53qTNH2oNYlinearly independentfPP8d2aRRsbCOzpvSrfGrUdb_pa0qIz1_f0pjjxnk1y_WceOgvpwmS6HwJSYPaL6XGVINCFDPGVG98qD5yNvmlUTYpNvoNGbu17lBruy_brAbN0oG9iDTdBS8LO0LoaWQMFoTOg.r4QjPYISMr7QqB_7PAKk3omHi-hcFnfYlbUBYVR2UOA&dib_tag=se&keywords=linear+algebra+-+by+Peter+Lax&qid=1728671251&s=books&sprefix=linear+algebra+-+by+peter+lax%2Cstripbooks%2C260&sr=1-1). This book is also an undergrad texbook, Contrary to its name, it is a very abstract book, with a more rigorous approach, suitable for (example), an "honors" undergraduate course

Alright, lets begin!

Let's start with some basic definitions and simple theorems, whose proof I shall skip. The proofs should be part of any standard linear algebra fare (in particular, the textbook by Peter lax)

# Basic definitions and theorems

**vector space**

A vector space over a field of scalars is a mathematical object that supports

1. addition
2. multiplication by a scalar

**linear combination**

A linear combination of vectors $x_1, x_2, \cdots, x_n$ is a vector of the form $k_1x_1+k_2x_2+\cdots+k_nx_n$


**subspace**

A subspace $Y$ of a vector space $X$ is a subset that is closed under the vector operations. i.e., linear combination of members of the space is also a member of the space. Please note here the difference between a *subset* and a *subspace*. A subset need not be closed under the vector operations

**linear independence**

A set of vectors $x_1, \cdots, x_n$ are linearly dependent iff

$$
k_1x_1 + k_2x_2 + \cdots + k_nx_n = 0
$$

where the $k$s are scalars and not all of them are zero. If the vectors are not linearly dependent, they are called linearly independent. 


**basis vectors**

A finite set of vectors that span a space $X$ and are linearly independent, are called the basis. The number of vectors in the set is called the **dimension** of the space (denoted as $dim\ X$). There can be many different sets of basis vectors but the dimension is always the same

**Completion of a partial basis**

Every linearly independent set of vectors of a space $X$ can be completed to form a basis for $X$. This theorem is very important and we will be using it a lot.

**Isomorphism of same dimension spaces**

Once we fix any basis for a space $X$ with dimension $n$, every vector $x \in X$ can be represented by a $n$ tuple of scalars $(k_1, \cdots k_n)$. Using this representation, two different spaces $X$ and $Y$ of the same dimension are isomorphic to one another.

Intuition - Any vector $y \in X$ can be written as $x = k_1x_1 + \cdots + k_nx_n$ where the $x$s are the basis. here, the $k$s form the tuple which defines the vector.


**Linear Map**

A linear map $T$ from a vector space $X$ to another space $U$ (not necessarily of the same dimensions) is a function which takes input an $x \in X$ and gives the output $u \in U$. As usual, $X$ is called the *domain* of $X$ and $U$ is called the *target space*. 

A linear map has the additional property

1. Sums and (scalar) product of input maps to sums and (scalar) product of the outputs. i.e., $T(x+y) = T(x) + T(y)$ and $T(kx) = kT(x)$

The image of $X$ under $T$ is also called the *range* of T.

Lets momentarily descend from the abstract world and to the world of matrices and relate the two.

An $m \times n$ matrix is an example of a linear map $T$, and a tuple of scalars in column format is an example of a vector $v$ 

A quick example is in order.

$$T = 
\begin{bmatrix}
1 & 5 & 6 \\
2 & 7 & 9 
\end{bmatrix}, x = \begin{bmatrix}1 \\ 3 \\ 5\end{bmatrix}$$

Then,

$$y=T(x) = T \times x = \begin{bmatrix}28 \\ 43\end{bmatrix}$$

Here, $T : X \mapsto U$, where $X$ is a 3-dimension vector space and $U$ is a 2-dimensional vector space, and $x \in X$ and $y \in Y$

The following are some important properties of linear maps

1. The value of the map on any given basis completely defines the map. This follows from the linearity property of the map
2. In matrix form, multiplication on the right side by a column vector gives a column vector which is a linear combination of the columns of the matrix. By this interpretation, the column rank is equal to the dimension of the range of $T$

Quick example:

$$\begin{bmatrix}
\vdots & \vdots & \vdots \\
col1 & col2 & col3 \\
\vdots & \vdots & \vdots
\end{bmatrix} \cdot 
\begin{bmatrix}a\\b\\c\end{bmatrix} = \begin{bmatrix} \vdots \\ a\cdot col1 + b\cdot col2 + c\cdot col3 \\ \vdots \end{bmatrix}$$


3. Similarly, multiplication from the left side by a row vector gives a row vector which is the linear combination of rows of the matrix. By this interpretation, the row rank is the dimension of the rowspace. 

$$\begin{bmatrix}a & b & c\end{bmatrix} \cdot \begin{bmatrix} 
\cdots & row1 & \cdots \\
\cdots & row2 & \cdots \\
\cdots & row3 & \cdots \\
\end{bmatrix} = \begin{bmatrix}\cdots & a\cdot row1 + b\cdot row2 + c\cdot row3 & \cdots\end{bmatrix}$$


4. **range-nullspace theorem**: the set of all vectors $v \in X$ such that $T(v) = 0$ forms a subspace of $X$ and is called the nullspace $N_T$ of $T$. We can show that $dim(X) = dim(R) + dim(N_T)$. This is a very fundamental result.

**Intuitive proof**: It is easy to show that the complement of $N_T$ is isomorphic to $R$. 

**Dot product or bilinear forms**

Once we choose a basis for a vector space, we can represent each vector by an element from $R^n$. Having done so, we can define a *dot product* of two vectors, which produces a scalar in the usual way, for example

$$\begin{bmatrix}a_1 & a_2 & a_3\end{bmatrix} \cdot \begin{bmatrix}b_1 \\ b_2 \\ b_3\end{bmatrix} = a_1b_1 + a_2b_2 + a_3b_3$$

In abstract terms, it is possible to define the dot product without the need for basis vectors. It is done by defining a *dual* vector space consisting of linear functions operating on the primal vector space. It can be shown that the dual and the primal vector space have the same dimensions.

In concrete terms, when dealing with $R^n$, if the vectors of primal space are denoted by column vectors, the elements of the dual space can be considered to be represented by row vectors

While solving linear equations, the row vectors typically arise as coefficients, and the column vectors arise as the unknowns. The coefficients are dual to the unknowns. This is in some sense reminiscent of the duality that is also encountered in linear programming.

**Change of Basis**

While dealing with $R^n$, when we don't explicitly specify the basis, we usually have in mind the **standard basis**, which has a 1 in the $j^{th}$ position and zero everywhere else. Of course, there is nothing special about the standard basis, and any other basis can be used equally well. Suppose we want to use vectors $e_j$ where $j \in [1, n]$ as the basis, and suppose we want to convert between the old representation and the new representation, we can use a map which maps each old basis to its corresponding new basis. This is well defined, since a map is well defined if we specify the values on all the basis vectors. Furthermore, it is easy to see that this map is one-to-one. 

**Complement of a subspace**

For every subspace $Y$ of space $X$, there is a complementary subspace $Z$ of $X$ such that every vector $x \in X$ can be written *uniquely* as $x = y + z$ where $y \in Y$ and $z \in Z$. Furthermore, $dim\ X = dim\ Y + dim\ Z$

Intuition: consider a basis $y_1, \cdots, y_m$ for $Y$. These can be completed by adding more linearly independent vectors $z_1, \cdots, z_n$ to form a full basis of $X$. The subspace spanned by the $z$s is the basis for $Z$

Some important points:

1. The complement of a subspace is not unique. There are many ways to complete the partial basis of $Y$, and each different choice gives rise to a different complement
2. A subspace and its complement are mutually exclusive, but *not* collectively exhaustive, and as such, they do not partition the parent vector space. i.e., there can be vectors which are not present either in $Y$ or its complement. For example, if $x$ is decomposed as $y + z$ as above, with both components non-zero, then $x$ is neither in $Y$, nor in its complement. Thus, it gives rise to 4 cases

    | y component  | z component | location |
    | ------------- | ------------- |-------|
    | 0  | 0  | the zero vector
    | 0  | non-zero  | in complement
    | non-zero | 0 | in subspace |
    | non-zero | non-zero | as a direct-sum subset|

3. The direct-sum subset is *not* a subspace. Example - the sum of the following two direct-sum vectors is not in the direct-sum: $(y+z), (y-z)$

**Orthogonal complement**

There is however, one unique complement called the orthogonal complement. In the same notation as above, suppose $Z$ is an orthogonal complement. then $\forall y \ \ \forall z, \ \  y \cdot z = 0$.

In abstract language, the orthogonal complement is a subset of the dual space, and it is usually called the annihilator of $Y$.

Note that, all the other properties of complements are still true for orthogonal complements.

In particular, $dim\ X = dim\ Y + dim\ Z$.

This fact is so important, but it is not usually part of the standard fare, that I will give the outline of a proof here.

**Theorem**: Let $X$ be a vector space, $dim(X) = n$. Let $Y$ be a subspace of $X$, spanned by $v_1, \cdots, v_r$. $dim(Y)=r$, then the orthogonal complement $Z$ has $dim(Z) = n-r$.

**Proof**: We will establish a 1:1 mapping between $Z$ and $R^{n-r}$.

First complete the partial basis of $Y$ to get a full basis $v_1, \cdots, v_n$. Every vector can be represented as $\sum{a_iv_i}$, so this is 1:1 with $\{a_i\}$. Let $z \in Z$. Define the mapping $T:z \mapsto z'$ where $$z' = [0, 0, \cdots, 0, z\cdot v_{r+1}, \cdots, z\cdot v_n]$$

Any such $z'$ also maps back to a unique $z \in Z$ by $z \cdot v_i = z'[i]$. Here we use the fact that a vector is uniquely specified by its values on the dot product on the basis vectors

In abstract language, the orthogonal complement is called annihilator and represented as a subspace of the dual space (remember that the dual space is a space of all bilinear functions). The proof of dimension usually involves proving an isomorphism between the annihilator and the dual of the quotient space $(X/Y)$. Effectively quotient space of a subspace is what you get by throwing away components of the basis of the subspace. i.e., the "rest" of the space apart from the subspace. 

Although the proof looks much cleaner there, I find the vesion I presented here to be more clear conceptually, where we establish an isomorphism between annihilator and $z' = [0, 0, \cdots, 0, l\cdot v_{r+1}, \cdots, l\cdot v_n]$

**Rowspace, columnspace and nullspace of a matrix**

The rows and columns of a matrix can be considered to be vectors. An $m \times n$ matrix has $m$ row vectors of dimension $n$ and $n$ column vectors of dimension $m$.

The rowspace is the subspace spanned by rows, and similarly for column space. The nullspace is the set of input vectors that maps to 0 vector under $T$.

The row/column rank of a matrix is defined as the max number of linearly independent rows/columns.

We are now in a position to restate the rank theorem

**The rank theorem**

The row rank of a matrix is the same as the column rank. i.e., the number of linearly independent rows in a matrix is equal to the number of linearly independent columns in the matrix

# The surprising nature of the rank theorem

Consider any matrix of any size, say $100 \times 1000$, filled with random numbers. 

1. There are 100 row vectors each of dimension 1000. The rows vectors look like $(x_1, x_2, \cdots, x_{1000})$
2. And there are 1000 column vectors, each of dimension 100. The column vectors look like $(y_1, y_2, \cdots, y_{100})$. 

The row vectors look very different from the column vectors. Looking individually, the numbers also seem to bear no relationship to each other. Even the dimensions do not match. And yet, the rank theorem asserts that if there are only 50 linearly independent rows, then there will only be 50 linearly independent columns amongst the 1000.

Another example: Consider the following matrix

$$T = 
\begin{bmatrix}
1 & 5 & 6 \\
2 & 7 & 9 \\
3 & 6 & 1 \\
\end{bmatrix}$$

Here, all the three rows are linearly independent, as are all the columns. However, I have made the column $C_3$ "just miss" to be equal to $C_1 + C_2$. ($3+6 \ne 1$). If I change that one number $x_{33}$ from 1 to 9, there are only 2 linearly independent columns. Now the rank theorem asserts that this change has forced one of the rows also to be linearly dependent on the other two rows. Yet, I am hard pressed to find out what is that linear combination by visual inspection. Can you spot the linear relationship between rows $R_1, R_2, R_3$?

i.e., given $R_1 = [1, 5, 6]$, $R_2 = [2, 7, 9]$ and $R_3 = [3, 6, 9]$, can you find three numbers $a, b, c$ (not all zero) such that $aR_1 + bR_2 + cR_3 = 0$ by visual inspection? The rank theorem guarantees its existence, and indeed, $3R_1 - 3R_2 + R_3 = 0$.

Lets look at the previous example a bit more closely. Suppose

$$T = 
\begin{bmatrix}
a & d & a+d \\
b & e & b+e \\
c & f & c+f \\
\end{bmatrix}$$

So that $C_3 = C_1 + C_2$ and lets try to solve generally for $xR_1 + yR_2 + zR_3 = 0$. Can you guess the values for $x, y, z$ from visual inspection? I certainly couldn't! We can use standard techniques (from linear algebra itself, of course!) to find 

$$\begin{eqnarray}
x &= bf - ce \\
y &= dc - af \\
z &= ae - bd 
\end{eqnarray}$$

To me, it is surprising that a simple relationship between columns translates to such a complicated relationship among the rows. Now if you consider a $1000 \times 1000$ matrix with a complicated relationship among the columns, one can only imagine how complicated the relationship between the rows will be, and yet, the rank theorem guarantees that such a relationship must exist!

Having thus shown how surprising the result of the theorem is, lets explore some common approaches to proving the rank theorem.


# An intuitive proof

**Transpose** of a matrix is the matrix obtained by swapping its rows and columns

Let $T: X \mapsto U$ be a linear map and $m \times n$ matrix. So $dim(X) = n$ and $dim(U) = m$. Let $T'$ be its transpose. Let $R \subset U$ be the range of $T$, with $dim(R)=r$. So the dimension of columnspace is $r$. And we need to show that the dimension of rowspace of $T$ (which is dimension of colspace of $T'$) = $r$.

$R$ has a orthogonal complement $S$, with $dim(S)=m-r$. let $s \in S$. Now $s$ kills every vector in $R$, which are nothing but linear combinations of columns of $T$, and hence in matrix form, we can write

$$\begin{bmatrix} 
\cdots & col1 & \cdots \\
\cdots & col2 & \cdots \\
\cdots & coln & \cdots \\
\end{bmatrix} \cdot s = 0$$

Observe that here, the columns have become rows, and it is actually the transpose matrix $T'$. Thus it is clear that $s \in N_{T'}$ where $N_{T'}$ is the nullspace of $T'$. So, $S = N_{T'}$ and thus $dim(N_{T'}) = m-r$.

Applying the range-nullspace theorem to $T'$, immediately gives the dimension of the range of $T'$ as $dim(R_{T'}) = r$. This is what we wanted to prove.


Leaving the mathematics aside, lets try to describe in words what is happening. Consider a $n \times n$ matrix with all rows and columns independent. Now lets see what happens when we make one of the columns to be linearly dependent on the other columns.

1. The columns fail to span the full space of $U$, and thus the range of $T$ decreases by 1.
2. This gives rise to an orthogonal complement subspace in U, with the dimension of 1
3. Since a vector $z$ in the orthogonal complement kills every vector in the range of $T$, it actually provides a linear combination between the rows of $T$. Just re-iterating this step in math: 

$$\begin{eqnarray}z \cdot c_1  &= 0 \\
z \cdot c_2 &= 0 \\
&\vdots \\
z \cdot c_n &= 0 \\
\implies z \cdot \begin{bmatrix}c_1 & \cdots & c_n\end{bmatrix} &= z \cdot T = 0\end{eqnarray}$$.
Remember that left multiplication by a row vector is equivalent to a linear combination of the rows. So the last equation is saying that there is a lienar combination of rows that gives 0, which means that the rows are not linearly independent! Thus, In this way, we see how a linear combination of columns have forced a linear combination of rows.

Now, we will briefly explore some other common proofs
:
# Proof using elementary operations

This is the most common proof

**elementary row operations**

There are 3 such elementary row operations

1. swap two rows of a matrix
2. add another row to current row
3. multiply current row by a scalar

The proof proceeds in the following steps

1. Show that each elementary row operation corresponds to multiplying by an elementary matrix that is invertible
1. Show that multiplying by an elementary matrix has the following effects
    1. Rowspace - unchanged, because the row operations are simply linear combinations of other rows
    2. nullspace - unchanged, because, if $ET(x) = 0$ iff $T(x) = 0$
    3. columnspace - changed, but preserves linear combinations. short proof - suppose $c_x$ are the columns, and suppose $a_1c_1 + \cdots + a_nc_n = 0$, then 
    $$a_1c_1 + \cdots + a_nc_n =  
\begin{bmatrix}
c1 & \cdots & c_n\end{bmatrix}\begin{bmatrix}
a1 \\ \vdots \\ a_n\end{bmatrix} = 0$$. So $$\begin{bmatrix}
a1 \\ \vdots \\ a_n\end{bmatrix}$$ is in the nullspace of $T$ and thus also in the nullspace after the elementary row operation
1. Use the elementary row operations to arrive at the [*reduced row echelon form*](https://en.wikipedia.org/wiki/Row_echelon_form#Reduced_row_echelon_form) $rref(T)$, from which you can just visually see that the row rank and column rank are equal

This proof is actually pretty elegant, especially when it shows that the column space does not change under elementary row operations. However, I don't find it very clear why a linear dependence on the rows/columns should induce a corresponding linear dependence on the column/rows 

# A small improvement of the above proof

The following improvement perhaps cuts more directly to the issue at hand.

Let $c_1, \cdots, c_r$ be independent column vectors in the matrix $T$ In the target space U, the basis is the [standard basis](https://en.wikipedia.org/wiki/Standard_basis). Perform a change of basis by choosing the linearly independent column vectors as a partial basis, and complete them to get a full basis. This [change of basis](https://en.wikipedia.org/wiki/Change_of_basis) can be represented as another invertible matrix $S:U \mapsto V$, where $V$ is another vector space of the same dimensions. Now consider the matrix $Q : X \mapsto V \stackrel{\text{def}}{=} S \cdot T$. It is easy to see that 
Q is of the following form
$$Q = \begin{bmatrix}
 I & X \\ 
 0 & 0\end{bmatrix}$$
 Since $S$ is invertible, $Q$ and $T$ have the same rowspace, nullspace, and preserves linear combinations on the column space. And from this matrix, it is easy to see that the row rank is equal to the column rank

There are two other less well known proofs, and I really like them, and can't help but mention one of these proofs. Both of these are mentioned on this [webpage](https://proofwiki.org/wiki/Column_Rank_of_Matrix_equals_Row_Rank)

# Proof using orthogonality
It proceeds by the following steps

1. Prove that linearly independent rows are mapped to linearly independent columns (really clever!)
2. this proves that $rowrank <= column rank
3. Apply the same method to the transpose, giving columnrank <= rowrank
4. hence rowrank=columnrank!

So there you go! I hope these different viewpoints of looking at a fundamental result helps in a deeper understanding. It also shows such a rich structure for linear combinations. Keep on combining linearly!