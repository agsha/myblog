Date: 2021-10-10 10:20 pm
Tags: misc
Authors: Sharath Gururaj
Title: The choice of programming languages
disqus_identifier: my_blog

# Introduction
Thanks to advances in compiler technologies, Programmers today are spoilt for choice with the myriad of mainstream programming languages available your next big idea. However, the landscape can quickly get confusing. Many different languages seem to offer the same features and generally "looks the same". Consider the website description of two languages:

* Kotlin: "A modern programming language
  that makes developers happier."
* Swift: "Swift is a general-purpose programming language built using a modern approach to safety, performance, and software design patterns."

You get the idea.

Young programmers with the next brilliant idea for a startup often pick languages for no more reason than the fact that its the "cool kid on the block".

This blog tries to throw some light on the factors you should consider while picking a language.

# Language features
Before we get to the languages themselves, let us briefly review some key terminology relating to language features

## Target language
There are three major types 

* Compiled to Native: This means that the compiler generates machine code that can be directly executed by the CPU. Example C, C++, Rust, Go
* Compiled to bytecode: This means that the compiler compiles to a intermediate "low level" language,  which then requires an interpreter. Example: Java compiles down to "bytecode" which is then interpreted by the jvm during execution.
* Interpreted: No separate compilation step is necessary. The language source code is interpreted "on the fly" by an interpreter. For example, python, javascript

Note that some languages offer multiple targets. For example, kotlin can be compiled both to bytecode as well as native. But they are usually popular only  in one particular mode. For example, kotlin is usually compiled to bytecode.




## Static typed vs dynamic typed 

Statically typed means that the type of every variable is known during compile time. This generally means that we need to specify the type of the variable while declaring the vaiable. For example, in java `String name;`. The variable `name` cannot hold anything other than a `String`

In contrast, In dynamic typed languages, the type of variables is not known to compilers and no such type declaration is necessary for variables. For example in python, The following is possible
````python
# amount is a string
amount = "2" 

# amount is a number
amount = 2
````

Static typed languages are more verbose compared to dynamic typed languages. But they are much easier to refactor, and eliminate a large class of programming errors at compile time. Static languages are also much more IDE friendly. This is because IDE tooling can easily figure out valid methods for auto complete. Once the codebase and the team grows larger, static typing makes the codebase easier to learn for new joinees, and easier to refactor.

# Garbage collection
There are 3 main classes of languages:

## Automatic garbage collection 

These programming languages track references to variables and can automatically free the memory when a variable is no longer used. Example: java, python, javascript, go

## Garbage collection by reference counting
In some programming languages, there is no built in garbage collection, but rather, the language offers standard libraries that can ease memory management. These libraries typically work by maintaining reference counters which automatically get incremented on an assignment, or decrementd when a variable goes out of scope. When properly used, these languages feel almost like true garbage collected languages, without the runtime overhead of an actual garbage collector. For example, `unique_ptr` in C++ offers such capabilities.

In other languages, such reference counting is built-in to the language itself. Thus, memory allocation is always "safe", and yet there is no separate garbage collection component. For example: rust.

## No garbage collection
Low level languages like C offer no GC.

# Threading support

## Support through standard libraries
Some languages have no built-in support for threads, but offer standard libraries which allows us to create native threads. For example, C, C++

## Language support for threads
Some languages offer language native syntax for paralellism and threads and come with strong memory models. For example, Java, Go, Rust. In the case of C++, although there is no language support for threads, it does have a well defined memory model. Sometimes, the language itself offers an abstraction of threads, which may or maynot correlate to operating system threads. For example, Go offers "green threads", which are supposedly more lightweight than OS threads. These green threads are managed by the language runtime and do no directly correspond to OS threads. For example, n green threads can be mapped to m OS threads.

## Very little or no language support
Python and Javascript are examples. In the case of python, there is a "Global interpreter lock" which effectively kills any possibility for true multi threading. In the case of Javascript, the language design constraints it to be single-threaded. More on this later.

Having covered the salient language features of interest, let us know discuss specific languages

