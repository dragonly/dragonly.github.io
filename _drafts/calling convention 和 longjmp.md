今天看CSAPP的时候看到setjmp和longjmp, 觉得实在是好玩, 于是看了一下在kernel 4.12.4中的实现, 顺便学习了了下x86的calling convention, 这里做一个记录.

Calling convention这个东西其实一般而言并不需要了解, 因为他是一个