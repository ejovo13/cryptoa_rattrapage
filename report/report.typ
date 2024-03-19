=== Schéma Cryptographique Probablement peu sûr


== Sujet 7

One way function: $ f_p : bb(Z)_p^times times bb(Z)_p^times &arrow.r bb(Z)_(p^3) \
  (x, y) &arrow.r.bar x \/ y mod p^3
$

== Parameters

$ p =  "0x"&"d2bf071417608219223ad076131586a9" \
  z =  "0x"&"4520670aac4c7f5af9f86bed585d6066dcb73b9ec8c9b885" \
       &"36b46e252e64a1d28da6f8cf0d8bbf60fa6a4f8ee9854909"
$


=== Quick Reminders

The multiplicative group of integers modulo $n$, written $bb(Z)_p^times$, is the set of integers coprime to $p$ from the set ${0, 1, .., n - 1}$


==== Some examples

- $bb(Z)_4^times = {1, 3}$
- $bb(Z)_9^times = {1, 2, 4, 5, 7, 8}$

=== Problem

We start by determining if $p$ is prime or not. It is indeed probably prime, according to a Miller-Rabin test with 100 trials.


=== Visualization

We can start playing around with the family of functions by using very simple visualizations. We do this to also get a feel for the geometric behavior of our function.