# Java
Java is a bytecode-compiled, static-typed, garbage collected language with built-in thread support which maps directly to operating system threads. Java should be your go-to general purpose language for any project that lasts more than a few months.

Java has a reputation to be [very verbose](http://steve-yegge.blogspot.com/2006/03/execution-in-kingdom-of-nouns.html) But this is not a problem with the language itself, but rather with the conventions that have come to be associated with the langauge. For example, for "value objects" go ahead and skip the setters and getters and directly use public variables. It is easy to refactor it later with the help of IDE if the need arises.

Java is sometimes castigated for the arbitrary stop-the-world garbage collection pauses. But in my experience, if you're running into this problem, there is probably a bug which is causing excessive temporary objects to be created. The garbage collector can easily collect several 10s of GB of garbage per second.

Although Java is an bytecode interpreted language, it is no slouch when compared to performance. Java speed can be expected to be around 70% to 90% of the speed of C/C++, the runtime safety offered by the JVM far outweighs the performance hit.

## What is Java good for
* Web applications: Java has library support for epoll system calls, which makes it good for serving CDN and static content. The good thread support can make effective use of todays multi-core CPUs
* Large enterprise projects. The static typing enables very intelligent IDE support and makes refactoring easy. As long as you keep your code simple, (don't create BS classes like `Delegator, ResourceManager, blah blah`) Java will be your friend for years to come. 


# Python
Python is a dynamic typed, interpreted, garbage collected language with very little thread support.

Python is a favorite for many programmers and is highly adopted in enterprise software as well as startups for their implementation. This, I think is a major mistake, which causes no end of troubles later on. Here are some reasons

## Speed
Python is **dead slow**. Python can be expected to be about **20-100 times slower** than Java or C/C++. If you want to see it for yourself, just implement this simple program in various languages and time the execution.

````python
count = 1
while count < 100000000
    count += 1
print(count)
````

## Maintenance
Python is dynamic typed. Python looks pretty in the beginning, but as the project grows, the lack of static typing will really bite you. Code gets harder to refactor. New joinees take longer to understand the contracts, Subtle corner cases are introduced, etc. Soon you'll be introducing bugs as fast as you fix them.

## Lack of thread support
As we all know, processor speeds have stopped increasing for almost a decade now. Moore's law is now seen in the core count, rather than the clock speed. In this age of multi-core, do you really want to choose a language which has almost no threading support? The global interpreter lock all but prevents use of multi-core CPUs. This makes python especially bad as a language for web servers, and yet, paradoxically, it is a popular choice for web servers. 

## What is python is good for

* As a replacement for bash scripts. This is because, readability matters more than speed, and the script size is small
* For small throw-away projects. Maybe, you want to quick filter a log file, or do some small string manipulation. Python is perfect for these, where you don't want static typing to get in the way
* For **interactive programming**. For example, in data science, we are exploring data, we need to quickly try out many different things. Furthermore, we don't want to recompute intermediate data everytime. The python REPL is very useful for this kind of programming.

## Avoid python for
* Web server and backend code. There is no multi threading support, pssh.
* Long lived software: The maintenance cost in the long run is much higher than static typed languages

# Javascript
Hoo boy, where to start? Let's start with a brief history. From the beginning, Javascript was designed and implemented to run on browsers. It started its life as a hacky scripting language, with equal parts good and bad, which lead to [books like these](https://www.oreilly.com/library/view/javascript-the-good/9780596517748/). Later, google arrived on the scene, with plans for their own chrome browser in 2004. As part of the browser, Google of course needed a good javascript interpreter and virtual machine. In 2004, they hired Lars Bak, gave him a big pile of money and sent him to a cave in Denmark, and asked him not to emerge until he had a world class js interpretor. As a result, he created precisely that: the v8 javascript virtual machine. Fast forward 2009, Ryan dahl get the idea to rip out the v8 engine from chrome, and run it as a standalone virtual machines with a good enough runtime library, and node.js was born.

Meanwhile, javascript: the language itself underwent a massive upheaval in the the of ECMAScript 6 specification. It cleaned up a lot of the syntax and enabled basic modular packaging capabilities.
The architecture of Javascript reflects its origins in the bowels of the  browser. Here it is heavily used almost as a event driven programming language, primarily to drive the GUI. For example, "on click of submit button, send a request to the server and fetch some data". Historically, there have been many attempts at a multi-threaded graphics library, but all thus far have been doomed to fail. Multi threaded even driven programming is notoriously hard.

Thus, by design, Javascript in its very nature is single threaded. The virtual machine maintains an "event queue". All javascript code executes in response to events in a single thread. Thus, coding in javascript leads to callback hell.

This has the very important consequence that if usercode blocks the single thread, (or example, maybe you're running some heavy encryption algorithm), then the entire event queue effectively gets blocked.

Proponents of node.js will point to one advantage that is quite popular.
The node.js eventing engine is implemented using [libuv](https://github.com/libuv/libuv) which uses native asynchronous I/O (for example, the `epoll` system call in linux) to avoid allocating a thread for each event. Although this is true, the real world benefits come with a lot of caveats that we'll cover shortly.

## Why you should never use node.js for the backend
* The asynchronous coding still is simply not how the human brain works. There are better things to do in life than debug a deeply nested asynchronous callback hell
* The single threaded nature of V8 means that
    * Its very difficult to exploit todays multicore CPU architectures
    * You have to take great care to make sure you don't block the main thread. Doing this will cause huge queueing delays for all other users
* The asynchronous I/O bit is more hype than real usefulness. Modern linux kernel threads are lightweight enough to switch thousands of threads without any noticeable context switching overhead. For example, these days, the linux kernel can switch thread context in a couple of hundred nanoseconds. The asynchronous IO maybe useful in some niche use cases such as CDN serving. However, in this case, there are much better native implementations, for example nginx. Asynchronous IO is only really useful when you have hundreds of thousands of connections, all of which  are mostly idle. In the real world, this is rarely the case.
* All the other bad things that come as part of being a dynamic typed language (see the section on python)
* Although the recent ECMAScript specifications have improved the language a lot, there is a bit chunk of a [bad part](https://medium.com/@Rewieer/javascript-the-bad-parts-and-how-to-avoid-them-1a7c9bc5a0dd), much bigger than other programming languages


Thus, the bottomline is that if you're coding for the browser, there is no escaping javascript. But if you're coding for a backend, it seems there is never really a justification to use javascript or node.js. You're better off using python or java

# Languages for System programming
By system programming, we mean access to low level machine features, such as pointers, or the memory layout of datastructures, or special purpose CPU instructions, or low level kernel APIs etc. For example, perhaps, you're building a database, and you need precise control over the header of your data files. System programming also places a premium on performance, often trying to extract every last bit of juice from the hardware.

System programming languages usually have the following features. They are statically typed and compiles to native code. 

## C/C++
We need no introduction to these languages here. Everything from operating systems to databases have been built with these languages. However we should talk about why people found the need to invent new system programming languages

* C/C++ compilation is slow. This is because the `#include` in each file makes compilation reuse very difficult. This is fine if the headers only contain declarations, but the recursive nature of headers means that even one bad header will propagate everywhere. 
* No garbage collection. Usually, a full-featured garbage collector is frowned upon in system programming languages, because there needs to be tight and predictable performance bounds for the running code. It is often unacceptable for the program to "freeze" because of a running garbage collector. However, it is possible to build deterministic garbage collection using some common techniques, such as incrementing a hidden reference count on variable assignment and decrementing the count in the object destructor. For example C++ offers the so called `smart pointers` which automatically manage the lifecycle of the underlying objects. However, built-in language support would always be a welcome feature
* No language support for threading and concurrency. Although C++ now has a well defined threading library and a memory model, having builtin threading support can make programming much simpler, for example using go `channels`.
* Obsolete syntax: C and C++ are well over 30 years old, and advancements in compiler technologies enables much cleaner syntax in a modern language

# When should you use C/C++
* If you're doing system programming, C/C++ is still an excellent choice.
* If you place an extreme premium on performance, C/C++ offers best in class performance. However, other languages such as go and rust can offer equally good performance with a much cleaner syntax

# Go
Go is a statically typed, native compiled, garbage collected language with built-in support for concurrency.
Go was created at google over the many frustrations faced with C++. It offers fast compilation speeds with a full featured garbage collector as well as language syntax for built in concurrency.

## When should you use go
* If you're doing system programming, but would like to make your life easier with a cleaner syntax, garbage collection and builtin concurrency, go for go. 

# Rust
Rust is a statically typed, native compiled, deterministic garbage collected language with built in thread support. 
Both go and rust offer a much cleaner syntax compared to C/C++. The main differences between Go and Rust are the following

* The Go garbage collector runs as a separate thread, and is non deterministic (i.e., you don't know when it will run and for how long), much similar to the java garbage collector. However rust uses a deterministic garbage collector similar to the smart pointer mechanism in C++
* Go threads are "green" threads, managed by the Go runtime, and may not correspond one-to-one with system threads, whereas rust threads are true system threads

## When should you use Rust
* If you're doing system programming, but would like to make your life easier with a cleaner syntax, a deterministic garbage collector and low level concurrency control, use rust. 


# Julia vs Python: The sad state of data science today
We will end this blog with a note on the current sad state of data science

Data Science has some unique requirements that has challenged the limits of compiler technology

* Often data scientists are precisely that: scientists. They are not well versed with programming languages. A simple syntax would be much preferable
* The need for a REPL: The day of a data scientist begins and ends with the REPL. This exploratory programming is an intrinsic part of the very nature of data science. For example, a data scientist may work in the following steps
    * read raw data from disk and do some cleansing and transformation. Call this pristine data
    * repeatedly make a copy of the pristine data, slice and dice it, explore alternatives, backtrack, explore other alternatives. Without a repl, we would need to keep saving the pristine data to disk and reload it when the program start, which makes for a terrible exploratory experience
* The need for speed. More often than not, todays data is **big** data. We need computation speeds approaching C/C++ or at least java. Certainly not the speed of python
* The need for rich text and graphical output. If you're a data scientist, you usually want to tell a story with the data. You want to write headings, you want boldface, italics, images, graphs and tables to tell your story. 

The reason that python is bad for data science today is due to the third point. **Python is very slow** and not really suitable for data of (say) tens of GBs. Currently the workaround is to use an optimized library such as `pandas`. However, pandas is fast only because the core parts are implemented in C (the so called `vectorized operations`). Pandas itself has weird quirks which I will cover in a later blog. If you ever need something that is not available in pandas, well good luck writing a C binding for python code.

## Julia
Enter Julia, the latest kid on the block. Sometimes it feels like a supwerpowered mutant language. Some examples

* It is _optionally_ typed. You can go with either static or dynamic typing
* It compiles to native code thus offering C like performance
* It is purpose built for data science and thus offers a true REPL. (languages like java offer a REPL as an afterthoughts and are not really true REPLs)


However, in practice, the language is pretty far from mainstream adoption

* The native speed is obtained only under specific conditions. For example, that all variables are statically typed. In general, it is extremely easy to screw up performance by forgetting to declare the types of some variables
* The REPL compilation is mind numbingly slow. It takes several seconds or sometimes minutes to (just in time) compile the code. It leads to a very frustrating experience
* This last point does not really have to with Julia, but rather to do with the need for rich text and graphical output. Currently, the de-facto standard for this rich graphical environment is the Jupyter notebook running on a browser. However, the user experience is far from satisfactory due to the inability to use your favorite IDE and all the tooling that comes along with it, for example, autocomplete, familiar key mappings, debugging tools, etc.

Thus data science today is in a sad state. Julia tries to fix it. Its heart is in the right place, but it is unlikely it will ever be as usable as python in the repl, while maintaining the speed of C.

# Conclusion
Programming languages were designed to solve specific classes of problems. Understanding the motivation and architecture of programming languages allows us to pick one that is well suited for the task at hand. On the flip side, a bad choice can quickly burden the dev team with tech debt. 


