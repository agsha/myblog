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

So naturally, I have put quite a bit of effort to understand the proof, but most proofs seem like "rabbit-out-of-a-hat". And yet, it is a fundamental theorem that is used ubiquitously in linear albegra.

The structure of this post is as follows:

1. Cover some basic definitions and theorems to get everyone on the same page
1. To show just how profound and non-obvious is the result of the theorem
1. Explore the common proofs of the theorem and show the proofs are not intuitive
1. Illustrate an intuitive way of thinking about the theorem

The target audience for this post is people who already have a decent understanding of the matrix-oriented, as well as the more abstract proofs, and who are looking for a more intuitive explanation of the result.

Although I try to cover most of the basic facts for the sake of completeness and as a refresher, It is by no means sufficient as an introduction to someone who is not aware of the subject.

In particular, familiarity with the following two books will be immensly helpful

1. [Linear algebra and its applications - by Gilbert Strang](https://www.amazon.com/Introduction-Linear-Algebra-Gilbert-Strang/dp/1733146679/ref=sr_1_1?crid=1JW0E99JN5SKE&dib=eyJ2IjoiMSJ9.F5NXQBUERLV6mEXR0WvWdC1VIo5KtbzV8WZcVUP2Dg4cb4i4DR40XDLNrVXwixRol38MYo6BTvYpyNTQVQ0gImwXuiqCQ59piMxv2_tRyE44IAugYBc4-ZNbbapORHJvxiCa1y1Dmv2TKy9e3Ss9FNH_k5b179BLKOjRGpHcSZiTDj5njPwn8N8jmqDIILP_SJ-OGLVSjZwqkUiOw5K5xa7fM9dhW9Yd2ITMbkE1hR4.ea-vft9gJC1k1gLg1yAzgwQ31yIYCgzAnEuQE1JHUwo&dib_tag=se&keywords=introduction+to+linear+algebra+gilbert+strang&qid=1728671128&s=books&sprefix=introduction+to+linear+algebra+gilbert+strang%2Cstripbooks%2C277&sr=1-1). This book is more of an application oriented introductory textbook for undergrads
1. [Linear algebra and its applications - by Peter Lax](https://www.amazon.com/Linear-Algebra-Its-Applications-Peter/dp/0471751561/ref=sr_1_1?crid=3DTKAMQYELAH8&dib=eyJ2IjoiMSJ9.QS-53qTNH2oNYLIfPP8d2aRRsbCOzpvSrfGrUdb_pa0qIz1_f0pjjxnk1y_WceOgvpwmS6HwJSYPaL6XGVINCFDPGVG98qD5yNvmlUTYpNvoNGbu17lBruy_brAbN0oG9iDTdBS8LO0LoaWQMFoTOg.r4QjPYISMr7QqB_7PAKk3omHi-hcFnfYlbUBYVR2UOA&dib_tag=se&keywords=linear+algebra+-+by+Peter+Lax&qid=1728671251&s=books&sprefix=linear+algebra+-+by+peter+lax%2Cstripbooks%2C260&sr=1-1). This book is also an undergrad texbook, Contrary to its name, it is a very abstract book, with a more rigorous approach, suitable for (example), an "honors" undergraduate course

Alright, lets begin!

Let's start with some basic definitions and simple theorems, whose proof I shall skip. The proofs should be part of any standard linear algebra text (in particular, the one by Peter lax)

**vector space**

A vector space over a field of scalars is a mathematical object that supports

1. addition
2. multiplication by a scalar

**linear combination**

A linear combination of vectors $x_1, x_2, ..., x_n$ is a vector of the form $k_1x_1+k_2x_2+...+k_nx_n$


**subspace**

A subspace $Y$ of a vector space $X$ is a subset that is closed under the vector operations. i.e., linear combination of members of the space is also a member of the space. Please note here the difference between a *subset* and a *subspace*. A subset need not be closed under the vector operations

**linear independence**

A set of vectors $x_1, ..., x_n$ are linearly dependent iff

$$
k_1x_1 + k_2x_2 + ... + k_nx_n = 0
$$

where the $k$s are scalars and not all of them are zero. If the vectors are not linearly dependent, they are called linearly independent. 


**basis vectors**

A finite set of vectors that span a space $X$ and are linearly independent, are called the basis. The number of vectors in the set is called the **dimension** of the space (denoted as $dim\ X$). There can be many different sets of basis vectors but the dimension is always the same

**Completion of a partial basis**

Every linearly independent set of vectors of a space $X$ can be completed to form a basis for $X$. This theorem is very important and we will be using it a lot.

**Isomorphism of same dimension spaces**

Once we fix any basis for a space $X$ with dimension $n$, every vector $x \in X$ can be represented by a $n$ tuple of scalars $(k_1, ... k_n)$. Using this representation, two diferent spaces $X$ and $Y$ of the same dimension are isomorphic to one another.

Intuition - Any vector $y \in X$ can be written as $x = k_1x_1 + ... + k_nx_n$ where the $x$s are the basis. here, the $k$s form the tuple which defines the vector.

**Complement of a subspace**

For every subspace $Y$ of space $X$, there is a complementary subspace $Z$ of $X$ such that every vector $x \in X$ can be written *uniquely* as $x = y + z$ where $y \in Y$ and $z \in Z$. Furthermore, $dim\ X = dim\ Y + dim\ Z$

Intuition: consider a basis $y_1, ..., y_m$ for $Y$. These can be completed by adding more linearly independent vectors $z_1, ..., z_n$ to form a full basis of $X$. The subspace spanned by the $z$s is the basis for $Z$

**Linear Mapping**
A linear map $T$ from a vector space $X$ to another space $U$ (not necessarily of the same dimensions) is a function which takes input an $x \in X$ and gives the output $u \in U$. As usual, $X$ is called the *domain* of $X$ and $U$ is called the *target space*. 

A linear map has the additional property

1. Sums and (scalar) product of input maps to sums and (scalar) product of the outputs. i.e., $T(x+y) = T(x) + T(y)$ and $T(kx) = kT(x)$

The image of $X$ under $T$ is also called the *range* of T.

Lets momentarily descend from the abstract world and to the world of matrices and relate the two.

An $m \times n$ matrix is an example of a linear map $T$, and a tuple of scalars in column format is an example of a vector $v$ 









