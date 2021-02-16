# Simulation-and-Performance-Evaluation
This document contains an explanation of the project context and the problem analysed, followed by a brief illustration of the simulator implementation created also using a flowchart to get a general idea of it in a short time and to graphically represent every step of the process. The experiments and graphs created will be explained to give an overview and to show the results obtained. The project is built with Python in order to exploit the benefits of using some common libraries for data manipulation such as Numpy and Matplolib for data visualization.

## Context
In the videogame Black Desert Online (BDO), an enhanced item can be bought at auction from other players or enhanced personally. Due to the complexity of the enhancement system, the optimal decision is not always obvious, because the maximum price of each item is set to a predefined value and players do not always keep the items in their possession, sometimes selling them is a useful tool to recover funds for the next upgrade. The order of upgrade levels are PRI, DUO, TRI, TET and PEN. As item reaches higher levels, it becomes stronger and more valuable. Of course, increasing the level also increases the difficulty of successfully obtaining the next upgrade. Each upgrade has a chance of happening. Each time an upgrade fails, the chance of the next one succeeding goes up by a predefined amount. This system is called "fail stacking". Failstacking is a process through which the player can increase his or her chances of success. Every time he fails an enhancement attempt, he will be given extra enhancement chances. This is an indicator of the times the player has continuously failed at enhancement. Therefore, the more times one fails enhancement in a row, the more failstacks one obtains and the more failstacks one has, the greater the chances to succeed at the current upgrade. A failstack (a set of failures) can be saved (with its additional chance) and used later. If an item is improved with failstacks, they are reset and have to be accumulated again. To make the process even more of a gamble, there are two ways to improve an object: one is what is called a "raw tap", or unsafe, and the other is called "cronned". When a “raw tap” fails, the value of the object decreases significantly as its quality drops. To return to the previous quality, the object must be upgraded twice. So, if the upgrade fails going from DUO to TRI, the item has a chance of dropping to PRI instead. A "cronned" upgrade, used to enchant items safely, involves the use of a predefined amount of an additional object called “Cron stone”, that actually prevents the level decrease when enhancing, but it’s fairly resource-intensive. In any case, an item that is upgraded (successfully or unsuccessfully) loses durability. Each item has 100 durability and this statistic must be kept at the maximum because if it is less than 100, the item is less usable in the game and also cannot be sold at auction. Obviously, it’s possible to restore the maximum durability of items but this has a cost. In fact, durability is restored by buying and using items called “Memory”. The goal of the simulator is to decide whether improving the equipment is an advantageous action compared to buying from other players at auction, considering that the item will have to be upgraded from basic to higher level. It will have to take into account also the costs of repairing durability and the possible cost of recovering failures if necessary.

## Simulation
To get a statistically relevant results from the project many simulations are carried out by the software. The use of a pseudo-random number generator, is necessary to obtain a sequence of random values that is representative of the distribution to be modelled. For this reason, a different incremental seed was used for each simulation. Parameters were initially set for the simulation and they will be used both to calculate the probability of a successful upgrade and to calculate the costs of cron and failstack. In fact, the failstack class has been created and 4 failstacks have been initialised so that each time an upgrade passes, the failstack that is most convenient for the level of upgrade desired at that moment is used. So for a DUO a failstack between 20 and 30 will be used, for a TRI one between 30 and 40, for a TET between 40 and 90 and for a PEN between 90 and 190. Obviously, each of these failstacks has a different predefined cost that has been set. Another parameter is the number of Crons needed to make a single upgrade attempt. Each level has a different number needed, in fact, only 1 Cron is used for a DUO attempt, for a TRI 38 Crons, for a TET 113 Crons, for a PEN 429 Crons. Each Cron has a cost of 1 million and each Memory, required to restore durability, has a cost of 2 million. An important parameter is the probability of success for each upgrade level, consisting of the basic probability and the probability that increases each time an upgrade attempt fais, taking failstacks into account. In order to calculate the cost and gain of improving an item, the cost of a basic item(PRI) worth 100 million and a maximum level item (PEN) worth 18 billion was established. Once the data had been initialised, it was decided to run simulations for one object using crons at a certain level. Therefore, for each object, with the cron at a different level, 2*10^3 simulations are carried out so as to have a very precise estimate of the results that will be obtained. In each simulation, the item is increased from the base level to the highest level, making thousands of attempts to improve it. The probabilty, given the current level and the failstack, is equal to the basic chance + (number of failstacks * increase of chance per failstack). In case of success, the failstack is lost and the item is improved, in case of failure, failures are counted for the current level and, if cron was used, no level is lost and no failstack is gained. if no cron was used, level is lost but failstack is gained (+3). At the end of a series of simulations, the costs incurred, the profit gained and the time spent are counted. In addition, graphs are created for each upgrade. A flowchart explaining the functioning of the simulator is shown below.
